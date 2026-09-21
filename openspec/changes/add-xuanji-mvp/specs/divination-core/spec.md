# divination-core — 六科占算核心

## ADDED Requirements

### Requirement: 确定性排盘（Deterministic Chart Computation）

凡涉及可计算对象（四柱、奇门局、紫微星曜落宫、飞星盘、抽签抽牌）， SHALL 由 `scripts/` 下带 pytest 的脚本完成，同输入必同输出；模型 SHALL NOT 凭记忆或生成补全排盘结果。

#### Scenario: 同一输入两次排盘一致
- **WHEN** 以相同出生时间与性别调用八字排盘脚本两次
- **THEN** 两次输出的四柱、大运、神煞完全一致，且脚本在 pytest 用例中有该输入的固定期望值

#### Scenario: 模型不得编盘
- **WHEN** 脚本缺失或执行失败
- **THEN** 技能显式报错并终止该科解读，不得由模型口头生成排盘结果顶替

### Requirement: 古籍引文可溯源（Traceable Classical Citations）

解读中引用的古籍原文 SHALL 能被 `scripts/audit_citations.py` 解析到 `references/` 知识表中登记的出处（书名 + 篇目）；无出处的引文 SHALL 被审计脚本标记并在输出前剔除。

#### Scenario: 引文全部命中出处
- **WHEN** 一次塔罗/八字解读产出 N 条古籍引文并运行引文审计
- **THEN** 审计报告显示 N/N 命中 `references/` 登记出处，无"编造经文"项

#### Scenario: 无出处引文被拦截
- **WHEN** 模型产出一条 references 中不存在出处的引文
- **THEN** 审计脚本返回非零退出码并列出该条目，技能改写或删除该引文后重跑

### Requirement: 娱乐免责声明（Entertainment Disclaimer）

每科解读输出 SHALL 在末尾携带娱乐免责声明；用户提出的医疗、法律、投资类问题 SHALL 被明确拒绝并建议咨询专业人士，不得借术数名义给出结论性建议。

#### Scenario: 免责声明随输出出现
- **WHEN** 任一科技能完成一次解读
- **THEN** 输出末尾含固定文案的娱乐免责声明（"仅供娱乐，不构成任何医疗/法律/投资建议"）

#### Scenario: 越界问题被拒答
- **WHEN** 用户询问"该买哪支股票"或"吃什么药"
- **THEN** 技能拒绝以术数作答并建议咨询专业人士，不输出任何择股/用药指向

### Requirement: 上游内容合规（Upstream Content Compliance）

对无有效 license 的上游仓（Numerologist_skills、yinyuan-skills、fengshui.skill、tarot-skill）SHALL 零逐字内容搬运；仅 bazi-skill 与 Master-skill（MIT）的内容可搬入且 SHALL 在 `NOTICE` 登记。验收 SHALL 以 8-gram Jaccard 相似度扫描对本仓 `skills/`、`scripts/`、`references/` 对四个无 license 仓零命中为准。

#### Scenario: 相似度扫描零命中
- **WHEN** 对本仓全部产出文件与四个无 license 上游仓运行相似度扫描
- **THEN** 无任何 ≥8 连续字/词的逐字命中；存在命中则删除或改写后重扫
