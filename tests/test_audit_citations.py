"""Tests for scripts/audit_citations.py (task 2.7)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import audit_citations as ac


class TestAuditCitations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = ac.load_registry()

    def test_registry_loaded(self):
        self.assertIn("滴天髓", self.registry)
        self.assertGreaterEqual(len(self.registry["滴天髓"]), 2)

    def test_registered_quote_passes(self):
        text = "正如《滴天髓》：「何知其人富，财气通门户。」所言，财气要通门户。"
        self.assertEqual(ac.audit(text, self.registry), [])

    def test_punctuated_variant_passes(self):
        text = "《子平真诠》：「八字用神，专求月令。」此为纲。"
        self.assertEqual(ac.audit(text, self.registry), [])

    def test_unregistered_book_fails(self):
        text = "《不存在的书》：「随便一句看起来像古籍的话。」"
        problems = ac.audit(text, self.registry)
        self.assertTrue(any("未登记出处" in p for p in problems))

    def test_garbled_quote_fails(self):
        text = "《滴天髓》：「这句话滴天髓里根本没说过。」"
        problems = ac.audit(text, self.registry)
        self.assertTrue(any("不在《滴天髓》" in p for p in problems))

    def test_paraphrase_without_brackets_ignored(self):
        text = "子平真诠说过，用神专求月令（转述，非直引）。"
        self.assertEqual(ac.audit(text, self.registry), [])

    def test_real_skill_files_are_clean(self):
        for md in sorted((REPO / "skills").rglob("*.md")):
            problems = ac.audit(md.read_text(encoding="utf-8"), self.registry)
            self.assertEqual(problems, [], f"{md.relative_to(REPO)}: {problems}")


if __name__ == "__main__":
    unittest.main()
