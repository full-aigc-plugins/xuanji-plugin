---
name: xuanji-fu
description: 娱乐向符箓/开运壁纸成象：按传统符箓与吉祥纹样的视觉语言构造生图提示词，经跨插件 handoff 交由 dreamina-canvas 或 comfy-design 生成。当用户想要 符箓图、开运壁纸、平安符样式、新年吉祥壁纸 等视觉产物时使用。本技能不经手付费请求，仅供装饰娱乐，不具备任何宗教或超自然效力。
---

# 玄机 · 符箓成象（娱乐向）

## 定位声明（必须先向用户说明）

生成的"符箓"是**装饰性图像创作**，取材于传统符箓的视觉美学（篆书笔意、朱砂红黄配色、云纹边框），不具备任何宗教或超自然效力；本插件与任何宗教组织无关。

## 提示词纪律（反概念艺术，硬约束）

- 写明图式："竖幅符纸样式的装饰图""手机壁纸比例（9:16）的吉祥纹样图"。
- 列全要素清单：纸/底材质、主字或主纹（具体到哪几个字/哪种纹样）、边框云纹样式、印章位置、配色（朱砂红/明黄/玄黑）。
- 手机壁纸默认 9:16；打印卡默认 3:4。
- **禁止**出现：concept art、概念艺术、艺术家演绎。
- **禁止**真实宗教人物肖像与任何可识别的活人形象。

## 成象 handoff（同 xuanji-chart）

hand off to the **`dreamina-canvas-generate-image`** skill.
Install: `npx skills add full-aigc-plugins/dreamina-canvas-plugin --skill dreamina-canvas-generate-image`

备选：hand off to the **`comfy-generate-image`** skill.
Install: `npx skills add full-aigc-plugins/comfy-design-plugin --skill comfy-generate-image`

- 玄机不经手任何付费请求；失败不自动重提交；生成图落盘 `.xuanji/`。
- 质量不满意时 hand off to the **`xuanji-loop`** skill. Install: `npx skills add full-aigc-plugins/xuanji-plugin --skill xuanji-loop`。

## 优雅降级（无生图插件时）

输出文字版"符面设计稿"（布局/配色/纹样描述），并提示可选安装 dreamina-canvas；不得中断。

## 红线

- **禁止**"开光、加持、供奉、消灾"类话术与一切收费引导（本插件完全免费）。
- **禁止**承诺"贴了就好/挂了就顺"式效果断言；只说"图个彩头、图个好看"。
- 输出末尾附免责声明：本结果为传统术数的娱乐化演绎，仅供娱乐，不构成任何医疗、法律、投资或其他专业建议。

## Gotchas

1. **先声明娱乐属性**：生成前说明这是装饰性图像、无效力，缺这句就是误导。
2. **禁功效断言**：不说"贴了就好"，只说"图个彩头"。
3. **主字主纹要具体**：提示词里必须写明具体字样/纹样，笼统的"一张符"必然跑偏。
4. **禁购物指引**：任何"法器/摆件购买"话术都是红线，与 xuanji-fengshui 同规。

## When to Use / Boundary

- 什么时候用：用户想要符箓样式的装饰图、开运壁纸、新年吉祥图。
- 不适用：要求"开光/加持/供奉"或承诺功效（硬红线）；真实宗教人物肖像与活人形象（拒绝生成）。

## Security

本技能不收集、不上传、不发送任何用户数据；无密钥、无凭据、无外部网络请求；抽取与校验全部由本地脚本完成。
