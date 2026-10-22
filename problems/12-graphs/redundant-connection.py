import random

TITLE = "Redundant Connection (불필요한 연결)"
LEVEL = "Medium"
SOURCE = "LeetCode 684"
PATTERN = "Union-Find: 이미 같은 집합인 두 정점을 잇는 간선 = 사이클"

DESCRIPTION = """
1 번부터 n 번까지 n 개의 정점으로 이루어진 트리(사이클 없는 연결 그래프)에 간선 하나가 추가되었습니다.
이 그래프의 간선 목록 edges (길이 n, edges[i] = [a, b] 는 a 와 b 를 잇는 무방향 간선) 가 주어집니다.

간선 하나를 지워서 다시 n 개 정점의 트리로 만들려고 합니다.
지울 수 있는 간선이 여러 개라면 edges 에서 가장 나중에 나오는 것을 return 하세요. (입력에 적힌 [a, b] 모양 그대로)

제한사항
- 3 ≤ n ≤ 100,000 (n == len(edges)), 단 n = 2 이면 같은 두 정점을 잇는 간선이 2 개 주어집니다
- 1 ≤ a, b ≤ n, a ≠ b
- 주어진 그래프는 연결되어 있고, 같은 간선이 반복되지 않습니다 (n = 2 인 경우 제외).

입출력 예
edges = [[1, 2], [1, 3], [2, 3]]                  →  [2, 3]
edges = [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]  →  [1, 4]
"""

SIGNATURE = "def solution(edges: list[list[int]]) -> list[int]:"

HINTS = [
    "트리에 간선을 하나 더하면 사이클이 정확히 하나 생깁니다. 그 사이클 위의 간선 중 아무거나 지우면 트리가 됩니다.",
    "간선을 입력 순서대로 하나씩 추가한다고 생각해 보세요. 어떤 간선 [a, b] 를 추가하기 '전에' 이미 a 와 b 가 연결되어 있다면, 그 간선이 사이클을 완성합니다.",
    "'이미 연결되어 있나?' 를 빠르게 묻는 자료구조가 Union-Find 입니다. find(a) == find(b) 인 첫 간선이 답입니다. 사이클을 닫는 간선은 사이클 간선들 중 입력에서 가장 나중에 나온 것이므로 문제 조건과 일치합니다.",
]

TESTS = [
    {"input": [[[1, 2], [1, 3], [2, 3]]], "output": [2, 3]},
    {"input": [[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]], "output": [1, 4]},
    {"input": [[[2, 3], [1, 2], [1, 3]]], "output": [1, 3]},
    {"input": [[[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]]], "output": [1, 3]},
    {"input": [[[3, 4], [1, 2], [2, 4], [3, 5], [2, 5]]], "output": [2, 5]},
    {"input": [[[1, 2], [2, 1]]], "output": [2, 1]},
    {"input": [[[5, 1], [1, 2], [2, 3], [3, 4], [4, 5], [1, 6]]], "output": [4, 5]},
]

PERF_LIMIT = 1.0


def perf_case():
    n = 100_000
    parent = [0, 0] + [random.randint(1, i - 1) for i in range(2, n + 1)]   # 무작위 트리
    edges = []
    for v in range(2, n + 1):
        edges.append([v, parent[v]] if random.random() < 0.5 else [parent[v], v])
    x = random.randint(3, n)
    while parent[x] == 1:                       # 조부모가 있는 정점 고르기
        x = random.randint(3, n)
    edges.append([x, parent[parent[x]]])        # 길이 3 짜리 짧은 사이클
    random.shuffle(edges)
    return {"input": [edges], "output": None}


EXPLANATION = """
핵심: 간선을 순서대로 Union 하다가, 두 끝점이 이미 같은 집합이면 그 간선이 사이클을 만든 "불필요한" 간선입니다.

edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]

[1,2] 다른 집합 → 합침      {1,2}
[2,3] 다른 집합 → 합침      {1,2,3}
[3,4] 다른 집합 → 합침      {1,2,3,4}
[1,4] find(1) == find(4) !  → 이미 연결됨 → 답 [1, 4]

   1 ── 2
   │    │       사이클 1-2-3-4-1 의 간선 중
   4 ── 3       입력에서 가장 나중에 나온 [1,4] 가 사이클을 "닫는" 간선
   │
   5 (1 과 연결)

왜 "가장 나중 간선" 이 보장되나?
사이클의 간선들 중 마지막 하나가 추가되기 전까지는 사이클이 완성되지 않으므로
find 가 같아지는 순간은 정확히 "사이클 간선 중 입력상 마지막" 간선입니다.

시간 O(n · α(n)), 공간 O(n)

면접 포인트
- 간선 하나씩 지워 보고 매번 연결성을 확인하는 풀이(brute_force)는 O(n^2) — n = 100,000 에서 시간 초과.
- 방향 그래프 버전(Redundant Connection II, LeetCode 685)은 "진입 차수 2 인 정점" 경우를 추가로 따져야 합니다.
- Union-Find 템플릿(find 에 경로 압축, union 에 랭크)을 실수 없이 쓰는 것이 이 문제의 전부입니다.
"""


def reference(edges):
    n = len(edges)
    parent = list(range(n + 1))
    rank = [0] * (n + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # 경로 압축(경로 절반 줄이기, path halving)
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return [a, b]                   # 이미 연결 → 이 간선이 사이클을 닫음
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
    return []


def brute_force(edges):
    # 뒤에서부터 간선 하나를 빼 보고, 나머지로 모든 정점이 연결되는지(=트리) DFS 로 확인: O(n^2)
    n = len(edges)
    for skip in range(n - 1, -1, -1):
        graph = [[] for _ in range(n + 1)]
        for i, (a, b) in enumerate(edges):
            if i != skip:
                graph[a].append(b)
                graph[b].append(a)
        seen = {1}
        stack = [1]
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        if len(seen) == n:
            return edges[skip]
    return []
