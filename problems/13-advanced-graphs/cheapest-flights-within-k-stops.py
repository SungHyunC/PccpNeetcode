import random

TITLE = "Cheapest Flights Within K Stops (K 번 이하 경유 최저가 항공권)"
LEVEL = "Medium"
SOURCE = "LeetCode 787"
PATTERN = "간선 수 제한 최단 경로 = 벨만-포드 k+1 라운드 (배열 복사)"

DESCRIPTION = """
0 번부터 n - 1 번까지 n 개의 도시가 있고, flights[i] = [from, to, price] 는
도시 from 에서 to 로 가는 편도 항공권이 price 원이라는 뜻입니다.
출발 도시 src 에서 도착 도시 dst 까지 '경유 횟수가 k 번 이하' 인 경로 중 가장 싼 가격을 return 하세요.
그런 경로가 없으면 -1 을 return 합니다.
(경유 횟수 = 중간에 들르는 도시 수. 비행기를 m 번 타면 경유는 m - 1 번)

제한사항
- 2 ≤ n ≤ 300
- 0 ≤ len(flights) ≤ 10,000, 같은 (from, to) 쌍은 한 번만 주어집니다.
- 1 ≤ price ≤ 10,000
- 0 ≤ src, dst, k < n, src ≠ dst

입출력 예
n = 5, flights = [[0,1,50],[1,2,50],[2,4,50],[0,3,300],[3,4,10],[1,4,200]], src = 0, dst = 4
k = 1  →  250   (0 → 1 → 4, 경유 1번)
k = 2  →  150   (0 → 1 → 2 → 4, 경유 2번)
k = 0  →  -1    (직항이 없음)
"""

SIGNATURE = "def solution(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:"

HINTS = [
    "그냥 다익스트라를 돌리면 '더 싸지만 경유가 많은' 경로가 먼저 확정되어, 경유 제한 안에 드는 더 비싼 경로를 놓칠 수 있습니다.",
    "경유 k 번 = 비행기 최대 k + 1 번 = 간선 최대 k + 1 개. '간선을 i 개 이하로 써서 도착하는 최소 비용' 을 i = 1, 2, ..., k+1 순서로 구하는 것이 벨만-포드의 라운드와 정확히 같습니다.",
    "각 라운드에서는 '이전 라운드의 거리' 만 보고 갱신해야 합니다. 같은 라운드 안에서 방금 갱신한 값을 다시 쓰면 간선을 두 개 이상 탈 수 있게 되어 경유 제한이 깨집니다. → prev = dist[:] 복사 후 prev 를 읽고 dist 에 쓰기.",
]

_F = [[0, 1, 50], [1, 2, 50], [2, 4, 50], [0, 3, 300], [3, 4, 10], [1, 4, 200]]

TESTS = [
    {"input": [5, _F, 0, 4, 1], "output": 250},
    {"input": [5, _F, 0, 4, 2], "output": 150},
    {"input": [5, _F, 0, 4, 0], "output": -1},
    {"input": [3, [[0, 1, 10], [1, 2, 10], [0, 2, 100]], 0, 2, 0], "output": 100},
    {"input": [3, [[0, 1, 10], [1, 2, 10], [0, 2, 100]], 0, 2, 1], "output": 20},
    {"input": [3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0], "output": 500},
    {"input": [4, [[0, 1, 1], [1, 2, 1], [0, 2, 5], [2, 3, 1]], 0, 3, 1], "output": 6},
    {"input": [4, [[0, 1, 1], [1, 0, 1], [1, 2, 1], [2, 3, 1], [0, 3, 10]], 0, 3, 2], "output": 3},
    {"input": [3, [[0, 1, 5]], 0, 2, 2], "output": -1},
    {"input": [2, [], 0, 1, 1], "output": -1},
]

PERF_LIMIT = 1.0


def perf_case():
    # 도시 0~269 는 촘촘한 무작위 항공망(도착지 299 로는 이어지지 않음),
    # 0 → 290 → 291 → ... → 299 는 비싼 직행 사슬(비행 10번), 0 → 270 → ... → 279 → 299 는 싸지만 비행 11번.
    # k = 9 이면 비싼 사슬만 허용됩니다. 모든 경로를 DFS 로 훑는 풀이는 촘촘한 항공망에서 빠져나오지 못합니다.
    n, k = 300, 9
    pairs = set()
    while len(pairs) < 9_000:
        u, v = random.randrange(270), random.randrange(270)
        if u != v:
            pairs.add((u, v))
    flights = [[u, v, random.randint(1, 10_000)] for u, v in sorted(pairs) if (u, v) != (0, 270)]
    chain_a = [0] + list(range(290, 300))
    chain_b = [0] + list(range(270, 280)) + [299]
    flights += [[u, v, 1000] for u, v in zip(chain_a, chain_a[1:])]
    flights += [[u, v, 1] for u, v in zip(chain_b, chain_b[1:])]
    random.shuffle(flights)
    return {"input": [n, flights, 0, n - 1, k], "output": 10_000}


