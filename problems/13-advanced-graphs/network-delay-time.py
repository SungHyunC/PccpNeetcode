import random

TITLE = "Network Delay Time (네트워크 지연 시간)"
LEVEL = "Medium"
SOURCE = "LeetCode 743 · 프로그래머스 Lv.2 '배달' 유형"
PATTERN = "다익스트라 (heapq + lazy deletion)"

DESCRIPTION = """
1 번부터 n 번까지 n 개의 서버가 있습니다. times[i] = [u, v, w] 는 서버 u 에서 v 로
신호를 보내면 w 밀리초가 걸린다는 뜻입니다 (단방향).
서버 k 에서 신호를 보냈을 때, 모든 서버가 신호를 받는 데 걸리는 최소 시간을 return 하세요.
신호를 받지 못하는 서버가 하나라도 있으면 -1 을 return 합니다.

제한사항
- 1 ≤ n ≤ 20,000
- 0 ≤ len(times) ≤ 120,000
- 1 ≤ u, v, k ≤ n, u ≠ v
- 0 ≤ w ≤ 1,000
- 같은 (u, v) 쌍이 여러 번 주어질 수 있습니다 (가장 빠른 것만 의미 있음).

입출력 예
times = [[1, 2, 3], [1, 3, 1], [3, 2, 1], [2, 4, 2]], n = 4, k = 1  →  4
(1→3 은 1, 1→3→2 는 2, 1→3→2→4 는 4. 가장 늦게 받는 서버 4 의 시간 = 4)

times = [[1, 2, 1]], n = 2, k = 2  →  -1   (서버 2 에서 1 로 가는 길이 없음)
"""

SIGNATURE = "def solution(times: list[list[int]], n: int, k: int) -> int:"

HINTS = [
    "'모든 서버가 받는 시간' = k 에서 각 서버까지의 최단 거리 중 최댓값입니다. 간선 비용이 서로 달라서 BFS 는 쓸 수 없습니다.",
    "음수 간선이 없는 단일 출발점 최단 거리 → 다익스트라(Dijkstra). 아직 확정되지 않은 정점 중 거리가 가장 짧은 것을 매번 꺼냅니다.",
    "가장 짧은 것을 매번 배열에서 찾으면 O(V^2) 입니다. heapq 에 (거리, 정점) 을 넣어 O(E log V) 로 만드세요.",
    "같은 정점이 힙에 여러 번 들어갈 수 있습니다. 꺼낸 거리 d 가 dist[u] 보다 크면 이미 더 짧은 거리로 처리된 낡은 항목이므로 continue (lazy deletion).",
]

TESTS = [
    {"input": [[[1, 2, 3], [1, 3, 1], [3, 2, 1], [2, 4, 2]], 4, 1], "output": 4},
    {"input": [[[1, 2, 1]], 2, 1], "output": 1},
    {"input": [[[1, 2, 1]], 2, 2], "output": -1},
    {"input": [[], 1, 1], "output": 0},
    {"input": [[[1, 2, 5], [2, 3, 5], [1, 3, 20], [3, 1, 1]], 3, 1], "output": 10},
    {"input": [[[1, 2, 1], [2, 1, 1]], 3, 1], "output": -1},
    {"input": [[[1, 2, 0], [2, 3, 0]], 3, 1], "output": 0},
    {"input": [[[1, 2, 7], [1, 2, 3]], 2, 1], "output": 3},
    {"input": [[[2, 1, 4], [2, 3, 1], [3, 1, 1], [1, 4, 6], [3, 4, 10]], 4, 2], "output": 8},
]

PERF_LIMIT = 1.0


def perf_case():
    n = 20_000
    # 비용 1 짜리 사슬 + 비싼 무작위 간선: 최단 경로가 간선을 많이 쓰게 되어 벨만-포드는 라운드가 많이 필요
    times = [[i, i + 1, 1] for i in range(1, n)]
    for _ in range(100_000):
        u, v = random.randint(1, n), random.randint(1, n)
        if u != v:
            times.append([u, v, random.randint(100, 1000)])
    random.shuffle(times)
    return {"input": [times, n, 1], "output": None}


