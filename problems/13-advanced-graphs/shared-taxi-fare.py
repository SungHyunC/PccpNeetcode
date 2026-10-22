import random

TITLE = "Shared Taxi Fare (합승 택시 요금)"
LEVEL = "Hard"
SOURCE = "프로그래머스 Lv.3 '합승 택시 요금' 유형 (2021 KAKAO BLIND)"
PATTERN = "경유점 k 를 전부 시도: d(s,k) + d(k,a) + d(k,b) — 다익스트라 3번 또는 플로이드-워셜"

DESCRIPTION = """
1 번부터 n 번까지 n 개의 지점이 있고, fares[i] = [c, d, f] 는 지점 c 와 d 사이를 택시로 이동하면
요금이 f 원이라는 뜻입니다 (양방향, 같은 요금).

두 친구가 지점 s 에서 함께 출발합니다. 한 명은 지점 a, 다른 한 명은 지점 b 로 가야 합니다.
둘은 어떤 지점 k 까지 택시를 함께 타고 가서(합승) 요금을 한 번만 낸 뒤,
k 에서 각자 택시를 따로 타고 목적지로 갈 수 있습니다. k 가 s 이면 처음부터 따로 타는 것이고,
k 가 a 나 b 여도 됩니다.

두 사람이 낸 택시 요금 합계의 최솟값을 return 하세요.

제한사항
- 3 ≤ n ≤ 1,000
- 1 ≤ len(fares) ≤ 20,000, 1 ≤ f ≤ 100,000
- s, a, b 는 서로 다르며, s 에서 a 와 b 로 가는 경로는 항상 존재합니다.
- 같은 두 지점을 잇는 요금 정보는 최대 한 번 주어집니다.
- (원본 문제는 n ≤ 200 입니다. 이 저장소에서는 n 을 키워 풀이 선택의 차이를 체감하게 했습니다.)

입출력 예
n = 4, s = 1, a = 3, b = 4,
fares = [[1, 2, 5], [2, 3, 5], [2, 4, 5], [1, 3, 20], [1, 4, 20]]  →  15
(1 → 2 까지 합승 5원, 2 → 3, 2 → 4 각자 5원씩. 따로 가면 20 + 20 = 40원)

n = 3, s = 1, a = 2, b = 3, fares = [[1, 2, 4], [1, 3, 4], [2, 3, 10]]  →  8
(처음부터 따로 타는 것이 가장 쌉니다: k = s)
"""

SIGNATURE = "def solution(n: int, s: int, a: int, b: int, fares: list[list[int]]) -> int:"

HINTS = [
    "합승이 끝나는 지점을 k 라 하면 총요금은 dist(s, k) + dist(k, a) + dist(k, b) 입니다. 모든 k 에 대해 이 값을 계산해 최솟값을 고르면 됩니다.",
    "필요한 최단 거리는 s, a, b 에서 출발하는 것뿐입니다. 그래프가 무방향이므로 dist(k, a) = dist(a, k) 입니다.",
    "다익스트라를 s, a, b 에서 한 번씩(총 3번) 돌리면 모든 k 에 대한 값을 O(1) 에 조합할 수 있습니다. 시간 O(E log V).",
    "n ≤ 200 인 원본 문제라면 플로이드-워셜로 모든 쌍 최단 거리를 구해도 됩니다. 하지만 O(n^3) 이라 n = 1,000 이면 10억 번 → 시간 초과입니다.",
]

TESTS = [
    {"input": [4, 1, 3, 4, [[1, 2, 5], [2, 3, 5], [2, 4, 5], [1, 3, 20], [1, 4, 20]]], "output": 15},
    {"input": [3, 1, 2, 3, [[1, 2, 4], [1, 3, 4], [2, 3, 10]]], "output": 8},
    {"input": [4, 1, 2, 3, [[1, 2, 3], [2, 3, 3], [1, 3, 10], [3, 4, 1]]], "output": 6},
    {"input": [3, 2, 1, 3, [[1, 2, 1], [2, 3, 1]]], "output": 2},
    {
        "input": [7, 1, 6, 7, [[1, 2, 3], [2, 3, 4], [3, 6, 2], [3, 7, 2], [1, 4, 1],
                              [4, 5, 1], [5, 6, 9], [5, 7, 9], [2, 5, 2]]],
        "output": 11,
    },
    {"input": [5, 1, 2, 3, [[1, 2, 7], [1, 3, 7], [4, 5, 1]]], "output": 14},
    {"input": [4, 1, 4, 3, [[1, 2, 2], [2, 3, 2], [3, 4, 2], [1, 4, 100]]], "output": 6},
]

