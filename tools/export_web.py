#!/usr/bin/env python3
"""problems/ 와 docs/ 의 내용을 웹 학습 허브에 내장합니다.

    python tools/export_web.py

1. web/app.html 안의 `/*DATA:START*/ ... /*DATA:END*/` 사이를 최신 문제 데이터로 바꿉니다.
2. app.html 을 완전한 HTML 문서로 감싼 web/index.html 을 만듭니다.
   → index.html 한 파일만 브라우저로 열어도 (서버 없이) 동작합니다.
3. web/src/course.html + course.js 와 실습 문제 데이터로 인터랙티브 코스 web/course.html 을 만듭니다.

    python tools/export_web.py --bare-dir <폴더>   # 문서 껍데기 없는 버전도 저장 (Artifact 게시용)
"""
import ast
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
COURSE_SRC = ROOT / "web" / "src" / "course.html"
COURSE_JS = ROOT / "web" / "src" / "course.js"
COURSE_OUT = ROOT / "web" / "course.html"
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


SKIP_DEFS = {"reference", "alternative", "brute_force", "prepare", "present", "check", "perf_case", "board_variant"}
SKIP_CONSTS = {"TITLE", "LEVEL", "SOURCE", "PATTERN", "DESCRIPTION", "SIGNATURE", "HINTS", "TESTS", "EXPLANATION",
               "COMPARE", "PERF_LIMIT", "IMPORTS"}


def source_of(fn):
    """함수 소스를 `def solution(...)` 형태로 바꾸고, 함수가 쓰는 모듈 수준 import 를 앞에 붙입니다."""
    if fn is None:
        return ""
    src = textwrap.dedent(inspect.getsource(fn))
    src = re.sub(rf"\b{fn.__name__}\(", "solution(", src)  # 재귀 호출도 함께 이름을 바꿈
    module_src = Path(fn.__code__.co_filename).read_text(encoding="utf-8")
    tree = ast.parse(module_src)
    uses = lambda name, text: re.search(rf"\b{re.escape(name)}\b", text)  # noqa: E731
    # 풀이가 기대는 모듈 수준 상수(MOD 등)와 도우미 함수(_merge_two 등)를 함께 옮깁니다
    helpers = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name not in SKIP_DEFS and node.name != fn.__name__:
            if uses(node.name, src):
                helpers.append(ast.get_source_segment(module_src, node))
        elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            if name not in SKIP_CONSTS and uses(name, src):
                helpers.insert(0, ast.get_source_segment(module_src, node))
    body = "\n\n\n".join(helpers + [src.rstrip()]) + "\n"
    imports = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = [(a.asname or a.name).split(".")[0] for a in node.names]
            if any(uses(n, body) for n in names):
                if not (isinstance(node, ast.ImportFrom) and node.module == "lib.structures"):
                    imports.append(ast.get_source_segment(module_src, node))
    return ("\n".join(imports) + "\n\n" if imports else "") + body


def standalone(body):
    return (
        "<!doctype html>\n<html lang=\"ko\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        "<style>body{margin:0}[hidden]{display:none!important}</style>\n</head>\n<body>\n"
        "<!-- 이 파일은 tools/export_web.py 가 생성합니다. web/app.html 또는 web/src/ 를 수정하세요. -->\n"
        + body + "\n</body>\n</html>\n"
    )


def build_course(problems_by_slug):
    """코스의 실습 칸(data-cell="slug")에 필요한 문제 데이터만 골라 내장합니다."""
    html = COURSE_SRC.read_text(encoding="utf-8")
    data = {}
    for slug in re.findall(r'data-cell="([a-z0-9-]+)"', html):
        p = problems_by_slug.get(slug)
        if p is None:
            continue  # course.js 안에 직접 정의한 실습 (예: warmup)
        tests = p.get("TESTS", [])
        json.dumps(tests)  # JSON 으로 표현할 수 없는 테스트가 있으면 여기서 실패
        data[slug] = {
            "title": p.title,
            "level": p.level,
            "source": p.get("SOURCE", ""),
            "description": textwrap.dedent(p.get("DESCRIPTION", "")).strip(),
            "signature": p.get("SIGNATURE", ""),
            "hints": p.get("HINTS", []),
            "reference": source_of(p.get("reference")),
            "tests": tests,
            "compare": p.get("COMPARE", "exact"),
        }
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    js = COURSE_JS.read_text(encoding="utf-8")
    scripts = f"<script>window.COURSE_DATA = {payload};</script>\n<script>\n{js}</script>"
    return html.replace("<!--COURSE:SCRIPTS-->", scripts), len(data)


def main():
    bare_dir = None
    if "--bare-dir" in sys.argv:
        bare_dir = Path(sys.argv[sys.argv.index("--bare-dir") + 1])
        bare_dir.mkdir(parents=True, exist_ok=True)
    by_slug = {}
    problems, topics = [], []
    seen_topics = set()
    for p in all_problems():
        try:
            p.module
        except Exception as e:  # noqa: BLE001
            print(f"건너뜀 {p.topic}/{p.slug}: {e!r}", file=sys.stderr)
            continue
        by_slug[p.slug] = p
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
    INDEX.write_text(standalone(new), encoding="utf-8")
    course, n_cells = build_course(by_slug)
    COURSE_OUT.write_text(standalone(course), encoding="utf-8")
    if bare_dir:
        (bare_dir / "course.html").write_text(course, encoding="utf-8")
    print(f"web/app.html, web/index.html 업데이트: 주제 {len(topics)}개, 문제 {len(problems)}개")
    print(f"web/course.html 업데이트: 실습 문제 {n_cells}개 내장")


if __name__ == "__main__":
    main()
