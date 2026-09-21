"""Tests for scripts/similarity_scan.py (task 2.8)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import similarity_scan as ss

COPIED = "这是一段足够长的上游原创句子，专门用来测试逐字连跑判定是否生效，玄学解读必须严谨对待。"


class TestSimilarityScan(unittest.TestCase):
    def test_unrelated_prose_clean(self):
        a = ss.normalize("玄机是娱乐向玄学插件，排盘归脚本、知识归登记表，模型只做解释层。")
        b = ss.normalize("今天天气不错，适合出门散步看云喝茶。")
        result = ss.scan_pair(a, b)
        self.assertLess(result["max_run"], ss.MAX_RUN_LIMIT)
        self.assertLess(result["ratio"], ss.RATIO_LIMIT)

    def test_copied_prose_flagged(self):
        result = ss.scan_pair(ss.normalize("前。" + COPIED + "。后"), ss.normalize(COPIED))
        self.assertGreaterEqual(result["max_run"], ss.MAX_RUN_LIMIT)

    def test_fact_tables_not_flagged(self):
        ours = ss.normalize(
            "六合：子丑、寅亥、卯戌、辰酉、巳申、午未。三合：申子辰合水局。"
            "六十甲子自甲子乙丑丙寅丁卯始。八门：休生伤杜景死惊开。"
        )
        up = ss.normalize(
            "六合组合为子丑合土、寅亥合木。三合局申子辰合水局、亥卯未合木局。"
            "起甲子乙丑丙寅丁卯。八门乃休生伤杜景死惊开。"
        )
        result = ss.scan_pair(ours, up)
        self.assertLess(result["max_run"], ss.MAX_RUN_LIMIT, result)

    def test_case_insensitive_boilerplate(self):
        # 扫描器源码自身包含上游仓名（大写），不得自证其罪
        ours = ss.normalize("scanner mentions FANzR-arch/Numerologist_skills in UPSTREAMS")
        up = ss.normalize("Numerologist_skills rocks")
        result = ss.scan_pair(ours, up)
        self.assertLess(result["max_run"], ss.MAX_RUN_LIMIT, result)

    def test_real_repo_against_upstreams_green(self):
        results = ss.scan()
        self.assertTrue(results, "scan produced no results — upstream dirs missing?")
        for r in results:
            self.assertEqual(r["verdict"], "OK", r)


if __name__ == "__main__":
    unittest.main()
