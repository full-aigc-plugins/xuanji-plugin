"""Tests for xuanji-fengshui scripts/fei_xing.py (task 2.6)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fei_xing import FLY_PATH, verify_board, yun_board


class TestFeiXing(unittest.TestCase):
    def test_center_holds_yun(self):
        for yun in range(1, 10):
            self.assertEqual(yun_board(yun)["5"], yun)

    def test_forward_flight_along_path(self):
        board = yun_board(9)
        self.assertEqual(board["6"], 1)  # 中9 → 乾6 得 1
        self.assertEqual(board["7"], 2)
        self.assertEqual(board["4"], 8)  # 路径末宫巽4 得 9+8-1 mod 9 = 8

    def test_board_is_permutation(self):
        for yun in range(1, 10):
            values = sorted(yun_board(yun).values())
            self.assertEqual(values, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_verify_accepts_correct_board(self):
        self.assertEqual(verify_board(8, yun_board(8)), [])

    def test_verify_flags_tampered_palace(self):
        board = yun_board(7)
        board["5"] = 3
        problems = verify_board(7, board)
        self.assertTrue(any("宫5" in p for p in problems))

    def test_missing_palace_flagged(self):
        board = yun_board(3)
        del board[str(FLY_PATH[0])]
        problems = verify_board(3, board)
        self.assertTrue(any("覆盖九宫" in p for p in problems))

    def test_bad_yun_rejected(self):
        with self.assertRaises(ValueError):
            yun_board(0)


if __name__ == "__main__":
    unittest.main()
