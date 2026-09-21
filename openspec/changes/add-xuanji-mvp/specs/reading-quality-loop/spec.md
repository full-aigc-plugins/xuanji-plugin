# reading-quality-loop — 观象环（生成质量环）

## ADDED Requirements

### Requirement: 独立解象（Independent Fresh-Context Judging）

观象环的评审 SHALL 由 fresh-context 独立子代理执行：不携带前轮对话与自己产出的解读记录，仅见成象结果与 rubric；评分 SHALL 沿 rubric 各维度给小数分（如 构图 0-3 / 符号正确性 0-3 / 氛围一致性 0-2 / 细节 0-2）；若上一轮分数更高而后一轮退步，SHALL 如实降分（反棘轮）。

#### Scenario: 解象人无前轮上下文
- **WHEN** 第 2 轮观象开始
- **THEN** 解象子代理仅收到本轮成象图、rubric 与上一轮分数数字，未收到自己此前的解读文本或修改建议

#### Scenario: 退步必须降分
- **WHEN** 第 3 轮成象相比第 2 轮符号错误更多
- **THEN** 解象本轮总分低于第 2 轮，不得为保持"进步叙事"抬分

### Requirement: 娱乐档循环上限（Entertainment Round Cap）

观象环 SHALL 最多执行 3 轮；出现 stall（总分两轮无提升 ≥0.5，或同一 gap 连续两轮被点名）SHALL 立即停止并向用户呈现当前最优成象，询问是否重摇，SHALL NOT 自动发起新一轮。

#### Scenario: 连续 stall 停下问人
- **WHEN** 第 2、3 轮总分差 < 0.5
- **THEN** 循环在第 3 轮后终止，向用户展示两轮成象与评分，询问"是否再摇一次"，不自动重摇

#### Scenario: 达标提前收敛
- **WHEN** 某轮总分 ≥ 8.0（满分 10）
- **THEN** 循环立即以该轮为定卦结果，不再继续消耗轮次

### Requirement: 循环证据留痕（Loop Evidence Trail）

观象环每轮 SHALL 将轮次号、成象产物路径、各维度分数、解象意见与决策（continue/stop/ask-user）追加写入 `.xuanji/loop-ledger.json`；数字历史 SHALL 保留全部轮次记录，SHALL NOT 被后轮覆盖。

#### Scenario: 台账完整可回放
- **WHEN** 观象环跑满 3 轮后检查 `.xuanji/loop-ledger.json`
- **THEN** 文件含 3 条轮次记录，每条含分数数组与决策字段，且第 1、2 轮记录与终止时一致
