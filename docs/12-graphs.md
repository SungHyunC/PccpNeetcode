# 12. 그래프 BFS/DFS (Graphs)

> 정점(vertex)과 간선(edge)으로 관계를 표현하고, BFS(너비 우선)·DFS(깊이 우선)로 "연결됐나? 몇 덩어리인가? 최단 몇 걸음인가? 순서를 정할 수 있나?" 를 답합니다.

## 이런 문제에서 떠올리세요

- 격자(지도, 미로, 섬, 오렌지, 토마토) + "상하좌우로 이어진" → 격자 그래프 BFS/DFS
- "최소 몇 번 / 몇 칸 / 몇 분" + 모든 이동 비용이 같음 → **BFS** (DFS 는 최단을 보장하지 않음)
- "몇 덩어리 / 몇 개의 그룹 / 네트워크 수" → 연결 요소 세기 (BFS/DFS 또는 **Union-Find**)
- "동시에 퍼진다", "여러 곳에서 시작" → **다중 시작점 BFS (multi-source BFS)**
- "A 를 하려면 B 를 먼저", 선후 관계, 빌드 순서 → **위상 정렬 (topological sort)**, 사이클 판별
- "간선을 하나씩 추가하며 이미 연결됐는지", "사이클을 만드는 간선" → **Union-Find**
- 한 글자씩 바꾸기, 상태 변환 → 상태를 정점으로 보는 **암시적 그래프 (implicit graph)** BFS
- 입력 크기 힌트: 정점 V, 간선 E 가 10^5 ~ 10^6 → O(V + E) 탐색. 격자 1000 × 1000 = 10^6 칸도 BFS 한 번은 가능 (파이썬은 빠듯)

## 핵심 개념

### 1) 그래프 표현: 인접 리스트(adjacency list)

```
edges = [[0,1],[0,2],[1,3],[2,3],[3,4]]   (무방향)

  0 ── 1                graph[0] = [1, 2]
  │    │                graph[1] = [0, 3]
  2 ── 3 ── 4           graph[2] = [0, 3]
                        graph[3] = [1, 2, 4]
                        graph[4] = [3]

공간 O(V + E). 인접 행렬(V × V)은 V ≤ 수백일 때만 (프로그래머스 '네트워크' 처럼 행렬로 주어지기도 함)
```

- 무방향이면 `graph[a].append(b)` 와 `graph[b].append(a)` **둘 다**
- 정점 번호가 1부터면 크기를 `n + 1` 로 잡기
- 정점이 문자열이면 `defaultdict(list)`

### 2) 격자 = 암시적 그래프

```
칸 (r, c) 의 이웃 = (r±1, c), (r, c±1)    ← 간선을 따로 만들지 않음

DIRS = [(1,0), (-1,0), (0,1), (0,-1)]      # 4방향 (대각선 포함 8방향이면 8개)

       (r-1,c)
          ▲
(r,c-1) ◀ ■ ▶ (r,c+1)        항상 0 <= nr < R and 0 <= nc < C 범위 검사 먼저!
          ▼
       (r+1,c)
```

### 3) BFS vs DFS

```
시작 S 에서 퍼지는 순서

BFS (큐, 동심원)              DFS (스택, 한 길로 끝까지)
  2 1 2 3                       1 2 3 4
  1 S 1 2                       S . . 5
  2 1 2 3                       . 8 7 6
→ 처음 방문한 순간의 레벨 = 최단 거리   → 최단 보장 없음. 연결성·사이클·경로 열거용
```

| | BFS | DFS |
|---|---|---|
| 자료구조 | `collections.deque` (popleft) | 재귀 호출 스택 / 리스트 스택 (pop) |
| 최단 거리 (가중치 동일) | ✅ 보장 | ❌ |
| 연결 요소, 영역 크기 | ✅ | ✅ |
| 사이클 판별, 위상 정렬 | Kahn(진입 차수) | 3색 표시, 후위 순서 |
| 파이썬 주의점 | `list.pop(0)` 은 O(n) → deque 필수 | 재귀 깊이 기본 1000 |

