"""Tests for xuanji-loop scripts/loop_ledger.py (task 3.2)."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from loop_ledger import append_round, decide, total_of


def entry(round_no: int, comp=2.0, symbol=2.0, mood=1.5, detail=1.0, verdict="continue"):
    return {
        "round": round_no,
        "artifact": f".xuanji/round-{round_no}.png",
        "scores": {"composition": comp, "symbol": symbol, "mood": mood, "detail": detail},
        "total": None,
        "verdict": verdict,
        "notes": f"round {round_no}",
    }


class TestLedger(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ledger = Path(self.tmp.name) / "loop-ledger.json"

    def tearDown(self):
        self.tmp.cleanup()

    def test_append_sequence_and_history_preserved(self):
        append_round(self.ledger, entry(1))
        append_round(self.ledger, entry(2))
        data = json.loads(self.ledger.read_text(encoding="utf-8"))
        self.assertEqual([r["round"] for r in data["rounds"]], [1, 2])
        self.assertEqual(data["rounds"][0]["notes"], "round 1")

    def test_round_number_gap_rejected(self):
        append_round(self.ledger, entry(1))
        with self.assertRaises(ValueError):
            append_round(self.ledger, entry(3))

    def test_bad_scores_rejected(self):
        bad = entry(1)
        bad["scores"] = {"composition": 2.0}
        with self.assertRaises(ValueError):
            append_round(self.ledger, bad)

    def test_negative_score_rejected(self):
        with self.assertRaises(ValueError):
            append_round(self.ledger, entry(1, comp=-1))

    def test_total_and_decisions(self):
        rounds = [
            entry(1, comp=2.0, symbol=2.0, mood=1.5, detail=1.0),  # 6.5
            entry(2, comp=2.0, symbol=2.0, mood=1.5, detail=1.0),  # 6.5 与上轮同分 → stall
        ]
        self.assertEqual(total_of(rounds[0]), 6.5)
        self.assertEqual(decide(rounds[:1]), "continue")
        self.assertEqual(decide(rounds), "stall")

    def test_reach_target(self):
        rounds = [entry(1, comp=3, symbol=3, mood=1.8, detail=0.5)]
        self.assertEqual(total_of(rounds[0]), 8.3)
        self.assertEqual(decide(rounds), "reach_target")

    def test_cap_reached(self):
        rounds = [entry(1), entry(2, comp=2.6), entry(3, comp=2.8)]
        self.assertEqual(decide(rounds), "cap_reached")

    def test_ask_user_verdict_wins(self):
        rounds = [entry(1, verdict="ask-user")]
        self.assertEqual(decide(rounds), "ask-user")

    def test_small_improvement_continues(self):
        rounds = [
            entry(1, comp=2.0, symbol=2.0, mood=1.0, detail=1.0),  # 6.0
            entry(2, comp=2.2, symbol=2.0, mood=1.2, detail=1.2),  # 6.6 → +0.6
        ]
        self.assertEqual(decide(rounds), "continue")


if __name__ == "__main__":
    unittest.main()
