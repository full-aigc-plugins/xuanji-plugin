# Design: add-xuanji-mvp

## Context

上游六个独立玄学 Skill 仓已被克隆至 `research/`（只读）。License 实测：`bazi-skill`（MIT © 2025 jinchenma94）、`Master-skill`（MIT © 2026 xr843）可合规搬运；`Numerologist_skills`、`yinyuan-skills`、`fengshui.skill` 无任何 license（默认版权全保留），`tarot-skill` 仅 README 裸写 "MIT" 无 LICENSE 文件（法律上无效，按不可搬处理）。生态内已有可复用资产：dream-loop（MIT，观象环原型）、comfy-design-plugin（house 分发骨架）、dreamina-canvas（自带 quote→confirm 付费台账）。

## Goals / Non-Goals

**Goals**

- 六科占算 + AIGC 成象 + 质量环的最小可玩闭环（MVP），纯娱乐定位。
- 确定性计算、知识、解释三层分离，从结构上防"张口瞎编"。
- License 合规可验收（相似度扫描零命中）。

**Non-Goals**

- 不做付费/会员/抽成；不自建生图计费通道；不做改命开光类话术。
- 不在 hook 层做质量门禁（image-factory 结论：契约层管质量，hooks 只做意图守卫，MVP 连意图守卫也省）。
- 不支持流年长文批命等重度产品形态。

## Decisions

### D1. 命名与身份

插件 id `xuanji`，仓库 `xuanji-plugin`，展示名「玄机 · 赛博玄学」，slogan「天机不可泄露，玄机可以参」。技能前缀 `xuanji-*` 与生态习惯（comfy-* / jianying-*）一致。

### D2. 三层分工（六个上游仓共同的黄金模式，升为插件铁律）

- `scripts/`：排盘/抽签/飞星/校验，纯 Python 标准库 + pytest，同输入同输出。八字排盘可参考 bazi-skill 的 `pai_pan.py`（MIT）重写搬入；塔罗抽牌自写（上游仅模式可参考）；奇门/紫微校验器 MVP 先做"校验模型给的盘"而非完整排盘（降低范围）。
- `references/`：古籍知识表 + 出处登记（书名/篇目/通行本页码或章句号），引文审计脚本据此校验。
- `SKILL.md`：交互流、输出约束、免责声明；模型只做解释层。

### D3. License 合规矩阵（验收即 spec 的 Upstream Content Compliance）

| 上游仓 | License | 可搬内容 | 备注 |
|---|---|---|---|
| bazi-skill | MIT | ✅ 内容+模式 | NOTICE 登记版权 |
| Master-skill | MIT | ✅ 内容+模式 | 只取引文审计/评测模式，不搬 20 个 persona |
| tarot-skill | 无（README 裸 "MIT"） | ❌ 仅模式 | 上游补 LICENSE 文件前不搬任何文本 |
| Numerologist_skills | 无 | ❌ 仅模式 | 工程化分层模式极佳，结构照搬、文字零搬 |
| yinyuan-skills | 无 | ❌ 仅模式 | 六模式菜单交互模式可抄 |
| fengshui.skill | 无 | ❌ 仅模式 | persona+方法论 references 结构可抄 |

验收：8-gram Jaccard 相似度扫描（沿用 research-upstream-sources-map 的方法）对本仓产出对四个不可搬仓零逐字命中。

### D4. 成象完全外置（本插件零计费面）

`xuanji-chart` / `xuanji-fu` 只产出**提示词 + 验收 rubric**，生图经跨插件 handoff：首选 `dreamina-canvas`（其 quote→confirm 台账即付费门禁），备选 `comfy-design`（其 harness 已有"发现免费/生成计费、一次提交"铁律）。跨插件引用写法：技能名 + `npx skills add full-aigc-plugins/<pkg> --skill <skill>`，禁止相对路径（工作区 Cross-Skill Reference Discipline）。不再移植 fal-batch.mjs —— dream-loop 的付费守卫在此是向下移植，宿主插件已有同级或更强实现。

### D5. 观象环 = dream-loop Pro 循环的娱乐档裁剪

保留：fresh-context 解象子代理、四维 rubric 小数分、反棘轮、stall 判据、证据台账（`.xuanji/loop-ledger.json`，吸取 image-factory"数字历史要可追溯"教训）。裁剪：轮次上限 3（Pro 无上限）、达标线 8/10、无时间预算、无 FPS 项；judge 子代理**不接收**自己此前的解读文本（worker/judge 分离）。

### D6. 分发骨架照抄 comfy-design-plugin 最小集

三宿主 manifest + `commands/` 镜像 + README/LICENSE/NOTICE。MVP **不**引入 vendored 技能五件套（lock/vendor/sync）——本插件全部技能自研，无外部 vendored 面；CI 仅 skills-check 自检（manifest 一致性断言 + 免责声明存在性断言）。

### D7. 免责与红线落点

免责声明作为每科 SKILL.md 的输出约束（非 hook 强制——MVP 无 hooks）；内容红线（拒答医疗/法律/投资、不出现改命收费话术）写入 harness 并在 skills-check 断言关键词存在。

## Risks / Trade-offs

- **[内容审核风险] 玄学内容在部分平台敏感** → 定位为"传统文化 + 娱乐"，全安装面声明娱乐边界；不碰红线话术。MVP 接受"部分应用商店可能拒收"的 trade-off。
- **[license 误搬风险] 相似度扫描可能漏改写级抄袭** → 扫描是底线不是上限；pattern 移植一律重写 + 换名 + 换例。
- **[跨插件依赖风险] 用户未装生图插件** → 优雅降级为纯文本解读（已有 spec）。
- **[范围风险] 奇门/紫微完整排盘工程量大** → MVP 用"脚本校验模型报盘"而非全量排盘，完整排盘留待后续 change。

## Migration Plan

全新仓，无迁移。落地顺序：仓库基建 → divination-core → 观象环 → 成象 → 分发注册。每步可独立验证（tasks.md 对应）。

## Open Questions

- marketplace 条目与图标（CDN logo）随首个发版走 bump-plugin 流程，MVP 期先用占位 logo。
- `xuanji-yinyuan` 是否拆为独立技能或并入 `xuanji-bazi`（姻缘高度依赖八字合婚）——倾向独立（上游为独立交互入口），实施时定。
