import random

TITLE = "Number of Islands (섬의 개수)"
LEVEL = "Medium"
SOURCE = "LeetCode 200"
PATTERN = "격자 BFS/DFS 로 연결 요소(connected component) 세기"

DESCRIPTION = """
지도 grid 가 문자열 리스트로 주어집니다. '1' 은 땅, '0' 은 물입니다.
상하좌우로 이어진 땅들은 하나의 섬입니다. (대각선은 이어진 것으로 보지 않습니다)
지도 바깥은 모두 물이라고 할 때, 섬의 개수를 return 하세요.

제한사항
- 1 ≤ len(grid) ≤ 300, 1 ≤ len(grid[i]) ≤ 300
- 모든 행의 길이는 같습니다.
- grid[i][j] 는 '0' 또는 '1' 입니다.

입출력 예
grid = ["11000",
        "11000",
        "00100",
        "00011"]   →  3

grid = ["101",
        "010",
        "101"]     →  5   (대각선은 연결되지 않음)
"""

SIGNATURE = "def solution(grid: list[str]) -> int:"

HINTS = [
    "격자의 각 칸을 정점, 상하좌우로 맞닿은 땅끼리를 간선으로 보면 '연결 요소의 개수' 를 세는 문제입니다.",
    "모든 칸을 차례로 보다가 아직 방문하지 않은 땅을 만나면 섬 개수를 1 늘리고, 그 칸과 이어진 땅을 BFS(또는 DFS)로 전부 방문 처리하세요.",
    "grid 의 행이 문자열이라 직접 수정할 수 없습니다. visited = [[False] * C for _ in range(R)] 를 따로 두고, 큐에 넣는 순간 visited 를 True 로 바꾸세요.",
    "재귀 DFS 는 300 × 300 이 전부 땅이면 깊이가 90,000 까지 갈 수 있어 RecursionError 가 납니다. collections.deque 로 BFS 를 하거나 리스트로 스택을 직접 관리하세요.",
]

TESTS = [
    {"input": [["11000", "11000", "00100", "00011"]], "output": 3},
    {"input": [["11110", "11010", "11000", "00000"]], "output": 1},
    {"input": [["101", "010", "101"]], "output": 5},
    {"input": [["0"]], "output": 0},
    {"input": [["1"]], "output": 1},
    {"input": [["111", "101", "111"]], "output": 1},
    {"input": [["1", "0", "1", "1"]], "output": 2},
    {"input": [["10101"]], "output": 3},
    {"input": [["000", "000"]], "output": 0},
]

PERF_LIMIT = 1.0


def perf_case():
    # 300 x 300 무작위 지도 + 왼쪽 위에 거대한 뱀 모양 섬 (재귀 DFS 라면 깊이가 매우 깊어짐)
    R = C = 300
    grid = [["1" if random.random() < 0.45 else "0" for _ in range(C)] for _ in range(R)]
    for r in range(0, 120):
        for c in range(C):
            grid[r][c] = "1" if r % 4 != 1 and r % 4 != 3 else "0"
        grid[r][C - 1 if r % 4 == 1 else 0] = "1"
    return {"input": [["".join(row) for row in grid]], "output": None}


EXPLANATION = """
핵심: 땅 칸 하나에서 BFS/DFS 를 시작하면 그 섬 전체가 방문 처리됩니다. "새 탐색을 시작한 횟수" = 섬의 개수.

grid            방문 순서 (BFS 시작점마다 섬 번호)
1 1 0 0 0       1 1 . . .
1 1 0 0 0       1 1 . . .
0 0 1 0 0       . . 2 . .
0 0 0 1 1       . . . 3 3     → 3

1. visited 2차원 배열 준비
2. 모든 (r, c) 순회: 땅이고 미방문이면 count += 1, BFS 시작
3. BFS: deque 에 시작점을 넣으며 visited 표시 → popleft → 상하좌우 이웃 중
   범위 안 + 땅 + 미방문이면 visited 표시 후 append

시간 O(R · C) — 모든 칸을 한 번씩 큐에 넣고 꺼냄
공간 O(R · C) — visited (+ 큐는 최악 O(min(R, C)) 정도)

면접 포인트
- visited 표시 시점: 큐에 "넣을 때" 표시해야 같은 칸이 여러 번 들어가지 않습니다. (꺼낼 때 표시하면 중복 삽입)
- 재귀 DFS(alternative)는 코드가 짧지만 파이썬 기본 재귀 한도가 1000 입니다.
  sys.setrecursionlimit(10**6) 을 쓰더라도 너무 깊으면 C 스택이 넘쳐 프로그램이 죽을 수 있습니다.
  효율성 테스트에는 지그재그 모양의 긴 섬이 들어 있습니다.
- grid 를 수정해도 된다면 방문한 땅을 '0' 으로 바꾸는 방식으로 visited 없이 풀 수 있습니다 (면접관에게 입력 수정 가능 여부를 물어보세요).
- Union-Find 로도 풀 수 있습니다 (땅끼리 union 후 루트 개수). 섬이 계속 추가되는 Number of Islands II 에서 유용합니다.
"""


def reference(grid):
    from collections import deque

    R, C = len(grid), len(grid[0])
    visited = [[False] * C for _ in range(R)]
    count = 0

    for sr in range(R):
        for sc in range(C):
            if grid[sr][sc] != "1" or visited[sr][sc]:
                continue
            count += 1                              # 새 섬 발견
            visited[sr][sc] = True
            queue = deque([(sr, sc)])
            while queue:
                r, c = queue.popleft()
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == "1" and not visited[nr][nc]:
                        visited[nr][nc] = True      # 큐에 넣을 때 방문 표시
                        queue.append((nr, nc))
    return count


def alternative(grid):
    # 재귀 DFS 버전: 짧지만 깊은 재귀에 주의 (setrecursionlimit 필수)
    import sys

    sys.setrecursionlimit(10**6)
    R, C = len(grid), len(grid[0])
    visited = [[False] * C for _ in range(R)]

    def dfs(r, c):
        if not (0 <= r < R and 0 <= c < C) or grid[r][c] != "1" or visited[r][c]:
            return
        visited[r][c] = True
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == "1" and not visited[r][c]:
                dfs(r, c)
                count += 1
    return count
