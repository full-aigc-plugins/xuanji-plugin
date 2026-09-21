"""Tests for xuanji-qimen scripts/verify_pan.py (task 2.3)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from verify_pan import expected_dipan, verify


class TestVerifyPan(unittest.TestCase):
    def test_yang_1_shun_xu(self):
        # 阳遁一局：戊在1宫，顺行 己2 庚3 …
        expect = expected_dipan("yang", 1)
        self.assertEqual(expect["1"], "戊")
        self.assertEqual(expect["2"], "己")
        self.assertEqual(expect["9"], "乙")

    def test_yin_9_ni_xing(self):
        # 阴遁九局：戊在9宫，逆行 8宫己、7宫庚 …
        expect = expected_dipan("yin", 9)
        self.assertEqual(expect["9"], "戊")
        self.assertEqual(expect["8"], "己")
        self.assertEqual(expect["1"], "乙")

    def test_legal_pan_passes(self):
        dipan = expected_dipan("yang", 3)
        self.assertEqual(verify("yang", 3, dipan, sorted("休生伤杜景死惊开"), None), [])

    def test_wrong_gong_flagged(self):
        dipan = expected_dipan("yang", 3)
        dipan["5"] = "乙"  # 篡改一宫
        problems = verify("yang", 3, dipan, None, None)
        self.assertTrue(any("宫5" in p for p in problems))

    def test_duplicate_yiqi_flagged(self):
        dipan = expected_dipan("yin", 2)
        dipan["1"] = dipan["2"]
        problems = verify("yin", 2, dipan, None, None)
        self.assertTrue(any("重复" in p for p in problems))

    def test_bad_bamen_set(self):
        dipan = expected_dipan("yang", 1)
        problems = verify("yang", 1, dipan, ["休", "生", "伤"], None)
        self.assertTrue(any("八门" in p for p in problems))

    def test_bad_ju_rejected(self):
        self.assertTrue(any("局数" in p for p in verify("yang", 0, {}, None, None)))

    def test_bad_mode_rejected(self):
        self.assertTrue(any("mode" in p for p in verify("zhuan", 1, {}, None, None)))


if __name__ == "__main__":
    unittest.main()