### 4) 방문 표시 타이밍: "큐에 넣을 때"

```
A 의 이웃 B, C / B 와 C 의 공통 이웃 D

꺼낼 때 표시:  큐 [B, C] → B 처리 시 D 넣음 → C 처리 시 D 또 넣음 (D 가 아직 미방문) → 중복!
넣을 때 표시:  B 처리 시 D 넣으며 visited[D] = True → C 는 D 를 건너뜀 ✔
```

BFS 에서 꺼낼 때 표시하면 같은 정점이 큐에 여러 번 들어가 최악 O(E) 개가 쌓이고, 거리도 덮어써질 수 있습니다.

### 5) 파이썬 재귀 DFS 의 함정

- 기본 재귀 한도 1000. 300 × 300 격자가 전부 땅이면 깊이 최대 90,000 → `RecursionError`
- `sys.setrecursionlimit(10**6)` 으로 한도를 올려도, 너무 깊으면 C 스택이 넘쳐 **프로세스가 그냥 죽을 수 있음** (에러 메시지도 없이)
- 해결: **BFS** 또는 **리스트로 직접 스택을 관리하는 반복 DFS** 를 기본으로 쓰기
- 프로그래머스는 재귀 한도를 올리면 대부분 통과하지만, 깊이가 10^5 를 넘을 수 있으면 반복문이 안전합니다

### 6) 위상 정렬 (Kahn 알고리즘)

```
선수 과목: 0→1, 0→2, 1→3, 2→3, 3→4

in-degree   0:0 1:1 2:1 3:2 4:1
queue [0]   → pop 0 → 1:0, 2:0 → queue [1, 2]
            → pop 1 → 3:1
            → pop 2 → 3:0 → queue [3]
            → pop 3 → 4:0 → queue [4] → pop 4
순서: 0 1 2 3 4  (꺼낸 개수 5 == V → 사이클 없음)

사이클이 있으면 그 위의 정점은 진입 차수가 0 이 되지 않아 끝내 꺼내지지 않음 → 꺼낸 개수 < V
```

### 7) Union-Find (Disjoint Set Union)

```
parent: 각 정점이 가리키는 부모. 루트 = 그룹 대표

union(1,2) union(3,4) union(2,4)      find(4) 경로 압축 후
     1          3                           1
     │          │      →   1                ├── 2
     2          4          ├── 2            ├── 3
                           └── 3            └── 4   ← 4 가 루트를 직접 가리킴
                               └── 4
union by rank: 낮은 트리를 높은 트리 밑에 → 높이 O(log n)
경로 압축 + 랭크 → 연산당 O(α(n)) ≈ 상수
```

- `find(a) == find(b)` → 이미 같은 그룹 (이 간선을 추가하면 **사이클**)
- 그룹 수 = n - (성공한 union 횟수)
- 간선이 계속 추가되는 온라인 상황, 크루스칼 MST(13장) 에서 핵심

## 코드 템플릿

### 템플릿 1: 인접 리스트 + BFS 최단 거리

```python
from collections import deque

def bfs(n, edges, start):
    graph = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)              # 무방향
    dist = [-1] * n                     # -1 = 미방문 (visited 겸용)
    dist[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1   # 넣을 때 방문 표시
                queue.append(v)
    return dist
```

### 템플릿 2: 격자 BFS (다중 시작점 포함)

```python
from collections import deque

def grid_bfs(grid, starts):
    R, C = len(grid), len(grid[0])
    dist = [[-1] * C for _ in range(R)]
    queue = deque()
    for r, c in starts:                 # 시작점이 여러 개면 전부 거리 0 으로
        dist[r][c] = 0
        queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != 0 and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    return dist
```

### 템플릿 3: DFS — 재귀 vs 반복

