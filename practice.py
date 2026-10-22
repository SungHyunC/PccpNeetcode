#!/usr/bin/env python3
"""PCCP · 코딩 인터뷰 연습용 로컬 채점기.

사용법은 `python practice.py help` 를 실행하세요.
외부 패키지 없이 파이썬 3.9+ 표준 라이브러리만 사용합니다.
"""
import argparse
import contextlib
import copy
import importlib.util
import inspect
import io
import json
import os
import random
import signal
import sys
import textwrap
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROBLEMS_DIR = ROOT / "problems"
WORKSPACE_DIR = ROOT / "workspace"
PROGRESS_FILE = ROOT / ".progress.json"
MOCK_FILE = ROOT / ".mock.json"
DEFAULT_TIMEOUT = 2.0  # 테스트 케이스 하나당 제한 시간(초)

sys.path.insert(0, str(ROOT))

# ───────────────────────── 출력 꾸미기 ─────────────────────────
USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def _c(code):
    return (lambda s: f"\033[{code}m{s}\033[0m") if USE_COLOR else (lambda s: str(s))


GREEN, RED, YELLOW, CYAN, DIM, BOLD = _c("32"), _c("31"), _c("33"), _c("36"), _c("2"), _c("1")
LEVEL_COLOR = {"Easy": GREEN, "Medium": YELLOW, "Hard": RED}


def short(value, limit=160):
    s = repr(value)
    return s if len(s) <= limit else s[: limit - 3] + "..."


# ───────────────────────── 문제 로딩 ─────────────────────────
class Problem:
    def __init__(self, path: Path):
        self.path = path
        self.topic = path.parent.name
        self.slug = path.stem
        self._module = None

    @property
    def module(self):
        if self._module is None:
            self._module = load_module(self.path, f"problem_{self.topic}_{self.slug}".replace("-", "_"))
        return self._module

    def get(self, name, default=None):
        return getattr(self.module, name, default)

    @property
    def title(self):
        return self.get("TITLE", self.slug)

    @property
    def level(self):
        return self.get("LEVEL", "?")

    @property
    def workspace_path(self):
        return WORKSPACE_DIR / self.topic / f"{self.slug}.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def all_problems():
    if not PROBLEMS_DIR.exists():
        return []
    return [Problem(p) for p in sorted(PROBLEMS_DIR.glob("*/*.py")) if not p.name.startswith("_")]


def topics():
    return sorted({p.topic for p in all_problems()})


def find_problem(key: str) -> Problem:
    problems = all_problems()
    if key.isdigit():
        idx = int(key) - 1
        if 0 <= idx < len(problems):
            return problems[idx]
    matches = [p for p in problems if p.slug == key or f"{p.topic}/{p.slug}" == key]
    if not matches:
        matches = [p for p in problems if key.lower() in p.slug.lower()]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        sys.exit(RED(f"'{key}' 문제를 찾을 수 없습니다. `python practice.py list` 로 목록을 확인하세요."))
    names = ", ".join(p.slug for p in matches[:10])
    sys.exit(YELLOW(f"'{key}' 에 해당하는 문제가 여러 개입니다: {names}"))


# ───────────────────────── 진행 상황 ─────────────────────────
def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def progress():
    return load_json(PROGRESS_FILE, {})


def update_progress(slug, **fields):
    data = progress()
    entry = data.setdefault(slug, {"status": "started", "attempts": 0, "hints": 0})
    entry.update(fields)
    save_json(PROGRESS_FILE, data)
    return entry


def status_icon(slug, prog):
    st = prog.get(slug, {}).get("status")
    return {"solved": GREEN("✔"), "started": YELLOW("…")}.get(st, DIM("·"))


# ───────────────────────── 채점 ─────────────────────────
class Timeout(Exception):
    pass


@contextlib.contextmanager
def time_limit(seconds):
    if not hasattr(signal, "SIGALRM") or seconds is None:
        yield  # Windows 등에서는 시간 제한 없이 실행합니다
        return

    def handler(signum, frame):
        raise Timeout()

    old = signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)


def normalize(value, mode):
    if mode == "unordered":
        return sorted(value, key=repr)
    if mode == "unordered_nested":
        return sorted((sorted(v, key=repr) if isinstance(v, (list, tuple)) else v for v in value), key=repr)
    return value


