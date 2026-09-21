---
name: xuanji-bazi
description: 娱乐向四柱八字排盘与解读。排盘由带测试的脚本完成（同输入同输出），模型只做解释。当用户提到 八字、四柱、排盘、命盘、算命、看运势、bazi、birth chart，或想了解性格/大运/流年等话题时使用。仅供娱乐，不构成任何专业建议。
---

# 玄机 · 四柱八字（娱乐向）

三铁律与免责口径以 **`xuanji-harness`** 技能为准。Install: `npx skills add full-aigc-plugins/xuanji-plugin --skill xuanji-harness`。

## 流程（三步）

Step 1 — 收集：阳历生日（`YYYY-MM-DD`）、时辰（钟点 `HH:MM` 或地支 子丑寅…，不确定可标未知做六字）、性别（男/女，决定大运顺逆）。信息一次问齐，展示汇总请用户确认。
Step 2 — 排盘（必须先跑脚本）：
   ```bash
   python3 scripts/pai_pan.py --solar 1990-05-15 --hour 12:00 --sex 男
   python3 scripts/pai_pan.py --solar 1990-05-15 --shichen 午 --sex 男
   python3 scripts/pai_pan.py --lunar 1990-04-21 --shichen 午 --sex 男
   ```
   四柱/大运/流年/神煞/警告**全部以脚本 stdout 为准**（含末尾免责声明节）。脚本失败即终止并告知，禁止口算补盘。
Step 3 — 解读：按脚本输出做日主强弱 → 十神 → 五行平衡 → 大运流年的娱乐化解读。解释口径对照：

- [references/wuxing-tables.md](references/wuxing-tables.md) — 五行/干支/十神/藏干表
- [references/shichen-table.md](references/shichen-table.md) — 时辰对照与五鼠遁
- [references/dayun-rules.md](references/dayun-rules.md) — 大运顺逆与起运
- [references/shensha-table.md](references/shensha-table.md) — 神煞口径（与脚本同表）
- [references/classical-texts.md](references/classical-texts.md) — 典籍论命要点（引文须过引文审计）

## 边界

- 时辰未知 → 时柱"未知"，只做六字分析。
- 脚本警告「节气交界/立春前后」→ 如实告知临界，采用脚本给出的唯一一套柱，不自行另算。
- 引用典籍原文时先查 `references/classical-texts.md` 出处，并跑本仓 `scripts/audit_citations.py`。
- 输出末尾保留脚本生成的免责声明；医疗/法律/投资提问一律拒绝并建议咨询专业人士。

仅供娱乐。人生在于自身的努力和选择。

## Gotchas

1. **夜子时跨日**：23:00 后出生用次日日柱（脚本自动处理），别自己改回当日。
2. **立春前出生**：年柱属上一年（脚本按立春精确分界），立春前后 24 小时脚本会出警告，照警告转述。
3. **节气交界日**：月柱可能只差几小时，脚本警告「节气交界」时如实告知用户，不自行二选一。
4. **神煞别口算**：神煞与脚本同表同口径，脚本没列的不要补算，更不要上网现查。

## When to Use / Boundary

- 什么时候用：用户给出出生信息想看性格、大运、流年，或提到八字/四柱/排盘时。
- 不适用：时辰与阳历/农历生日全部未知（无法排盘）；医疗、法律、投资决策咨询（越界拒答）。

## Security

本技能不收集、不上传、不发送任何用户数据；无密钥、无凭据、无外部网络请求；排盘与校验全部由本地脚本完成。
