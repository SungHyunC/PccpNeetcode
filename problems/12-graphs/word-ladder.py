import random

TITLE = "Word Ladder (단어 사다리)"
LEVEL = "Hard"
SOURCE = "LeetCode 127 · 프로그래머스 Lv.3 '단어 변환' 유형"
PATTERN = "암시적 그래프(implicit graph) BFS + 와일드카드 버킷"

DESCRIPTION = """
시작 단어 begin, 목표 단어 end, 단어 목록 word_list 가 주어집니다.
한 번에 한 글자만 바꿀 수 있고, 바꾼 결과는 반드시 word_list 에 있는 단어여야 합니다.
begin 에서 end 까지 가는 가장 짧은 변환 과정에 등장하는 단어의 수(begin 과 end 포함)를 return 하세요.
변환할 수 없다면 0 을 return 합니다.

제한사항
- 1 ≤ len(begin) ≤ 10, 모든 단어의 길이는 같습니다.
- 1 ≤ len(word_list) ≤ 20,000
- 모든 단어는 영어 소문자로만 이루어져 있고, begin ≠ end 입니다.
- begin 은 word_list 에 없을 수도 있습니다. word_list 안에 중복 단어는 없습니다.

입출력 예
begin = "cold", end = "warm",
word_list = ["cord", "card", "ward", "warm", "worm", "word", "wore"]  →  5
(cold → cord → card → ward → warm)

begin = "cold", end = "warm", word_list = ["cord", "card", "ward"]   →  0   (end 가 목록에 없음)
"""

SIGNATURE = "def solution(begin: str, end: str, word_list: list[str]) -> int:"

HINTS = [
    "단어를 정점, '한 글자만 다른 두 단어' 를 간선으로 보면 가중치 없는 그래프의 최단 거리 문제 → BFS 입니다.",
    "모든 단어 쌍을 비교해 간선을 만들면 O(N^2 · L) 입니다. N = 20,000 이면 2억 쌍 → 시간 초과.",
    "이웃을 '만들어서' 찾으세요: 단어의 각 자리를 a~z 로 바꿔 보고 word_list(set)에 있는지 확인하면 단어당 26 · L 번만 확인하면 됩니다.",
    "또는 'h*t', '*it' 처럼 한 자리를 * 로 바꾼 패턴을 키로 하는 dict(버킷)를 미리 만들어 두면, 같은 버킷의 단어들이 곧 이웃입니다. 한 번 쓴 버킷은 비워 두면 같은 이웃을 다시 훑지 않습니다.",
]

TESTS = [
    {"input": ["cold", "warm", ["cord", "card", "ward", "warm", "worm", "word", "wore"]], "output": 5},
    {"input": ["cold", "warm", ["cord", "card", "ward"]], "output": 0},
    {"input": ["a", "c", ["a", "b", "c"]], "output": 2},
    {"input": ["cat", "cot", ["cot"]], "output": 2},
    {"input": ["lead", "gold", ["load", "goad", "gold", "lend"]], "output": 4},
    {"input": ["abc", "xyz", ["abd", "xyz"]], "output": 0},
    {"input": ["hot", "dog", ["hot", "dog"]], "output": 0},
    {"input": ["same", "sane", ["lame", "lane", "sane"]], "output": 2},
    {"input": ["aaaa", "bbbb", ["baaa", "bbaa", "bbba", "bbbb", "abbb", "aabb"]], "output": 5},
]

PERF_LIMIT = 1.0


def perf_case():
    alphabet = "abcdefghij"
    words = set()
    while len(words) < 20_000:
        words.add("".join(random.choice(alphabet) for _ in range(5)))
    words = sorted(words)
    random.shuffle(words)
    return {"input": [words[0], words[-1], words[1:]], "output": None}