EXPLANATION = """
핵심: "간선을 최대 k+1 개 사용" 하는 최단 경로 → 벨만-포드를 k+1 라운드만 돌립니다.
라운드 i 가 끝난 dist[v] = "간선 i 개 이하로 v 에 도착하는 최소 비용".

함정 1: 같은 라운드 안에서 갱신값을 재사용 (복사 안 함)
  flights = [[0,1,100],[1,2,100],[0,2,500]], k = 0 (직항만 가능)
  라운드 1 에서 0→1 로 dist[1] = 100 갱신 직후 1→2 로 dist[2] = 200 갱신 → 간선 2개를 써 버림 ✘
  prev(이전 라운드 값)에서 읽으면 dist[1] = ∞ 상태라 1→2 는 무시 → 정답 500 ✔

함정 2: 평범한 다익스트라
  flights = [[0,1,1],[1,2,1],[0,2,5],[2,3,1]], k = 1
  다익스트라는 2 를 비용 2 (0→1→2, 경유 1) 로 먼저 확정 → 2→3 은 경유 2 라 불가 → -1 ✘
  실제 답: 0→2→3 = 6 (경유 1) ✔ — 비싸지만 경유가 적은 상태도 살려 둬야 함

1. dist = [∞] * n, dist[src] = 0
2. k + 1 번 반복: prev = dist[:] 복사, 모든 간선 (u, v, p) 에 대해
   prev[u] + p < dist[v] 면 dist[v] = prev[u] + p
3. dist[dst] 가 ∞ 면 -1

시간 O(k · E), 공간 O(n)

면접 포인트
- 다른 정답: (비용, 정점, 사용한 간선 수) 상태로 다익스트라/BFS (alternative).
  같은 정점이라도 "간선을 덜 쓴 상태" 는 비용이 더 커도 의미가 있으므로, 정점마다 지금까지 본 최소 간선 수(stops[v])보다
  간선을 더 적게 쓴 상태만 다시 넣습니다.
- 상태 공간 확장(state expansion): 제약이 있으면 정점을 (정점, 제약 상태) 로 늘린 그래프에서 최단 경로를 구한다는 일반 원리.
- 모든 경로를 DFS 로 다 보는 풀이(brute_force)는 정답이지만 경로 수가 지수적이라 큰 입력에서 끝나지 않습니다.
"""


def reference(n, flights, src, dst, k):
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):                  # 비행 최대 k+1 번 = 라운드 k+1 번
        prev = dist[:]                      # 이전 라운드 값만 읽기 (중요!)
        for u, v, price in flights:
            if prev[u] + price < dist[v]:
                dist[v] = prev[u] + price
    return dist[dst] if dist[dst] < INF else -1


def alternative(n, flights, src, dst, k):
    # (비용, 정점, 탄 비행 수) 상태 다익스트라
    import heapq

    graph = [[] for _ in range(n)]
    for u, v, price in flights:
        graph[u].append((v, price))
    best_legs = [float("inf")] * n          # 정점에 도착했던 상태 중 가장 적은 비행 수
    heap = [(0, src, 0)]
    while heap:
        cost, u, legs = heapq.heappop(heap)
        if u == dst:
            return cost                     # 비용 순으로 꺼내므로 처음 도착이 최저가
        if legs >= best_legs[u] or legs == k + 1:
            continue                        # 더 싸고 비행도 적거나 같은 상태를 이미 처리함 / 비행 횟수 소진
        best_legs[u] = legs
        for v, price in graph[u]:
            heapq.heappush(heap, (cost + price, v, legs + 1))
    return -1


def brute_force(n, flights, src, dst, k):
    # 경유 제한 안의 모든 경로를 DFS 로 탐색 (지수 시간)
    graph = [[] for _ in range(n)]
    for u, v, price in flights:
        graph[u].append((v, price))
    best = float("inf")

    def dfs(u, cost, legs):
        nonlocal best
        if cost >= best:
            return
        if u == dst:
            best = cost
            return
        if legs == k + 1:
            return
        for v, price in graph[u]:
            dfs(v, cost + price, legs + 1)

    dfs(src, 0, 0)
    return best if best < float("inf") else -1
