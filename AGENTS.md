# Repository Agent Guidance

<!-- partme-agent-plugin-policy:v1 -->
## Partme Agent Plugin Architecture Rules v1

- 组织级架构规范（唯一事实源）：[Partme Agent Plugin Architecture Rules v1](https://github.com/full-aigc-plugins/.github/blob/main/docs/standards/partme-agent-plugin-architecture-rules-v1.md)。
- **Harness 可选**：默认直接使用 Skills + CLI/MCP；只有确有必要时才保留最多一个可发现的 `skills/*-harness/SKILL.md`，其 `scripts/harness.py` 也可选。
- 不复制宿主 Agent Runtime 或已有 CLI/MCP 的业务执行、任务数据库与权威状态；代码能力必须能追踪到真实 Agent → Skill/Command → Tool → 结果的调用链。
- 保留本仓库现有 OpenSpec、安全门禁、发布及验证要求。静态校验不代表真实宿主可执行性；所有上线宣称均需实际宿主验收。
- CI 统一使用组织级 [Partme Plugin Architecture 检查器](https://github.com/full-aigc-plugins/.github/blob/main/scripts/check_plugin_architecture.py)，不得复制实现或禁用检查。
<!-- /partme-agent-plugin-policy:v1 -->
