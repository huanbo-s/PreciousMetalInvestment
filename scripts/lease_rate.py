#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lease_rate.py — 隐含黄金租赁利率推算（黄金框架补丁 第3号 · L.3 配套脚本）

方法
----
    implied_lease ≈ SOFR − implied_forward
    implied_forward = ln(F_far / F_near) / ΔT   （COMEX 黄金期货日历价差，连续复利、ACT/365）

设计定位：**趋势观察工具，非水平精确**。已知近似（详见补丁3 L.3）：
    1. 无交易所假日历：合约到期按"交割月倒数第三个工作日"近似，误差 ±1–2 天；
    2. 用隔夜 SOFR 平铺整个期限，忽略利率期限结构；
    3. 未扣仓储/保险成本：对水平造成约 −0.1 ~ −0.4 个百分点的常量负偏置，不影响趋势。
    因此：看序列的变化方向与突变，不要引用绝对水平。

数据源（全部免费公开）
----------------------
    期货收盘  Yahoo Finance chart API（非官方、延迟行情；取日线收盘）
    SOFR      纽约联储 Markets API（官方、免key）；失败退回 FRED fredgraph CSV（免key）
    端点属公开但非契约接口，可能变更；任何一环失败会明确报错并指出失败源。

同步规则（对应用户要求"参与计算的数据同步"）
--------------------------------------------
    每组价差的两条期货腿取**同一交易所、同一结算日**的收盘（天然同步）；
    SOFR 取 ≤ 该结算日的最近发布值（SOFR 为 T+1 上午发布，可能有 1 个工作日错位），
    错位天数写入输出记录，供审计。

用法
----
    python3 scripts/lease_rate.py                        # 拉最新数据，追加 data/lease_rate.csv
    python3 scripts/lease_rate.py --selftest             # 离线自检（不联网）：验证数学与合约选择逻辑
    python3 scripts/lease_rate.py --pairs 2              # 计算的日历价差组数（默认 2）
    python3 scripts/lease_rate.py --print-indicator-row  # 附带打印 data/indicators.csv 体例行，供人工粘贴
    python3 scripts/lease_rate.py --outfile PATH         # 自定义输出 CSV 路径

