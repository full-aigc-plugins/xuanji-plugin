"""Tests for scripts/check_distribution.py (task 1.3)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import check_distribution as cd


class TestCheckDistribution(unittest.TestCase):
    def test_green_on_current_repo(self):
        problems = cd.check()
        self.assertEqual(problems, [], f"unexpected problems: {problems}")

    def test_every_skill_has_disclaimer(self):
        for skill_dir in sorted((REPO / "skills").iterdir()):
            if not (skill_dir / "SKILL.md").exists():
                continue
            if skill_dir.name == "xuanji-harness":
                continue
            body = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("仅供娱乐", body, skill_dir.name)

    def test_missing_manifest_detected(self):
        orig = cd.MANIFESTS
        cd.MANIFESTS = orig[:-1] + (cd.REPO / "nonexistent.json",)
        try:
            problems = cd.check()
        finally:
            cd.MANIFESTS = orig
        self.assertTrue(any("missing manifest" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
