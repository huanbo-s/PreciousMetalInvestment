# Gold&Silver Project State

These instructions apply to `/Users/huanbosun/Documents/Gold&Silver`.

## How Agents Should Use This File

- Read this file first when opening this project.
- Treat this file as the single source of durable project context and overall project state.
- Update this file when the current session creates durable context that future agents should inherit, or when the user explicitly asks to record something here.
- Do not create separate long-term memory files such as `INITIALIZE.md` or `PROJECT_MEMORY.md` unless the user explicitly asks for them.
- If this file conflicts with the user's latest message or the current repository state, follow the user's latest message/current repository, then update this file if the correction should persist.

## Project Overview

This project supports a precious-metals research and trading framework.

GitHub repository: `https://github.com/huanbo-s/PreciousMetalInvestment`

The user's research documents are:

- Continuously updated source of truth: `/Users/huanbosun/Documents/Gold&Silver/research/黄金中长期趋势研究框架（持续更新版）.md`
- Frozen original archive: `/Users/huanbosun/Documents/Gold&Silver/research/黄金中长期趋势研究框架 v2.md`

The frozen archive keeps the original filename and original content for future backtracking and constraint checks. Do not update the archive during ordinary theory discussion or monitoring work. All ongoing revisions should be made to the continuously updated source-of-truth file.

The project has two intended agent roles:

1. Theory Research Agent
   - Purpose: optimize, critique, and update `research/黄金中长期趋势研究框架（持续更新版）.md`.
   - Focus: pricing logic, macro regime framework, debt/fiscal dominance thesis, probability bookkeeping, falsification conditions, scenario analysis, and methodological discipline.
   - Output: revisions to the research framework itself, or structured review notes before revisions when the user asks for discussion first.

2. Market Signal Monitoring Agent
   - Purpose: translate the theory framework into periodic market monitoring and trading-discipline checks.
   - Focus: actual market signals, dashboard updates, event reaction logs, and whether the gold/precious-metals bull thesis is intact, delayed, or broken.
   - Output: updates to `dashboard.md`, `data/indicators.csv`, and `data/event_log.csv`; may flag that the theory framework needs review, but should not rewrite the core thesis unless the user explicitly asks.
   - Required first step for every market-data update: confirm the current absolute time before pulling data, then record local time, UTC time, data cutoff, and market-session caveats in the update.
   - Required second step: decide whether the user asked for a lightweight update or a full update. If the user did not specify, check each data source's age against its cadence and choose automatically: lightweight when only daily/high-sensitivity data are stale; full when any weekly, semi-monthly, monthly, quarterly, or event-driven core signal is stale or a major event occurred.
   - Required news-context step for every update, lightweight or full: after pulling and checking market data, retrieve recent important news to identify whether key data have just been released or are about to be released, and whether recent news helps explain short-term precious-metals price action or market sentiment.
   - News is auxiliary context only. It must be separated from data evidence and framework conclusions, and must not override the project's own research framework or trading-discipline signals.
   - Every update must explicitly record `update_mode` (`lightweight` or `full`) and explain why that mode was chosen.

## Current Status

The project has an initial monitoring scaffold:

- `/Users/huanbosun/Documents/Gold&Silver/dashboard_plan.md`: durable rules for the precious-metals bull-market risk dashboard.
- `/Users/huanbosun/Documents/Gold&Silver/dashboard.md`: periodic dashboard template.
- `/Users/huanbosun/Documents/Gold&Silver/data/indicators.csv`: indicator history table.
- `/Users/huanbosun/Documents/Gold&Silver/data/event_log.csv`: key-event reaction log.
- `/Users/huanbosun/Documents/Gold&Silver/data/physical_tightness.csv`: raw physical-tightness observation table for Patch 3 §6.4B.

The research framework now has two project-local copies under `research/`: a frozen `v2` archive and a clearly named continuously updated working file.

Theory framework update completed on 2026-06-21:

- Applied `/Users/huanbosun/Documents/Gold&Silver/research/patches/黄金框架补丁 第1号 底仓分量与硬核层.md` to `/Users/huanbosun/Documents/Gold&Silver/research/黄金中长期趋势研究框架（持续更新版）.md`.
- Applied `/Users/huanbosun/Documents/Gold&Silver/research/patches/黄金框架补丁 第2号 政治路径层级与一阶监测组.md` to `/Users/huanbosun/Documents/Gold&Silver/research/黄金中长期趋势研究框架（持续更新版）.md`.
- The frozen archive `/Users/huanbosun/Documents/Gold&Silver/research/黄金中长期趋势研究框架 v2.md` was intentionally not modified.
- Patch 1 changes the treatment of structural demand: the former "structural base position" is now split into hard-core price-negative-sensitive buyers and soft-layer price-sensitive buyers. The `$3,800` structural support idea is now treated as a hypothesis to be tested during a real drawdown, not as a pre-verified left-side entry reason.
- Patch 2 adds political-tail hierarchy and the first-order monitoring group. Political/constitutional shocks and Fed-independence risks remain second-order variables unless the market-based escalation triggers in §9.7 light up. Market monitoring should now begin with the first-order chain: inflation + employment -> Fed reaction function -> real rates -> gold.