仅用 Python 标准库；无第三方依赖。退出码：0 成功（含 SUSPECT 警示），1 数据源失败。
"""

from __future__ import annotations

import argparse
import calendar
import csv
import json
import math
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

# ------------------------------ 配置 ------------------------------ #

MONTH_CODES = {2: "G", 4: "J", 6: "M", 8: "Q", 10: "V", 12: "Z"}  # 黄金活跃合约月
MIN_DAYS_TO_EXPIRY = 20        # 近月合约距到期不足此天数则跳过（避开交割期噪声）
YAHOO_HOSTS = ("query1.finance.yahoo.com", "query2.finance.yahoo.com")
HTTP_TIMEOUT = 25
HTTP_RETRIES = 2
SANITY_RANGE = (-5.0, 20.0)    # 隐含租赁利率合理界（%），越界标记 SUSPECT
STALE_DAYS_WARN = 6            # 结算日距今超过此天数提示数据可能陈旧
USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")

CSV_COLUMNS = [
    "run_utc", "pair", "sync_date", "near_contract", "near_close", "near_expiry",
    "far_contract", "far_close", "far_expiry", "spread_days",
    "implied_fwd_pct", "sofr_pct", "sofr_date", "sofr_lag_days",
    "implied_lease_pct", "flag", "notes",
]


class DataSourceError(RuntimeError):
    """任一免费数据源失败时抛出，消息中注明失败源。"""


# ------------------------------ 工具函数 ------------------------------ #

def third_to_last_bday(year: int, month: int) -> date:
    """交割月倒数第三个工作日（近似最后交易日；不含交易所假日历——已声明近似）。"""
    last_dom = calendar.monthrange(year, month)[1]
    bdays = []
    d = last_dom
    while d >= 1 and len(bdays) < 3:
        cand = date(year, month, d)
        if cand.weekday() < 5:  # Mon-Fri
            bdays.append(cand)
        d -= 1
    if len(bdays) < 3:
        raise ValueError(f"无法定位 {year}-{month} 的倒数第三个工作日")
    return bdays[2]


def pick_contracts(today: date, n: int, min_days: int = MIN_DAYS_TO_EXPIRY):
    """按活跃月序挑选距到期 >= min_days 的最近 n 个合约。

    返回 [(yahoo_symbol, expiry_date), ...]，如 [("GCQ26.CMX", 2026-08-27), ...]
    """
    out = []
    y, m = today.year, today.month
    for _ in range(30):  # 最多向前看 30 个自然月
        if m in MONTH_CODES:
            exp = third_to_last_bday(y, m)
            if (exp - today).days >= min_days:
                sym = f"GC{MONTH_CODES[m]}{str(y)[-2:]}.CMX"
                out.append((sym, exp))
                if len(out) == n:
                    return out
        m += 1
        if m > 12:
            m, y = 1, y + 1
    raise ValueError("未能选出足够的合约")


def _http_get(url: str) -> bytes:
    last_err = None
    for attempt in range(HTTP_RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": USER_AGENT, "Accept": "application/json,text/csv,*/*"})
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                return resp.read()
        except (urllib.error.HTTPError, urllib.error.URLError, OSError) as e:
            last_err = e
            if attempt < HTTP_RETRIES:
                time.sleep(2 * (attempt + 1))
    raise DataSourceError(f"HTTP 失败: {url} :: {last_err}")


def fetch_futures_daily(symbol: str, range_days: int = 10) -> dict:
    """取单个合约近若干日的日线收盘。返回 {date: close}。"""
    errs = []
    for host in YAHOO_HOSTS:
        url = (f"https://{host}/v8/finance/chart/{symbol}"
               f"?interval=1d&range={range_days}d")
        try:
            data = json.loads(_http_get(url).decode("utf-8"))
            result = data["chart"]["result"][0]
            stamps = result.get("timestamp") or []
            closes = result["indicators"]["quote"][0].get("close") or []
            series = {}
            for ts, c in zip(stamps, closes):
                if c is None:
                    continue
                d = datetime.fromtimestamp(ts, tz=timezone.utc).date()
                series[d] = float(c)
            if series:
                return series
            errs.append(f"{host}: 返回为空")
        except DataSourceError as e:
            errs.append(str(e))
        except (KeyError, IndexError, TypeError, ValueError) as e:
            errs.append(f"{host}: 响应结构异常 ({e})")
    raise DataSourceError(f"期货源失败 [{symbol}] :: " + " | ".join(errs))


def fetch_sofr() -> dict:
    """取近若干日 SOFR。返回 {date: rate_pct}。主源纽约联储，备源 FRED。"""
    # 主源：NY Fed Markets API（官方）
    try:
        url = "https://markets.newyorkfed.org/api/rates/secured/sofr/last/10.json"
        data = json.loads(_http_get(url).decode("utf-8"))
        out = {}
        for row in data.get("refRates", []):
            d = datetime.strptime(row["effectiveDate"], "%Y-%m-%d").date()
            out[d] = float(row["percentRate"])
        if out:
            return out
    except (DataSourceError, KeyError, TypeError, ValueError) as e:
        print(f"[warn] NY Fed SOFR 源失败，改用 FRED 备源: {e}", file=sys.stderr)
    # 备源：FRED fredgraph CSV（免key）
    try:
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SOFR"
        text = _http_get(url).decode("utf-8", errors="replace")
        out = {}
        for line in text.splitlines()[1:]:
            parts = line.strip().split(",")
            if len(parts) < 2 or parts[1] in (".", ""):
                continue
            try:
                d = datetime.strptime(parts[0], "%Y-%m-%d").date()
                out[d] = float(parts[1])
            except ValueError:
                continue
        if out:
            return out
        raise DataSourceError("FRED SOFR 返回为空")
    except DataSourceError:
        raise
    except Exception as e:  # noqa: BLE001 —— 汇总为数据源错误，便于上层统一处理
        raise DataSourceError(f"FRED SOFR 备源失败 :: {e}")


# ------------------------------ 核心计算 ------------------------------ #

def implied_forward_pct(f_near: float, f_far: float, days: int) -> float:
    """日历价差隐含远期利率（%，连续复利、ACT/365）。"""
    if days <= 0:
        raise ValueError("价差天数必须为正")
    return math.log(f_far / f_near) / (days / 365.0) * 100.0


def compute_pairs(contract_series: list, sofr_map: dict, today: date) -> list:
    """contract_series: [(symbol, expiry, {date: close}), ...] 按到期升序。
    对相邻两合约构造价差组，返回每组一条记录（dict）。"""
    rows = []
    sofr_dates = sorted(sofr_map)
    for (s1, e1, ser1), (s2, e2, ser2) in zip(contract_series, contract_series[1:]):
        common = sorted(set(ser1) & set(ser2))
        if not common:
            print(f"[warn] {s1}/{s2} 无同日收盘，跳过该组", file=sys.stderr)
            continue
        sync = common[-1]
        if (today - sync).days > STALE_DAYS_WARN:
            print(f"[warn] {s1}/{s2} 最近同步日 {sync} 距今超过 "
                  f"{STALE_DAYS_WARN} 天，数据可能陈旧", file=sys.stderr)
        f1, f2 = ser1[sync], ser2[sync]
        days = (e2 - e1).days
        fwd = implied_forward_pct(f1, f2, days)
        s_dates = [d for d in sofr_dates if d <= sync]
        if not s_dates:
            raise DataSourceError("SOFR 序列中没有早于结算日的观测，无法同步")
        sd = s_dates[-1]
        sofr = sofr_map[sd]
        lease = sofr - fwd
        flag = "OK" if SANITY_RANGE[0] <= lease <= SANITY_RANGE[1] else "SUSPECT"
        rows.append({
            "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "pair": f"{s1.split('.')[0]}-{s2.split('.')[0]}",
            "sync_date": sync.isoformat(),
            "near_contract": s1, "near_close": round(f1, 2),
            "near_expiry": e1.isoformat(),
            "far_contract": s2, "far_close": round(f2, 2),
            "far_expiry": e2.isoformat(),
            "spread_days": days,
            "implied_fwd_pct": round(fwd, 3),
            "sofr_pct": round(sofr, 3), "sofr_date": sd.isoformat(),
            "sofr_lag_days": (sync - sd).days,
            "implied_lease_pct": round(lease, 3),
            "flag": flag, "notes": "",
        })
    if not rows:
        raise DataSourceError("没有任何一组价差可计算（各合约无共同结算日）")
    return rows


# ------------------------------ 输出 ------------------------------ #

def default_outfile() -> Path:
    """默认输出到 <repo_root>/data/lease_rate.csv（假定脚本位于 <repo_root>/scripts/）。"""
    return Path(__file__).resolve().parent.parent / "data" / "lease_rate.csv"


def load_prev_lease(outfile: Path, pair: str):
    if not outfile.exists():
        return None
    try:
        with outfile.open(newline="", encoding="utf-8") as f:
            prev = [r for r in csv.DictReader(f) if r.get("pair") == pair]
        return float(prev[-1]["implied_lease_pct"]) if prev else None
    except Exception:  # 历史文件损坏不阻断本次写入
        return None


def append_rows(outfile: Path, rows: list) -> None:
    outfile.parent.mkdir(parents=True, exist_ok=True)
    new_file = not outfile.exists()
    with outfile.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        if new_file:
            w.writeheader()
        for r in rows:
            w.writerow(r)


def print_summary(rows: list, outfile: Path, prev_map: dict, indicator_row: bool) -> None:
    print("=" * 72)
    print("隐含黄金租赁利率（趋势工具，勿引用绝对水平；负常量偏置≈仓储成本）")
    for r in rows:
        prev = prev_map.get(r["pair"])
        delta = "" if prev is None else f"（上次 {prev:+.3f} → Δ {r['implied_lease_pct'] - prev:+.3f}）"
        print(f"  {r['pair']}: lease {r['implied_lease_pct']:+.3f}%  "
              f"= SOFR {r['sofr_pct']:.3f}% − fwd {r['implied_fwd_pct']:.3f}%  "
              f"@ {r['sync_date']} {delta} [{r['flag']}]")
        if r["flag"] == "SUSPECT":
            print("    [!] 越出合理界，优先怀疑数据错误（错腿/坏点），核对后再解读。")
        if r["sofr_lag_days"] > 1:
            print(f"    [!] SOFR 错位 {r['sofr_lag_days']} 天（>1 个工作日），已记录。")
    print(f"  已追加 {len(rows)} 行 → {outfile}")
    print("  读法提醒（补丁3 L.2）：单点不定案；回调期与其他实物信号共振才有检验意义；")
    print("  尖峰先排除物流/套利成因（2025年初伦敦→纽约搬运潮为先例）。")
    if indicator_row:
        r = rows[0]
        prev = prev_map.get(r["pair"])
        print("-" * 72)
        print("indicators.csv 体例行（如需登记，人工粘贴，status 由你判定）：")
        print(f"{r['sync_date']},implied_gold_lease_{r['pair']},"
              f"{r['implied_lease_pct']},{'' if prev is None else prev},"
              f"weekly,scripts/lease_rate.py (Yahoo COMEX curve + NY Fed SOFR),,"
              f"\"fwd={r['implied_fwd_pct']}%; sofr={r['sofr_pct']}% ({r['sofr_date']})\"")
    print("=" * 72)


# ------------------------------ 自检 ------------------------------ #

def selftest() -> int:
    print("[selftest] 1/4 远期利率数学 ...", end=" ")
    fwd = implied_forward_pct(4000.0, 4020.0, 61)
    assert abs(fwd - 2.9843) < 0.01, fwd
    assert abs((4.30 - fwd) - 1.3157) < 0.01
    print(f"PASS (fwd={fwd:.4f}%)")

    print("[selftest] 2/4 倒数第三个工作日（结构性质）...", end=" ")
    for y, m in [(2026, 8), (2026, 10), (2026, 12), (2027, 2)]:
        exp = third_to_last_bday(y, m)
        assert exp.year == y and exp.month == m and exp.weekday() < 5
        later = [d for d in range(exp.day + 1, calendar.monthrange(y, m)[1] + 1)
                 if date(y, m, d).weekday() < 5]
        assert len(later) == 2, (exp, later)  # 其后恰好还有两个工作日
    print("PASS")

    print("[selftest] 3/4 合约选择逻辑 ...", end=" ")
    picks = pick_contracts(date(2026, 7, 4), 3)
    syms = [s for s, _ in picks]
    assert all(s.startswith("GC") and s.endswith(".CMX") for s in syms)
    assert all((e - date(2026, 7, 4)).days >= MIN_DAYS_TO_EXPIRY for _, e in picks)
    assert [e.month for _, e in picks] == [8, 10, 12], picks  # 2026-07-04 → Q/V/Z
    print(f"PASS ({', '.join(syms)})")

    print("[selftest] 4/4 合成数据全链路 ...", end=" ")
    today = date(2026, 7, 4)
    (s1, e1), (s2, e2), (s3, e3) = pick_contracts(today, 3)
    d0 = date(2026, 7, 2)
    series = [
        (s1, e1, {d0: 4000.0}),
        (s2, e2, {d0: 4000.0 * math.exp(0.02 * (e2 - e1).days / 365.0)}),
        (s3, e3, {d0: 4000.0 * math.exp(0.02 * (e3 - e1).days / 365.0)}),
    ]  # 构造隐含远期恒为 2.00% 的曲线
    rows = compute_pairs(series, {date(2026, 7, 1): 3.50}, today)
    assert len(rows) == 2
    for r in rows:
        assert abs(r["implied_fwd_pct"] - 2.0) < 1e-6
        assert abs(r["implied_lease_pct"] - 1.5) < 1e-6
        assert r["flag"] == "OK" and r["sofr_lag_days"] == 1
    print("PASS (lease=+1.500%)")
    print("[selftest] 全部通过。联网端点未在此自检中验证，首次真实运行即为端点验证。")
    return 0


# ------------------------------ 主流程 ------------------------------ #

def main() -> int:
    ap = argparse.ArgumentParser(description="隐含黄金租赁利率推算（补丁3 L.3）")
    ap.add_argument("--pairs", type=int, default=2, help="日历价差组数（默认2）")
    ap.add_argument("--outfile", type=Path, default=None, help="输出 CSV 路径")
    ap.add_argument("--print-indicator-row", action="store_true",
                    help="附带打印 indicators.csv 体例行")
    ap.add_argument("--selftest", action="store_true", help="离线自检，不联网")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    outfile = args.outfile or default_outfile()
    today = date.today()
    try:
        picks = pick_contracts(today, args.pairs + 1)
        print(f"[info] 选定合约: {', '.join(s for s, _ in picks)}")
        contract_series = []
        for sym, exp in picks:
            ser = fetch_futures_daily(sym)
            contract_series.append((sym, exp, ser))
            print(f"[info] {sym} 取得 {len(ser)} 个收盘，最新 {max(ser)}")
        sofr_map = fetch_sofr()
        print(f"[info] SOFR 最新观测 {max(sofr_map)} = {sofr_map[max(sofr_map)]:.3f}%")
        rows = compute_pairs(contract_series, sofr_map, today)
    except DataSourceError as e:
        print(f"[error] 数据源失败，本次未写入任何数据：{e}", file=sys.stderr)
        print("[error] 排查顺序：①网络 ②Yahoo 合约代码是否变更（GC+月码+年2位+.CMX）"
              "③NY Fed/FRED 端点格式是否变更。按 AGENTS.md 惯例记录源失败。",
              file=sys.stderr)
        return 1

    prev_map = {r["pair"]: load_prev_lease(outfile, r["pair"]) for r in rows}
    append_rows(outfile, rows)
    print_summary(rows, outfile, prev_map, args.print_indicator_row)
    return 0


if __name__ == "__main__":
    sys.exit(main())
