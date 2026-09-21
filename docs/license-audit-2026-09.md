# License 审计报告（2026-09）

生成时间：2026-09-22；工具：`scripts/similarity_scan.py`（8-gram Jaccard + 最长逐字连跑，prose-only 抽取：md 剥离代码块、py 仅注释与字符串）。

## 判定口径

- **max_run < 15 个归一化字符** 且 **共享 gram 比例 < 0.005** → OK（零逐字搬运）。
- 事实性固定序列（六十甲子、生肖六合/三合/相冲、24 节气枚举、八门九星序、22 牌名序、仪奇序、十二宫、四化键、五鼠遁口诀）与功能性词元（CLI 参数名、frontmatter 键、文件名、上游仓名）在两侧预先剥离——它们是不受版权保护的口径与接口，不是创作表达。
- 判定聚焦**创作性散文**的逐字命中。

## 可搬内容仓（MIT，NOTICE 已登记归属）

| 上游仓 | License | 搬入物 |
|---|---|---|
| jinchenma94/bazi-skill | MIT（© 2025 jinchenma94） | `skills/xuanji-bazi/` 的排盘核心与五行/时辰/大运/神煞/典籍参考表（重排 + 归属头） |
| xr843/Master-skill | MIT（© 2026 xr843） | 仅"引文审计"模式启发（`scripts/audit_citations.py` 为零搬运自写），无 persona 内容 |

## 零搬运仓（无有效 license，仅模式移植）

| 上游仓 | License 状态 | 共享 8-gram | 比例 | 最长连跑 | 判定 |
|---|---|---|---|---|---|
| Numerologist_skills | 无 license（零搬运仓） | 79 | 0.002216 | 14 | ✅ OK |
| yinyuan-skills | 无 license（零搬运仓） | 58 | 0.001627 | 13 | ✅ OK |
| fengshui.skill | 无 license（零搬运仓） | 17 | 0.000477 | 11 | ✅ OK |
| tarot-skill | 无 license（零搬运仓） | 9 | 0.000252 | 10 | ✅ OK |

## 特例说明

- **tarot-skill**：README 裸写 "MIT" 但仓库无 LICENSE 文件，法律上不构成有效授权 → 按"零搬运"处理。若上游补齐 LICENSE 文件可升级为可搬仓（待上游动作）。
- 本仓 README 的 `[NOTICE](./NOTICE)` 为**本包自身**文件链接，属家规允许的自包引用，不计违规。

## 结论

**全绿。** 对四个无 license 上游仓零逐字搬运；两 MIT 仓归属已登记于仓根 NOTICE。
