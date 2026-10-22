TITLE = "Alien Dictionary (외계어 사전)"
LEVEL = "Hard"
SOURCE = "LeetCode 269"
PATTERN = "인접 단어 비교로 간선 만들기 + 위상 정렬"

DESCRIPTION = """
영어 소문자를 쓰지만 알파벳 순서가 우리와 다른 외계 언어가 있습니다.
이 언어의 사전 순서대로 정렬된 단어 목록 words 가 주어질 때, 단어에 등장하는 글자들의 순서를 추측해
하나의 문자열로 return 하세요.

- words 에 등장하는 모든 글자가 정확히 한 번씩 들어 있어야 합니다.
- 가능한 순서가 여러 개면 아무거나 return 해도 됩니다. (채점은 'words 가 그 순서로 정렬되어 있는지' 로 확인합니다)
- 주어진 정렬과 모순되어 가능한 순서가 없으면 빈 문자열 "" 을 return 하세요.

사전 순서 규칙: 두 단어를 앞에서부터 비교해 처음으로 다른 글자의 순서로 결정합니다.
모든 글자가 같은데 한 단어가 다른 단어의 접두사(prefix)라면, 더 짧은 단어가 앞입니다.

제한사항
- 1 ≤ len(words) ≤ 100
- 1 ≤ len(words[i]) ≤ 100
- words[i] 는 영어 소문자로만 이루어져 있습니다.

입출력 예
words = ["dog", "dot", "gut", "tug"]  →  예: "dgtou"
  (dog < dot 에서 g < t, dot < gut 에서 d < g. o 와 u 는 위치 제약이 없음)
words = ["z", "x", "z"]               →  ""   (z < x 이면서 x < z: 모순)
words = ["abc", "ab"]                 →  ""   (접두사인 더 짧은 단어가 뒤에 있음: 모순)
"""

SIGNATURE = "def solution(words: list[str]) -> str:"

HINTS = [
    "인접한 두 단어 words[i], words[i+1] 만 비교하면 됩니다. 처음으로 다른 글자 c1 ≠ c2 가 나오면 'c1 이 c2 보다 앞' 이라는 정보(간선 c1 → c2)를 하나 얻고, 그 뒤 글자는 아무 정보도 주지 않습니다.",
    "다른 글자가 하나도 없는데 앞 단어가 더 길다면(예: 'abc' 다음 'ab') 그 자체로 모순이므로 바로 \"\" 를 return 하세요.",
    "글자들을 정점으로 하는 방향 그래프에서 위상 정렬(Kahn)을 하세요. 모든 글자를 진입 차수 0 으로 초기화하는 것을 잊지 마세요 (간선이 없는 글자도 결과에 들어가야 함).",
    "위상 정렬 결과의 길이가 글자 수보다 짧다면 사이클이 있다는 뜻 → \"\".",
]


def check(result, expected, words):
    """결과가 '모든 글자를 한 번씩 포함하고, words 가 그 순서로 정렬되는' 올바른 순서인지 검사."""
    if expected == "":
        return result == ""
    if not isinstance(result, str):
        return False
    letters = {ch for w in words for ch in w}
    if len(result) != len(letters) or set(result) != letters:
        return False
    rank = {ch: i for i, ch in enumerate(result)}
    keys = [[rank[ch] for ch in w] for w in words]
    # 리스트 비교는 사전식이며, 접두사인 짧은 리스트가 더 작다고 판단 → 사전 순서 규칙과 동일
    return all(keys[i] <= keys[i + 1] for i in range(len(keys) - 1))


TESTS = [
    {"input": [["dog", "dot", "gut", "tug"]], "output": "dgtou"},
    {"input": [["z", "x"]], "output": "zx"},
    {"input": [["z", "x", "z"]], "output": ""},
    {"input": [["abc", "ab"]], "output": ""},
    {"input": [["abc"]], "output": "abc"},
    {"input": [["ca", "cb", "ba"]], "output": "cab"},
    {"input": [["ab", "adc"]], "output": "abdc"},
    {"input": [["xy", "xy"]], "output": "xy"},
    {"input": [["a", "b", "ca", "cc"]], "output": "abc"},
    {"input": [["ba", "bc", "ac", "cab"]], "output": "bac"},
    {"input": [["ac", "ab", "zc", "zb"]], "output": "aczb"},
    {"input": [["b", "a", "c", "ab"]], "output": ""},
]

