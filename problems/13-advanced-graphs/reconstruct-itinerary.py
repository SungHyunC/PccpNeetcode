TITLE = "Reconstruct Itinerary (여행 경로 재구성)"
LEVEL = "Hard"
SOURCE = "LeetCode 332 · 프로그래머스 Lv.3 '여행경로' 유형"
PATTERN = "오일러 경로(Eulerian path) — 히어홀저(Hierholzer) 알고리즘"

DESCRIPTION = """
항공권 목록 tickets 가 주어집니다. tickets[i] = [from, to] 는 공항 from 에서 to 로 가는 편도 항공권입니다.
여행자는 항상 "ICN" 공항에서 출발하며, 가진 항공권을 모두 정확히 한 번씩 사용해야 합니다.

방문하는 공항을 순서대로 담은 리스트를 return 하세요.
가능한 경로가 여러 개라면 공항 이름을 이어 붙인 순서가 사전 순으로 가장 앞서는 경로를 return 합니다.
(즉, 각 단계에서 갈 수 있는 공항이 여럿이면 가능한 한 알파벳 순으로 빠른 쪽을 고르되, 모든 항공권을 쓸 수 있어야 합니다)

제한사항
- 1 ≤ len(tickets) ≤ 10,000
- 공항 이름은 영어 대문자 3 글자입니다.
- 같은 항공권이 여러 장 있을 수 있습니다.
- 모든 항공권을 사용하는 경로가 적어도 하나 존재합니다.

입출력 예
tickets = [["ICN", "BKK"], ["ICN", "CDG"], ["CDG", "ICN"]]  →  ["ICN", "CDG", "ICN", "BKK"]
(사전 순으로는 BKK 가 먼저지만, ICN → BKK 로 가면 남은 항공권을 쓸 수 없음)

tickets = [["ICN", "NRT"], ["NRT", "LAX"], ["LAX", "JFK"]]  →  ["ICN", "NRT", "LAX", "JFK"]
"""

SIGNATURE = "def solution(tickets: list[list[str]]) -> list[str]:"

HINTS = [
    "공항을 정점, 항공권을 간선으로 보면 '모든 간선을 정확히 한 번씩 지나는 경로' = 오일러 경로를 찾는 문제입니다.",
    "가장 쉬운 접근: 목적지를 정렬해 두고 DFS 백트래킹. 사전 순으로 앞선 공항부터 시도하고, 항공권을 다 쓰지 못하고 막히면 되돌아갑니다. 작은 입력은 이걸로 충분합니다.",
    "더 빠른 방법(히어홀저): 막다른 곳에 도달한 공항을 '결과의 뒤쪽' 부터 채웁니다. DFS 에서 더 이상 나갈 간선이 없을 때 공항을 route 에 추가하고, 마지막에 route 를 뒤집으면 됩니다.",
    "각 공항의 목적지 리스트를 '역순' 으로 정렬해 두면 pop() 으로 사전 순 가장 앞선 목적지를 O(1) 에 꺼낼 수 있습니다. 재귀 대신 스택을 쓰면 항공권이 많아도 안전합니다.",
]

TESTS = [
    {"input": [[["ICN", "BKK"], ["ICN", "CDG"], ["CDG", "ICN"]]], "output": ["ICN", "CDG", "ICN", "BKK"]},
    {"input": [[["ICN", "NRT"], ["NRT", "LAX"], ["LAX", "JFK"]]], "output": ["ICN", "NRT", "LAX", "JFK"]},
    {"input": [[["ICN", "HND"]]], "output": ["ICN", "HND"]},
    {
        "input": [[["ICN", "AAA"], ["AAA", "ICN"], ["ICN", "BBB"], ["BBB", "ICN"]]],
        "output": ["ICN", "AAA", "ICN", "BBB", "ICN"],
    },
    {
        "input": [[["ICN", "SIN"], ["SIN", "ICN"], ["ICN", "SIN"], ["SIN", "ICN"]]],
        "output": ["ICN", "SIN", "ICN", "SIN", "ICN"],
    },
    {
        "input": [[["ICN", "DXB"], ["DXB", "ICN"], ["ICN", "AMS"], ["AMS", "DXB"], ["DXB", "AMS"]]],
        "output": ["ICN", "AMS", "DXB", "AMS", "DXB", "ICN"],
    },
    {
        "input": [[["PUS", "ICN"], ["ICN", "PUS"], ["ICN", "GMP"], ["GMP", "CJU"], ["CJU", "ICN"]]],
        "output": ["ICN", "GMP", "CJU", "ICN", "PUS", "ICN"],
    },
    {
        "input": [[["ICN", "ZZZ"], ["ICN", "AAA"], ["AAA", "BBB"], ["BBB", "ICN"], ["BBB", "AAA"], ["AAA", "BBB"]]],
        "output": ["ICN", "AAA", "BBB", "AAA", "BBB", "ICN", "ZZZ"],
    },
]

