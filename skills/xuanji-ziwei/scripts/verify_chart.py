#!/usr/bin/env python3
"""紫微斗数命盘合法性校验（MVP：校验模型所报之盘的结构，不做安星）。

玄机插件（xuanji-plugin, Apache-2.0）原创。

规则（校验口径）:
- 十二宫齐全且各唯一：命宫、兄弟、夫妻、子女、财帛、疾厄、迁移、
  交友(仆役)、官禄(事业)、田宅、福德、父母。
- 主星只能是十四主星之一：紫微系（紫微/天机/太阳/武曲/天同/廉贞）
  与天府系（天府/太阴/贪狼/巨门/天相/天梁/七杀/破军）。
  本校验只查"报出的每颗星都属主星/辅星表、主星不得重宫"，不查安星公式。
- 四化键必须合法：化禄/化权/化科/化忌，且值的格式为"星名"。

用法:
  python3 verify_chart.py \
    --palaces '{"命宫":["紫微","天府"],"夫妻宫":["贪狼"],...}' \
    --sihua '{"化禄":"武曲","化权":"太阳","化科":"天梁","化忌":"廉贞"}'

退出码 0=结构合法；1=校验失败；2=参数错误。
"""

from __future__ import annotations

import argparse
import json
import sys

PALACE_NAMES = (
    "命宫", "兄弟", "夫妻", "子女", "财帛", "疾厄",
    "迁移", "交友", "官禄", "田宅", "福德", "父母",
)
PALACE_ALIASES = {"仆役": "交友", "事业": "官禄", "田宅宫": "田宅"}
MAJOR_STARS = {
    "紫微", "天机", "太阳", "武曲", "天同", "廉贞",
    "天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军",
}
SIHUA_KEYS = {"化禄", "化权", "化科", "化忌"}

# 常见辅星/煞星：允许出现在宫内，但不参与"主星"判定
SUPPORT_STARS = {
    "左辅", "右弼", "文昌", "文曲", "天魁", "天钺", "禄存", "天马",
    "擎羊", "陀罗", "火星", "铃星", "地空", "地劫", "化禄", "化权", "化科", "化忌",
}


def normalize(palaces: dict) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for key, stars in palaces.items():
        name = PALACE_ALIASES.get(key, key)
        out[name] = list(stars)
    return out


def verify(palaces_raw: dict, sihua: dict | None) -> list[str]:
    problems: list[str] = []
    palaces = normalize(palaces_raw)
    missing = [p for p in PALACE_NAMES if p not in palaces]
    if missing:
        problems.append(f"缺宫：{'、'.join(missing)}")
    unknown = [k for k in palaces if k not in PALACE_NAMES]
    if unknown:
        problems.append(f"未知宫位名：{'、'.join(unknown)}")

    seen_major: dict[str, str] = {}
    for name, stars in palaces.items():
        if not isinstance(stars, list) or not stars:
            problems.append(f"{name} 必须是至少一颗星的数组")
            continue
        duplicates_in_palace = len(stars) != len(set(stars))
        if duplicates_in_palace:
            problems.append(f"{name} 宫内星重复：{stars}")
        for star in stars:
            if star in MAJOR_STARS:
                if star in seen_major:
                    problems.append(f"主星 {star} 同时见于 {seen_major[star]} 与 {name}")
                seen_major[star] = name
            elif star not in SUPPORT_STARS:
                problems.append(f"{name} 宫的 {star!r} 不在主星/辅星表中（安星错漏或错别字）")

    if sihua is not None:
        if set(sihua) != SIHUA_KEYS:
            problems.append(f"四化键必须恰为 {sorted(SIHUA_KEYS)}，收到 {sorted(sihua)}")
        for key, star in sihua.items():
            if star not in MAJOR_STARS:
                problems.append(f"{key} 的 {star!r} 不是十四主星")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="紫微斗数命盘合法性校验")
    parser.add_argument("--palaces", required=True, help='命盘 JSON：{"命宫":["紫微",...],...}')
    parser.add_argument("--sihua", help='四化 JSON：{"化禄":"武曲",...}')
    args = parser.parse_args()
    try:
        palaces = json.loads(args.palaces)
        if not isinstance(palaces, dict):
            raise TypeError
    except (ValueError, TypeError):
        print("参数错误：--palaces 需要宫->星数组的 JSON 对象", file=sys.stderr)
        return 2
    sihua = json.loads(args.sihua) if args.sihua else None

    problems = verify(palaces, sihua)
    if problems:
        for p in problems:
            print(f"FAIL {p}")
        print("结论：此盘结构不合法，禁止基于它解读；请重排后复检。")
        return 1
    print("结论：命盘结构合法（十二宫齐、主星不重宫），可进入解读。")
    print("本结果为传统术数的娱乐化演绎，仅供娱乐，不构成任何专业建议。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
