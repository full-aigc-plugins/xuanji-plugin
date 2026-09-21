---
name: xuanji-chart
description: 娱乐向命盘可视化成象：把八字/紫微/奇门/塔罗的排盘结果转成命盘图、塔罗牌面图、罗盘仪轨图的成象提示词，经跨插件 handoff 交由 dreamina-canvas 或 comfy-design 生图。当用户想要 命盘图、牌面图、罗盘图、把排盘结果画出来，或成象后需进入质量环时使用。本技能不经手付费请求，仅供娱乐。
---

# 玄机 · 命盘成象（娱乐向）

## 提示词纪律（反概念艺术，硬约束）

成象目标是**图表/牌面级精确图**，不是艺术演绎。提示词必须：

- 写明图式："正俯视的仪表盘式命盘图""平铺正视角的塔罗牌面""俯视的黄铜罗盘仪轨图"。
- 列全要素清单（解象环照此打分）：盘面层数、宫位/牌位数量与排布、符号名称、配色基调、文字位置。
- **禁止**出现：concept art、概念艺术、艺术家演绎、电影感、氛围大图。

## 成象 handoff（二选一，按已安装者）

hand off to the **`dreamina-canvas-generate-image`** skill.
Install: `npx skills add full-aigc-plugins/dreamina-canvas-plugin --skill dreamina-canvas-generate-image`

备选：hand off to the **`comfy-generate-image`** skill.
Install: `npx skills add full-aigc-plugins/comfy-design-plugin --skill comfy-generate-image`

- 玄机不经手任何付费请求：报价、确认、提交、下载全部走宿主插件流程；失败不自动重提交。
- 生成图落盘 `.xuanji/`，然后 hand off to the **`xuanji-loop`** skill. Install: `npx skills add full-aigc-plugins/xuanji-plugin --skill xuanji-loop` 进入质量环。

## 优雅降级（无任何生图插件时）

纯文本照常完成：输出"文字版盘面"（宫位表/牌面描述），并提示可选安装：
`npx skills add full-aigc-plugins/xuanji-plugin --skill xuanji-chart` 已在；请安装 dreamina-canvas（`npx skills add full-aigc-plugins/dreamina-canvas-plugin --skill dreamina-canvas-generate-image`）以启用图像成象。**不得**因此中断解读。

## 边界

排盘数字必须来自对应科技能的脚本输出；成象只做"翻译"，不改任何数字。输出末尾附免责声明：本结果为传统术数的娱乐化演绎，仅供娱乐，不构成任何医疗、法律、投资或其他专业建议。

## Gotchas

1. **提示词里禁出现 concept art**：成象要的是图表/牌面级精确图，概念艺术话术会让整图跑偏。
2. **要素清单必须列全**：层数/宫位/符号/配色缺一项，解象环就在这项上反复扣分。
3. **排盘数字不二次创作**：图上的数字符号必须来自对应科技能的脚本输出。
4. **不经手付费**：报价、确认、重试全在宿主插件（dreamina-canvas/comfy-design），本技能只出提示词。

## When to Use / Boundary

- 什么时候用：用户想把排盘结果变成命盘图/牌面图/罗盘图，或成象后要进质量环。
- 不适用：未安装任何生图插件且用户拒绝安装（走优雅降级，不硬来）；修改排盘数字迁就画面（禁止）。

## Security

本技能不收集、不上传、不发送任何用户数据；无密钥、无凭据、无外部网络请求；抽取与校验全部由本地脚本完成。
