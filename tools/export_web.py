#!/usr/bin/env python3
"""problems/ 와 docs/ 의 내용을 웹 학습 허브에 내장합니다.

    python tools/export_web.py

1. web/app.html 안의 `/*DATA:START*/ ... /*DATA:END*/` 사이를 최신 문제 데이터로 바꿉니다.
2. app.html 을 완전한 HTML 문서로 감싼 web/index.html 을 만듭니다.
   → index.html 한 파일만 브라우저로 열어도 (서버 없이) 동작합니다.
"""
import inspect
import json
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from practice import all_problems  # noqa: E402

APP = ROOT / "web" / "app.html"
INDEX = ROOT / "web" / "index.html"
DOCS = ROOT / "docs"


def topic_meta(topic):
    doc = DOCS / f"{topic}.md"
    name, summary = topic, ""
    if doc.exists():
        text = doc.read_text(encoding="utf-8")
        m = re.search(r"^#\s+(.+)$", text, re.M)
        if m:
            name = re.sub(r"^\d+\.\s*", "", m.group(1)).strip()
        m = re.search(r"^>\s*(.+)$", text, re.M)
        if m:
            summary = m.group(1).strip()
    return {"id": topic, "name": name, "summary": summary, "doc": f"docs/{topic}.md"}


def clip(text, limit=300):
    return text if len(text) <= limit else text[: limit - 3] + "..."


def source_of(fn):
    if fn is None:
        return ""
    src = textwrap.dedent(inspect.getsource(fn))
    return re.sub(r"^def (reference|brute_force|alternative)\(", "def solution(", src, count=1)


def main():
    problems, topics = [], []
    seen_topics = set()
    for p in all_problems():
        try:
            p.module
        except Exception as e:  # noqa: BLE001
            print(f"건너뜀 {p.topic}/{p.slug}: {e!r}", file=sys.stderr)
            continue
        if p.topic not in seen_topics:
            seen_topics.add(p.topic)
            topics.append(topic_meta(p.topic))
        tests = [
            {"call": clip(", ".join(repr(a) for a in t["input"])), "output": clip(repr(t["output"]))}
            for t in p.get("TESTS", [])[:3]
        ]
        problems.append({
            "slug": p.slug,
            "topic": p.topic,
            "title": p.title,
            "level": p.level,
            "source": p.get("SOURCE", ""),
            "pattern": p.get("PATTERN", ""),
            "description": textwrap.dedent(p.get("DESCRIPTION", "")).strip(),
            "signature": p.get("SIGNATURE", ""),
            "hints": p.get("HINTS", []),
            "explanation": textwrap.dedent(p.get("EXPLANATION", "")).strip(),
            "solution": source_of(p.get("reference")),
            "alternative": source_of(p.get("alternative") or p.get("brute_force")),
            "tests": tests,
            "hasPerf": p.get("perf_case") is not None,
        })
    data = {"topics": topics, "problems": problems}
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</", "<\\/")  # </script> 가 문자열 안에 있어도 안전하도록
    html = APP.read_text(encoding="utf-8")
    new = re.sub(
        r"/\*DATA:START\*/.*?/\*DATA:END\*/",
        lambda _: f"/*DATA:START*/{payload}/*DATA:END*/",
        html,
        count=1,
        flags=re.S,
    )
    APP.write_text(new, encoding="utf-8")
    INDEX.write_text(
        "<!doctype html>\n<html lang=\"ko\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        "<style>body{margin:0}[hidden]{display:none!important}</style>\n</head>\n<body>\n"
        "<!-- 이 파일은 tools/export_web.py 가 web/app.html 로부터 생성합니다. app.html 을 수정하세요. -->\n"
        + new + "\n</body>\n</html>\n",
        encoding="utf-8",
    )
    print(f"web/app.html, web/index.html 업데이트: 주제 {len(topics)}개, 문제 {len(problems)}개")


if __name__ == "__main__":
    main()