EXPLANATION = """
핵심: 오일러 경로(모든 간선을 한 번씩) + 사전 순 최소. 히어홀저 알고리즘은 O(E log E) 에 바로 구합니다.

tickets = [ICN→BKK, ICN→CDG, CDG→ICN]

그냥 탐욕(사전 순)으로 가면:  ICN → BKK (막힘! CDG 관련 항공권 2장이 남음) ✘

히어홀저(스택):
stack           목적지 남은 것                 route(막힌 순서)
[ICN]           ICN:[BKK, CDG]
[ICN, BKK]      BKK 에서 갈 곳 없음 → pop       [BKK]
[ICN, CDG]      ICN 의 다음 목적지 CDG
[ICN, CDG, ICN] CDG→ICN
[ICN, CDG, ICN] ICN 갈 곳 없음 → pop            [BKK, ICN]
                CDG 갈 곳 없음 → pop            [BKK, ICN, CDG]
                ICN 갈 곳 없음 → pop            [BKK, ICN, CDG, ICN]
뒤집기 → [ICN, CDG, ICN, BKK] ✔

왜 될까? 먼저 막히는 공항(BKK)은 경로의 "맨 끝" 이어야만 합니다. 막힌 순서대로 뒤에서부터 채우면
사전 순으로 먼저 들어갔다가 막힌 곁가지가 자연스럽게 경로 뒤쪽으로 밀려납니다.

1. graph[from] = 목적지 리스트를 역순 정렬 (pop() 이 사전 순 최소)
2. stack = ["ICN"]. 꼭대기 공항에 남은 목적지가 있으면 pop 해서 push, 없으면 stack 에서 꺼내 route 에 추가
3. route 를 뒤집어 반환

시간 O(E log E) — 정렬, 공간 O(E)

면접 포인트
- 백트래킹(brute_force)도 정답이며 프로그래머스 '여행경로' 처럼 항공권이 적으면 충분합니다.
  하지만 최악의 경우 막다른 길을 반복해서 되돌아가 지수 시간이 걸릴 수 있고, 재귀 깊이도 항공권 수만큼 깊어집니다.
- 오일러 경로 존재 조건(방향 그래프): 출발점은 (나가는 간선 - 들어오는 간선) = 1 (또는 모두 0 이면 회로), 도착점은 -1, 나머지는 0.
- LeetCode 332 는 출발 공항이 "JFK" 입니다. 출발지만 바꾸면 같은 문제입니다.
"""


def reference(tickets):
    from collections import defaultdict

    graph = defaultdict(list)
    for src, dst in sorted(tickets, reverse=True):     # 역순 정렬 → pop() 이 사전 순 최소
        graph[src].append(dst)

    stack = ["ICN"]
    route = []
    while stack:
        airport = stack[-1]
        if graph[airport]:
            stack.append(graph[airport].pop())        # 아직 안 쓴 항공권으로 이동
        else:
            route.append(stack.pop())                 # 막힘 → 경로의 뒤쪽부터 확정
    return route[::-1]


def brute_force(tickets):
    # 정렬된 순서로 DFS 백트래킹: 처음 찾은 완전한 경로가 사전 순 최소
    import sys
    from collections import defaultdict

    sys.setrecursionlimit(100_000)
    graph = defaultdict(list)
    for i, (src, dst) in enumerate(sorted(tickets)):
        graph[src].append((dst, i))
    used = [False] * len(tickets)
    path = ["ICN"]

    def dfs(airport):
        if len(path) == len(tickets) + 1:
            return True
        for dst, i in graph[airport]:
            if not used[i]:
                used[i] = True
                path.append(dst)
                if dfs(dst):
                    return True
                path.pop()                  # 막혔으면 되돌리기
                used[i] = False
        return False

    dfs("ICN")
    return path
