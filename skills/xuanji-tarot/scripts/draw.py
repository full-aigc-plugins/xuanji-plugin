#!/usr/bin/env python3
"""塔罗抽牌（可播种复现，仅标准库）。

玄机插件（xuanji-plugin, Apache-2.0）原创；仅参考无 license 上游的
"脚本抽签 + 测试" 结构模式，零内容搬运。

用法:
  python3 draw.py --spread three-card            # 默认三牌阵
  python3 draw.py --spread one-card --question "..."
  python3 draw.py --seed 20260922 --spread celtic-cross

输出 JSON（stdout）: {spread, question, seed, cards: [{position, name, arcana, orientation}]}
同 seed 同 spread 同张数 ⇒ 结果完全一致。
"""

from __future__ import annotations

import argparse
import json
import random
import sys

MAJOR_ARCANA = [
    "愚者", "魔术师", "女祭司", "女皇", "皇帝", "教皇",
    "恋人", "战车", "力量", "隐士", "命运之轮", "正义",
    "吊人", "死神", "节制", "恶魔", "高塔", "星星",
    "月亮", "太阳", "审判", "世界",
]

SUITS = {
    "权杖": ("火", "行动、激情、事业"),
    "圣杯": ("水", "情感、关系、直觉"),
    "宝剑": ("风", "思维、冲突、真相"),
    "星币": ("土", "物质、财务、身体"),
}
RANKS = [
    "Ace", "二", "三", "四", "五", "六", "七", "八", "九", "十",
    "侍从", "骑士", "王后", "国王",
]

SPREADS = {
    "one-card": 1,
    "three-card": 3,
    "five-card": 5,
    "celtic-cross": 10,
}


def full_deck() -> list[dict]:
    deck = [{"name": name, "arcana": "major"} for name in MAJOR_ARCANA]
    for suit in SUITS:
        for rank in RANKS:
            deck.append({"name": f"{suit}{rank}", "arcana": "minor"})
    return deck


def draw(seed: int | None, spread: str, question: str | None) -> dict:
    if spread not in SPREADS:
        raise ValueError(f"unknown spread: {spread}")
    n = SPREADS[spread]
    rng = random.Random(seed)  # seed=None 时仍可用，但结果不可复现
    deck = full_deck()
    picked = rng.sample(deck, n)
    cards = [
        {
            "position": i + 1,
            "name": card["name"],
            "arcana": card["arcana"],
            "orientation": "逆位" if rng.random() < 0.5 else "正位",
        }
        for i, card in enumerate(picked)
    ]
    return {"spread": spread, "question": question, "seed": seed, "cards": cards}


def main() -> int:
    parser = argparse.ArgumentParser(description="塔罗抽牌（可播种复现）")
    parser.add_argument("--spread", default="three-card", choices=sorted(SPREADS), help="牌阵")
    parser.add_argument("--question", help="所问之事（仅记录）")
    parser.add_argument("--seed", type=int, help="随机种子（复现用）")
    args = parser.parse_args()
    try:
        result = draw(args.seed, args.spread, args.question)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
