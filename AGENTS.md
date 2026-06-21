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

## Current Status

The project has an initial monitoring scaffold:

- `/Users/huanbosun/Documents/Gold&Silver/dashboard_plan.md`: durable rules for the precious-metals bull-market risk dashboard.
- `/Users/huanbosun/Documents/Gold&Silver/dashboard.md`: periodic dashboard template.
- `/Users/huanbosun/Documents/Gold&Silver/data/indicators.csv`: indicator history table.
- `/Users/huanbosun/Documents/Gold&Silver/data/event_log.csv`: key-event reaction log.

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

## Important Decisions

- The user currently holds a heavy precious-metals position and needs a trading framework that can continuously test whether the bull-market thesis is breaking.
- The dashboard should function as a risk and falsification tool, not as a narrative-confirmation tool.
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

## Next Actions

- Improve the first market-signal update by adding reliable daily ETF price/flow sources for GLD, SLV, and GDX. Yahoo Finance and Stooq were unreliable/blocked during the first update.
- Build or add a Python updater for automatically retrievable data, especially FRED series. Keep manually verified sources for ETF/COT/WGC/AI capex where needed.
- When the user asks for theory work, use `research/黄金中长期趋势研究框架（持续更新版）.md` as the source document.
- When the user asks for monitoring work, update `dashboard.md` and the CSV logs first, then summarize whether any red/yellow/blue/green conditions changed.

## Python Environment

The project's dependencies are already installed in the virtual environment at `/Users/huanbosun/Documents/myenv`. Activate it before running Python code.