First formal market-signal update completed for 2026-06-20 05:40 Beijing time:

- `/Users/huanbosun/Documents/Gold&Silver/dashboard.md` now contains the first dated dashboard.
- `/Users/huanbosun/Documents/Gold&Silver/reports/2026-06-20-first-gold-analysis.md` contains the first analysis note.
- `data/indicators.csv` and `data/event_log.csv` contain the first set of observations.

Second formal market-signal update completed for 2026-06-22 01:52 Beijing time:

- `/Users/huanbosun/Documents/Gold&Silver/dashboard.md` now contains the second dated dashboard using the Patch 2 monitoring order.
- `/Users/huanbosun/Documents/Gold&Silver/reports/2026-06-22-gold-monitoring-update.md` contains the second analysis note.
- `data/indicators.csv` and `data/event_log.csv` contain the second set of observations.
- Core conclusion: long-term bull thesis remains intact but weak; one-order chain still suppresses gold because inflation is elevated, employment has not cracked, the FOMC reaction function remains hawkish, and real yields rose. No right-side confirmation and no political-tail upgrade under §9.7.

Full market-signal update completed for 2026-06-25 22:51 Beijing time:

- `/Users/huanbosun/Documents/Gold&Silver/dashboard.md`, `data/indicators.csv`, and `data/event_log.csv` were updated and pushed to remote `main` at commit `97a11f1`.
- Core conclusion: gold entered the 3800-4000 test zone after settling below 4000, moving bull-market integrity to yellow/key-zone test. This was not a formal bull-thesis break because 3800 had not been broken and held for two weeks.

Full market-signal update completed for 2026-07-02 03:49 Beijing time:

- `/Users/huanbosun/Documents/Gold&Silver/dashboard.md` now reflects the July 1 market close and the latest framework state.
- `/Users/huanbosun/Documents/Gold&Silver/reports/2026-07-02-gold-monitoring-update.md` was first created as the pre-NFP formal update note; it was later replaced by the post-NFP 20:44 update below.
- `data/indicators.csv` and `data/event_log.csv` include July 1/July 2 observations.
- Core conclusion: gold rebounded above 4000 to 4068.30, but the state remains yellow/key-zone test rather than a right-side turn. ADP softened and real yields eased, but 2Y remains above the policy upper bound, COT net long rose to +115,395, ETF flows remain negative, and the official June payroll report is still pending.

Post-NFP full market-signal update completed for 2026-07-02 20:44 Beijing time:

- `/Users/huanbosun/Documents/Gold&Silver/dashboard.md` now reflects the BLS June payroll report and user-provided real-time London gold, silver, and DXY readings.
- `/Users/huanbosun/Documents/Gold&Silver/reports/2026-07-02-gold-monitoring-update.md` contains the post-NFP formal update note.
- `data/indicators.csv` and `data/event_log.csv` include BLS June payroll data, downward revisions, labor-force details, wage data, and the user-provided real-time market readings.
- Core conclusion: state improved to yellow/repair test after payrolls slowed to +57,000 and the prior two months were revised down by 74,000; user-provided London gold around 4135 and DXY around 100.637 show a stronger repair move, but this is not a right-side turn until settlement, rates, ETF/flow, and COT confirmation catch up.

Physical-tightness supplemental update completed for 2026-07-04 06:28 Beijing time:

- `/Users/huanbosun/Documents/Gold&Silver/data/physical_tightness.csv` was created as the raw Patch 3 physical-tightness observation table.
- `/Users/huanbosun/Documents/Gold&Silver/reports/2026-07-04-physical-tightness-update.md` records the source parsing and official-source availability review.
- Parsed user-provided SGE daily quotation workbook: 2026-07-03 Au99.99 close 910.98 CNY/g, volume 4334.58 kg; Au(T+D) close 910.26 CNY/g.
- Parsed user-provided CME `Gold_Stocks.xls`: report date 2026-07-02, activity date 2026-07-01; registered gold stocks 14,826,009.194 oz; eligible 12,634,943.363 oz; combined 27,460,952.557 oz.
- Parsed and officially re-downloaded SGE lease-rate PDF for 2026-06-22 to 2026-06-26; checksum matched the local PDF. Six-month weighted lease reference rate 0.30%; one-year weighted rate 0.36%.
- Official CFTC 2026 disaggregated futures-only zip was re-pulled; standard gold latest row still 2026-06-23, with Managed Money net long +115,395 contracts. No 2026-06-30 row was available.
- CME direct XLS re-download from the official endpoint failed in this environment (HTTP/2 stream error / no transfer), so the CME observation uses the user-provided official workbook while recording the re-download failure.
- WGC ETF flows require login/registration for downloads; Swiss-Impex requires manual or browser-based export workflow; LBMA historical tables require MyLBMA/IBA licensing.
- Core conclusion: physical tightness is no longer blank, but only a baseline has been started. It still does not support a hard-core floor or right-side turn until several weeks of COMEX/SGE/lease data and at least one swing-flow divergence are observed.