def is_correct(problem, result, expected, args):
    custom = problem.get("check")
    if custom is not None:
        return bool(custom(result, expected, *args))
    mode = problem.get("COMPARE", "exact")
    if mode == "float":
        return abs(result - expected) <= 1e-6 * max(1.0, abs(expected))
    if isinstance(result, tuple) and isinstance(expected, list):
        result = list(result)
    return normalize(result, mode) == normalize(expected, mode)


def run_case(problem, func, case, timeout):
    """케이스 하나를 실행하고 (ok, result, elapsed, stdout, error) 를 돌려줍니다."""
    raw_args = copy.deepcopy(case["input"])
    prepare = problem.get("prepare")
    present = problem.get("present")
    args = list(prepare(*copy.deepcopy(raw_args))) if prepare else copy.deepcopy(raw_args)
    buf = io.StringIO()
    start = time.perf_counter()
    try:
        with contextlib.redirect_stdout(buf), time_limit(timeout):
            result = func(*args)
    except Timeout:
        return False, None, time.perf_counter() - start, buf.getvalue(), f"시간 초과 (> {timeout}s)"
    except Exception:
        return False, None, time.perf_counter() - start, buf.getvalue(), traceback.format_exc(limit=-3)
    elapsed = time.perf_counter() - start
    try:
        if present:
            result = present(result)
        ok = is_correct(problem, result, case["output"], raw_args)
    except Exception:
        return False, result, elapsed, buf.getvalue(), "결과 비교 중 오류:\n" + traceback.format_exc(limit=-2)
    return ok, result, elapsed, buf.getvalue(), None


def perf_case(problem):
    maker = problem.get("perf_case")
    if maker is None:
        return None
    random.seed(12345)
    case = maker()
    if case.get("output") is None:
        ref = problem.get("reference")
        prepare = problem.get("prepare")
        present = problem.get("present")
        args = list(prepare(*copy.deepcopy(case["input"]))) if prepare else copy.deepcopy(case["input"])
        out = ref(*args)
        case["output"] = present(out) if present else out
    return case


def judge(problem, func, verbose=True, label="정확성", perf=True):
    tests = problem.get("TESTS", [])
    passed = 0
    for i, case in enumerate(tests, 1):
        ok, result, elapsed, out, err = run_case(problem, func, case, DEFAULT_TIMEOUT)
        passed += ok
        if not verbose:
            continue
        mark = GREEN("통과") if ok else RED("실패")
        print(f"  {label} 테스트 {i:>2} 〉 {mark} ({elapsed * 1000:.2f}ms)")
        if not ok:
            print(DIM(f"      입력     : {short(case['input'])}"))
            print(DIM(f"      기댓값   : {short(case['output'])}"))
            if err:
                print(RED(textwrap.indent(err.rstrip(), "      ")))
            else:
                print(DIM("      실행 결과: ") + RED(short(result)))
            if out.strip():
                print(DIM("      출력(print):\n" + textwrap.indent(out.rstrip()[:800], "        ")))
    perf_ok = None
    pcase = perf_case(problem) if perf else None
    if pcase is not None:
        limit = problem.get("PERF_LIMIT", 1.0)
        ok, result, elapsed, out, err = run_case(problem, func, pcase, limit * 3)
        perf_ok = ok and elapsed <= limit
        if verbose:
            mark = GREEN("통과") if perf_ok else RED("실패")
            note = err or ("오답" if not ok else ("" if perf_ok else f"제한 {limit}s 초과"))
            print(f"  효율성 테스트  〉 {mark} ({elapsed * 1000:.1f}ms) {RED(note) if note else ''}")
    return passed, len(tests), perf_ok


def load_solution(path: Path):
    if not path.exists():
        sys.exit(RED(f"풀이 파일이 없습니다: {path}\n먼저 `python practice.py start <문제>` 를 실행하세요."))
    try:
        module = load_module(path, "user_solution_" + path.stem.replace("-", "_"))
    except Exception:
        print(RED("풀이 파일을 불러오는 중 오류가 발생했습니다:"))
        traceback.print_exc(limit=-3)
        sys.exit(1)
    func = getattr(module, "solution", None)
    if func is None:
        sys.exit(RED("풀이 파일에 `solution` 함수가 없습니다."))
    return func


