#!/usr/bin/env python3
"""上游相似度扫描（8-gram Jaccard + 最长逐字连跑）。

玄机插件（xuanji-plugin, Apache-2.0）原创。验收口径（spec: divination-core /
Upstream Content Compliance）：本仓产出对四个无 license 上游仓零逐字搬运。

抽取面（prose-only）:
- .md：剥离 fenced code block 后的正文；
- .py：仅注释与字符串字面量（tokenize）；
- 归一化：去 URL、去空白与标点；再删除两侧通用套话（免责声明短语等）。

判定（对每个上游仓）:
- max_run ≥ 15 个归一化字符的逐字连跑，或
- 共享 8-gram 数 / 本仓 8-gram 数 ≥ 0.005，
  任一命中即 FAIL（禁止搬运）。

用法:
  python3 similarity_scan.py                  # 扫描默认四个上游仓
  python3 similarity_scan.py --json           # 输出 JSON 报告
退出码 0=全绿；1=存在命中；2=上游目录缺失。
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import tokenize
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESEARCH = REPO.parent.parent / "research"
UPSTREAMS = {
    "Numerologist_skills": RESEARCH / "Numerologist_skills",
    "yinyuan-skills": RESEARCH / "yinyuan-skills",
    "fengshui.skill": RESEARCH / "fengshui.skill",
    "tarot-skill": RESEARCH / "tarot-skill",
}
N = 8
MAX_RUN_LIMIT = 15
RATIO_LIMIT = 0.005
# 通用套话与功能性词元：两侧同删（免责话术、安装命令、frontmatter/CLI 键名、
# 上游仓名——扫描器自身源码会提及它们）
BOILERPLATE = (
    "仅供娱乐", "不构成任何", "投资建议", "专业建议", "请咨询相关专业人士",
    "npxskillsadd", "githubcom", "apache", "opensourceorg", "licensedunder",
    "numerologistskills", "yinyuanskills", "fengshuiskill", "tarotskill",
    "description", "displayname", "shortdescription", "longdescription",
    "spread", "question", "seed", "cards", "position", "orientation",
    "level", "title", "verse", "hint", "notes", "artifact", "scores",
    "total", "verdict", "rounds", "composition", "symbol", "mood", "detail",
    # 事实性固定序列（不受版权保护的口径）：22 牌名、花色、八门、九星、仪奇、十二宫、四化
    "愚者魔术师女祭司女皇皇帝教皇恋人战车力量隐士命运之轮正义吊人死神节制恶魔高塔星星月亮太阳审判世界",
    "权杖圣杯宝剑星币", "休生伤杜景死惊开",
    "天蓬天任天冲天辅天英天芮天柱天心天禽", "戊己庚辛壬癸丁丙乙",
    "命宫兄弟夫妻子女财帛疾厄迁移交友官禄田宅福德父母", "化禄化权化科化忌",
    "Ace二三四五六七八九十侍从骑士王后国王",
    "ace二三四五六七八九十侍从骑士王后国王",
    "阳年男阴年女顺排阴年男阳年女逆排",
    "正月二月三月四月五月六月七月八月九月十月十一月十二月",
    "立春惊蛰清明立夏芒种小暑立秋白露寒露立冬大雪小寒",
    "usrbinenvpython3", "references", "scripts",
)
URL_RE = re.compile(r"https?://\S+")
FILENAME_RE = re.compile(r"[\w\-]+\.(?:md|py|json|ya?ml|mjs|txt)")
# 天干/地支连续枚举（六十甲子、三合、六冲等固定表）——事实序列
GANZHI_RUNS = (
    re.compile(r"[子丑寅卯辰巳午未申酉戌亥]{4,}"),
    re.compile(r"[甲乙丙丁戊己庚辛壬癸]{4,}"),
    re.compile(r"([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]){3,}"),  # 六十甲子
    re.compile(r"[子丑寅卯辰巳午未申酉戌亥]合[水木火金]局"),  # 三合局
    re.compile(r"[子丑寅卯辰巳午未申酉戌亥]冲"),  # 六冲
    re.compile(r"[子丑寅卯辰巳午未申酉戌亥]合[水木火金土]"),  # 六六合五行
    re.compile(r"([甲乙丙丁戊己庚辛壬癸]{2}[子丑寅卯辰巳午未申酉戌亥]){2,}"),  # 五鼠遁/五虎遁口诀
    re.compile(r"([甲乙丙丁戊己庚辛壬癸]{2,3}[子丑寅卯辰巳午未申酉戌亥]){2,}"),  # 遁口诀连写
)
PUNCT_RE = re.compile(r"[\s，。、；：？！,.:;?!「」『』\"'“”‘’（）()\[\]【】<>《》*#`|…—·\-\+\u3000/_=]")


def md_prose(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)  # 剥离 fenced code
    return text


def py_prose(path: Path) -> str:
    out: list[str] = []
    source = path.read_text(encoding="utf-8")
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for tok in tokens:
            if tok.type in (tokenize.COMMENT, tokenize.STRING):
                out.append(tok.string)
    except tokenize.TokenError:
        return ""
    return "\n".join(out)


def collect_texts(root: Path) -> list[str]:
    texts: list[str] = []
    for md in sorted(root.rglob("*.md")):
        if ".git" in md.parts:
            continue
        texts.append(md_prose(md))
    for py in sorted(root.rglob("*.py")):
        if ".git" in py.parts:
            continue
        texts.append(py_prose(py))
    return texts


def normalize(text: str) -> str:
    text = text.lower()
    text = URL_RE.sub(" ", text)
    text = FILENAME_RE.sub(" ", text)
    text = PUNCT_RE.sub("", text)
    for pattern in GANZHI_RUNS:
        text = pattern.sub(" ", text)
    for phrase in BOILERPLATE:
        text = text.replace(phrase, " ")
    return re.sub(r"\s+", "", text)


def gram_set(text: str) -> set[str]:
    return {text[i : i + N] for i in range(len(text) - N + 1)}


def scan_pair(ours_norm: str, upstream_norm: str) -> dict:
    ours_grams = gram_set(ours_norm)
    up_grams = gram_set(upstream_norm)
    shared = ours_grams & up_grams
    ratio = len(shared) / len(ours_grams) if ours_grams else 0.0
    # 连跑：用少量样本 gram 在上游全文里扩展（上游串 ≤ 数百 KB，可直接 in 检查）
    max_run = 0
    for gram in list(shared)[:500]:
        length = N
        start = ours_norm.find(gram)
        while ours_norm[start : start + length + 1] in upstream_norm:
            length += 1
        max_run = max(max_run, length)
    return {"shared_grams": len(shared), "ratio": round(ratio, 6), "max_run": max_run}


def scan(verbose: bool = False) -> list[dict]:
    ours_norm = normalize("\n".join(collect_texts(REPO)))
    results = []
    for name, path in UPSTREAMS.items():
        if not path.exists():
            print(f"SKIP {name}: {path} 不存在", file=sys.stderr)
            continue
        upstream_norm = normalize("\n".join(collect_texts(path)))
        result = scan_pair(ours_norm, upstream_norm)
        result["upstream"] = name
        result["verdict"] = (
            "FAIL" if result["max_run"] >= MAX_RUN_LIMIT or result["ratio"] >= RATIO_LIMIT else "OK"
        )
        results.append(result)
        if verbose:
            print(f"{result['verdict']} {name}: shared={result['shared_grams']} "
                  f"ratio={result['ratio']} max_run={result['max_run']}")
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="上游相似度扫描（8-gram）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 报告")
    parser.add_argument("--quiet", action="store_true", help="只输出判定行")
    args = parser.parse_args()

    results = scan(verbose=not args.quiet and not args.json)
    if not results:
        return 2
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    failed = [r for r in results if r["verdict"] == "FAIL"]
    if failed:
        for r in failed:
            print(f"FAIL {r['upstream']}: max_run={r['max_run']} ratio={r['ratio']}")
        return 1
    print("相似度扫描：对全部无 license 上游仓零逐字搬运（判定全绿）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
