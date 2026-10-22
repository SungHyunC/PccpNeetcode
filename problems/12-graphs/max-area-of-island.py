import random

TITLE = "Max Area of Island (가장 큰 섬의 넓이)"
LEVEL = "Medium"
SOURCE = "LeetCode 695"
PATTERN = "격자 탐색하며 연결 요소의 크기 세기 (반복 DFS)"

DESCRIPTION = """
0(물)과 1(땅)로 이루어진 R × C 격자 grid 가 주어집니다.
상하좌우로 이어진 1 들의 묶음을 섬이라 하고, 섬의 넓이는 그 섬에 속한 칸의 수입니다.
가장 큰 섬의 넓이를 return 하세요. 섬이 하나도 없으면 0 을 return 합니다.

제한사항
- 1 ≤ R, C ≤ 300
- grid[i][j] 는 0 또는 1

입출력 예
grid = [[0, 0, 1, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 1, 0]]   →  4   (왼쪽 위 ㄱ자 섬 4칸, 오른쪽 아래 섬 3칸)

grid = [[0, 0, 0]]          →  0
"""

SIGNATURE = "def solution(grid: list[list[int]]) -> int:"

HINTS = [
    "Number of Islands 에서 '섬 개수' 대신 '섬마다 방문한 칸 수' 를 세면 됩니다.",
    "탐색을 시작할 때 area = 0 으로 두고, 스택/큐에서 칸을 하나 꺼낼 때마다 area += 1 하세요. 탐색이 끝나면 best = max(best, area).",
    "방문한 땅을 0 으로 바꾸면 visited 배열 없이도 풀 수 있습니다 (입력을 바꿔도 되는지 확인). 재귀 대신 리스트를 스택으로 쓰면 깊은 섬에서도 안전합니다.",
]

TESTS = [
    {"input": [[[0, 0, 1, 0, 0], [1, 1, 1, 0, 0], [0, 0, 0, 1, 1], [0, 0, 0, 1, 0]]], "output": 4},
    {"input": [[[0, 0, 0]]], "output": 0},
    {"input": [[[1]]], "output": 1},
    {"input": [[[1, 1], [1, 1]]], "output": 4},
    {"input": [[[1, 0, 1], [0, 1, 0], [1, 0, 1]]], "output": 1},
    {"input": [[[1, 1, 0, 1], [1, 0, 0, 1], [0, 0, 1, 1], [1, 0, 1, 0]]], "output": 5},
    {"input": [[[1], [1], [0], [1]]], "output": 2},
]

PERF_LIMIT = 1.0


def perf_case():
    R = C = 300
    grid = [[1 if random.random() < 0.55 else 0 for _ in range(C)] for _ in range(R)]
    return {"input": [grid], "output": None}


EXPLANATION = """
핵심: 연결 요소(섬)마다 탐색하면서 방문한 칸 수를 센다. 최댓값이 답.

grid                 섬별 넓이
0 0 1 0 0            . . A . .
1 1 1 0 0            A A A . .      A = 4
0 0 0 1 1            . . . B B      B = 3
0 0 0 1 0            . . . B .      → max = 4

1. 모든 칸 (r, c) 순회, 땅이면 탐색 시작: grid[r][c] = 0 (방문 표시), stack = [(r, c)], area = 0
2. stack 에서 pop 할 때마다 area += 1, 이웃 중 땅이면 0 으로 바꾸고 push
3. best = max(best, area)

시간 O(R · C), 공간 O(R · C) (스택 최악)

면접 포인트
- 반복 DFS(스택)와 BFS(큐)는 방문 순서만 다를 뿐 연결 요소 크기를 구하는 데는 둘 다 정답입니다.
  리스트의 pop() 은 O(1), pop(0) 은 O(n) 이므로 BFS 는 반드시 deque.popleft() 를 쓰세요.
- 입력을 수정하는 풀이(제자리 방문 표시)는 공간을 아끼지만, 면접에서는 "입력을 바꿔도 되나요?" 라고 먼저 묻는 습관을 보이세요.
- 응용: 프로그래머스 '석유 시추'(PCCP 기출 유형)는 섬마다 넓이를 구한 뒤 열 단위로 합산하는 문제입니다.
"""


def reference(grid):
    R, C = len(grid), len(grid[0])
    best = 0
    for sr in range(R):
        for sc in range(C):
            if grid[sr][sc] != 1:
                continue
            grid[sr][sc] = 0                    # 제자리 방문 표시
            stack = [(sr, sc)]
            area = 0
            while stack:
                r, c = stack.pop()
                area += 1
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                        grid[nr][nc] = 0        # 넣을 때 표시 → 중복 push 방지
                        stack.append((nr, nc))
            best = max(best, area)
    return best


def alternative(grid):
    # BFS + 별도 visited 배열 (입력을 바꾸지 않는 버전)
    from collections import deque

    R, C = len(grid), len(grid[0])
    visited = [[False] * C for _ in range(R)]
    best = 0
    for sr in range(R):
        for sc in range(C):
            if grid[sr][sc] != 1 or visited[sr][sc]:
                continue
            visited[sr][sc] = True
            queue = deque([(sr, sc)])
            area = 0
            while queue:
                r, c = queue.popleft()
                area += 1
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1 and not visited[nr][nc]:
                        visited[nr][nc] = True
                        queue.append((nr, nc))
            best = max(best, area)
    return best
