"""Tests for xuanji-yinyuan scripts/qiu_qian.py (task 2.5)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qiu_qian import SIGNS, draw_sign


class TestQiuQian(unittest.TestCase):
    def test_sign_table_shapes(self):
        self.assertEqual(len(SIGNS), 24)
        for index, level, title, verse, hint in SIGNS:
            self.assertEqual(index, SIGNS[index - 1][0])
            self.assertIn(level, ("上上", "上", "中吉", "中", "中平", "下"))
            self.assertTrue(title and verse and hint)

    def test_seed_reproducible(self):
        self.assertEqual(draw_sign(7, "q"), draw_sign(7, "q"))

    def test_question_recorded(self):
        result = draw_sign(1, "值得继续吗")
        self.assertEqual(result["question"], "值得继续吗")
        self.assertIn("title", result["sign"])

    def test_draws_cover_most_signs(self):
        seen = {draw_sign(s, None)["sign"]["index"] for s in range(200)}
        self.assertGreater(len(seen), 15)


if __name__ == "__main__":
    unittest.main()
