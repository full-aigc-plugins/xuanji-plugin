---
name: xuanji-loop
description: 娱乐向成象质量环（观象环）：成象后由 fresh-context 独立解象子代理按四维 rubric 小数评分，反棘轮（退步必须降分），最多 3 轮，stall 即停下问用户。当需要为命盘图/塔罗牌面/符箓等成象结果做质量迭代、或用户对成象结果不满意要求改进时使用。仅供娱乐。
---

# 玄机 · 观象环（成象质量环）

移植自 dream-loop 的 Pro 循环，裁剪为娱乐档：**≤3 轮、达标 8/10、stall 停下问人、绝不自动重摇**。

## 循环（每轮五步）

Step 1 — 成象：hand off to the **`xuanji-chart`** skill. Install: `npx skills add full-aigc-plugins/xuanji-plugin --skill xuanji-chart`（或 `xuanji-fu`）。产出图存 `.xuanji/round-<n>.png`。
Step 2 — 自检：自己先看一遍图是否符合成象提示词的要素清单。
Step 3 — 独立解象（关键步）：派一个 **fresh-context 解象子代理**——它只收到：本轮成象图 + 下述 rubric + 前轮总分数字。**不**给它自己此前的解读文本、修改建议或提示词草稿（防止顺着旧思路打分）。
Step 4 — 记账（必须走脚本）：
   ```bash
   python3 scripts/loop_ledger.py append --ledger .xuanji/loop-ledger.json \
     --entry '{"round":1,"artifact":".xuanji/round-1.png","scores":{"composition":2.5,"symbol":2.0,"mood":1.5,"detail":1.0},"total":7.0,"verdict":"continue","notes":"..."}'
   ```

   ```bash
   python3 scripts/loop_ledger.py decide --ledger .xuanji/loop-ledger.json
   ```
Step 5 — 决策（以脚本 decide 输出为准）：

| decide 输出 | 动作 |
|---|---|
| `continue` | 按解象意见修改提示词/重成象，回到第 1 步 |
| `stall`（两轮提分 < 0.5 或同一 gap 连续两轮被点名） | 停止迭代，展示当前最优成象，**问用户**是否重摇 |
| `reach_target`（≥ 8.0） | 定卦：以本轮为最终结果 |
| `cap_reached`（已满 3 轮） | 定卦或交用户裁决，**不得**自动开新一轮 |
| `ask-user` / `stop` | 按记录的直接交用户 |

## 解象 rubric（子代理 prompt 模板要点）

四维 rubric 与完整子代理 prompt 见 [references/rubric.md](references/rubric.md)；评分口径要点：小数分、可执行差距清单、反棘轮。

## 边界

- 台账 append-only：脚本会拒绝乱序/缺字段/负分，并校验历史未被改动；**禁止**手改 `.xuanji/loop-ledger.json`。
- 娱乐档：任何情况下不自动发起第 4 轮；不自动重提交付费生图请求（付费门禁见 harness）。
- 输出末尾附免责声明：本结果为传统术数的娱乐化演绎，仅供娱乐，不构成任何医疗、法律、投资或其他专业建议。

## Gotchas

1. **台账只能追加**：loop_ledger.py 是 append-only，手改 `.xuanji/loop-ledger.json` 会被校验出违约。
2. **轮次号必须连续**：append 会拒绝跳号（1 之后必须是 2），乱序即参数错误。
3. **解象人必须清空上下文**：给子代理喂了自己的旧解读，评分就失去独立性——这是观象环的命门。
4. **反棘轮**：本轮比上轮差，总分必须更低；为叙事好看抬分 = 数据造假。

## When to Use / Boundary

- 什么时候用：成象结果需要质量迭代，或用户对命盘图/符箓/牌面不满意要求改进。
- 不适用：需要第 4 轮的"再改一版"（娱乐档硬上限 3 轮，交用户裁决）；没有成象产物的纯文本解读。

## Security

本技能不收集、不上传、不发送任何用户数据；无密钥、无凭据、无外部网络请求；抽取与校验全部由本地脚本完成。