EXPLANATION = """
핵심: 정렬된 단어 목록에서 "인접한 두 단어의 첫 번째 다른 글자" 가 글자 순서 정보(간선)를 줍니다.
간선들로 방향 그래프를 만들고 위상 정렬하면 글자 순서가 됩니다.

words = ["dog", "dot", "gut", "tug"]
  dog vs dot → 3번째 글자 g ≠ t → g → t
  dot vs gut → 1번째 글자 d ≠ g → d → g
  gut vs tug → 1번째 글자 g ≠ t → g → t (중복 간선은 한 번만)

  d ──▶ g ──▶ t        o, u : 간선 없음 (진입 차수 0)
위상 정렬 (Kahn): 큐 [d, o, u] → d 를 꺼내면 g 의 진입 차수 0 → [o, u, g] → ... → "dougt"
d 가 g 앞, g 가 t 앞이기만 하면 되므로 "dgtou", "odgut" 등도 모두 정답

모순 두 가지
1) 사이클: ["z","x","z"] → z → x, x → z → 위상 정렬 결과 길이 < 글자 수 → ""
2) 접두사 역전: ["abc","ab"] → 다른 글자가 없는데 앞 단어가 더 김 → ""

1. 모든 글자를 진입 차수 0, 빈 이웃 집합으로 초기화
2. 인접 단어 쌍마다 첫 번째 다른 글자 (c1, c2) → c2 가 graph[c1] 에 없으면 추가하고 indeg[c2] += 1
   다른 글자가 없고 len(w1) > len(w2) 면 "" 반환
3. Kahn 위상 정렬. 결과 길이가 글자 수와 다르면 ""

시간 O(C) — C = 모든 단어 글자 수의 합 (간선은 최대 단어 수 - 1 개, 글자는 최대 26 개)
공간 O(1) ~ O(26^2)

면접 포인트
- "모든 단어 쌍을 비교해야 하나요?" → 아니요. 정렬 관계는 전이적이라 인접 쌍만으로 충분합니다.
- 첫 번째 다른 글자 "이후" 는 아무 정보도 없다는 점, 그리고 접두사 예외를 놓치지 않는 것이 가장 흔한 실수 포인트입니다.
- 간선을 set 으로 관리해 같은 간선이 두 번 들어가 진입 차수가 과하게 세지는 버그를 막으세요.
- 답이 여러 개일 수 있음을 면접관에게 먼저 확인하세요 (사전 순으로 가장 앞선 답을 원하면 큐 대신 최소 힙 사용).
"""


def reference(words):
    from collections import deque

    graph = {ch: set() for w in words for ch in w}     # 모든 글자를 정점으로 등록
    indeg = {ch: 0 for ch in graph}

    for w1, w2 in zip(words, words[1:]):
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if c2 not in graph[c1]:                 # 중복 간선 방지
                    graph[c1].add(c2)
                    indeg[c2] += 1
                break                                   # 첫 번째 다른 글자만 의미 있음
        else:
            if len(w1) > len(w2):                       # "abc" 다음에 "ab" → 모순
                return ""

    queue = deque(ch for ch in graph if indeg[ch] == 0)
    order = []
    while queue:
        ch = queue.popleft()
        order.append(ch)
        for nxt in graph[ch]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)

    return "".join(order) if len(order) == len(graph) else ""   # 짧으면 사이클


def alternative(words):
    # DFS 후위 순서(post-order)를 뒤집어 위상 정렬 + 3색 표시로 사이클 판별
    graph = {ch: [] for w in words for ch in w}
    for w1, w2 in zip(words, words[1:]):
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                graph[c1].append(c2)
                break
        else:
            if len(w1) > len(w2):
                return ""

    state = {ch: 0 for ch in graph}     # 0 미방문, 1 방문 중, 2 완료
    post = []

    def dfs(u):
        state[u] = 1
        for v in graph[u]:
            if state[v] == 1:
                return False            # 방문 중인 정점을 다시 만남 → 사이클
            if state[v] == 0 and not dfs(v):
                return False
        state[u] = 2
        post.append(u)
        return True

    for ch in graph:
        if state[ch] == 0 and not dfs(ch):
            return ""
    return "".join(reversed(post))
