# 13. 고급 그래프 (Advanced Graphs)

> 간선에 비용(가중치)이 붙으면 BFS 대신 다익스트라·벨만-포드·플로이드-워셜을, "모두 최소 비용으로 잇기" 는 MST(크루스칼·프림)를 씁니다. 제약 조건(정점 수, 음수 간선, 경유 횟수)을 보고 알고리즘을 고르는 것이 핵심입니다.

## 이런 문제에서 떠올리세요

- "최소 비용 / 최단 시간" + 간선마다 비용이 다름 + 음수 없음 → **다익스트라 (Dijkstra)**
- 음수 간선이 있음, "음의 사이클이 있으면 ..." , "최대 k 번 경유" → **벨만-포드 (Bellman-Ford)**
- 모든 쌍의 최단 거리, 정점 수 n ≤ 200~400 → **플로이드-워셜 (Floyd-Warshall)**
- "모든 점/섬/도시를 최소 비용으로 연결" → **최소 신장 트리 (MST)**: 크루스칼 / 프림
- 이동 비용이 0 또는 1 뿐 (예: 벽 부수기 1, 그냥 이동 0) → **0-1 BFS** (deque 양쪽 삽입)
- "경로 위 최댓값을 최소로" (병목, intensity, effort) → 합 대신 max 를 쓰는 다익스트라 / 이분 탐색 + BFS / Union-Find
- 선후 관계를 "추측" 해야 함 (외계어 사전) → 간선 만들기 + 위상 정렬
- "모든 간선을 한 번씩" (항공권 전부 사용) → 오일러 경로, 히어홀저 알고리즘
- 입력 크기 힌트: V ≤ 10^5, E ≤ 2·10^5 → O(E log V) 다익스트라. V ≤ 200 → O(V^3) 플로이드 가능. V ≤ 1000 이고 완전 그래프 → O(V^2) 프림/다익스트라

## 핵심 개념

### 1) 다익스트라: "가장 가까운 미확정 정점은 더 짧아질 수 없다"

```
간선: A→B 4, A→C 1, C→B 1, C→D 5, B→D 2        시작 A

     A ──4──▶ B
     │      ↗ │
     1    1   2
     ▼  ↗     ▼
     C ──5──▶ D

heap [(0,A)]
pop (0,A) → push (4,B), (1,C)                      dist A0 B4 C1 D∞
pop (1,C) → B: 1+1=2 < 4 갱신 push (2,B), D: push (6,D)  dist A0 B2 C1 D6
pop (2,B) → D: 2+2=4 < 6 갱신 push (4,D)             dist A0 B2 C1 D4
pop (4,B) → 4 > dist[B]=2 → 낡은 항목 ✂ continue      ← lazy deletion
pop (4,D) → 이웃 없음.  pop (6,D) → 낡은 항목 ✂
```

- 힙에는 같은 정점이 여러 번 들어갈 수 있습니다 (파이썬 heapq 에는 decrease-key 가 없음).
- 그래서 꺼낸 값이 `d > dist[u]` 면 **낡은 항목** 이므로 버립니다 (lazy deletion). 이 한 줄이 빠지면 최악 성능이 크게 나빠집니다.
- **음수 간선이 있으면 틀립니다**: 이미 확정한 정점이 나중에 음수 간선으로 더 짧아질 수 있기 때문.

### 2) 벨만-포드: 모든 간선을 V-1 번 완화

```
라운드 i 가 끝나면 dist[v] = "간선 i 개 이하를 써서 v 에 가는 최단 거리" (배열을 복사해서 갱신할 때)
V-1 라운드면 모든 최단 경로 확정 (단순 경로는 간선 ≤ V-1 개)
V 번째 라운드에서도 갱신이 일어나면 → 음의 사이클 존재
"최대 k 번 경유" = 간선 ≤ k+1 개 → k+1 라운드만 (Cheapest Flights)
```

### 3) 플로이드-워셜: 경유 정점을 하나씩 허용

```
dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
k 루프가 반드시 가장 바깥!  k 단계 후 dist = "1..k 만 경유 가능할 때의 최단 거리"

  i ────────▶ j          k = 1, 2, ..., n 순서로 "k 를 거쳐 가면 더 짧은가?"
   \        ↗
    ▶  k  ─
```

### 4) 최소 신장 트리 (MST)

