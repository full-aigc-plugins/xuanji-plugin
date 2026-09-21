#!/usr/bin/env python3
"""奇门遁甲排盘合法性校验（MVP：校验模型所报之盘，不做时家定局）。

玄机插件（xuanji-plugin, Apache-2.0）原创；结构模式参考无 license 上游
（确定性校验归脚本），内容零搬运。

规则（校验口径）:
- 地盘：仪奇序列 戊己庚辛壬癸丁丙乙。
  阳遁 k 局：戊落 k 宫，按宫号顺行（9 回 1）；宫 p 得 sequence[(p-k) mod 9]。
  阴遁 k 局：戊落 k 宫，按宫号逆行（1 回 9）；宫 p 得 sequence[(k-p) mod 9]。
- 八门集合 = {休,生,伤,杜,景,死,惊,开}（提供时须恰为 8 门各一）。
- 九星集合 = {天蓬,天任,天冲,天辅,天英,天芮,天柱,天心,天禽}（提供时须恰为 9 星各一）。

用法:
  python3 verify_pan.py --mode yang --ju 3 \
    --dipan '{"1":"戊","2":"己","3":"庚","4":"辛","5":"壬","6":"癸","7":"丁","8":"丙","9":"乙"}' \
    --bamen 休,生,伤,杜,景,死,惊,开 --jiuxing 天蓬,天任,天冲,天辅,天英,天芮,天柱,天心,天禽

退出码 0=合法；1=校验失败（原因列表见 stdout）；2=参数错误。
"""

from __future__ import annotations

import argparse
import json
import sys

SEQUENCE = "戊己庚辛壬癸丁丙乙"
PALACES = tuple("123456789")
BAMEN = {"休", "生", "伤", "杜", "景", "死", "惊", "开"}
JIUXING = {"天蓬", "天任", "天冲", "天辅", "天英", "天芮", "天柱", "天心", "天禽"}


def expected_dipan(mode: str, ju: int) -> dict[str, str]:
    seq = list(SEQUENCE)
    k = PALACES.index(str(ju))
    out = {}
    for p in PALACES:
        i = PALACES.index(p)
        if mode == "yang":
            out[p] = seq[(i - k) % 9]
        else:
            out[p] = seq[(k - i) % 9]
    return out


def verify(mode: str, ju: int, dipan: dict[str, str], bamen: list[str] | None,
           jiuxing: list[str] | None) -> list[str]:
    problems: list[str] = []
    if mode not in ("yin", "yang"):
        problems.append(f"mode 必须是 yin|yang，收到 {mode!r}")
        return problems
    if ju not in range(1, 10):
        problems.append(f"局数必须是 1-9，收到 {ju!r}")
        return problems
    if sorted(dipan) != sorted(PALACES):
        problems.append(f"地盘必须覆盖九宫 1-9，收到 {sorted(dipan)}")
        return problems
    expect = expected_dipan(mode, ju)
    for p in PALACES:
        got = dipan[p]
        if got not in SEQUENCE:
            problems.append(f"宫{p} 的 {got!r} 不属于仪奇序列 {SEQUENCE}")
        elif got != expect[p]:
            problems.append(f"宫{p} 应为 {expect[p]}，报盘为 {got}")
    if len(set(dipan.values())) != 9:
        problems.append("地盘九宫存在重复仪奇")
    if bamen is not None and sorted(bamen) != sorted(BAMEN):
        problems.append(f"八门集合不符：{bamen}")
    if jiuxing is not None and sorted(jiuxing) != sorted(JIUXING):
        problems.append(f"九星集合不符：{jiuxing}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="奇门遁甲排盘合法性校验")
    parser.add_argument("--mode", required=True, choices=("yin", "yang"), help="阴遁/阳遁")
    parser.add_argument("--ju", required=True, type=int, help="局数 1-9")
    parser.add_argument("--dipan", required=True, help="地盘 JSON：{\"宫\":\"仪奇\"} ×9")
    parser.add_argument("--bamen", help="八门，逗号分隔（可选）")
    parser.add_argument("--jiuxing", help="九星，逗号分隔（可选）")
    args = parser.parse_args()

    try:
        dipan = json.loads(args.dipan)
        if not isinstance(dipan, dict):
            raise TypeError
    except (ValueError, TypeError):
        print("参数错误：--dipan 需要是 {\"宫\":\"仪奇\"} 形式的 JSON 对象", file=sys.stderr)
        return 2
    bamen = [x for x in args.bamen.split(",") if x] if args.bamen else None
    jiuxing = [x for x in args.jiuxing.split(",") if x] if args.jiuxing else None

    problems = verify(args.mode, args.ju, dipan, bamen, jiuxing)
    if problems:
        for p in problems:
            print(f"FAIL {p}")
        print("结论：此盘不合法，禁止基于它解读；请重排或修正后复检。")
        return 1
    print("结论：地盘排布合法（口径见脚本头注），可进入解读。")
    print("本结果为传统术数的娱乐化演绎，仅供娱乐，不构成任何专业建议。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
