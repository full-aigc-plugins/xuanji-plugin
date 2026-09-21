# safe-skill-distribution — 分发面

## ADDED Requirements

### Requirement: 多宿主清单一致（Multi-Host Manifest Consistency）

`.zcode-plugin/plugin.json`、`.codex-plugin/plugin.json`、`kimi.plugin.json` 三份清单 SHALL 声明一致的插件名（`xuanji`）、版本号与技能集合；`commands/` 下的斜杠命令 SHALL 与 `skills/` 一一对应。

#### Scenario: 三清单字段一致
- **WHEN** 对三份宿主 manifest 运行一致性断言脚本
- **THEN** name、version、技能名集合三方完全一致，任何一方缺失技能即断言失败

### Requirement: 安装面带娱乐定位（Entertainment Positioning at Install Surface）

README 与每个 SKILL.md 的 frontmatter description SHALL 明示"传统术数 + 娱乐定位"；安装面（README 首屏、marketplace 简介）SHALL 声明不提供医疗/法律/投资建议、无任何付费收费项。

#### Scenario: README 首屏含定位与边界
- **WHEN** 阅读 README 首屏
- **THEN** 可见"娱乐定位"表述与免责边界声明，且不存在任何付费引导话术
