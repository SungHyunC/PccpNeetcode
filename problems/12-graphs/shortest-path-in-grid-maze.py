import random

TITLE = "Shortest Path in Grid Maze (미로 최단 거리)"
LEVEL = "Medium"
SOURCE = "프로그래머스 Lv.2 '게임 맵 최단거리' 유형"
PATTERN = "가중치 없는 격자 최단 거리 = BFS"

DESCRIPTION = """
탐험가가 R × C 크기의 미로 왼쪽 위 칸 (0, 0) 에 있습니다. 출구는 오른쪽 아래 칸 (R-1, C-1) 입니다.
maps[r][c] 가 1 이면 지나갈 수 있는 길, 0 이면 벽입니다.
탐험가는 한 번에 상하좌우 중 한 칸으로 이동할 수 있고, 벽이나 미로 바깥으로는 갈 수 없습니다.

출구까지 가는 동안 지나는 칸 수의 최솟값을 return 하세요. 출발 칸과 도착 칸도 셉니다.
출구에 도착할 수 없으면 -1 을 return 합니다.

제한사항
- 1 ≤ R, C ≤ 300
- maps[r][c] 는 0 또는 1
- 출발 칸과 도착 칸은 항상 1 입니다.

입출력 예
maps = [[1, 1, 1],
        [0, 0, 1],
        [1, 1, 1]]   →  5    ((0,0)→(0,1)→(0,2)→(1,2)→(2,2))

maps = [[1, 0],
        [0, 1]]      →  -1   (출구가 벽에 막혀 있음)

maps = [[1]]         →  1    (출발 칸이 곧 출구)
"""

SIGNATURE = "def solution(maps: list[list[int]]) -> int:"

HINTS = [
    "모든 이동의 비용이 1 로 같을 때 최단 거리는 BFS(너비 우선 탐색)로 구합니다. DFS 로 모든 경로를 다 보면 경로 수가 폭발합니다.",
    "dist[r][c] = 출발점에서 (r, c) 까지 지나는 칸 수. dist[0][0] = 1 로 시작하고, 이웃 칸은 dist[r][c] + 1 입니다.",
    "collections.deque 를 큐로 쓰세요. 이웃을 큐에 '넣을 때' dist 를 기록하면 그 칸은 이미 방문한 것으로 처리되어 중복으로 들어가지 않습니다.",
    "BFS 가 끝났는데 dist[R-1][C-1] 이 아직 기록되지 않았다면 -1 입니다. 출구를 꺼내는 순간 바로 return 해도 됩니다.",
]

TESTS = [
    {"input": [[[1, 1, 1], [0, 0, 1], [1, 1, 1]]], "output": 5},
    {"input": [[[1, 0], [0, 1]]], "output": -1},
    {"input": [[[1]]], "output": 1},
    {"input": [[[1, 1, 1, 1]]], "output": 4},
    {"input": [[[1], [1], [1]]], "output": 3},
    {
        "input": [[
            [1, 1, 0, 1, 1],
            [0, 1, 1, 1, 0],
            [1, 1, 0, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ]],
        "output": 9,
    },
    {"input": [[[1, 1, 1], [1, 1, 0], [1, 0, 1]]], "output": -1},
    {
        "input": [[
            [1, 0, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 1],
            [1, 1, 1, 0, 1, 1],
            [0, 0, 0, 0, 1, 0],
            [1, 1, 1, 1, 1, 1],
        ]],
        "output": 16,
    },
]

PERF_LIMIT = 1.0


def perf_case():
    R = C = 300
    maps = [[0 if random.random() < 0.25 else 1 for _ in range(C)] for _ in range(R)]
    maps[0][0] = maps[R - 1][C - 1] = 1
    for c in range(C):          # 맨 윗줄과 맨 오른쪽 열을 뚫어 출구까지 가는 길을 보장
        maps[0][c] = 1
    for r in range(R):
        maps[r][C - 1] = 1
    return {"input": [maps], "output": None}


EXPLANATION = """
핵심: 간선 비용이 모두 1 인 그래프의 최단 거리 → BFS. 큐에서 먼저 나오는 칸일수록 출발점에 가깝습니다.

maps            dist (지난 칸 수)
1 1 1           1 2 3
0 0 1           . . 4
1 1 1           7 6 5    → dist[2][2] = 5
                         (왼쪽 아래 1 들은 출구보다 늦게 방문)

BFS 는 "거리 1 인 칸들 → 거리 2 인 칸들 → ..." 처럼 동심원(레벨)으로 퍼집니다.
그래서 어떤 칸을 처음 방문했을 때의 거리가 곧 최단 거리입니다.

1. dist = R × C 크기의 0 배열 (0 = 미방문), dist[0][0] = 1, queue = deque([(0, 0)])
2. popleft 한 칸이 출구면 dist 반환
3. 상하좌우 이웃 중 범위 안 + 길(1) + 미방문이면 dist = 현재 + 1, append
4. 큐가 비면 -1

시간 O(R · C), 공간 O(R · C)

면접 포인트
- "왜 DFS 가 아니라 BFS 인가?" → DFS 는 처음 찾은 경로가 최단이라는 보장이 없어 모든 경로를 봐야 합니다(brute_force).
  경로 수는 지수적으로 늘어나므로 300 × 300 에서는 끝나지 않습니다.
- 방문 표시를 "꺼낼 때" 하면 같은 칸이 큐에 여러 번 들어가 느려집니다. "넣을 때" 표시하세요.
- 큐로 list 와 pop(0) 을 쓰면 O(n) 이 곱해집니다. deque.popleft() 는 O(1).
- 변형: 벽을 k 번 부술 수 있다면 상태를 (r, c, 부순 횟수) 로 늘린 BFS, 이동 비용이 0/1 이면 0-1 BFS, 비용이 다양하면 다익스트라.
- 프로그래머스 '게임 맵 최단거리', '미로 탈출'(레버를 거쳐 가기 → BFS 두 번), '리코쳇 로봇'(미끄러지는 이동) 이 같은 틀입니다.
"""


def reference(maps):
    from collections import deque

    R, C = len(maps), len(maps[0])
    dist = [[0] * C for _ in range(R)]      # 0 = 아직 방문 안 함
    dist[0][0] = 1
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        if (r, c) == (R - 1, C - 1):
            return dist[r][c]               # BFS 에서 처음 도착한 순간이 최단
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and maps[nr][nc] == 1 and dist[nr][nc] == 0:
                dist[nr][nc] = dist[r][c] + 1   # 넣을 때 방문 표시 + 거리 기록
                queue.append((nr, nc))
    return -1


def brute_force(maps):
    # DFS 로 모든 경로를 탐색 (가지치기를 해도 최악은 지수 시간 → 작은 입력에서만 사용 가능)
    R, C = len(maps), len(maps[0])
    visited = [[False] * C for _ in range(R)]
    best = float("inf")

    def dfs(r, c, length):
        nonlocal best
        if length >= best:
            return                          # 이미 찾은 경로보다 길면 중단
        if (r, c) == (R - 1, C - 1):
            best = length
            return
        for dr, dc in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and maps[nr][nc] == 1 and not visited[nr][nc]:
                visited[nr][nc] = True
                dfs(nr, nc, length + 1)
                visited[nr][nc] = False

    visited[0][0] = True
    dfs(0, 0, 1)
    return best if best != float("inf") else -1
