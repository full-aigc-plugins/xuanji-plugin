#!/usr/bin/env python3
"""玄空飞星运盘计算与校验（MVP：运盘/年盘，山向盘不在范围）。

玄机插件（xuanji-plugin, Apache-2.0）原创。

规则（校验口径）:
- 洛书飞泊路径：中5 → 乾6 → 兑7 → 艮8 → 离9 → 坎1 → 坤2 → 震3 → 巽4。
  运数 k（1-9）入中宫，沿路径顺飞递增：宫 path[i] 得星 (k+i)（mod 9，0 记 9）。
- 九星：一白(贪狼,水)、二黑(巨门,土)、三碧(禄存,木)、四绿(文昌,木)、
  五黄(廉贞,土)、六白(武曲,金)、七赤(破军,金)、八白(左辅,土)、九紫(右弼,火)。
- 校验模式：给定模型报出的运盘 JSON {"宫": 星数}，与本工具按运数算出的盘逐宫核对。

用法:
  python3 fei_xing.py --yun 9
  python3 fei_xing.py --yun 9 --verify '{"5":9,"6":1,"7":2,"8":3,"9":4,"1":5,"2":6,"3":7,"4":8}'

退出码 0=一致/计算成功；1=校验不一致；2=参数错误。
"""

from __future__ import annotations

import argparse
import json
import sys

FLY_PATH = ("5", "6", "7", "8", "9", "1", "2", "3", "4")  # 中→乾→兑→艮→离→坎→坤→震→巽
PALACE_NAMES = {"1": "坎(北)", "2": "坤(西南)", "3": "震(东)", "4": "巽(东南)",
                "5": "中", "6": "乾(西北)", "7": "兑(西)", "8": "艮(东北)", "9": "离(南)"}
STARS = {
    1: "一白·贪狼·水", 2: "二黑·巨门·土", 3: "三碧·禄存·木",
    4: "四绿·文昌·木", 5: "五黄·廉贞·土", 6: "六白·武曲·金",
    7: "七赤·破军·金", 8: "八白·左辅·土", 9: "九紫·右弼·火",
}


def yun_board(yun: int) -> dict[str, int]:
    """运数入中，沿飞泊路径顺飞。"""
    if yun not in range(1, 10):
        raise ValueError("运数必须是 1-9")
    out: dict[str, int] = {}
    for i, palace in enumerate(FLY_PATH):
        out[palace] = (yun + i - 1) % 9 + 1
    return out


def verify_board(yun: int, reported: dict[str, int]) -> list[str]:
    expect = yun_board(yun)
    problems: list[str] = []
    if sorted(reported) != sorted(FLY_PATH):
        problems.append(f"运盘必须覆盖九宫 1-9，收到 {sorted(reported)}")
        return problems
    for palace, star in reported.items():
        if star != expect[palace]:
            problems.append(f"宫{palace}{PALACE_NAMES[palace]} 应为{STARS[expect[palace]]}，报盘为{star}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="玄空飞星运盘计算与校验")
    parser.add_argument("--yun", required=True, type=int, help="运数 1-9（如 2024 年起为九运）")
    parser.add_argument("--verify", help='校验模式：模型报盘 JSON {"宫": 星数}')
    args = parser.parse_args()

    try:
        board = yun_board(args.yun)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.verify:
        try:
            reported = {str(k): int(v) for k, v in json.loads(args.verify).items()}
        except (ValueError, TypeError):
            print('参数错误：--verify 需要 {"宫": 星数} 形式的 JSON 对象', file=sys.stderr)
            return 2
        problems = verify_board(args.yun, reported)
        if problems:
            for p in problems:
                print(f"FAIL {p}")
            print("结论：报盘与运盘不符，禁止基于它解读。")
            return 1
        print(f"结论：报盘与{args.yun}运盘一致，可进入解读。")
    else:
        print(f"{args.yun}运飞星盘（运盘）：")
        for palace in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            star = board[palace]
            print(f"- 宫{palace} {PALACE_NAMES[palace]}：{STARS[star]}")
    print("本结果为传统术数的娱乐化演绎，仅供娱乐，不构成任何专业建议。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
