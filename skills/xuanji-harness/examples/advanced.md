# 示例：跨插件 handoff 写法

正确：hand off to the **`dreamina-canvas-generate-image`** skill. Install: `npx skills add full-aigc-plugins/dreamina-canvas-plugin --skill dreamina-canvas-generate-image`
错误：`../dreamina-canvas-plugin/skills/...` 相对路径（安装粒度是单技能，路径必然 404）。
