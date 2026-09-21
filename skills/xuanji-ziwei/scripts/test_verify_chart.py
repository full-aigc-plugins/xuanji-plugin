"""Tests for xuanji-ziwei scripts/verify_chart.py (task 2.4)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from verify_chart import PALACE_NAMES, verify


def full_chart() -> dict:
    majors = ["紫微", "天机", "太阳", "武曲", "天同", "廉贞",
              "天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"]
    chart = {name: [] for name in PALACE_NAMES}
    for i, star in enumerate(majors[:12]):
        chart[PALACE_NAMES[i]] = [star]
    chart["福德"] = ["左辅"]  # 补两颗辅星使空宫不报错：允许辅星独守
    chart["父母"] = ["右弼"]
    return chart


class TestVerifyChart(unittest.TestCase):
    def test_legal_chart_passes(self):
        self.assertEqual(verify(full_chart(), None), [])

    def test_legal_chart_with_sihua(self):
        sihua = {"化禄": "武曲", "化权": "太阳", "化科": "天梁", "化忌": "廉贞"}
        self.assertEqual(verify(full_chart(), sihua), [])

    def test_missing_palace_flagged(self):
        chart = full_chart()
        del chart["夫妻"]
        problems = verify(chart, None)
        self.assertTrue(any("缺宫" in p and "夫妻" in p for p in problems))

    def test_star_in_two_palaces_flagged(self):
        chart = full_chart()
        chart["财帛"].append("紫微")
        problems = verify(chart, None)
        self.assertTrue(any("紫微" in p and "同时见于" in p for p in problems))

    def test_unknown_star_flagged(self):
        chart = full_chart()
        chart["命宫"].append("天喜星君")
        problems = verify(chart, None)
        self.assertTrue(any("不在主星/辅星表中" in p for p in problems))

    def test_bad_sihua_key_flagged(self):
        problems = verify(full_chart(), {"化禄": "武曲"})
        self.assertTrue(any("四化键" in p for p in problems))

    def test_sihua_non_major_star_flagged(self):
        sihua = {"化禄": "左辅", "化权": "太阳", "化科": "天梁", "化忌": "廉贞"}
        problems = verify(full_chart(), sihua)
        self.assertTrue(any("不是十四主星" in p for p in problems))

    def test_alias_normalization(self):
        chart = full_chart()
        chart["仆役"] = chart.pop("交友")
        # 归一化后交友宫存在 → 不应再报缺宫
        self.assertFalse(any("缺宫" in p and "交友" in p for p in verify(chart, None)))


if __name__ == "__main__":
    unittest.main()
