---
name: xuanji-harness
description: 玄机插件团的调用规范（仅供娱乐的契约层）：三铁律、付费门禁、免责声明固定文案与跨插件 handoff 写法。当任意 xuanji-* 技能需要确认计算/知识/解释分工、涉及生图付费边界或免责话术口径时，先读本规范。
---

# Xuanji Harness — 团队调用规范

## 三铁律

1. **确定性计算归脚本**：凡排盘（四柱/飞星）、抽签抽牌、宫位校验，必须调用技能目录下 `scripts/` 中带 pytest 的脚本；同输入必同输出。模型**禁止**口算排盘、禁止凭记忆万年历改干支、禁止在脚本失败时口头补盘。脚本失败 = 该科解读终止并如实告知。
2. **古籍知识归 references（带出处）**：解读中引用的古籍原文必须能在本仓 `references/citations-registry.md` 登记出处（书名 + 篇目）。产出引文后必须跑 `scripts/audit_citations.py`；审计未过的引文删除或改写，**严禁编造经文**。
3. **模型只做解释**：解释、建议、话术全部基于脚本数字与 references 知识，不得反向修改盘面数字迁就说法。

## 娱乐边界（硬约束）

- 每次解读输出末尾**必须**携带免责声明固定文案（见下）。
- 用户提出医疗、法律、投资类问题（买什么股票、吃什么药、要不要离婚诉讼等）时：拒绝以术数作答，建议咨询专业人士，**不得**给出任何择股/用药/诉讼指向。
- **禁止**出现"改命、开光、法事、消灾收费"类话术；禁止引导任何付费、捐献、转账行为。本插件完全免费。
- 语气中性建设性，不输出极端或恐吓性断语。

### 免责声明固定文案

```
——
本结果为传统术数的娱乐化演绎，仅供娱乐，不构成任何医疗、法律、投资或其他专业建议；如有现实需求，请咨询相关专业人士。
```

## 付费门禁（生图）

- 玄机本插件**不经手任何付费请求**：`xuanji-chart` / `xuanji-fu` 只产出提示词与验收标准。
- 生图 handoff 首选 **dreamina-canvas**（其 quote→confirm 台账即门禁），备选 **comfy-design**（发现免费/生成计费、一次提交）。未安装则走各成象技能的优雅降级路径。
- 失败不自动重提交；提交 id 一旦产生立即落盘 `.xuanji/` 台账。
- 观象环（`xuanji-loop`）≤ 3 轮；stall（两轮提分 < 0.5 或同一 gap 连续两轮被点名）即停，问用户是否重摇。

## 跨插件 handoff 写法

引用生态内其他技能时，一律使用**技能名 + 安装命令**，禁止相对路径：

```markdown
hand off to the **dreamina-canvas-generate-image** skill.
Install: `npx skills add full-aigc-plugins/dreamina-canvas-plugin --skill dreamina-canvas-generate-image`.
```

## 分发面约定

- 三宿主 manifest（`.zcode-plugin/plugin.json` / `.codex-plugin/plugin.json` / `kimi.plugin.json`）的 name、version、技能集合必须一致，由 `scripts/check_distribution.py` 断言。
- 全部 SKILL.md 的 frontmatter description 与 README 首屏必须带娱乐定位表述。

## Gotchas

1. **脚本失败不许补盘**：宁可终止并如实告知，也不许口头编盘——铁律一的红线。
2. **引文先审计再出口**：表外直引必须改写为转述，audit_citations.py 拦下的条目不许硬闯。
3. **付费请求不经手**：生图报价/确认/重试全在宿主插件，玄机侧出现任何付费引导都是事故。
4. **观象环 ≤3 轮**：stall 即停、问人；自动重摇烧 quota 是明令禁止的事故。

## When to Use / Boundary

- 什么时候用：任意 xuanji-* 技能执行中需要确认三铁律分工、付费门禁边界或免责话术口径时。
- 不适用：直接面向用户单独调用（本技能是内部契约层，不是用户入口）。

## Security

本技能不收集、不上传、不发送任何用户数据；无密钥、无凭据、无外部网络请求；抽取与校验全部由本地脚本完成。
