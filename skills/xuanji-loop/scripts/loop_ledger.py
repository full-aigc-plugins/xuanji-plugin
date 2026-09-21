#!/usr/bin/env python3
"""观象环台账（append-only）。

玄机插件（xuanji-plugin, Apache-2.0）原创。设计吸取教训：数字历史必须
可追溯，后轮不得覆盖前轮记录（append-only，写即校验）。

台账文件格式（JSON）:
  {"plugin": "xuanji", "task": "...", "rounds": [
      {"round": 1, "artifact": "path/to/image.png",
       "scores": {"composition": 2.5, "symbol": 2.0, "mood": 1.5, "detail": 1.0},
       "total": 7.0, "verdict": "continue", "notes": "..."}
  ]}

API:
  append_round(ledger_path, round_entry)  -> 校验并追加；round 序号必须为
      len(rounds)+1；已有记录禁止改动（追加后整体重读校验一致性）。
  decide(rounds, cap=3, target=8.0, stall_delta=0.5) -> 决策：
      reach_target / stall / cap_reached / continue。

CLI:
  python3 loop_ledger.py append --ledger .xuanji/loop-ledger.json --entry '<json>'
  python3 loop_ledger.py decide --ledger .xuanji/loop-ledger.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCORE_KEYS = {"composition", "symbol", "mood", "detail"}
VERDICTS = {"continue", "stop", "ask-user"}


def _load(path: Path) -> dict:
    if not path.exists():
        return {"plugin": "xuanji", "rounds": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "rounds" not in data or not isinstance(data["rounds"], list):
        raise ValueError("台账文件格式不合法：需要含 rounds 数组的 JSON 对象")
    return data


def _validate_entry(entry: dict, expected_round: int) -> None:
    if entry.get("round") != expected_round:
        raise ValueError(f"round 序号必须为 {expected_round}，收到 {entry.get('round')!r}")
    scores = entry.get("scores")
    if not isinstance(scores, dict) or set(scores) != SCORE_KEYS:
        raise ValueError(f"scores 必须恰含 {sorted(SCORE_KEYS)}")
    for key, value in scores.items():
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"分数 {key} 必须是非负数")
    if entry.get("verdict") not in VERDICTS:
        raise ValueError(f"verdict 必须是 {sorted(VERDICTS)}")
    for field in ("artifact", "notes"):
        if not isinstance(entry.get(field), str):
            raise TypeError(f"{field} 必须是字符串（artifact 留痕、notes 留言）")


def append_round(path: Path, entry: dict) -> dict:
    ledger = _load(path)
    _validate_entry(entry, len(ledger["rounds"]) + 1)
    before = json.dumps(ledger["rounds"], ensure_ascii=False)
    ledger["rounds"].append(entry)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
    after = json.loads(path.read_text(encoding="utf-8"))
    prior = json.dumps(after["rounds"][:-1], ensure_ascii=False)
    if prior != before:
        raise RuntimeError("append-only 违约：追加导致历史记录被改动")
    return after


def total_of(entry: dict) -> float:
    return round(sum(entry["scores"].values()), 2)


def decide(rounds: list[dict], cap: int = 3, target: float = 8.0, stall_delta: float = 0.5) -> str:
    if not rounds:
        return "continue"
    last = rounds[-1]
    if last["verdict"] in ("stop", "ask-user"):
        return "ask-user" if last["verdict"] == "ask-user" else "stop"
    if total_of(last) >= target:
        return "reach_target"
    if len(rounds) >= cap:
        return "cap_reached"
    if len(rounds) >= 2:
        prev, curr = rounds[-2], rounds[-1]
        if total_of(curr) - total_of(prev) < stall_delta:
            return "stall"
    return "continue"


def main() -> int:
    parser = argparse.ArgumentParser(description="观象环台账（append-only）")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_append = sub.add_parser("append", help="追加一轮记录")
    p_append.add_argument("--ledger", required=True, help="台账 JSON 路径")
    p_append.add_argument("--entry", required=True, help="轮次记录 JSON 字符串")

    p_decide = sub.add_parser("decide", help="基于台账给决策")
    p_decide.add_argument("--ledger", required=True)

    args = parser.parse_args()
    path = Path(args.ledger)

    if args.cmd == "append":
        try:
            entry = json.loads(args.entry)
        except ValueError:
            print("参数错误：--entry 需要合法 JSON", file=sys.stderr)
            return 2
        try:
            ledger = append_round(path, entry)
        except (ValueError, TypeError, RuntimeError) as exc:
            print(f"FAIL {exc}", file=sys.stderr)
            return 2
        print(f"round {entry['round']} 已追加（共 {len(ledger['rounds'])} 轮）")
        return 0

    ledger = _load(path)
    print(decide(ledger["rounds"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