EXPLANATION = """
핵심: 그래프가 눈에 보이지 않는(implicit) BFS. 이웃을 "필요할 때 만들어서" 찾습니다.

cold ─ cord ─ card ─ ward ─ warm         레벨(단어 수)
         │                    │          cold      : 1
        word ─ worm ──────────┘          cord      : 2
         │                               card, word: 3
        wore                             ward, worm, wore: 4
                                         warm      : 5  ← 처음 도착한 레벨이 최단

와일드카드 버킷:
  "c*rd" → [cord, card]      "*ord" → [cord, word]
  "wor*" → [word, worm, wore] ...
  같은 버킷에 있는 단어끼리는 한 글자만 다름 = 이웃

1. end 가 word_list 에 없으면 0
2. 단어마다 L 개의 패턴(한 글자를 * 로)을 키로 버킷에 저장
3. BFS: dist[begin] = 1. 꺼낸 단어의 패턴 L 개 → 버킷 속 미방문 단어를 dist + 1 로 큐에
   사용한 버킷은 비워서 다시 훑지 않기
4. end 를 꺼내면 dist[end] 반환, 큐가 비면 0

시간 O(N · L^2) — 단어 N 개 × 패턴 L 개 × 패턴 문자열 만들기 O(L)
공간 O(N · L^2)

면접 포인트
- 그래프를 미리 다 만들지 않고 이웃을 생성하는 "암시적 그래프" 사고방식을 설명하세요.
- 26 · L 로 이웃 생성(alternative) vs 와일드카드 버킷: 둘 다 정석. N 이 작고 L 이 크면 전자, 단어가 많으면 후자가 유리.
- 양방향 BFS(bidirectional BFS): begin 과 end 에서 동시에, 항상 더 작은 쪽 프론티어를 확장하면 탐색량이 크게 줄어듭니다.
- 경로 자체를 모두 구하라는 Word Ladder II 는 BFS 로 레벨 그래프를 만든 뒤 DFS 로 경로를 복원합니다.
- 프로그래머스 '단어 변환' (Lv.3) 은 변환 "횟수" 를 묻습니다 (= 이 문제의 답 - 1).
"""


def reference(begin, end, word_list):
    from collections import defaultdict, deque

    words = set(word_list)
    if end not in words:
        return 0
    L = len(begin)
    buckets = defaultdict(list)                 # "c*rd" → [cord, card]
    for w in words:
        for i in range(L):
            buckets[w[:i] + "*" + w[i + 1:]].append(w)

    dist = {begin: 1}
    queue = deque([begin])
    while queue:
        word = queue.popleft()
        if word == end:
            return dist[word]
        for i in range(L):
            key = word[:i] + "*" + word[i + 1:]
            for nxt in buckets.get(key, ()):
                if nxt not in dist:
                    dist[nxt] = dist[word] + 1
                    queue.append(nxt)
            buckets[key] = []                   # 이 버킷의 단어는 모두 큐에 들어감 → 다시 볼 필요 없음
    return 0


def alternative(begin, end, word_list):
    # 자리마다 a~z 로 바꿔 보며 이웃 생성: 단어당 26 · L 번 확인
    from collections import deque

    words = set(word_list)
    if end not in words:
        return 0
    words.discard(begin)
    queue = deque([(begin, 1)])
    while queue:
        word, steps = queue.popleft()
        if word == end:
            return steps
        for i in range(len(word)):
            for ch in "abcdefghijklmnopqrstuvwxyz":
                nxt = word[:i] + ch + word[i + 1:]
                if nxt in words:
                    words.remove(nxt)           # 방문 처리 = 집합에서 제거
                    queue.append((nxt, steps + 1))
    return 0


def brute_force(begin, end, word_list):
    # 모든 단어 쌍을 비교해 인접 리스트를 만든 뒤 BFS: O(N^2 · L) → 단어가 많으면 시간 초과
    from collections import deque

    nodes = list(dict.fromkeys([begin] + word_list))
    if end not in word_list:
        return 0

    def one_diff(a, b):
        return sum(x != y for x, y in zip(a, b)) == 1

    graph = {w: [v for v in nodes if one_diff(w, v)] for w in nodes}
    dist = {begin: 1}
    queue = deque([begin])
    while queue:
        w = queue.popleft()
        if w == end:
            return dist[w]
        for v in graph[w]:
            if v not in dist:
                dist[v] = dist[w] + 1
                queue.append(v)
    return 0
