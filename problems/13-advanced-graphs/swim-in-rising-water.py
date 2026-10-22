import random

TITLE = "Swim in Rising Water (차오르는 물에서 수영하기)"
LEVEL = "Hard"
SOURCE = "LeetCode 778"
PATTERN = "최소 병목 경로(minimax path): 다익스트라 변형 (합 대신 max)"

DESCRIPTION = """
n × n 격자 grid 의 각 칸에는 지형의 높이가 적혀 있고, 0 부터 n² - 1 까지의 값이 한 번씩 등장합니다.
시각 t 에는 모든 곳의 수위가 t 입니다. 수위가 t 일 때는 높이가 t 이하인 칸들 사이만 헤엄쳐 다닐 수 있고,
상하좌우로 인접한 칸 이동은 (두 칸 모두 높이 t 이하라면) 시간이 들지 않습니다.

시각 0 에 왼쪽 위 (0, 0) 에서 출발해 오른쪽 아래 (n-1, n-1) 에 도착할 수 있는 가장 이른 시각을 return 하세요.
다르게 말하면, 출발점에서 도착점까지의 경로 중 '경로 위 최대 높이' 가 가장 작은 경로의 그 최대 높이입니다.

제한사항
- 1 ≤ n ≤ 200
- grid 의 값은 0 ~ n² - 1 이 한 번씩 등장 (모두 다름)

입출력 예
grid = [[0, 2],
        [1, 3]]        →  3    (도착 칸의 높이가 3 이므로 최소 3)

grid = [[0, 5, 6],
        [1, 8, 7],
        [2, 3, 4]]     →  4    (0 → 1 → 2 → 3 → 4 경로의 최댓값 4)
"""

SIGNATURE = "def solution(grid: list[list[int]]) -> int:"

HINTS = [
    "어떤 경로의 '비용' 을 간선 합이 아니라 경로 위 칸 높이의 최댓값으로 정의하면, 이 비용을 최소화하는 경로 문제입니다.",
    "방법 1: 답 t 를 정하면 '높이 ≤ t 인 칸만으로 도착 가능한가?' 를 BFS 로 판정할 수 있고, t 가 커질수록 가능해지므로 이분 탐색할 수 있습니다. O(n² log n²).",
    "방법 2: 다익스트라에서 새 거리 = dist[u] + w 대신 max(dist[u], grid[v]) 로 바꾸세요. 힙에서 꺼낸 순간 그 칸까지의 최소 '최대 높이' 가 확정됩니다.",
    "방법 3: 칸을 높이 순으로 하나씩 '물에 잠기게' 하며 이웃과 Union-Find 로 합치다가, 시작과 끝이 같은 집합이 되는 순간의 높이가 답입니다.",
]

TESTS = [
    {"input": [[[0, 2], [1, 3]]], "output": 3},
    {"input": [[[0, 5, 6], [1, 8, 7], [2, 3, 4]]], "output": 4},
    {"input": [[[0]]], "output": 0},
    {"input": [[[3, 2], [0, 1]]], "output": 3},
    {"input": [[[0, 1, 2], [5, 4, 3], [6, 7, 8]]], "output": 8},
    {
        "input": [[[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16],
                   [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]]],
        "output": 16,
    },
    {"input": [[[0, 8, 7], [3, 6, 2], [1, 5, 4]]], "output": 5},
]

PERF_LIMIT = 1.0