# ───────────────────────── 명령어 ─────────────────────────
def cmd_list(args):
    prog = progress()
    problems = all_problems()
    current = None
    for i, p in enumerate(problems, 1):
        if args.topic and args.topic not in p.topic:
            continue
        if args.level and p.level.lower() != args.level.lower():
            continue
        if p.topic != current:
            current = p.topic
            print("\n" + BOLD(CYAN(f"■ {p.topic}")))
        lv = LEVEL_COLOR.get(p.level, str)(f"{p.level:<6}")
        print(f"  {status_icon(p.slug, prog)} {i:>3}. {lv} {p.title}  {DIM(p.slug + ' · ' + p.get('PATTERN', ''))}")
    print(DIM("\n✔ 해결  … 진행중  · 미시도 | 번호나 slug 로 문제를 지정할 수 있습니다 (예: start 1, start two-sum)"))


def print_problem(p):
    lv = LEVEL_COLOR.get(p.level, str)(p.level)
    print(BOLD(f"\n{p.title}") + f"  [{lv}]  {DIM(p.get('SOURCE', ''))}")
    print(DIM(f"주제: {p.topic} · 패턴: {p.get('PATTERN', '-')}"))
    print("─" * 60)
    print(textwrap.dedent(p.get("DESCRIPTION", "")).strip())
    print("─" * 60)
    print(CYAN(p.get("SIGNATURE", "def solution(...):")))


def cmd_show(args):
    print_problem(find_problem(args.problem))


def workspace_template(p):
    desc = textwrap.dedent(p.get("DESCRIPTION", "")).strip()
    header = f"{p.title} ({p.get('SOURCE', '')}) · {p.level}\n주제: {p.topic}\n\n{desc}"
    header = header.replace("\\", "\\\\").replace('"""', "'''")  # 백슬래시가 docstring 을 깨지 않도록
    lines = ['"""', header, '"""']
    imports = p.get("IMPORTS", "")
    if imports:
        lines += [
            "import os, sys",
            "sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))",
            textwrap.dedent(imports).strip(),
        ]
    first = p.get("TESTS", [{}])[0].get("input", [])
    lines += [
        "",
        "",
        p.get("SIGNATURE", "def solution():"),
        "    # 여기에 풀이를 작성하세요",
        "    pass",
        "",
        "",
        'if __name__ == "__main__":',
        "    # 직접 실행해서 디버깅할 수 있습니다. 채점은 `python practice.py test " + p.slug + "`",
    ]
    if p.get("prepare"):
        lines.append(f"    # 입력 예시(원본 표기): {short(first, 300)}")
        lines.append("    pass")
    else:
        lines.append(f"    print(solution(*{first!r}))")
    return "\n".join(lines) + "\n"


def cmd_start(args):
    p = find_problem(args.problem)
    print_problem(p)
    path = p.workspace_path
    if path.exists() and not args.force:
        print(YELLOW(f"\n이미 풀이 파일이 있습니다: {path.relative_to(ROOT)} (덮어쓰려면 --force)"))
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(workspace_template(p), encoding="utf-8")
        print(GREEN(f"\n풀이 파일을 만들었습니다: {path.relative_to(ROOT)}"))
    if p.slug not in progress():
        update_progress(p.slug, status="started", started_at=time.strftime("%Y-%m-%d %H:%M"))
    print(DIM(f"다 풀었으면: python practice.py test {p.slug}   막히면: python practice.py hint {p.slug}"))


def cmd_test(args):
    p = find_problem(args.problem)
    path = Path(args.file) if args.file else p.workspace_path
    func = load_solution(path)
    print(BOLD(f"\n▶ {p.title} 채점 ({path.relative_to(ROOT) if path.is_relative_to(ROOT) else path})"))
    passed, total, perf_ok = judge(p, func)
    all_ok = passed == total and perf_ok is not False
    entry = progress().get(p.slug, {})
    attempts = entry.get("attempts", 0) + 1
    if all_ok:
        update_progress(p.slug, status="solved", attempts=attempts, solved_at=time.strftime("%Y-%m-%d %H:%M"))
        print(GREEN(BOLD(f"\n🎉 정답입니다! ({passed}/{total})")))
        print(DIM(f"모범 풀이와 비교해 보세요: python practice.py solution {p.slug}"))
    else:
        status = "solved" if entry.get("status") == "solved" else "started"
        update_progress(p.slug, status=status, attempts=attempts)
        print(RED(BOLD(f"\n정확성 {passed}/{total}" + ("" if perf_ok is not False else " · 효율성 실패"))))
        print(DIM(f"힌트: python practice.py hint {p.slug}"))


