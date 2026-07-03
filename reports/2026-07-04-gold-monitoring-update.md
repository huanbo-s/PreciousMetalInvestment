# 2026-07-04 黄金市场状态更新

更新时间：2026-07-04 06:28:36 北京时间（UTC 2026-07-03 22:28:36）
更新模式：full

本次选择 full update，因为7月2日非农后的COMEX结算价已经出炉，周频初请和外央行托管美债更新，且补丁3要求周更前验证实物紧张度脚本。7月3日美国金融市场因独立日观察假期休市，所以本期以7月2日美国结算价和官方数据截止作为锚。06:28进一步合并补录用户提供的SGE每日行情、CME Gold Stocks和SGE租借费率PDF，并对可访问官网源做复核。

## 核心结论

黄金状态维持“黄灯”，但修复确认增强。7月2日COMEX黄金结算价为4112.70，已经站上4100-4115修复区；银价结算60.643，结束七周连跌。这说明非农后的反弹不只是盘中读数，而是至少得到了一次美国结算价确认。

但这还不是右侧转折。初请失业金截至6月27日只有215k，4周均值约222k，远低于260-280k裂痕阈值。2年期美债即使按非农后的新闻报价约4.108%，仍高于3.75%的政策利率上限。ETF资金流、COT洗净后重建、10Y实际利率正式回落都没有确认；实物紧张度已建立首批读数，但只有单期基线，不能证明硬核托底。

## 数据与质量

可靠更新：

- BLS 6月就业报告：非农+57k，失业率4.2%，劳动参与率61.5%，平均时薪+0.3% MoM / +3.5% YoY。
- FRED：DFII10/DGS2/DGS10至2026-07-01，T10YIE至2026-07-02，ICSA至2026-06-27，WMTSECL1至2026-07-01。
- COMEX结算：黄金4112.70，白银60.643。
- CFTC历史包：黄金最新行仍为2026-06-23，管理基金净多+115395张。
- CME Gold Stocks：报告日2026-07-02、活动日2026-07-01；注册库存14826009.194盎司不变，合格库存12634943.363盎司，较前值减少98867.700盎司，合计27460952.557盎司。
- SGE每日行情：2026-07-03 Au99.99收盘910.98元/克，成交量4334.58千克；Au(T+D)收盘910.26元/克。
- SGE黄金同业租借参考费率：2026-06-22至2026-06-26，6个月加权0.30%，1年加权0.36%；官网重下PDF与本地PDF校验一致。

缺口：

- `scripts/lease_rate.py`联网后因Yahoo COMEX曲线返回HTTP 429失败，仍未写入`data/lease_rate.csv`；本次使用SGE官方租借参考费率作为并行/替代基线读数。
- Yahoo chart对GLD/SLV/GDX/DXY返回429，Stooq返回浏览器验证页，因此本期不能可靠登记ETF/GDX日频价格或资金流。
- CME官方XLS直连下载在当前环境中一次HTTP/2中断、一次长时间无传输；本期使用用户提供的CME官方工作簿，并记录官网重拉失败。
- WGC ETF flows下载需要登录/注册，Swiss-Impex需要手工或浏览器导出，LBMA历史表需要MyLBMA/IBA许可，因此SGE-London溢价、瑞士出口、印度溢价和零售金币溢价仍未完成。
- 缺测只降低本期确认度，不能反向解释为“实物不紧张”或“ETF已经转好”。

## 框架判断

一阶主轴继续缓和：弱非农、美元回落、收益率新闻报价下行，对黄金短线有利。但就业链没有完成从“招聘变慢”到“裁员裂缝”的转换，通胀仍高，工资仍粘。Fed反应函数尚未被迫转向宽松。

回调阶段从“关键区测试”推进到“修复确认增强”：4000附近承接有效，4100-4115修复区已被结算价收复。但银价仍未修复63.885参考位，COT净多未洗净，ETF未转正。

政治尾部未升格：T10YIE约2.23，外央行托管美债从2636947降至2625883百万美元，属于需观察的一周回落，不是断崖式逃离。

实物紧张度观察组从“空白”推进到“初始读数建立”：COMEX合格库存单日下降、SGE Au99.99价格与成交量、SGE官方租借费率已经入库，并新增`data/physical_tightness.csv`作为原始登记表。但这些只是基线第一周，尚未形成“价格敏感资金退出而实物多项同向紧张”的背离构型，因此不能给3800-4000托底假设加分。

## 后续观察

下一步关键在2026-07-06美国市场恢复交易后：

1. 黄金能否守住4100-4115上方，而不是假期前后的一次性修复。
2. 2Y是否继续向3.75%政策上限下方靠近。
3. 10Y实际利率是否在FRED官方日频中确认回落。
4. ETF周度流量是否转正，COT是否出现洗净后重建。
5. COMEX库存、SGE租借费率和SGE现货读数能否连续两到四周形成同向基线；租赁利率脚本能否在Yahoo限流解除后补充隐含租赁利率。

结论：不触发牛市重审，也不触发增量资金蓝灯许可。当前最合适的表述是：长期牛市论题未破，短线修复更强，但右侧确认仍缺。

## 主要来源

- BLS Employment Situation Summary, June 2026.
- FRED: `DFII10`, `DGS2`, `DGS10`, `T10YIE`, `DFEDTARU`, `ICSA`, `PCEPILFE`, `WMTSECL1`.
- CFTC Disaggregated COT `fut_disagg_txt_2026.zip`.
- CME Group / user-provided official `Gold_Stocks.xls`.
- Shanghai Gold Exchange daily quotation workbook and official lease-rate PDF.
- WSJ / Dow Jones Market Data / FactSet: COMEX gold and silver settlements, dollar and Treasury yield context.
- AP / Barron's / MarketWatch / Kiplinger: jobless claims, market holiday, Fed and market reaction context.
- WGC / Swiss-Impex / LBMA official pages for availability checks.
- Local updater attempt: `scripts/lease_rate.py`.
