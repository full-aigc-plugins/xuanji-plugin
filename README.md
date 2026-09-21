# 玄机 · 赛博玄学（xuanji-plugin）

> 天机不可泄露，玄机可以参。

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
| | |
|---|---|
| Current version | 0.1.0 |
| 安装 | `npx skills add full-aigc-plugins/xuanji-plugin --skill xuanji-bazi` |

**玄机**是一个娱乐向玄学 Agent Skills 插件：八字、奇门遁甲、紫微斗数、姻缘、风水、塔罗六科传统术数，配合 AIGC 成象（命盘图、塔罗牌面、符箓壁纸、罗盘可视化）。

**本插件仅供娱乐。** 传统术数是文化遗产与民俗趣味，不构成任何医疗、法律、投资建议；本插件完全免费，无任何付费项目。

## 三条铁律

1. **确定性计算归脚本** —— 排盘、抽签、飞星全部由带 pytest 的脚本完成，同输入同输出；模型只做解释，禁止口算排盘、禁止编造古籍引文。
2. **古籍知识归 references（带出处）** —— 每条引文可被 `scripts/audit_citations.py` 审计到出处。
3. **娱乐优先** —— 全部输出附免责声明；医疗/法律/投资类提问一律拒绝并建议咨询专业人士；观象环最多 3 轮，卡住就停下来问人，绝不自动重摇烧钱。

## 技能一览

| 技能 | 用途 |
|---|---|
| `xuanji-bazi` | 四柱八字排盘与解读（天定历法锚点，脚本排盘） |
| `xuanji-qimen` | 奇门遁甲问测（脚本校验所报之盘） |
| `xuanji-ziwei` | 紫微斗数命盘解读（脚本校验星曜落宫） |
| `xuanji-yinyuan` | 月老姻缘：合婚 / 生肖配对 / 求签 / 桃花 |
| `xuanji-fengshui` | 阳宅风水：玄空飞星排盘与解读 |
| `xuanji-tarot` | 塔罗牌阵抽取与解读 |
| `xuanji-loop` | 观象环：成象质量环（独立解象 + 反棘轮 + ≤3 轮） |
| `xuanji-chart` | 命盘图 / 塔罗牌面 / 罗盘可视化成象 |
| `xuanji-fu` | 符箓 / 开运壁纸成象 |
| `xuanji-harness` | 契约层：三铁律、付费门禁、免责声明（内部规范） |

## AIGC 成象（可选）

成象技能本身不调用任何付费 API：它们产出**提示词与验收标准**，生图经跨插件 handoff 由已安装的生成插件完成——首选 [dreamina-canvas](https://github.com/full-aigc-plugins/dreamina-canvas-plugin)（自带报价→确认台账），备选 comfy-design。未安装任何生图插件时，六科解读照常可用（纯文本），技能会提示可选安装命令。

## License

Apache-2.0。MIT 上游归属见 [NOTICE](./NOTICE)。本插件与任何宗教组织无关，亦未获任何平台背书。
