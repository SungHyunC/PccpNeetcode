TITLE = "Rotting Oranges (썩어 가는 오렌지)"
LEVEL = "Medium"
SOURCE = "LeetCode 994 · 백준 7576 '토마토' 유형"
PATTERN = "다중 시작점 BFS (multi-source BFS)"

DESCRIPTION = """
R × C 격자의 각 칸에는 다음 중 하나가 있습니다.
- 0: 빈 칸
- 1: 싱싱한 오렌지
- 2: 썩은 오렌지

1분이 지날 때마다, 썩은 오렌지와 상하좌우로 맞닿은 싱싱한 오렌지가 모두 동시에 썩습니다.
모든 오렌지가 썩을 때까지 걸리는 최소 시간(분)을 return 하세요.
끝까지 썩지 않는 오렌지가 남는다면 -1 을 return 합니다. 처음부터 싱싱한 오렌지가 없으면 0 입니다.

제한사항
- 1 ≤ R, C ≤ 300
- grid[i][j] 는 0, 1, 2 중 하나

입출력 예
grid = [[2, 1, 1],
        [1, 1, 0],
        [0, 1, 1]]   →  4

grid = [[2, 1, 1],
        [0, 1, 1],
        [1, 0, 1]]   →  -1   (왼쪽 아래 오렌지는 빈 칸에 둘러싸여 썩지 않음)

grid = [[0, 2]]      →  0
"""

SIGNATURE = "def solution(grid: list[list[int]]) -> int:"

HINTS = [
    "매 분마다 격자 전체를 훑어 새로 썩을 칸을 찾으면 최악에 (R·C) 분 × (R·C) 칸 = O((R·C)^2) 입니다. 너무 느립니다.",
    "썩는 과정은 썩은 오렌지들에서 '동시에' 퍼져 나가는 BFS 와 같습니다. 처음 썩은 오렌지를 전부 큐에 넣고 시작하세요 (다중 시작점 BFS).",
    "큐를 레벨 단위로 처리하거나(for _ in range(len(queue))), 칸마다 썩은 시각 time[r][c] 를 기록하세요. 싱싱한 오렌지 개수 fresh 를 세어 두고 썩힐 때마다 1 씩 줄이면, 마지막에 fresh > 0 인지로 -1 을 판단할 수 있습니다.",
]

TESTS = [
    {"input": [[[2, 1, 1], [1, 1, 0], [0, 1, 1]]], "output": 4},
    {"input": [[[2, 1, 1], [0, 1, 1], [1, 0, 1]]], "output": -1},
    {"input": [[[0, 2]]], "output": 0},
    {"input": [[[0]]], "output": 0},
    {"input": [[[1]]], "output": -1},
    {"input": [[[2, 1, 1, 1, 2]]], "output": 2},
    {"input": [[[1, 1, 1], [1, 2, 1], [1, 1, 1]]], "output": 2},
    {"input": [[[2, 2], [1, 1], [0, 0], [2, 0]]], "output": 1},
    {"input": [[[2, 0, 1]]], "output": -1},
]

PERF_LIMIT = 1.0


def perf_case():
    # 싱싱한 오렌지로 가득 찬 300 x 300 격자, 썩은 오렌지는 왼쪽 위 하나 → 598 분
    R = C = 300
    grid = [[1] * C for _ in range(R)]
    grid[0][0] = 2
    return {"input": [grid], "output": 598}


EXPLANATION = """
핵심: 처음 썩은 오렌지 "전부" 를 큐에 넣고 BFS → 모든 시작점에서 동시에 퍼지는 것과 같습니다.
BFS 레벨(거리) = 경과 시간(분).

grid             0분           1분           2분           3분           4분
2 1 1            2 1 1         2 2 1         2 2 2         2 2 2         2 2 2
1 1 0     →      1 1 0    →    2 1 0    →    2 2 0    →    2 2 0    →    2 2 0
0 1 1            0 1 1         0 1 1         0 1 1         0 2 1         0 2 2

1. 썩은 칸은 모두 큐에, 싱싱한 칸은 개수 fresh 로 센다
2. minutes = 0. 큐가 비어 있지 않고 fresh > 0 인 동안:
   현재 큐 크기만큼(한 레벨) 꺼내며 이웃의 싱싱한 오렌지를 2 로 바꾸고 큐에 넣고 fresh -= 1
   한 레벨이 끝나면 minutes += 1
3. fresh == 0 이면 minutes, 아니면 -1

시간 O(R · C) — 각 칸은 큐에 최대 한 번
공간 O(R · C)

면접 포인트
- 시작점이 여러 개인 BFS 는 "가상의 출발점 하나가 모든 시작점과 거리 0 으로 연결" 된 것과 같다고 설명하세요.
- 시작점마다 BFS 를 따로 돌리면 O(k · R · C) 로 느려집니다.
- 'fresh > 0' 조건을 while 에 넣지 않으면, 마지막 레벨 이후에도 minutes 가 1 더 늘어나는 off-by-one 실수가 나기 쉽습니다.
- 같은 패턴: 백준 7576 '토마토', 4179 '불!'(불이 번지는 미로), LeetCode 286 Walls and Gates, 542 01 Matrix.
"""


def reference(grid):
    from collections import deque

    R, C = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 2:
                queue.append((r, c))            # 모든 시작점을 한꺼번에
            elif grid[r][c] == 1:
                fresh += 1

    minutes = 0
    while queue and fresh > 0:
        for _ in range(len(queue)):             # 한 레벨 = 1분
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                    grid[nr][nc] = 2            # 넣을 때 썩힘(방문 표시)
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1

    return minutes if fresh == 0 else -1


def brute_force(grid):
    # 매 분 격자 전체를 시뮬레이션: O((R·C)^2) → 큰 입력에서 시간 초과
    R, C = len(grid), len(grid[0])
    minutes = 0
    while True:
        to_rot = []
        for r in range(R):
            for c in range(C):
                if grid[r][c] == 1:
                    for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                        if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 2:
                            to_rot.append((r, c))
                            break
        if not to_rot:
            break
        for r, c in to_rot:
            grid[r][c] = 2
        minutes += 1
    if any(1 in row for row in grid):
        return -1
    return minutes