def cmd_hint(args):
    p = find_problem(args.problem)
    hints = p.get("HINTS", [])
    if not hints:
        print("이 문제에는 힌트가 없습니다.")
        return
    seen = progress().get(p.slug, {}).get("hints", 0)
    n = len(hints) if args.all else min(seen + 1, len(hints))
    print(BOLD(f"\n💡 {p.title} 힌트 ({n}/{len(hints)})"))
    for i, h in enumerate(hints[:n], 1):
        print(f"  {i}. {h}")
    update_progress(p.slug, hints=max(seen, n))
    if n < len(hints):
        print(DIM("다음 힌트를 보려면 같은 명령을 한 번 더 실행하세요."))


def cmd_solution(args):
    p = find_problem(args.problem)
    ref = p.get("reference")
    print(BOLD(f"\n📘 {p.title} 모범 풀이"))
    exp = p.get("EXPLANATION")
    if exp:
        print(textwrap.dedent(exp).strip())
        print("─" * 60)
    if ref:
        src = inspect.getsource(ref).replace("def reference(", "def solution(", 1)
        print(CYAN(src))
    for name in ("alternative", "brute_force"):
        fn = p.get(name)
        if fn:
            print(DIM(f"# 다른 풀이 ({name})"))
            print(inspect.getsource(fn))


def cmd_random(args):
    prog = progress()
    pool = [
        p
        for p in all_problems()
        if prog.get(p.slug, {}).get("status") != "solved"
        and (not args.topic or args.topic in p.topic)
        and (not args.level or p.level.lower() == args.level.lower())
    ]
    if not pool:
        print(GREEN("조건에 맞는 미해결 문제가 없습니다. 대단해요!"))
        return
    args.problem = random.choice(pool).slug
    args.force = False
    cmd_start(args)


def cmd_stats(args):
    prog = progress()
    problems = all_problems()
    print(BOLD("\n📊 주제별 진행 상황"))
    total_solved = 0
    for t in topics():
        items = [p for p in problems if p.topic == t]
        solved = sum(prog.get(p.slug, {}).get("status") == "solved" for p in items)
        total_solved += solved
        bar = "█" * solved + "░" * (len(items) - solved)
        print(f"  {t:<24} {GREEN(bar)} {solved}/{len(items)}")
    print(BOLD(f"\n  전체 {total_solved}/{len(problems)}"))


MOCK_MODES = {
    # PCCP: 4문제 120분 1000점 (문제당 250점으로 계산)
    "pccp": {"count": 4, "minutes": 120, "levels": ["Easy", "Medium", "Medium", "Hard"]},
    # 미국 테크 기업 온사이트 한 세션: 45분 2문제
    "interview": {"count": 2, "minutes": 45, "levels": ["Medium", "Medium"]},
    # 온라인 코딩 테스트(OA): 90분 3문제
    "oa": {"count": 3, "minutes": 90, "levels": ["Easy", "Medium", "Hard"]},
}


