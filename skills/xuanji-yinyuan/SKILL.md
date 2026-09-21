---
name: xuanji-yinyuan
description: 娱乐向月老姻缘测算，六模式菜单（八字合婚/生肖配对/紫微夫妻宫/求签/桃花运势/八字速配），求签由可复现脚本完成。当用户提到 姻缘、合婚、配对、月老、求签、桃花、脱单、我和TA合适吗、生肖配对 时使用。仅供娱乐，不构成任何专业建议。
---

# 玄机 · 月老姻缘（娱乐向）

## 入口：先亮六模式菜单

按 [references/matching-rules.md](references/matching-rules.md) 的菜单表列出 6 个模式，请用户选号并按"需要的信息"栏收集材料。

## 各模式口径

Step 1 — 模式 1/3（八字合婚/紫微夫妻宫）：排盘/校验遵守对应技能，拿到盘后回本技能做配对解读。
  - hand off to the **`xuanji-bazi`** skill. Install: `npx skills add full-aigc-plugins/xuanji-plugin --skill xuanji-bazi`
  - hand off to the **`xuanji-ziwei`** skill. Install: `npx skills add full-aigc-plugins/xuanji-plugin --skill xuanji-ziwei`
Step 2 — 模式 4（求签）：必须走脚本，禁止口算抽签：
  ```bash
  python3 scripts/qiu_qian.py --question "这段感情值得继续吗"
  ```
  同 `--seed` 可复现；签文 + hint 原样呈现，再配一段娱乐化解读。
Step 3 — 模式 2/5/6：按 matching-rules 的规则表计分与描述，只谈倾向不谈必然。

## 红线（本技能特别加强）

- 不做"你们不合适/必分手"式劝分结论；给沟通建议，不给关系判决。
- 不承诺"本月必脱单"类结果。
- 输出末尾附免责声明：本结果为传统术数的娱乐化演绎，仅供娱乐，不构成任何医疗、法律、投资或其他专业建议；如有现实需求，请咨询相关专业人士。

## Gotchas

1. **别替用户分手**：规则计分只描述倾向，<0 也只说"需要多沟通"，禁止劝分结论。
2. **求签必须走脚本**：qiu_qian.py 才能出签，口算抽签是翻车点；同 seed 同签可复现。
3. **年支速配是粗筛**：无时辰时只比年支并注明粗筛，别当成八字合婚的精度说话。
4. **敏感话题中立**：第三者、婚姻危机等只引导理性沟通，不做道德审判。

## When to Use / Boundary

- 什么时候用：用户带着感情话题来求测，或提到姻缘/合婚/求签/桃花/配对。
- 不适用：替用户做"分不分手"的决定（只给沟通建议不给关系判决）；医疗、法律、投资决策咨询（越界拒答）。

## Security

本技能不收集、不上传、不发送任何用户数据；无密钥、无凭据、无外部网络请求；抽取与校验全部由本地脚本完成。
