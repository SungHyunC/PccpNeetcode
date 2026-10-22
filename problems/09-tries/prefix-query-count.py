import random
import string
from bisect import bisect_left

TITLE = "Prefix Query Count (와일드카드 접두사 질의 개수)"
LEVEL = "Medium"
SOURCE = "PCCP 기출 유형 (프로그래머스 '가사 검색' 유형)"
PATTERN = "길이별 트라이 + 노드마다 통과하는 단어 수 저장"

DESCRIPTION = """
검색 엔진 팀이 자동 완성 기능을 만들고 있습니다.
사전 단어 목록 words 와 검색어 목록 queries 가 주어집니다.

검색어는 영어 소문자로 된 접두사 뒤에 '?' 가 1개 이상 붙은 형태입니다. '?' 하나는 아무 소문자 한 글자와 일치합니다.
즉, 검색어 "fro??" 는 'fro 로 시작하는 5글자 단어' 와 일치합니다. ("frodo", "front" 는 일치, "frozen", "fro" 는 불일치)
'?' 는 검색어의 끝부분에만 연속해서 나타나며, 검색어 전체가 '?' 일 수도 있습니다.

각 검색어와 일치하는 단어의 개수를 검색어 순서대로 담아 return 하세요.

제한사항
- 0 ≤ len(words) ≤ 50,000, 1 ≤ len(queries) ≤ 50,000
- 1 ≤ 단어 길이, 검색어 길이 ≤ 10
- words 의 단어는 영어 소문자이며 모두 다릅니다.
- queries 에는 중복이 있을 수 있습니다.
- 효율성 테스트가 있습니다 (검색어마다 단어 전체를 훑으면 시간 초과).

입출력 예
words   = ["frodo", "front", "frost", "frozen", "frame", "kakao"]
queries = ["fro??", "fro???", "fr???", "pro?", "?????", "k????"]
→ [3, 1, 4, 0, 5, 1]
"""

SIGNATURE = "def solution(words: list[str], queries: list[str]) -> list[int]:"

HINTS = [
    "검색어마다 모든 단어를 확인하면 50,000 x 50,000 = 25억 번 비교입니다. 단어 쪽을 미리 가공해 두어야 합니다.",
    "검색어와 일치하려면 (1) 길이가 같고 (2) 접두사가 같아야 합니다. 그러니 단어를 '길이별로' 나눠 두면 길이 조건은 공짜로 해결됩니다.",
    "길이별 트라이를 만들고, 각 노드에 '이 노드를 지나간 단어의 수(count)'를 저장하세요. 검색어의 '?' 앞까지 내려간 노드의 count 가 답입니다. 전부 '?' 이면 그 길이 트라이의 루트 count.",
    "다른 방법: 길이별로 단어를 정렬해 두고 bisect 로 [prefix, prefix + '{') 범위의 개수를 셉니다 ('{' 는 'z' 다음 문자).",
]

TESTS = [
    {
        "input": [
            ["frodo", "front", "frost", "frozen", "frame", "kakao"],
            ["fro??", "fro???", "fr???", "pro?", "?????", "k????"],
        ],
        "output": [3, 1, 4, 0, 5, 1],
    },
    {"input": [[], ["a?"]], "output": [0]},
    {"input": [["a", "b", "cc"], ["?", "??", "???"]], "output": [2, 1, 0]},
    {"input": [["a"], ["?"]], "output": [1]},
    {
        "input": [
            ["apple", "apply", "ape", "apt", "april"],
            ["ap???", "app??", "a??", "apr??", "appl?", "appl?"],
        ],
        "output": [3, 2, 2, 1, 2, 2],
    },
    {
        "input": [["abc", "abd", "abcd"], ["abc?", "ab?", "abcd??????", "abcde?"]],
        "output": [1, 2, 0, 0],
    },
    {
        "input": [["zzzzzzzzzz", "zzzzzzzzzy"], ["zzzzzzzzz?", "??????????", "z?"]],
        "output": [2, 2, 0],
    },
]


def _rand_word(lo, hi, alphabet):
    return "".join(random.choice(alphabet) for _ in range(random.randint(lo, hi)))


PERF_LIMIT = 1.0