PERF_LIMIT = 1.0


def perf_case():
    n = 1000
    pairs = set()
    for v in range(2, n + 1):                   # 무작위 트리로 연결성 보장
        u = random.randint(1, v - 1)
        pairs.add((u, v))
    while len(pairs) < 20_000:
        u, v = random.randint(1, n), random.randint(1, n)
        if u != v and (v, u) not in pairs:
            pairs.add((u, v))
    fares = [[u, v, random.randint(1, 100_000)] for u, v in pairs]
    random.shuffle(fares)
    return {"input": [n, 1, n // 2, n, fares], "output": None}


EXPLANATION = """
핵심: 합승이 끝나는 지점 k 를 "모두" 시도합니다. 총요금 = d(s,k) + d(k,a) + d(k,b).

          s
          │ d(s,k)  ← 둘이 함께 (한 번만 냄)
          k
        ↙   ↘
  d(k,a)     d(k,b) ← 각자
     a         b

필요한 거리는 "s 에서", "a 에서", "b 에서" 출발하는 최단 거리 세 종류뿐 (무방향이라 d(k,a) = d(a,k)).

풀이 1 (reference): 다익스트라 3번
1. 인접 리스트 (양방향)
2. ds = dijkstra(s), da = dijkstra(a), db = dijkstra(b)
3. answer = min(ds[k] + da[k] + db[k] for k in 1..n)
시간 O(E log V) × 3, 공간 O(V + E)

풀이 2 (alternative): 플로이드-워셜 (Floyd-Warshall)
1. dist[i][j] 를 간선 요금으로 초기화 (dist[i][i] = 0)
2. for k: for i: for j: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])   ← k 가 가장 바깥!
3. answer = min(dist[s][k] + dist[k][a] + dist[k][b])
시간 O(n^3), 공간 O(n^2)

언제 무엇을?
- 원본(n ≤ 200): 200^3 = 800만 → 플로이드도 통과. 코드가 짧아 실전에서 실수가 적음.
- 이 저장소 버전(n ≤ 1,000): 1000^3 = 10억 → 플로이드는 시간 초과. 다익스트라 3번은 수 밀리초.
- "출발점이 몇 개 안 된다" 는 관찰이 핵심. 출발점이 정점 수만큼 많고 n 이 작으면 플로이드.

면접 포인트
- k 를 고정해 보는 발상("어디서 갈라지나?")은 경유점 문제의 공통 기법입니다.
- 방향 그래프라면 d(k, a) 를 구하려고 a 에서 "역방향 그래프" 로 다익스트라를 돌려야 합니다.
- 플로이드-워셜의 반복 순서(k 가 가장 바깥)를 틀리면 오답입니다. 이유: k 단계가 끝나면 "1..k 만 경유한 최단 거리" 가 확정됨.
"""


def reference(n, s, a, b, fares):
    import heapq

    graph = [[] for _ in range(n + 1)]
    for c, d, f in fares:
        graph[c].append((d, f))             # 양방향
        graph[d].append((c, f))

    def dijkstra(start):
        dist = [float("inf")] * (n + 1)
        dist[start] = 0
        heap = [(0, start)]
        while heap:
            du, u = heapq.heappop(heap)
            if du > dist[u]:
                continue                    # 낡은 항목 건너뛰기
            for v, w in graph[u]:
                if du + w < dist[v]:
                    dist[v] = du + w
                    heapq.heappush(heap, (dist[v], v))
        return dist

    ds, da, db = dijkstra(s), dijkstra(a), dijkstra(b)
    # 합승 종료 지점 k 를 모두 시도
    return min(ds[k] + da[k] + db[k] for k in range(1, n + 1))


def alternative(n, s, a, b, fares):
    # 플로이드-워셜: 모든 쌍 최단 거리 O(n^3) — 원본 제약(n ≤ 200)에서만 충분히 빠름
    INF = float("inf")
    dist = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dist[i][i] = 0
    for c, d, f in fares:
        dist[c][d] = dist[d][c] = min(dist[c][d], f)
    for k in range(1, n + 1):               # 경유 정점 k 가 반드시 가장 바깥 루프
        dk = dist[k]
        for i in range(1, n + 1):
            di = dist[i]
            dik = di[k]
            if dik == INF:
                continue
            for j in range(1, n + 1):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    return min(dist[s][k] + dist[k][a] + dist[k][b] for k in range(1, n + 1))
