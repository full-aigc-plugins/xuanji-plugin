#!/usr/bin/env python3
"""古籍引文审计：校验输出中的《书》：「原文」直引是否都在出处登记表内。

玄机插件（xuanji-plugin, Apache-2.0）原创；模式受 MIT 上游 xr843/Master-skill
的离线引文审计启发（归属见 NOTICE），实现为零搬运自写。

规则:
- 识别输出文本中的直引：《书名》…「原文」。
- 书名必须在 references/citations-registry.md 登记过；原文与登记文本按
  归一化（去空白、去中英文标点）后互为包含即通过。
- 任何一条不命中即整体不通过（exit 1），列出未命中项。

用法:
  python3 audit_citations.py --file reading-output.md
  python3 audit_citations.py --json '[{"book":"滴天髓","text":"何知其人富，财气通门户"}]'
退出码 0=全部命中；1=存在未命中；2=参数错误。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REGISTRY = REPO / "references" / "citations-registry.md"
CITATION_RE = re.compile(r"《(?P<book>[^》]+?)》(?P<between>[^「]*?)「(?P<text>[^」]+)」")
_STRIP_RE = re.compile(r"[\s，。、；：？！,.:;?!「」『』\"'“”‘’（）()\[\]【】…—·\-\u3000]")


def load_registry(path: Path = REGISTRY) -> dict[str, list[str]]:
    raw = path.read_text(encoding="utf-8")
    m = re.search(r"```json\s*(\{.*?\})\s*```", raw, re.DOTALL)
    if not m:
        raise ValueError("registry 缺少 ```json 数据块")
    data = json.loads(m.group(1))
    table: dict[str, list[str]] = {}
    for item in data.get("citations", []):
        table.setdefault(item["book"], []).append(item["text"])
    return table


def normalize(text: str) -> str:
    return _STRIP_RE.sub("", text)


def audit(text: str, registry: dict[str, list[str]]) -> list[str]:
    misses: list[str] = []
    for match in CITATION_RE.finditer(text):
        book = match.group("book").strip()
        quote = normalize(match.group("text"))
        registered = registry.get(book)
        if not registered:
            misses.append(f"未登记出处：《{book}》")
            continue
        if not any(quote in normalize(entry) or normalize(entry) in quote for entry in registered):
            misses.append(f"原文不在《{book}》登记条目中：「{match.group('text')}」")
    return misses


def main() -> int:
    parser = argparse.ArgumentParser(description="古籍引文出处审计")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="待审计的输出文本文件")
    group.add_argument("--json", help='引文数组 JSON：[{"book":"滴天髓","text":"..."}]')
    args = parser.parse_args()

    try:
        registry = load_registry()
    except (ValueError, OSError) as exc:
        print(f"registry 加载失败：{exc}", file=sys.stderr)
        return 2

    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
        misses = audit(text, registry)
    else:
        try:
            items = json.loads(args.json)
        except ValueError:
            print("参数错误：--json 需要引文数组", file=sys.stderr)
            return 2
        pseudo = "".join(
            f"《{it['book']}》：「{it['text']}」" for it in items
        )
        misses = audit(pseudo, registry)

    if misses:
        for miss in misses:
            print(f"FAIL {miss}")
        print("审计结论：存在表外直引，删除或改为转述后重跑。")
        return 1
    print("审计结论：全部直引命中登记出处，放行。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
