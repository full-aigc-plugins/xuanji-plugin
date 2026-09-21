# auspicious-visual-generation — AIGC 成象

## ADDED Requirements

### Requirement: 成象提示词纪律（Non-Concept-Art Prompt Discipline）

成象提示词 SHALL 要求生成"牌面/图表级精确图"（塔罗牌面、命盘图、罗盘仪轨图、符箓正形），SHALL NOT 使用"concept art / 概念艺术 / 艺术家演绎"类表述（移植 dream-loop 反概念艺术纪律）。

#### Scenario: 塔罗牌面提示词合规
- **WHEN** `xuanji-chart` 为"星星牌正位"构造生图提示词
- **THEN** 提示词描述牌面构图要素（人物、七星、水壶、颜色）且不含"概念艺术/插画演绎"字样

### Requirement: 付费门禁（Paid Generation Gate）

生图 SHALL 经由生态内已带付费守卫的宿主插件（首选 `dreamina-canvas` 的 quote→confirm 台账流程，备选 `comfy-design`）完成；本插件 SHALL NOT 自建计费通道、SHALL NOT 自动重提交失败任务，跨插件引用 SHALL 使用技能名 + 安装命令而非相对路径。

#### Scenario: 生图前先报价确认
- **WHEN** 用户要求生成一张符箓壁纸且已安装 dreamina-canvas
- **THEN** 流程先产出 quota 报价并获得用户确认后才提交生成，提交 id 立即落盘 `.xuanji/` 台账

#### Scenario: 失败不自动重摇
- **WHEN** 生图任务失败或超时
- **THEN** 技能向用户报告失败原因并等待指示，不自动重新提交任何付费请求

### Requirement: 优雅降级（Graceful Degradation）

未安装任何生图插件时，六科纯文本解读 SHALL 照常可用，且 SHALL 提示用户可选安装生图插件以启用成象（附安装命令），不得因此中断解读。

#### Scenario: 无生图插件时纯文本完成
- **WHEN** 用户环境未安装 dreamina-canvas 与 comfy-design 且请求塔罗解读
- **THEN** 技能完成纯文本牌面描述与解读，并输出"可选安装 dreamina-canvas 以生成牌面图"提示