```
크루스칼: 간선을 비용순으로 보며 사이클이 안 생기면 채택 (Union-Find)

   간선(비용순)   채택?          A ─1─ B
   A-B 1          ✔                ╲   │
   B-C 2          ✔                3╲  │ 2
   A-C 3          ✘ (사이클)          ╲ │
   C-D 4          ✔              D ─4─ C       total = 1 + 2 + 4 = 7

프림: 트리에서 출발해 "트리와 가장 가까운 정점" 을 하나씩 붙임 (다익스트라와 거의 같은 모양, 비용이 누적 거리 대신 간선 하나)
```

| | 크루스칼 | 프림 (힙) | 프림 (배열) |
|---|---|---|---|
| 시간 | O(E log E) | O(E log V) | O(V^2) |
| 어울리는 경우 | 간선 목록이 주어짐, 희소 그래프 | 인접 리스트, 희소~보통 | 완전 그래프 / 밀집 그래프 (점 좌표 문제) |

### 5) 0-1 BFS

```
비용 0 간선 → deque 앞에 (appendleft), 비용 1 간선 → 뒤에 (append)
deque 가 항상 "거리 d 인 정점들 + 거리 d+1 인 정점들" 순서로 유지되어 다익스트라와 같은 결과를 O(V + E) 에
```

### 6) 어떤 최단 경로 알고리즘을 쓸까? (결정표)

| 상황 | 알고리즘 | 시간 | 파이썬 감각 |
|---|---|---|---|
| 모든 간선 비용 동일 | BFS | O(V + E) | 10^6 까지 |
| 비용이 0 또는 1 | 0-1 BFS | O(V + E) | 10^6 까지 |
| 비용 ≥ 0, 출발점 하나 | 다익스트라 (heapq) | O(E log V) | E ≤ 수십만 |
| 비용 ≥ 0, 완전/밀집 그래프 | 배열 다익스트라 | O(V^2) | V ≤ 수천 |
| 음수 간선 / 음의 사이클 판별 | 벨만-포드 | O(V · E) | V·E ≤ 10^7 |
| 간선 수(경유 횟수) 제한 | 벨만-포드 k 라운드 / (정점, 횟수) 상태 다익스트라 | O(k · E) | |
| 모든 쌍 최단 거리 | 플로이드-워셜 | O(V^3) | V ≤ 200 (빠듯하면 400) |
| 출발점이 몇 개뿐 (예: s, a, b) | 다익스트라 여러 번 | O(c · E log V) | 합승 택시 |
| 경로 위 최댓값 최소화 | max 다익스트라 / 이분 탐색 + BFS / Union-Find | O(E log V) | 수영, 등산코스 |
| DAG (사이클 없음) | 위상 정렬 순서로 DP | O(V + E) | 음수 간선도 OK |

## 코드 템플릿

### 템플릿 1: 다익스트라 (heapq + lazy deletion)

```python
import heapq

def dijkstra(n, graph, start):          # graph[u] = [(v, w), ...]
    INF = float("inf")
    dist = [INF] * n
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:                 # 낡은 항목 → 버리기 (lazy deletion)
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist
```

### 템플릿 2: 벨만-포드 (음의 사이클 판별 / k 라운드 제한)

```python
def bellman_ford(n, edges, start, rounds=None):
    INF = float("inf")
    dist = [INF] * n
    dist[start] = 0
    for _ in range(rounds or n - 1):
        prev = dist[:]                  # 라운드 제한이 있으면 반드시 복사본에서 읽기
        for u, v, w in edges:
            if prev[u] != INF and prev[u] + w < dist[v]:
                dist[v] = prev[u] + w
    # 음의 사이클 판별: 한 번 더 돌려서 갱신되면 사이클 존재
    has_negative_cycle = any(dist[u] != INF and dist[u] + w < dist[v] for u, v, w in edges)
    return dist, has_negative_cycle
```

### 템플릿 3: 플로이드-워셜

```python
def floyd(n, edges):                    # 정점 0..n-1
    INF = float("inf")
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)  # 같은 쌍에 간선이 여러 개면 최솟값
    for k in range(n):                  # k 가 가장 바깥!
        dk = dist[k]
        for i in range(n):
            dik = dist[i][k]
            if dik == INF:
                continue
            di = dist[i]
            for j in range(n):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    return dist
```

### 템플릿 4: 크루스칼 MST (Union-Find)

