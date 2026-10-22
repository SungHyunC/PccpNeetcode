import random

TITLE = "Number of Connected Components (연결 요소의 개수)"
LEVEL = "Medium"
SOURCE = "LeetCode 323 · 프로그래머스 Lv.3 '네트워크' 유형"
PATTERN = "Union-Find (경로 압축 + 랭크 합치기)"

DESCRIPTION = """
0 번부터 n - 1 번까지 n 개의 컴퓨터가 있고, edges[i] = [a, b] 는 컴퓨터 a 와 b 가 케이블로 직접 연결되어 있다는 뜻입니다.
케이블은 양방향이며, 직접 또는 다른 컴퓨터를 거쳐 연결된 컴퓨터들은 같은 네트워크에 속합니다.
네트워크(연결 요소, connected component)의 개수를 return 하세요.

제한사항
- 1 ≤ n ≤ 100,000
- 0 ≤ len(edges) ≤ 200,000
- 0 ≤ a, b < n, 같은 간선이 여러 번 주어지거나 a == b 인 간선이 있을 수 있습니다.

입출력 예
n = 5, edges = [[0, 1], [1, 2], [3, 4]]  →  2   ({0,1,2}, {3,4})
n = 4, edges = []                        →  4   (모두 따로)
"""

SIGNATURE = "def solution(n: int, edges: list[list[int]]) -> int:"

HINTS = [
    "인접 리스트를 만들고, 방문하지 않은 정점에서 BFS/DFS 를 시작한 횟수를 세면 답입니다. (Number of Islands 의 일반 그래프 버전)",
    "다른 방법: 처음엔 n 개의 그룹이 있다고 보고, 간선 [a, b] 로 '서로 다른 그룹' 두 개를 합칠 때마다 그룹 수를 1 줄입니다. → Union-Find (Disjoint Set Union)",
    "find(x): x 의 대표(루트)를 찾되, 찾는 길에 있던 정점들이 루트를 직접 가리키게 바꿉니다(경로 압축). union(a, b): 루트가 다르면 랭크(높이)가 낮은 쪽 트리를 높은 쪽 밑에 붙입니다.",
]

TESTS = [
    {"input": [5, [[0, 1], [1, 2], [3, 4]]], "output": 2},
    {"input": [4, []], "output": 4},
    {"input": [1, []], "output": 1},
    {"input": [5, [[0, 1], [1, 2], [2, 3], [3, 4]]], "output": 1},
    {"input": [4, [[0, 1], [1, 0], [0, 1]]], "output": 3},
    {"input": [3, [[1, 1]]], "output": 3},
    {"input": [6, [[0, 1], [1, 2], [2, 0], [3, 4]]], "output": 3},
    {"input": [7, [[6, 5], [4, 3], [2, 1], [5, 4]]], "output": 3},
]

PERF_LIMIT = 1.0


def perf_case():
    n = 100_000
    edges = [[random.randrange(n), random.randrange(n)] for _ in range(80_000)]
    edges += [[i, i + 1] for i in range(0, 40_000)]        # 아주 긴 사슬 하나
    random.shuffle(edges)
    return {"input": [n, edges], "output": None}


EXPLANATION = """
핵심: Union-Find(서로소 집합, Disjoint Set Union). 간선 하나가 서로 다른 두 그룹을 이으면 그룹 수가 1 줄어듭니다.

n = 7, edges = [[6,5],[4,3],[2,1],[5,4]]

초기: {0} {1} {2} {3} {4} {5} {6}        components = 7
[6,5] 루트가 다름 → 합침 {5,6}            components = 6
[4,3] 루트가 다름 → 합침 {3,4}            components = 5
[2,1] 루트가 다름 → 합침 {1,2}            components = 4
[5,4] 루트가 다름 → 합침 {3,4,5,6}        components = 3
최종: {0}, {1,2}, {3,4,5,6} → 3
(이미 같은 그룹인 두 정점을 잇는 간선은 개수를 줄이지 않습니다 — 사이클을 만드는 간선)

1. parent[i] = i, rank[i] = 0, components = n
2. 간선마다 union(a, b): find(a) != find(b) 이면 합치고 components -= 1
3. components 반환

find 경로 압축(path compression):        union by rank:
   1                                      랭크가 낮은 루트를 높은 루트 밑에 붙여
   │          find(4) 후      1           트리 높이가 log n 이하로 유지
   2          ─────────▶   ┌─┼─┐
   │                       2 3 4
   3
   │
   4

시간 O((V + E) · α(V)) ≈ O(V + E) — α 는 역 아커만 함수로 사실상 상수
공간 O(V)

면접 포인트
- BFS/DFS(alternative)도 O(V + E) 로 정답입니다. 간선이 "실시간으로 추가" 되며 매번 그룹 수를 물으면 Union-Find 가 유리합니다.
- 경로 압축만 해도 실전에서는 충분히 빠르지만, 둘 다 쓰면 이론적으로 α(n) 보장.
- 재귀 find 는 경로 압축 전 트리가 깊으면 재귀 한도에 걸릴 수 있어 반복문 버전을 추천합니다.
- 프로그래머스 '네트워크' 는 인접 행렬(computers[i][j])로 주어지는 같은 문제입니다.
"""


def reference(n, edges):
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        root = x
        while parent[root] != root:         # 1) 루트 찾기
            root = parent[root]
        while parent[x] != root:            # 2) 경로 압축: 지나온 정점이 루트를 직접 가리키게
            parent[x], x = root, parent[x]
        return root

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False                    # 이미 같은 그룹
        if rank[ra] < rank[rb]:             # union by rank: 낮은 트리를 높은 트리 밑으로
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
        return True

    components = n
    for a, b in edges:
        if union(a, b):
            components -= 1
    return components


def alternative(n, edges):
    # 인접 리스트 + BFS 로 연결 요소 세기
    from collections import deque

    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    visited = [False] * n
    count = 0
    for s in range(n):
        if visited[s]:
            continue
        count += 1
        visited[s] = True
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)
    return count
