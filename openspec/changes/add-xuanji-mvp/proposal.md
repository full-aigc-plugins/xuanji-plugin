# Proposal: add-xuanji-mvp

## Why

赛博玄学 Skill 生态已现（八字/奇门/紫微/姻缘/风水/塔罗六个独立上游仓），但它们分散、无 AIGC 成象面、且多数无 license。full-aigc-plugins 生态缺一个**娱乐向、合规、可成象**的玄学插件：把六科术数装进一个插件，确定性排盘归脚本防幻觉，古籍知识带出处防瞎编，生图交给生态内已有付费守卫的插件，自身不碰计费通道。

## What Changes

- 新增插件 `xuanji`（玄机 · 赛博玄学，仓库 `xuanji-plugin`），MVP 含六科占算技能：`xuanji-bazi` / `xuanji-qimen` / `xuanji-ziwei` / `xuanji-yinyuan` / `xuanji-fengshui` / `xuanji-tarot`。
- 新增 AIGC 成象技能 `xuanji-fu`（符箓/开运壁纸）与 `xuanji-chart`（命盘图/塔罗牌面/罗盘可视化），经跨插件 handoff 调用 dreamina-canvas 或 comfy-design，本插件不自建付费生图通道。
- 新增质量环技能 `xuanji-loop`（观象环）：成象 → 独立解象子代理按 rubric 小数评分（反棘轮）→ ≤3 轮或 stall 即停下问用户。
- 新增契约层技能 `xuanji-harness`：三铁律（确定性归脚本/知识归 references 带出处/模型只解释）、付费门禁约定、免责声明强制。
- 上游内容合规：仅 `bazi-skill`、`Master-skill`（均 MIT）可搬内容并记入 NOTICE；其余四仓（Numerologist_skills / yinyuan-skills / fengshui.skill / tarot-skill）**零逐字搬运**，只移植结构与方法论，以 8-gram Jaccard 相似度扫描验收。
- 全部输出强制娱乐免责声明；拒绝医疗/法律/投资类提问。

## Capabilities

### New Capabilities

- `divination-core` — 六科占算核心：确定性排盘脚本（带测试）、带出处的古籍知识表、引文审计、免责声明强制、上游内容合规。
- `auspicious-visual-generation` — AIGC 成象：反概念艺术提示词纪律、付费门禁（复用宿主插件 quote→confirm）、未装生图插件时优雅降级为纯文本解读。
- `reading-quality-loop` — 观象环：独立 fresh-context 解象子代理、小数分 + 反棘轮、娱乐档 ≤3 轮 + stall 停下问人、每轮证据落盘。
- `safe-skill-distribution` — 分发面：三宿主 manifest 一致性、README/SKILL.md 安装面带娱乐定位。

### Modified Capabilities

（无 —— 全新插件，无既有 spec。）

## Impact

- **新增仓库**：`full-aigc-plugins-repositories/xuanji-plugin`（本仓）， Apache-2.0 + NOTICE 归属区。
- **跨插件依赖（运行时可选）**：`dreamina-canvas`（付费生图首选，自带 quote→confirm 台账）或 `comfy-design`（备选）；按 Cross-Skill Reference Discipline 用技能名 + 安装命令引用，禁止相对路径。
- **只读引用**：`research/` 下六个上游仓（Numerologist_skills、bazi-skill、yinyuan-skills、Master-skill、fengshui.skill、tarot-skill），永不直接修改。
- **无外部新增依赖**：排盘/抽签脚本纯 Python 标准库 + pytest；生图通道完全外置。
- **非目标（Non-goals）**：不做"改命/开光/法事"类付费话术；不做付费会员/抽成体系；不做自建生图 API 通道与 quota 扣费；不在 hook 层做视觉门禁（借鉴 image-factory 结论：契约层管质量，hooks 只做意图守卫且 MVP 可省）；不支持流年全文批命等长文付费产品；不上线真实付费功能（MVP 仅娱乐）。