```python
def kruskal(n, edges):                  # edges = [(w, u, v), ...]
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = used = 0
    for w, u, v in sorted(edges):
        ru, rv = find(u), find(v)
        if ru != rv:                    # 사이클이 생기지 않을 때만 채택
            parent[ru] = rv
            total += w
            used += 1
            if used == n - 1:
                break
    return total if used == n - 1 else -1   # -1: 연결 불가
```

### 템플릿 5: 프림 MST (힙)

```python
import heapq

def prim(n, graph):                     # graph[u] = [(v, w), ...] 무방향
    visited = [False] * n
    heap = [(0, 0)]                     # (연결 비용, 정점)
    total = count = 0
    while heap and count < n:
        w, u = heapq.heappop(heap)
        if visited[u]:
            continue                    # 이미 트리에 들어간 정점
        visited[u] = True
        total += w
        count += 1
        for v, cost in graph[u]:
            if not visited[v]:
                heapq.heappush(heap, (cost, v))
    return total
```

### 템플릿 6: 0-1 BFS

```python
from collections import deque

def zero_one_bfs(n, graph, start):      # graph[u] = [(v, w)], w 는 0 또는 1
    INF = float("inf")
    dist = [INF] * n
    dist[start] = 0
    dq = deque([start])
    while dq:
        u = dq.popleft()
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if w == 0:
                    dq.appendleft(v)    # 비용 0 → 앞에
                else:
                    dq.append(v)        # 비용 1 → 뒤에
    return dist
```

## 시간 · 공간 복잡도

| 알고리즘 | 시간 | 공간 | 음수 간선 |
|---|---|---|---|
| BFS | O(V + E) | O(V) | - (비용 동일) |
| 0-1 BFS | O(V + E) | O(V) | ❌ |
| 다익스트라 (힙) | O(E log V) | O(V + E) | ❌ |
| 다익스트라 (배열) | O(V^2) | O(V) | ❌ |
| 벨만-포드 | O(V · E) | O(V) | ✅ (음의 사이클 판별 가능) |
| 플로이드-워셜 | O(V^3) | O(V^2) | ✅ (음의 사이클이 없을 때) |
| 크루스칼 | O(E log E) | O(V + E) | 무관 |
| 프림 (힙 / 배열) | O(E log V) / O(V^2) | O(V + E) / O(V) | 무관 |
| 위상 정렬 | O(V + E) | O(V + E) | 무관 |
| 히어홀저 (오일러 경로) | O(E log E) (사전 순 정렬 포함) | O(E) | 무관 |

## 자주 하는 실수

- [ ] 다익스트라에서 `if d > dist[u]: continue` 누락 → 낡은 항목까지 처리해 느려짐
- [ ] 힙에 `(정점, 거리)` 순서로 넣음 → 정점 번호 기준으로 정렬됨. **`(거리, 정점)`** 순서
- [ ] 음수 간선이 있는데 다익스트라 사용
- [ ] 무방향 그래프인데 간선을 한 방향만 추가 (합승 택시, MST)
- [ ] 같은 쌍에 간선이 여러 개일 때 플로이드 초기화에서 최솟값을 안 취함 (`dist[u][v] = w` 로 덮어씀)
- [ ] 플로이드의 루프 순서를 i, j, k 로 씀 → 오답. **k, i, j**
- [ ] 벨만-포드 k 라운드 제한 문제에서 배열을 복사하지 않음 → 한 라운드에 간선 여러 개를 타 버림
- [ ] `INF + w` 비교: `float("inf")` 는 괜찮지만 `10**9` 같은 큰 수를 쓰면 더해서 넘치거나 잘못된 갱신이 생길 수 있음 → `dist[u] != INF` 확인
- [ ] 도달 불가 처리 (-1 반환) 누락
- [ ] 정점 번호 1-index 인데 배열을 n 크기로 만듦
- [ ] MST 에서 간선이 n-1 개가 안 되면 연결 불가인데 그대로 합계를 반환
- [ ] 최소 병목 경로를 "합" 다익스트라로 풀어 버림 (Swim in Rising Water 는 `max`)
- [ ] 외계어 사전에서 첫 번째 다른 글자 이후까지 비교하거나, 접두사 역전(`"abc"` 다음 `"ab"`)을 놓침

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Network Delay Time | Medium | heapq 다익스트라 + lazy deletion, 최댓값 | `python practice.py start network-delay-time` |
| 2 | Cheapest Flights Within K Stops | Medium | 벨만-포드 k+1 라운드(배열 복사), 상태 다익스트라 | `python practice.py start cheapest-flights-within-k-stops` |
| 3 | Min Cost to Connect All Points | Medium | 완전 그래프 MST → O(V^2) 프림, 크루스칼 비교 | `python practice.py start min-cost-to-connect-all-points` |
| 4 | Shared Taxi Fare (합승 택시 요금) | Hard | 경유점 k 전부 시도, 다익스트라 3번 vs 플로이드 | `python practice.py start shared-taxi-fare` |
| 5 | Swim in Rising Water | Hard | 최소 병목 경로: max 다익스트라 / 이분 탐색 + BFS | `python practice.py start swim-in-rising-water` |
| 6 | Alien Dictionary | Hard | 인접 단어 비교로 간선 → 위상 정렬, 모순 판별 | `python practice.py start alien-dictionary` |
| 7 | Reconstruct Itinerary (여행경로) | Hard | 오일러 경로, 히어홀저 (막힌 순서 뒤집기) | `python practice.py start reconstruct-itinerary` |