def perf_case():
    # 가운데 열에 가장 높은 값들로 "벽" 을 세워 답이 n² 근처가 되게 함
    # → t 를 0 부터 하나씩 올리는 풀이는 수만 번 BFS 를 하게 됨
    n = 200
    wall = list(range(n * n - n, n * n))
    rest = list(range(n * n - n))
    random.shuffle(wall)
    random.shuffle(rest)
    grid = []
    for r in range(n):
        row = rest[r * (n - 1):(r + 1) * (n - 1)]
        row.insert(n // 2, wall[r])
        grid.append(row)
    return {"input": [grid], "output": None}


EXPLANATION = """
핵심: 경로 비용 = 경로 위 최대 높이 (병목, bottleneck). 이 비용을 최소화 → "합" 대신 "max" 를 쓰는 다익스트라.

다익스트라가 여전히 맞는 이유: max(현재 비용, 다음 칸 높이) 는 경로가 길어져도 줄어들지 않는(단조 증가) 비용이라
"힙에서 가장 작은 비용으로 꺼낸 칸은 확정" 이라는 성질이 그대로 성립합니다.

grid           힙에서 꺼내는 순서 (비용)
0 5 6          (0,0):0 → (1,0):1 → (2,0):2 → (2,1):3 → (2,2):4 도착 ✔
1 8 7          5, 6, 7, 8 칸은 꺼내기 전에 끝남
2 3 4

1. time[r][c] = 그 칸까지의 최소 "최대 높이". 시작 = grid[0][0]
2. 힙에 (grid[0][0], 0, 0). pop (t, r, c) — 도착점이면 t 반환
3. 이웃 (nr, nc): nt = max(t, grid[nr][nc]) 가 더 작으면 갱신 후 push

시간 O(n² log n), 공간 O(n²)

다른 풀이
- 이분 탐색 + BFS (alternative): lo = grid[0][0], hi = n²-1. "t 이하 칸만으로 도달 가능?" 판정을 log(n²) 번.
- Union-Find: 높이 순으로 칸을 활성화하며 활성화된 이웃과 union, find(start) == find(end) 가 되는 순간의 높이.
- t = 0, 1, 2, ... 를 하나씩 올리며 매번 BFS 하는 풀이(brute_force)는 O(n^4) → 큰 입력에서 시간 초과.

면접 포인트
- "최소 병목 경로" 는 Path With Minimum Effort(1631), 프로그래머스 '등산코스 정하기'(2022 KAKAO, intensity 최소화)와 같은 구조입니다.
- 다익스트라는 "비용이 경로를 따라 줄지 않는다" 는 조건만 있으면 합이 아닌 다른 비용에도 쓸 수 있다는 점을 강조하세요.
"""


def reference(grid):
    import heapq

    n = len(grid)
    best = [[float("inf")] * n for _ in range(n)]
    best[0][0] = grid[0][0]
    heap = [(grid[0][0], 0, 0)]
    while heap:
        t, r, c = heapq.heappop(heap)
        if (r, c) == (n - 1, n - 1):
            return t                            # 처음 꺼낸 순간 = 최소 병목
        if t > best[r][c]:
            continue
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < n and 0 <= nc < n:
                nt = max(t, grid[nr][nc])       # 합 대신 max
                if nt < best[nr][nc]:
                    best[nr][nc] = nt
                    heapq.heappush(heap, (nt, nr, nc))
    return -1


def alternative(grid):
    # 이분 탐색 + BFS: "높이 t 이하 칸만으로 도착 가능한가?" 는 t 에 대해 단조
    from collections import deque

    n = len(grid)

    def reachable(t):
        if grid[0][0] > t:
            return False
        seen = [[False] * n for _ in range(n)]
        seen[0][0] = True
        queue = deque([(0, 0)])
        while queue:
            r, c = queue.popleft()
            if (r, c) == (n - 1, n - 1):
                return True
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < n and 0 <= nc < n and not seen[nr][nc] and grid[nr][nc] <= t:
                    seen[nr][nc] = True
                    queue.append((nr, nc))
        return False

    lo, hi = max(grid[0][0], grid[n - 1][n - 1]), n * n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if reachable(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def brute_force(grid):
    # t 를 0 부터 하나씩 올리며 매번 BFS: O(n^4)
    from collections import deque

    n = len(grid)
    for t in range(n * n):
        if grid[0][0] > t:
            continue
        seen = {(0, 0)}
        queue = deque([(0, 0)])
        while queue:
            r, c = queue.popleft()
            if (r, c) == (n - 1, n - 1):
                return t
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen and grid[nr][nc] <= t:
                    seen.add((nr, nc))
                    queue.append((nr, nc))
    return -1
