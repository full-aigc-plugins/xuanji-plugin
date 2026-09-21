# Tasks: add-xuanji-mvp

## 1. 仓库基建

- [x] 1.1 建立分发骨架：`.zcode-plugin/plugin.json` + `.codex-plugin/plugin.json` + `kimi.plugin.json`（name=xuanji, version=0.1.0, 六+三技能清单一致）、`commands/` 斜杠命令镜像、`.gitignore`、`LICENSE`（Apache-2.0）、`NOTICE`（登记 bazi-skill / Master-skill 两项 MIT 归属）、README（首屏含娱乐定位与免责边界）
- [x] 1.2 建立 `skills/xuanji-harness/SKILL.md`：三铁律（确定性归脚本/知识归 references 带出处/模型只解释）、付费门禁约定、免责声明固定文案、跨插件 handoff 写法
- [x] 1.3 CI：`skills-check` 工作流 —— 三 manifest 一致性断言脚本 + 免责声明存在性断言（`scripts/check_distribution.py`，pytest 覆盖）

## 2. divination-core（六科占算）

- [x] 2.1 `skills/xuanji-bazi/`：SKILL.md + `references/`（wuxing/shensha/shichen/dayun 知识表，含出处栏；内容基于 MIT 上游搬入并重排）+ `scripts/pai_pan.py`（重写自 MIT 上游）+ pytest 固定用例
- [x] 2.2 `skills/xuanji-tarot/`：SKILL.md + `references/`（78 张牌意表 + 牌阵，自写）+ `scripts/draw.py`（可播种随机抽牌，自写）+ pytest
- [x] 2.3 `skills/xuanji-qimen/`：SKILL.md + `references/ruleset.md` + `scripts/verify_pan.py`（校验模型所报之盘的局数/三奇六仪排布合法性，MVP 不做完整排盘）+ pytest
- [x] 2.4 `skills/xuanji-ziwei/`：SKILL.md + `references/`（十四主星/四化表）+ `scripts/verify_chart.py`（校验星曜落宫合法性）+ pytest
- [x] 2.5 `skills/xuanji-yinyuan/`：SKILL.md + `references/`（合婚/生肖配对/求签规则，自写）+ `scripts/qiu_qian.py`（求签抽取，自写）+ pytest；六模式菜单交互（移植上游交互模式，文案重写）
- [x] 2.6 `skills/xuanji-fengshui/`：SKILL.md + `references/`（飞星/八宅/择日知识表，自写）+ `scripts/fei_xing.py`（飞星盘计算，自写）+ pytest
- [x] 2.7 `scripts/audit_citations.py` + `references/citations-registry.md`：引文出处登记表与审计脚本，pytest 覆盖命中/未命中两路
- [x] 2.8 `scripts/similarity_scan.py`：对本仓 skills/scripts/references 对四个不可搬上游仓做 8-gram Jaccard 扫描，pytest 用假夹具验证扫描逻辑

## 3. reading-quality-loop（观象环）

- [x] 3.1 `skills/xuanji-loop/SKILL.md`：观象环流程（成象→解象→定卦）、四维 rubric（构图 0-3/符号正确性 0-3/氛围 0-2/细节 0-2）、fresh-context 解象子代理 prompt 模板、反棘轮与 stall 判据、≤3 轮上限、`.xuanji/loop-ledger.json` 台账格式
- [x] 3.2 `scripts/loop_ledger.py`：台账追加写与校验（轮次记录不可被覆盖），pytest

## 4. auspicious-visual-generation（AIGC 成象）

- [x] 4.1 `skills/xuanji-chart/SKILL.md`：命盘图/塔罗牌面/罗盘可视化提示词纪律（反概念艺术）+ 跨插件 handoff（dreamina-canvas 首选/comfy-design 备选，技能名+安装命令写法）+ 优雅降级路径
- [x] 4.2 `skills/xuanji-fu/SKILL.md`：符箓/开运壁纸成象提示词模板库 + 同 4.1 的门禁与降级约束

## 5. 验收与注册

- [x] 5.1 全技能过 TRACE 评分 ≥ 4.5（`scripts/evaluate-package.sh xuanji-plugin`），低于线的按 JSON 分轴修订
- [x] 5.2 跑 `similarity_scan.py` 全绿（四不可搬仓零逐字命中），报告存 `docs/license-audit-2026-09.md`
- [x] 5.3 交叉链接审计：全仓无跨技能 `../` 相对路径（工作区审计脚本零输出）
- [x] 5.4 在 `full-aigc-plugins` hub 注册 marketplace 条目 + README 表行；首个 tag 发版走既有 bump-plugin 流程（修复其已知三缺陷的方案实施时定）

## Audit 2026-09-22（实施留痕）

- 18/18 任务完成；`openspec validate --strict` 绿；68 项 pytest 全绿；`check_distribution.py` 全绿；相似度扫描对 4 个无 license 上游仓零逐字搬运（报告见 `docs/license-audit-2026-09.md`）。
- TRACE 全技能 ≥ 4.52（evaluation-results/ 下 10 份 JSON 为证）。
- 任务 5.4 的 hub 注册（marketplace.json / kimi-marketplace.json / catalog.json / README 表行）已落**本地**；首个 tag `v0.1.0` 发版（commit + push + tag，触发 CDN 图标生效）待用户决策后走 bump-plugin 流程。
- 仓尚未 `git init`/提交（按约定等用户指示）。