## 더 풀어 볼 문제

- LeetCode 1631. Path With Minimum Effort (최소 병목)
- LeetCode 1514. Path with Maximum Probability (곱 → 최대 힙 다익스트라)
- LeetCode 1334. Find the City With the Smallest Number of Neighbors (플로이드)
- LeetCode 1135. Connecting Cities With Minimum Cost (크루스칼)
- LeetCode 1368. Minimum Cost to Make at Least One Valid Path in a Grid (0-1 BFS)
- LeetCode 2290. Minimum Obstacle Removal to Reach Corner (0-1 BFS)
- LeetCode 1976. Number of Ways to Arrive at Destination (다익스트라 + 경로 수)
- 프로그래머스 Lv.2 배달 (다익스트라)
- 프로그래머스 Lv.3 합승 택시 요금 (2021 KAKAO BLIND)
- 프로그래머스 Lv.3 섬 연결하기 (크루스칼)
- 프로그래머스 Lv.3 여행경로 (DFS / 오일러 경로)
- 프로그래머스 Lv.3 부대복귀 (역방향 BFS/다익스트라)
- 프로그래머스 Lv.3 등산코스 정하기 (2022 KAKAO, 최소 병목 다익스트라)
- 프로그래머스 Lv.3 순위 (플로이드로 승패 전이)
- 프로그래머스 Lv.3 경주로 건설 (상태 확장 다익스트라: 방향까지 상태로)

## 영어로 설명하기 (미국 면접용)

- "Because the edge weights are non-negative but not uniform, I'll use Dijkstra's algorithm with a min-heap instead of plain BFS."
- "Python's heapq doesn't support decrease-key, so I push duplicates and skip any popped entry whose distance is larger than the best one recorded — that's lazy deletion."
- "With the stop limit, the cheapest path might use too many edges, so I run Bellman-Ford for exactly k plus one rounds and read from a copy of the previous round's distances."
- "The input is a complete graph with about n squared over two edges, so the O(n squared) array version of Prim's algorithm beats Kruskal, which would have to sort every edge."
- "Since only three sources matter, I run Dijkstra from s, a and b, then try every split point k and take the minimum of the three distances summed; Floyd-Warshall would also work, but it's O(n cubed)."

## 체크리스트

- [ ] 결정표를 보고 BFS / 0-1 BFS / 다익스트라 / 벨만-포드 / 플로이드 중 무엇을 쓸지 고를 수 있다
- [ ] heapq 다익스트라를 lazy deletion 포함해 5분 안에 쓴다
- [ ] 다익스트라가 음수 간선에서 틀리는 이유를 예시로 설명할 수 있다
- [ ] 벨만-포드에서 라운드 수의 의미(간선 개수)와 배열 복사의 이유를 설명할 수 있다
- [ ] 플로이드-워셜의 k-i-j 순서를 외우고 이유를 말할 수 있다
- [ ] 크루스칼과 프림을 모두 구현하고, 희소/밀집 그래프에서 무엇이 유리한지 안다
- [ ] "경유점 k 를 고정" 하는 발상(합승 택시)을 다른 문제에 적용할 수 있다
- [ ] 합 대신 max 비용으로 다익스트라를 변형할 수 있다 (최소 병목)
- [ ] 위상 정렬로 순서를 복원하고 사이클/모순을 판별한다
- [ ] 오일러 경로를 히어홀저로 구하고, 사전 순 최소 조건을 처리한다