EXPLANATION = """
핵심: 다익스트라(Dijkstra). "지금까지 확정되지 않은 정점 중 가장 가까운 정점" 은 더 짧아질 수 없으므로 확정하고,
그 정점에서 나가는 간선으로 이웃의 거리를 갱신(relax)합니다.

times = [[1,2,3],[1,3,1],[3,2,1],[2,4,2]], k = 1

      3            힙                       dist (1..4)
  1 ────▶ 2 ──2──▶ 4   [(0,1)]              [0, ∞, ∞, ∞]
  │       ▲            pop (0,1) → push (3,2),(1,3)   [0, 3, 1, ∞]
  1       1            pop (1,3) → 2 를 1+1=2 로 갱신, push (2,2)   [0, 2, 1, ∞]
  ▼       │            pop (2,2) → push (4,4)          [0, 2, 1, 4]
  3 ──────┘            pop (3,2) → 3 > dist[2]=2 → 낡은 항목, 건너뜀 ✂
                       pop (4,4)                       최댓값 = 4

1. 인접 리스트 graph[u] = [(v, w), ...]
2. dist = [∞] * (n+1), dist[k] = 0, heap = [(0, k)]
3. heap 에서 (d, u) pop. d > dist[u] 면 continue (lazy deletion)
4. 이웃 (v, w): d + w < dist[v] 면 갱신 후 push
5. max(dist[1..n]) 이 ∞ 면 -1

시간 O(E log V) — 각 간선이 최대 한 번 push 를 일으킴
공간 O(V + E)

면접 포인트
- "왜 BFS 가 아니라 다익스트라?" → 간선 비용이 다름. 비용이 모두 같으면 BFS, 0/1 이면 0-1 BFS.
- `if d > dist[u]: continue` 가 빠지면 낡은 항목도 이웃을 다시 훑어 최악 O(E^2) 까지 느려질 수 있습니다.
- 음수 간선이 있으면 다익스트라의 "꺼낸 순간 확정" 가정이 깨집니다 → 벨만-포드(brute_force).
- 정점이 적고 간선이 매우 많은(밀집 그래프, E ≈ V^2) 경우에는 힙 없는 O(V^2) 다익스트라(alternative)가 더 빠를 수도 있습니다.
- 프로그래머스 '배달'(Lv.2), '가장 먼 노드'(Lv.3, 비용이 모두 1 → BFS) 와 비교해 보세요.
"""


def reference(times, n, k):
    import heapq

    graph = [[] for _ in range(n + 1)]
    for u, v, w in times:
        graph[u].append((v, w))

    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[k] = 0
    heap = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue                        # 이미 더 짧은 거리로 확정된 정점 (낡은 항목)
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    answer = max(dist[1:])
    return answer if answer < INF else -1


def alternative(times, n, k):
    # 힙 없는 O(V^2) 다익스트라: 매번 미확정 정점 중 최소를 선형 탐색 (밀집 그래프용)
    INF = float("inf")
    graph = [[] for _ in range(n + 1)]
    for u, v, w in times:
        graph[u].append((v, w))
    dist = [INF] * (n + 1)
    dist[k] = 0
    done = [False] * (n + 1)
    for _ in range(n):
        u, best = -1, INF
        for i in range(1, n + 1):
            if not done[i] and dist[i] < best:
                u, best = i, dist[i]
        if u == -1:
            break                           # 남은 정점은 도달 불가
        done[u] = True
        for v, w in graph[u]:
            if best + w < dist[v]:
                dist[v] = best + w
    answer = max(dist[1:])
    return answer if answer < INF else -1


def brute_force(times, n, k):
    # 벨만-포드: 모든 간선을 V-1 번 완화 O(V · E). 음수 간선도 처리 가능하지만 느림
    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[k] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in times:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break                           # 더 이상 갱신이 없으면 조기 종료
    answer = max(dist[1:])
    return answer if answer < INF else -1