def cmd_mock(args):
    if args.action == "status":
        mock = load_json(MOCK_FILE, None)
        if not mock:
            print("진행 중인 모의고사가 없습니다. `python practice.py mock start` 로 시작하세요.")
            return
        left = mock["deadline"] - time.time()
        print(BOLD(f"\n⏱ 모의고사 ({mock['mode']}) · 남은 시간 {max(0, int(left // 60))}분 {max(0, int(left % 60))}초"))
        for i, slug in enumerate(mock["problems"], 1):
            p = find_problem(slug)
            print(f"  {i}. {p.title} [{p.level}] → {p.workspace_path.relative_to(ROOT)}")
        return
    if args.action == "submit":
        mock = load_json(MOCK_FILE, None)
        if not mock:
            print("진행 중인 모의고사가 없습니다.")
            return
        late = time.time() > mock["deadline"]
        per = 1000 / len(mock["problems"])
        score = 0.0
        print(BOLD(f"\n📝 모의고사 채점 ({mock['mode']})" + (RED(" · 시간 초과 제출") if late else "")))
        for slug in mock["problems"]:
            p = find_problem(slug)
            if not p.workspace_path.exists():
                print(f"  {p.title}: 미제출 0점")
                continue
            try:
                func = load_solution(p.workspace_path)
                passed, total, perf_ok = judge(p, func, verbose=False)
            except SystemExit:
                passed, total, perf_ok = 0, 1, None
            # 정확성 80% + 효율성 20% (효율성 테스트가 없으면 정확성 100%)
            ratio = passed / total if total else 0
            pts = per * (ratio * 0.8 + (0.2 if perf_ok else 0)) if perf_ok is not None else per * ratio
            score += pts
            print(f"  {p.title:<40} 정확성 {passed}/{total}  효율성 {'-' if perf_ok is None else ('O' if perf_ok else 'X')}  → {pts:.0f}점")
        elapsed = (time.time() - mock["started"]) / 60
        print(BOLD(f"\n  총점 {score:.0f} / 1000  (소요 {elapsed:.0f}분)"))
        if mock["mode"] == "pccp":
            print(DIM("  PCCP는 400점 이상이면 합격, 점수에 따라 Lv.1~5 등급이 부여됩니다 (등급 구간은 공식 안내 확인)."))
        MOCK_FILE.unlink()
        return
    cfg = MOCK_MODES[args.mode]
    prog = progress()
    chosen = []
    problems = all_problems()
    for level in cfg["levels"]:
        pool = [p for p in problems if p.level == level and p not in chosen]
        fresh = [p for p in pool if prog.get(p.slug, {}).get("status") != "solved"]
        pick = random.choice(fresh or pool or [p for p in problems if p not in chosen])
        chosen.append(pick)
    now = time.time()
    save_json(MOCK_FILE, {
        "mode": args.mode,
        "problems": [p.slug for p in chosen],
        "started": now,
        "deadline": now + cfg["minutes"] * 60,
    })
    print(BOLD(f"\n🚀 {args.mode.upper()} 모의고사 시작! {cfg['count']}문제 · {cfg['minutes']}분"))
    for i, p in enumerate(chosen, 1):
        path = p.workspace_path
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(workspace_template(p), encoding="utf-8")
        print(f"  {i}. {p.title} [{p.level}] → {path.relative_to(ROOT)}")
    print(DIM("\n문제 설명은 각 파일 상단에 있습니다. 힌트/정답 보기는 참아 주세요 😉"))
    print(DIM("남은 시간: python practice.py mock status   제출: python practice.py mock submit"))


def cmd_quiz(args):
    """문제 설명만 보고 어떤 패턴(주제)인지 맞히는 퀴즈."""
    problems = all_problems()
    if len(problems) < 4:
        print("문제가 부족합니다.")
        return
    all_topics = topics()
    score = 0
    rounds = min(args.n, len(problems))
    for r, p in enumerate(random.sample(problems, rounds), 1):
        options = random.sample([t for t in all_topics if t != p.topic], 3) + [p.topic]
        random.shuffle(options)
        desc = textwrap.dedent(p.get("DESCRIPTION", "")).strip().split("\n")
        print(BOLD(f"\n[{r}/{rounds}] 이 문제는 어떤 주제일까요?"))
        print(textwrap.indent("\n".join(desc[:8]), "  "))
        for i, o in enumerate(options, 1):
            print(f"   {i}) {o}")
        try:
            ans = input("  번호 입력 > ").strip()
        except EOFError:
            return
        if ans.isdigit() and 1 <= int(ans) <= 4 and options[int(ans) - 1] == p.topic:
            score += 1
            print(GREEN(f"  정답! 패턴: {p.get('PATTERN', '')}"))
        else:
            print(RED(f"  오답. 정답은 {p.topic} · 패턴: {p.get('PATTERN', '')} ({p.slug})"))
    print(BOLD(f"\n결과: {score}/{rounds}"))