def perf_case():
    alphabet = "abcdefgh"
    words = set()
    while len(words) < 50_000:
        words.add(_rand_word(2, 10, alphabet))
    words = list(words)
    queries = []
    for _ in range(50_000):
        w = random.choice(words)
        k = random.randint(0, len(w) - 1)  # 앞 k 글자를 남기고 나머지는 '?'
        queries.append(w[:k] + "?" * (len(w) - k))
    return {"input": [words, queries], "output": None}


EXPLANATION = """
핵심: 일치 조건 = "길이가 같다" + "접두사가 같다". 길이로 먼저 나누고, 접두사는 트라이로 셉니다.
트라이의 각 노드에 "이 노드를 지나간 단어 수"를 저장하면, 접두사 끝 노드의 count 가 곧 정답입니다.

  길이 5 트라이 (frodo, front, frost, frame, kakao)
    root(5)
     ├─ f(4)
     │   └─ r(4)
     │       ├─ o(3) ─ d(1)… , n(1)… , s(1)…
     │       └─ a(1) ─ m(1) ─ e(1)
     └─ k(1) ─ a(1) ─ k(1) ─ a(1) ─ o(1)

  "fro??" → 길이 5 트라이에서 f → r → o 까지 내려감 → count 3
  "?????" → 길이 5 트라이의 root count → 5

1. tries[길이] = 루트 노드. 단어를 넣을 때 루트부터 지나가는 모든 노드의 count += 1
2. 검색어 q: L = len(q), prefix = q.rstrip('?')
3. 길이 L 트라이가 없으면 0. 있으면 prefix 를 따라 내려가다 끊기면 0, 끝까지 가면 그 노드의 count

시간: 구축 O(총 단어 길이), 질의 O(검색어 길이) → 전체 O(ΣL), 공간 O(총 단어 길이)
면접 포인트:
- 프로그래머스 '가사 검색'(2020 카카오 블라인드) 과 같은 유형입니다. 원래 문제는 '?' 가 접두사 쪽에 올 수도 있는데,
  그때는 단어를 뒤집어 넣은 트라이를 하나 더 만들고 검색어도 뒤집어 같은 방법으로 셉니다.
- 트라이 대신 길이별 정렬 + 이분 탐색(bisect) 도 O((N + Q) log N) 으로 통과합니다 (alternative).
- 해시맵에 (길이, 접두사) 를 모두 세어 두는 방법도 있지만, 단어마다 접두사를 전부 잘라 만드는 비용 O(L^2) 과 메모리를 고려해야 합니다.
- 검색어 중복이 많다면 결과를 캐시(dict)해도 좋습니다.
"""


def reference(words, queries):
    class Node:
        __slots__ = ("children", "count")

        def __init__(self):
            self.children = {}
            self.count = 0   # 이 노드를 지나간 단어 수

    tries = {}  # 단어 길이 → 그 길이 단어들만 담은 트라이
    for w in words:
        node = tries.setdefault(len(w), Node())
        node.count += 1
        for ch in w:
            node = node.children.setdefault(ch, Node())
            node.count += 1

    answer = []
    for q in queries:
        node = tries.get(len(q))
        for ch in q.rstrip("?"):          # '?' 앞의 접두사만 따라 내려감
            if node is None:
                break
            node = node.children.get(ch)
        answer.append(node.count if node else 0)
    return answer


def alternative(words, queries):
    # 길이별 정렬 + 이분 탐색: prefix 로 시작하는 범위 = [prefix, prefix + '{')
    by_len = {}
    for w in words:
        by_len.setdefault(len(w), []).append(w)
    for arr in by_len.values():
        arr.sort()
    answer = []
    for q in queries:
        arr = by_len.get(len(q), [])
        prefix = q.rstrip("?")
        answer.append(bisect_left(arr, prefix + "{") - bisect_left(arr, prefix))
    return answer


def brute_force(words, queries):
    # 검색어마다 모든 단어 확인: O(N·Q) → 효율성 실패
    answer = []
    for q in queries:
        prefix = q.rstrip("?")
        answer.append(sum(1 for w in words if len(w) == len(q) and w.startswith(prefix)))
    return answer
