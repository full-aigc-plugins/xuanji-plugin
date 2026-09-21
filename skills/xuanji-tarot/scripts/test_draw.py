"""Tests for xuanji-tarot scripts/draw.py (task 2.2)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from draw import SPREADS, draw, full_deck


class TestDraw(unittest.TestCase):
    def test_deck_has_78_unique_cards(self):
        deck = full_deck()
        self.assertEqual(len(deck), 78)
        self.assertEqual(len({c["name"] for c in deck}), 78)
        self.assertEqual(sum(1 for c in deck if c["arcana"] == "major"), 22)

    def test_same_seed_reproducible(self):
        a = draw(42, "three-card", None)
        b = draw(42, "three-card", None)
        self.assertEqual(a, b)

    def test_different_seed_likely_differs(self):
        seen = {tuple(c["name"] for c in draw(s, "three-card", None)["cards"]) for s in range(30)}
        self.assertGreater(len(seen), 20)

    def test_card_count_matches_spread(self):
        for spread, n in SPREADS.items():
            result = draw(7, spread, None)
            self.assertEqual(len(result["cards"]), n, spread)
            for i, card in enumerate(result["cards"]):
                self.assertEqual(card["position"], i + 1)
                self.assertIn(card["orientation"], ("正位", "逆位"))

    def test_no_duplicate_cards_in_one_draw(self):
        result = draw(3, "celtic-cross", None)
        names = [c["name"] for c in result["cards"]]
        self.assertEqual(len(names), len(set(names)))

    def test_unknown_spread_rejected(self):
        with self.assertRaises(ValueError):
            draw(1, "twelve-card", None)


if __name__ == "__main__":
    unittest.main()
