#!/usr/bin/env python3
"""Distribution consistency checks for xuanji-plugin.

Asserts (task 1.3, spec: safe-skill-distribution):
1. The three host manifests (.zcode-plugin/plugin.json, .codex-plugin/plugin.json,
   kimi.plugin.json) agree on name and version, and cover the same skill set
   (skills/ directory vs zcode/kimi manifests; codex manifest lists skills via
   directory convention).
2. Every SKILL.md frontmatter description carries the entertainment positioning.
3. Every SKILL.md body carries the mandatory disclaimer marker.
4. Red-line guard: no paid-ritual solicitation keywords anywhere in skills/.

Exit 0 = all green; exit 1 = violations listed on stdout.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFESTS = (
    REPO / ".zcode-plugin" / "plugin.json",
    REPO / ".codex-plugin" / "plugin.json",
    REPO / "kimi.plugin.json",
)
SKILLS_DIR = REPO / "skills"

ENTERTAINMENT_MARKERS = ("娱乐", "entertainment")
DISCLAIMER_MARKER = "仅供娱乐"
# 只匹配"劝导付费"形状的短语；"禁止转账"这类禁令句由 ALLOWED_CONTEXT 放行
REDLINE_KEYWORDS = ("付费解锁", "扫码支付", "转账至", "奉献金", "功德箱", "开光费", "法事费")
ALLOWED_CONTEXT = ("禁止", "不得", "拒绝", "不经手", "免费", "无任何付费", "付费门禁", "红线", "并非")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    block = text[3:end].strip()
    body = text[end + 4 :]
    meta: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, body


def check() -> list[str]:
    problems: list[str] = []

    # 1. manifest consistency
    manifests = {}
    for path in MANIFESTS:
        if not path.exists():
            problems.append(f"missing manifest: {path.relative_to(REPO)}")
            continue
        manifests[path] = json.loads(path.read_text(encoding="utf-8"))
    if len(manifests) == 3:
        names = {m["name"] for m in manifests.values()}
        if len(names) != 1:
            problems.append(f"manifest name mismatch: {sorted(names)}")
        base_versions = {re.sub(r"\+.*$", "", m["version"]) for m in manifests.values()}
        if len(base_versions) != 1:
            problems.append(f"manifest version mismatch: {sorted(base_versions)}")
        zcode = manifests.get(MANIFESTS[0])
        kimi = manifests.get(MANIFESTS[2])
        if zcode is not None and kimi is not None:
            for field in ("homepage", "license"):
                if zcode.get(field) != kimi.get(field):
                    problems.append(f"manifest {field} mismatch: {zcode.get(field)!r} != {kimi.get(field)!r}")

    actual_skills = sorted(p.name for p in SKILLS_DIR.iterdir() if (p / "SKILL.md").exists())
    if not actual_skills:
        problems.append("skills/ contains no skill directories")
    if len(manifests) == 3:
        for manifest_path, label in ((MANIFESTS[0], "zcode"), (MANIFESTS[2], "kimi")):
            value = manifests[manifest_path].get("skills")
            if isinstance(value, list) and sorted(value) != actual_skills:
                problems.append(
                    f"{label} manifest skills {sorted(value)} != skills/ dirs {actual_skills}"
                )
            # 字符串值（目录约定，如 "skills" / "./skills/"）视为宿主目录引用，不做集合比对

    # commands/ mirror: one command per non-internal skill
    internal = {"xuanji-harness"}
    expected_commands = {s for s in actual_skills if s not in internal}
    commands_dir = REPO / "commands"
    actual_commands = {p.stem for p in commands_dir.glob("*.md")} if commands_dir.exists() else set()
    if actual_commands != expected_commands:
        problems.append(
            f"commands/ mirror mismatch: extra={sorted(actual_commands - expected_commands)} "
            f"missing={sorted(expected_commands - actual_commands)}"
        )

    # 2/3. per-skill checks
    for skill in actual_skills:
        md = SKILLS_DIR / skill / "SKILL.md"
        meta, body = parse_frontmatter(md.read_text(encoding="utf-8"))
        desc = meta.get("description", "")
        if not any(marker in desc for marker in ENTERTAINMENT_MARKERS):
            problems.append(f"{skill}: frontmatter description lacks entertainment positioning")
        if skill == "xuanji-harness":
            continue  # harness states the disclaimer instead of emitting it
        if DISCLAIMER_MARKER not in body:
            problems.append(f"{skill}: body lacks disclaimer marker '{DISCLAIMER_MARKER}'")

    # 4. red-line keywords across all skill files
    def line_at(text: str, pos: int) -> str:
        start = text.rfind("\n", 0, pos) + 1
        end = text.find("\n", pos)
        return text[start : end if end >= 0 else len(text)]

    for md in sorted(SKILLS_DIR.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for kw in REDLINE_KEYWORDS:
            pos = text.find(kw)
            while pos >= 0:
                line = line_at(text, pos)
                if not any(word in line for word in ALLOWED_CONTEXT):
                    rel = md.relative_to(REPO)
                    problems.append(f"red-line keyword {kw!r} found in {rel}: {line.strip()}")
                pos = text.find(kw, pos + 1)
        for m in re.finditer(r"(付费|收款|转账|支付宝|微信支付)", text):
            line = line_at(text, m.start())
            if any(word in line for word in ALLOWED_CONTEXT):
                continue
            rel = md.relative_to(REPO)
            problems.append(f"payment term {m.group(0)!r} needs free-context review in {rel}: {line.strip()}")
    return problems


def main() -> int:
    problems = check()
    if problems:
        for p in problems:
            print(f"FAIL {p}")
        return 1
    print("distribution checks: all green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