Full market-signal update completed for 2026-07-04 04:54 Beijing time:

- `/Users/huanbosun/Documents/Gold&Silver/dashboard.md` now reflects the July 2 COMEX settlement confirmation, the July 3 U.S. Independence Day observed market holiday, latest FRED series, and data-quality caveats.
- `/Users/huanbosun/Documents/Gold&Silver/reports/2026-07-04-gold-monitoring-update.md` contains the formal update note.
- `data/indicators.csv` and `data/event_log.csv` include July 2 COMEX gold/silver settlement, WSJ Dollar Index, WTI/Brent settlement, June 27 initial claims, July 1 WMTSECL1, FRED rate updates, COT staleness, ETF source failure, and lease-rate source failure.
- Core conclusion: state remains yellow but improves to "repair confirmation strengthened" because COMEX gold settled at 4112.70, above the 4100-4115 repair zone. This is not a blue/right-side turn because initial claims remain low at 215,000, 2Y remains above the policy upper bound, official post-NFP real-yield confirmation is pending, ETF/COT confirmation is missing, and `scripts/lease_rate.py` failed on Yahoo HTTP 429 with no `data/lease_rate.csv` written.

Full market-signal update completed for 2026-07-13 02:35 Beijing time:

- `/Users/huanbosun/Documents/Gold&Silver/dashboard.md` now reflects the July 10 weekly market close, latest FRED rates/claims/WMTSECL1, updated CFTC COT through 2026-07-07, SGE daily quotation through 2026-07-10, SGE lease-rate data through 2026-07-03, and the July 13-17 CPI/PPI/Warsh testimony risk window.
- `/Users/huanbosun/Documents/Gold&Silver/reports/2026-07-13-gold-monitoring-update.md` contains the formal update note.
- `data/indicators.csv`, `data/event_log.csv`, and `data/physical_tightness.csv` include the latest July 13 observations.
- Core conclusion: state remains yellow but is downgraded from "repair confirmation strengthened" to "repair weakening / high-level consolidation." Gold settled at 4104.10 on 2026-07-10, still near the 4100 repair zone, but real yields rose to 2.31, DGS2 stayed at 4.16 above the 3.75 policy upper bound, silver weakened to 59.809, COT Managed Money net long remained elevated at +116,161, and ETF/physical confirmation remains missing.
- Physical tightness: SGE Au99.99 closed at 897.25 CNY/g on 2026-07-10; SGE 6M/1Y weighted lease reference rates for 2026-06-29 to 2026-07-03 were 0.30%/0.20%. The 1Y lease rate fell from 0.36%, so there is no lease-rate tightness spike. CME Gold_Stocks direct pull timed out; latest usable CME inventory remains activity date 2026-07-01.
- Data quality: `scripts/lease_rate.py` again failed on Yahoo HTTP 429; Yahoo chart returned `Edge: Too Many Requests`; Stooq returned browser verification HTML; WGC still requires login/registration. These are missing-data caveats, not evidence of looseness.
- Next focus: June CPI on Tuesday July 14, PPI Wednesday July 15, retail sales and claims Thursday July 16, and Warsh congressional testimony. If CPI/PPI are sticky and 2Y/real yields rise while gold falls below 4000, the yellow state should move closer to orange.

Full market-signal update completed for 2026-07-20 04:06 Beijing time:

