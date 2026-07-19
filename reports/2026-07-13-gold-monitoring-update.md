# 2026-07-13 黄金市场状态更新

更新时间：2026-07-13 02:35:49 北京时间（UTC 2026-07-12 18:35:50）
更新模式：full

本次选择 full update，因为距离上次更新已超过一周，周频核心信号过期；同时7月10日COMEX周收盘、FRED初请和利率、CFTC COT、SGE现货与租借费率、本周CPI/PPI和Warsh证词前瞻均需要纳入。更新发生在美国周日下午、Globex常规开盘前，因此不使用周日晚盘薄流动性报价。

## 核心结论

黄金状态维持黄灯，但从“修复确认增强”降为“修复转弱/高位震荡”。7月10日COMEX黄金结算4104.10美元/盎司，周跌0.21%，仍勉强守住4100附近；白银结算59.809美元，周跌1.38%，继续低于63.885修复参考位。

这不是红灯：黄金没有跌破3800并站稳，10年实际利率2.31%尚未触发2.5%重审线，政治尾部组合也没有点亮。但这也不是蓝灯：2年期收益率4.16%仍高于3.75%的政策上限，10年TIPS实际利率重新上行，初请只有215k，COT净多仍偏高，ETF周流量和实物紧张度都没有确认。

## 数据与质量

可靠更新：

- COMEX结算：黄金4104.10，白银59.809，分别周跌0.21%和1.38%。
- FRED：DFII10 2.31、DGS2 4.16、DGS10 4.54、T10YIE 2.24、DFEDTARU 3.75、ICSA 215000、WMTSECL1 2597278。
- CFTC：2026-07-07黄金管理基金净多+116161张，较2026-06-23的+115395略高，仍不是洗净状态。
- SGE每日行情：2026-07-10 Au99.99收897.25元/克，成交量3554.2千克。
- SGE租借费率：2026-06-29至2026-07-03，6个月加权0.30%，1年加权0.20%。
- 油价：WTI 71.41、Brent 76.01，周线明显反弹。

缺口：

- `scripts/lease_rate.py`仍因Yahoo COMEX曲线HTTP 429失败，未写入`data/lease_rate.csv`。
- Yahoo chart仍返回`Edge: Too Many Requests`；Stooq返回浏览器验证页，因此GLD/SLV/GDX价格和ETF资金流不能可靠登记。
- CME Gold Stocks直连下载本次20秒超时，未取得新库存读数。
- WGC ETF flows需要登录/注册，Swiss-Impex需要手工或浏览器导出，LBMA历史表需要MyLBMA/IBA许可。

## 框架判断

一阶主轴本周转弱。弱非农仍然提供修复火种，但初请和4周均值仍处于低位，说明就业尚未进入裁员裂缝。与此同时，实际利率从2.25升至2.31，2Y仍高于政策上限，FOMC纪要显示官员对通胀和加息路径仍有分歧。对黄金而言，这是“有就业支持，但被利率重新压住”的状态。

实物紧张度没有共振。SGE Au99.99回落，SGE 1年租借参考费率从0.36降至0.20，CME库存新读数缺失。当前不能用实物侧给3800-4000托底假设加分。

政治尾部维持观察。WMTSECL1两周合计下降39669百万美元，需要继续跟踪；但T10YIE稳定在2.24，没有出现通胀预期飙升或名义收益率被压住的组合，因此不升格。

## 后续观察

1. 本周CPI/PPI是否确认通胀粘性，尤其是否推动2Y和10Y实际利率继续上行。
2. Warsh国会证词是否强化“少前瞻指引、数据依赖、保留加息可能”的反应函数。
3. 黄金能否继续守住4100，若跌回4000下方，3800-4000需求响应测试重新启动。
4. COT是否开始真正洗净，ETF周度流量是否转正。
5. SGE租借费率、COMEX库存和SGE-London溢价能否形成连续实物紧张证据。

结论：长期牛市论题未破，但本周修复动能变弱。当前最合适的纪律表述是：黄灯、修复转弱、等待CPI/PPI和利率确认；不加仓蓝灯，不触发红灯。

## 主要来源

- FRED: `DFII10`, `DGS2`, `DGS10`, `T10YIE`, `DFEDTARU`, `ICSA`, `PCEPILFE`, `WMTSECL1`.
- CFTC Disaggregated COT `fut_disagg_txt_2026.zip`.
- WSJ / Dow Jones Market Data / FactSet: COMEX gold and silver settlements, WSJ Dollar Index, WTI/Brent settlements.
- Shanghai Gold Exchange daily quotation and official gold lease-rate page.
- AP / MarketWatch / Barron's / Kiplinger / Investopedia: FOMC minutes, CPI/PPI calendar, Warsh testimony, oil/geopolitical context.