def cmd_verify(args):
    """모든 문제의 모범 풀이가 테스트를 통과하는지 확인 (문제 작성자용)."""
    bad = 0
    count = 0
    for p in all_problems():
        if args.topic and args.topic not in p.topic:
            continue
        count += 1
        problems = []
        try:
            for name in ("TITLE", "LEVEL", "DESCRIPTION", "SIGNATURE", "HINTS", "TESTS", "reference"):
                if p.get(name) is None:
                    problems.append(f"{name} 없음")
            if p.level not in ("Easy", "Medium", "Hard"):
                problems.append(f"LEVEL 값 오류: {p.level}")
            if len(p.get("TESTS", [])) < 3:
                problems.append("TESTS 3개 미만")
            if p.get("reference") and not problems:
                passed, total, perf_ok = judge(p, p.get("reference"), verbose=False)
                if passed != total:
                    problems.append(f"모범 풀이가 정확성 {passed}/{total}")
                if perf_ok is False:
                    problems.append("모범 풀이가 효율성 실패")
                for name in ("alternative", "brute_force"):
                    fn = p.get(name)
                    if fn:
                        ap, at, _ = judge(p, fn, verbose=False, perf=False)
                        if ap != at:
                            problems.append(f"{name} 풀이가 {ap}/{at}")
        except Exception as e:  # noqa: BLE001
            problems.append(f"예외: {e!r}")
        if problems:
            bad += 1
            print(RED(f"✘ {p.topic}/{p.slug}: " + "; ".join(problems)))
        elif args.verbose:
            print(GREEN(f"✔ {p.topic}/{p.slug}"))
    print((GREEN if not bad else RED)(f"\n검증 완료: {count - bad}/{count} 문제 정상"))
    sys.exit(1 if bad else 0)


HELP = f"""
{BOLD('PCCP · 코딩 인터뷰 로컬 채점기')}

  python practice.py list [--topic 02] [--level Easy]   문제 목록과 진행 상황
  python practice.py show <문제>                        문제 설명 보기
  python practice.py start <문제>                       workspace/ 에 풀이 파일 만들기
  python practice.py test <문제> [--file 경로]          내 풀이 채점 (정확성 + 효율성)
  python practice.py hint <문제> [--all]                힌트를 하나씩 공개
  python practice.py solution <문제>                    모범 풀이 + 해설
  python practice.py random [--topic ..] [--level ..]   안 푼 문제 하나 랜덤 출제
  python practice.py stats                              주제별 진행률
  python practice.py quiz [-n 10]                       문제 설명 → 패턴 맞히기 퀴즈
  python practice.py mock start [--mode pccp|oa|interview]   실전 모의고사 (타이머)
  python practice.py mock status | submit               남은 시간 / 제출 후 채점
  python practice.py verify [--topic ..] [-v]           (작성자용) 모범 풀이 검증

  <문제> 자리에는 list 의 번호, slug(two-sum), 또는 slug 일부를 넣을 수 있습니다.
"""


def main(argv=None):
    parser = argparse.ArgumentParser(prog="practice.py", add_help=False)
    sub = parser.add_subparsers(dest="cmd")

    s = sub.add_parser("list")
    s.add_argument("--topic")
    s.add_argument("--level")
    for name in ("show", "hint", "solution"):
        s = sub.add_parser(name)
        s.add_argument("problem")
        if name == "hint":
            s.add_argument("--all", action="store_true")
    s = sub.add_parser("start")
    s.add_argument("problem")
    s.add_argument("--force", action="store_true")
    s = sub.add_parser("test")
    s.add_argument("problem")
    s.add_argument("--file")
    s = sub.add_parser("random")
    s.add_argument("--topic")
    s.add_argument("--level")
    sub.add_parser("stats")
    s = sub.add_parser("quiz")
    s.add_argument("-n", type=int, default=10)
    s = sub.add_parser("mock")
    s.add_argument("action", nargs="?", default="start", choices=["start", "status", "submit"])
    s.add_argument("--mode", default="pccp", choices=list(MOCK_MODES))
    s = sub.add_parser("verify")
    s.add_argument("--topic")
    s.add_argument("-v", "--verbose", action="store_true")
    sub.add_parser("help")

    args = parser.parse_args(argv)
    handlers = {
        "list": cmd_list, "show": cmd_show, "start": cmd_start, "test": cmd_test,
        "hint": cmd_hint, "solution": cmd_solution, "random": cmd_random, "stats": cmd_stats,
        "quiz": cmd_quiz, "mock": cmd_mock, "verify": cmd_verify,
    }
    if args.cmd in handlers:
        handlers[args.cmd](args)
    else:
        print(HELP)


if __name__ == "__main__":
    main()
