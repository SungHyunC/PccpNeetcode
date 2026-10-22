import random

TITLE = "Min Cost to Connect All Points (모든 점을 잇는 최소 비용)"
LEVEL = "Medium"
SOURCE = "LeetCode 1584"
PATTERN = "최소 신장 트리(MST): 밀집 그래프는 O(V^2) 프림"

DESCRIPTION = """
2차원 평면 위의 서로 다른 점들의 좌표 points[i] = [x, y] 가 주어집니다.
두 점 [x1, y1], [x2, y2] 를 선으로 잇는 비용은 맨해튼 거리 |x1 - x2| + |y1 - y2| 입니다.
모든 점이 (직접 또는 다른 점을 거쳐) 서로 연결되도록 선을 그을 때, 필요한 최소 총비용을 return 하세요.

제한사항
- 1 ≤ len(points) ≤ 800
- -1,000,000 ≤ x, y ≤ 1,000,000
- 모든 점은 서로 다릅니다.

입출력 예
points = [[0, 0], [1, 0], [5, 0]]                        →  5    (1 + 4)
points = [[0, 0], [10, 0], [0, 10], [10, 10], [5, 5]]    →  40   (가운데 점에서 네 꼭짓점으로 10 씩)
points = [[0, 0]]                                        →  0
"""

SIGNATURE = "def solution(points: list[list[int]]) -> int:"

HINTS = [
    "모든 점을 사이클 없이 최소 비용으로 잇는 것 = 최소 신장 트리(Minimum Spanning Tree). 간선은 모든 점 쌍(n(n-1)/2 개)입니다.",
    "크루스칼: 모든 간선을 비용순 정렬 후, Union-Find 로 사이클을 만들지 않는 간선만 n-1 개 고르기. O(n^2 log n).",
    "프림: 트리에서 출발해 '트리와 가장 가까운 점' 을 하나씩 붙입니다. 간선이 n^2 개인 밀집 그래프에서는 힙 없이 min_dist 배열을 매번 선형 탐색하는 O(n^2) 프림이 가장 빠릅니다.",
]

TESTS = [
    {"input": [[[0, 0], [1, 0], [5, 0]]], "output": 5},
    {"input": [[[0, 0], [10, 0], [0, 10], [10, 10], [5, 5]]], "output": 40},
    {"input": [[[0, 0]]], "output": 0},
    {"input": [[[0, 0], [1, 1]]], "output": 2},
    {"input": [[[-1, -1], [1, 1], [-1, 1], [1, -1]]], "output": 6},
    {"input": [[[1, 7], [-3, 2], [8, -4], [0, 0], [6, 5], [-5, -6]]], "output": 41},
    {"input": [[[-1000000, -1000000], [1000000, 1000000]]], "output": 4000000},
]

PERF_LIMIT = 1.5


def perf_case():
    points = set()
    while len(points) < 800:
        points.add((random.randint(-10**6, 10**6), random.randint(-10**6, 10**6)))
    return {"input": [[list(p) for p in points]], "output": None}


EXPLANATION = """
핵심: 최소 신장 트리(MST). 모든 점 쌍이 간선인 "완전 그래프" 라 간선 수가 E ≈ n^2/2 로 매우 많습니다.

프림(Prim) 동작 — 트리에 가장 싸게 붙일 수 있는 점을 하나씩 추가
points: A(0,0) B(1,0) C(5,0)

min_dist  A  B  C        트리
시작      0  ∞  ∞        {}
A 추가    -  1  5        {A}           total = 0
B 추가    -  -  4        {A, B}        total = 1   (C 까지 거리가 B 덕분에 5→4)
C 추가    -  -  -        {A, B, C}     total = 5

1. min_dist[i] = 트리까지의 최소 연결 비용 (처음엔 ∞, 시작점 0)
2. n 번 반복: 트리 밖 점 중 min_dist 최소인 u 를 선형 탐색으로 골라 트리에 추가, total += min_dist[u]
3. u 와 트리 밖 점들 사이 거리로 min_dist 갱신

시간 O(n^2) — 간선을 미리 만들지 않음, 공간 O(n)

MST 알고리즘 비교 (V 정점, E 간선)
| 알고리즘 | 시간 | 어울리는 그래프 |
| 크루스칼(정렬 + Union-Find) | O(E log E) | 희소(sparse), 간선 목록이 주어질 때 |
| 프림 + 힙 | O(E log V) | 희소~보통 |
| 프림 + 배열 | O(V^2) | 밀집(dense), 완전 그래프 ← 이 문제 |

면접 포인트
- 크루스칼(alternative)도 정답이고 설명하기 쉽습니다. 다만 n = 800 이면 간선 32만 개를 정렬해야 해서 프림보다 느립니다.
- MST 의 정당성: "컷 성질(cut property)" — 어떤 분할을 가로지르는 가장 싼 간선은 반드시 어떤 MST 에 포함됩니다.
- 간선 수 n-1 개를 고르면 바로 멈출 수 있습니다 (크루스칼 조기 종료).
- 프로그래머스 '섬 연결하기'(Lv.3)는 간선 목록이 주어지는 크루스칼 정석 문제입니다.
"""


def reference(points):
    n = len(points)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    INF = float("inf")
    min_dist = [INF] * n                # 트리까지의 최소 연결 비용
    remaining = set(range(1, n))        # 아직 트리 밖에 있는 점
    u = 0                               # 0 번 점에서 시작
    total = 0
    while remaining:
        ux, uy = xs[u], ys[u]
        nxt, best = -1, INF
        for v in remaining:
            d = abs(ux - xs[v]) + abs(uy - ys[v])
            if d < min_dist[v]:
                min_dist[v] = d         # 방금 추가한 u 덕분에 더 싸게 연결 가능
            if min_dist[v] < best:
                nxt, best = v, min_dist[v]
        total += best                   # 트리에 가장 싸게 붙는 점 추가
        remaining.remove(nxt)
        u = nxt
    return total


def alternative(points):
    # 크루스칼: 모든 간선 정렬 + Union-Find. O(n^2 log n)
    n = len(points)
    edges = []
    for i in range(n):
        xi, yi = points[i]
        for j in range(i + 1, n):
            edges.append((abs(xi - points[j][0]) + abs(yi - points[j][1]), i, j))
    edges.sort()

    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total, used = 0, 0
    for w, i, j in edges:
        ri, rj = find(i), find(j)
        if ri != rj:                    # 사이클을 만들지 않는 간선만 선택
            parent[ri] = rj
            total += w
            used += 1
            if used == n - 1:
                break
    return total