```python
import sys
sys.setrecursionlimit(10**6)            # 재귀 DFS 를 쓸 때는 필수 (그래도 너무 깊으면 위험)

def dfs_recursive(u, graph, visited):
    visited[u] = True
    for v in graph[u]:
        if not visited[v]:
            dfs_recursive(v, graph, visited)

def dfs_iterative(start, graph, visited):
    visited[start] = True
    stack = [start]
    while stack:
        u = stack.pop()
        for v in graph[u]:
            if not visited[v]:
                visited[v] = True       # 넣을 때 표시 (연결 요소 탐색 용도)
                stack.append(v)
```

### 템플릿 4: 위상 정렬 (Kahn)

```python
from collections import deque

def topo_sort(n, edges):                # edges: (u, v) = u 다음에 v
    graph = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indeg[v] += 1
    queue = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return order if len(order) == n else []   # 빈 리스트 = 사이클 존재
```

### 템플릿 5: Union-Find (경로 압축 + 랭크)

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # 경로 압축(절반 줄이기)
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                # 이미 같은 집합 → 사이클
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra            # 낮은 트리를 높은 트리 밑에
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True
```

## 시간 · 공간 복잡도

| 알고리즘 | 시간 | 공간 | 비고 |
|---|---|---|---|
| BFS / DFS (인접 리스트) | O(V + E) | O(V) | 인접 행렬이면 O(V^2) |
| 격자 BFS / DFS | O(R · C) | O(R · C) | 간선은 칸당 최대 4개 |
| 다중 시작점 BFS | O(V + E) | O(V) | 시작점마다 따로 돌리면 O(k(V+E)) |
| 위상 정렬 (Kahn / DFS) | O(V + E) | O(V + E) | |
| Union-Find (경로 압축 + 랭크) | 연산당 O(α(n)) | O(n) | α(n) ≤ 4 (사실상 상수) |
| 단어 사다리 (버킷) | O(N · L^2) | O(N · L^2) | N 단어, 길이 L |

## 자주 하는 실수

- [ ] 무방향 그래프인데 한쪽 방향 간선만 추가
- [ ] BFS 큐로 `list.pop(0)` 사용 → O(n). `deque.popleft()` 사용하기
- [ ] 방문 표시를 큐에서 **꺼낼 때** 함 → 같은 정점이 중복으로 들어감. **넣을 때** 표시
- [ ] 시작점 방문 표시 누락 → 시작점으로 되돌아와 거리가 꼬임
- [ ] 격자 범위 검사 순서: `grid[nr][nc]` 를 먼저 읽고 범위 검사 → IndexError, 또는 **음수 인덱스가 반대편 칸을 읽는 조용한 버그**
- [ ] 재귀 DFS 에서 `sys.setrecursionlimit` 누락 → 큰 입력에서 RecursionError
- [ ] 1번부터 시작하는 정점 번호인데 크기를 n 으로 잡음
- [ ] 다중 시작점 BFS 에서 레벨 수를 셀 때 마지막 레벨 뒤에 +1 이 한 번 더 되는 off-by-one (Rotting Oranges 에서 `while queue and fresh > 0`)
- [ ] "도달 불가능" 처리 누락 (-1 / 0 반환 조건)
- [ ] 방향 그래프 사이클 판별을 무방향처럼 visited 하나로만 함 → 3색(미방문/방문 중/완료) 또는 Kahn 사용
- [ ] Union-Find 에서 `parent[a] = b` 처럼 루트가 아닌 정점끼리 연결 → 반드시 `find` 결과(루트)끼리 연결

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Number of Islands | Medium | 격자 연결 요소 세기, BFS vs 재귀 DFS | `python practice.py start number-of-islands` |
| 2 | Max Area of Island | Medium | 연결 요소 크기, 반복 DFS(스택) | `python practice.py start max-area-of-island` |
| 3 | Shortest Path in Grid Maze | Medium | 가중치 없는 최단 거리 = BFS (게임 맵 최단거리 유형) | `python practice.py start shortest-path-in-grid-maze` |
| 4 | Rotting Oranges | Medium | 다중 시작점 BFS, 레벨 = 시간 | `python practice.py start rotting-oranges` |
| 5 | Pacific Atlantic Water Flow | Medium | 바다에서 거꾸로 BFS 두 번 + 교집합 | `python practice.py start pacific-atlantic-water-flow` |
| 6 | Course Schedule | Medium | 위상 정렬(Kahn)로 사이클 판별 | `python practice.py start course-schedule` |
| 7 | Number of Connected Components | Medium | Union-Find 로 그룹 수 세기 | `python practice.py start number-of-connected-components` |
| 8 | Redundant Connection | Medium | Union-Find: 이미 연결된 두 정점 = 사이클 간선 | `python practice.py start redundant-connection` |
| 9 | Word Ladder | Hard | 암시적 그래프 BFS + 와일드카드 버킷 | `python practice.py start word-ladder` |

## 더 풀어 볼 문제

- LeetCode 133. Clone Graph
- LeetCode 130. Surrounded Regions (가장자리에서 거꾸로 탐색)
- LeetCode 286. Walls and Gates (다중 시작점 BFS)
- LeetCode 210. Course Schedule II (위상 정렬 순서 반환)
- LeetCode 261. Graph Valid Tree (간선 수 = V-1 + 연결성)
- LeetCode 1091. Shortest Path in Binary Matrix (8방향 BFS)
- LeetCode 785. Is Graph Bipartite? (BFS 2색 칠하기)
- 프로그래머스 Lv.2 게임 맵 최단거리
- 프로그래머스 Lv.3 네트워크
- 프로그래머스 Lv.3 단어 변환
- 프로그래머스 Lv.2 타겟 넘버
- 프로그래머스 Lv.2 무인도 여행 (섬마다 합 구하기)
- 프로그래머스 Lv.2 미로 탈출 (레버 경유 → BFS 두 번)
- 프로그래머스 Lv.2 전력망을 둘로 나누기 (간선 하나씩 끊고 연결 요소 크기)
- 프로그래머스 [PCCP 기출문제] 석유 시추 (연결 요소 크기 + 열별 합산)
- 프로그래머스 Lv.3 가장 먼 노드 (BFS 거리)

## 영어로 설명하기 (미국 면접용)

- "I'll model the grid as an implicit graph where each cell is a node and its four neighbors are the edges, so I don't need to build an adjacency list."
- "Since every move costs the same, BFS gives the shortest path: the first time we pop the target, its distance is minimal."
- "I mark a cell as visited when I push it onto the queue rather than when I pop it, so each cell is enqueued at most once and the whole traversal is O(rows times columns)."
- "In Python I prefer iterative BFS or an explicit stack over recursive DFS, because the default recursion limit is about a thousand frames and a large grid could overflow it."
- "To detect a cycle in the prerequisite graph I use Kahn's algorithm: if the number of nodes I can pop with zero in-degree is less than the total, there is a cycle."

## 체크리스트

- [ ] 간선 목록 → 인접 리스트(무방향/방향, 0-index/1-index)를 실수 없이 만든다
- [ ] 격자 4방향 BFS 를 deque 로 5분 안에 쓸 수 있다
- [ ] "최단 거리" 문제에서 왜 DFS 가 아닌 BFS 인지 설명할 수 있다
- [ ] 방문 표시를 큐에 넣을 때 해야 하는 이유를 설명할 수 있다
- [ ] 재귀 DFS 의 재귀 한도 문제와 해결책(setrecursionlimit, 반복 DFS)을 안다
- [ ] 다중 시작점 BFS 로 "동시에 퍼지는" 문제를 푼다
- [ ] Kahn 알고리즘으로 위상 정렬과 사이클 판별을 한다
- [ ] Union-Find 를 경로 압축 + union by rank 로 구현하고, 언제 BFS 보다 유리한지 말할 수 있다
- [ ] "거꾸로 탐색"(바다에서, 출구에서)이 유리한 상황을 알아본다