- `/Users/huanbosun/Documents/Gold&Silver/dashboard.md` now reflects the user-provided 2026-07-17 London gold close 4018, intraday low 3959, silver close 55.91, official FRED rates/claims/WMTSECL1, BLS CPI/PPI, U.S. Census retail sales, CFTC COT through 2026-07-14, SGE daily quotation through 2026-07-17, and SGE lease-rate data through 2026-07-10.
- `/Users/huanbosun/Documents/Gold&Silver/reports/2026-07-20-gold-monitoring-update.md` contains the formal update note.
- `data/indicators.csv`, `data/event_log.csv`, and `data/physical_tightness.csv` include the latest July 20 observations.
- Core conclusion: state is downgraded to yellow/orange key-zone test. Gold's 2026-07-17 low at 3959 reactivated the 3800-4000 demand-response test, but the close back above 4000 means the 3800 two-week red trigger is not active. Silver at 55.91, 10Y TIPS at 2.35, DGS2 at 4.16, and COT Managed Money net long at +120,779 prevent a right-side turn.
- Macro interpretation: June CPI and PPI cooled, but initial claims fell to 208,000 with a 214,250 four-week average, retail sales still rose 0.2%, and Warsh's testimony did not provide a dovish pivot. The live risk is "soft landing + high real rates", which delays the gold bull-market clock.
- Physical tightness: SGE Au99.99 closed at 872.48 CNY/g on 2026-07-17 with 5,776.98 kg volume; SGE 6M/1Y weighted lease reference rates for 2026-07-06 to 2026-07-10 were 0.30%/0.26%. The modest 1Y lease-rate rise is not a tightness spike. CME Gold_Stocks direct pull timed out after 25 seconds; latest usable CME inventory remains activity date 2026-07-01.
- Data quality: `scripts/lease_rate.py` again failed on Yahoo HTTP 429; Yahoo GLD/SLV/GDX chart endpoints returned `Edge: Too Many Requests`; WGC still requires login/registration. These are missing-data caveats, not evidence of looseness.
- Next focus: whether gold can reclaim 4100-4115, whether it instead closes repeatedly below 4000, whether DFII10 reaches 2.5, and whether physical/ETF/COT evidence can finally show genuine demand-response confirmation.

## Important Decisions

- The user currently holds a heavy precious-metals position and needs a trading framework that can continuously test whether the bull-market thesis is breaking.
- The dashboard should function as a risk and falsification tool, not as a narrative-confirmation tool.
- Every commit message must begin with exactly one English category prefix: `[Architecture Optimization]` for framework, configuration, tooling, documentation-structure, or process-rule changes; `[Data Update]` for market-data, dashboard-reading, report, indicator-log, or event-log updates.
- Separate three clocks: long-term thesis, market/position timing, and concrete trading actions.
- The monitoring framework should distinguish:
  - Bull market intact but in correction.
  - Correction entering late stage.
  - Turn confirmed.
  - Bull thesis requires reassessment.
- Future agents should not merge the two roles casually. Theory agents improve the thesis; monitoring agents apply the thesis to current data and record evidence.
- Preserve `research/黄金中长期趋势研究框架 v2.md` as an unchanged baseline unless the user explicitly asks to replace or modify the archive.
- For future theory work, preserve the Patch 1 distinction between hard-core layer and soft layer. Do not use "central-bank/structural buying" as an automatic left-side support argument without the ex-post demand-response test described in §9.1.
- For future monitoring work, preserve Patch 2's layer order: first-order main-axis monitoring group, then K-shaped distribution front line, then cycle confirmation, then transition signals. Do not promote political-tail narratives to first-order status without the §9.7 market triggers.
- Every market update must begin by recording the exact update time. "Latest data" is not valid unless tied to a timestamp and data cutoff.
- Unless the user explicitly requests lightweight or full, every market update must first compare each indicator's latest data timestamp against its required cadence, then choose update mode. Do not perform unnecessary full refreshes for slow data, and do not use a lightweight refresh when slow or event-driven core data are stale.
- Every market update must include a brief recent-news section after data collection. Use news to detect fresh data releases and interpret short-term market sentiment, but keep it clearly labeled as auxiliary context; the investment judgment still comes from the framework and monitored signals.

## Next Actions

- Improve the first market-signal update by adding reliable daily ETF price/flow sources for GLD, SLV, and GDX. Yahoo Finance and Stooq were unreliable/blocked during the first update.
- Build or add a Python updater for automatically retrievable data, especially FRED series. First implemented module: `scripts/lease_rate.py` (implied gold lease rate, patch 3 §6.4B; weekly; stdlib-only; Yahoo COMEX curve + NY Fed SOFR with FRED fallback; run before each weekly dashboard update, appends `data/lease_rate.csv`). Next automation candidates: COMEX registered/eligible stocks and an importer for `data/physical_tightness.csv` from user-exported CME/SGE/Swiss-Impex/WGC files. Keep manually verified sources for ETF/COT/WGC/AI capex where needed.
- When the user asks for theory work, use `research/黄金中长期趋势研究框架（持续更新版）.md` as the source document.
- When the user asks for monitoring work, update `dashboard.md` and the CSV logs first, then summarize whether any red/yellow/blue/green conditions changed.

## Python Environment

The project's dependencies are already installed in the virtual environment at `/Users/huanbosun/Documents/myenv`. Activate it before running Python code.
