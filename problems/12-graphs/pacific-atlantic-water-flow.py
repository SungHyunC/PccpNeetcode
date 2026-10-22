import random

TITLE = "Pacific Atlantic Water Flow (태평양 대서양 물 흐름)"
LEVEL = "Medium"
SOURCE = "LeetCode 417"
PATTERN = "거꾸로 생각하기: 바다에서 거슬러 올라가는 BFS 두 번"

DESCRIPTION = """
R × C 크기의 섬 지형이 높이 배열 heights 로 주어집니다.
섬의 위쪽과 왼쪽 가장자리는 태평양(Pacific), 아래쪽과 오른쪽 가장자리는 대서양(Atlantic)에 맞닿아 있습니다.

비가 오면 물은 어떤 칸에서 상하좌우 이웃 칸 중 높이가 같거나 더 낮은 칸으로 흐를 수 있습니다.
가장자리 칸의 물은 맞닿은 바다로 바로 흘러 나갈 수 있습니다.

물이 태평양과 대서양 양쪽 모두로 흘러갈 수 있는 칸의 좌표 [r, c] 를 모두 return 하세요. 순서는 상관없습니다.

제한사항
- 1 ≤ R, C ≤ 200
- 0 ≤ heights[r][c] ≤ 100,000

입출력 예
heights = [[1, 2],
           [3, 4]]   →  [[0, 1], [1, 0], [1, 1]]
(0,0) 은 태평양 쪽 가장자리지만, 이웃이 모두 더 높아서 대서양으로 갈 수 없습니다.

heights = [[3, 3, 3],
           [3, 1, 3],
           [3, 3, 3]]  →  가운데 (1,1) 을 제외한 8 칸
"""

SIGNATURE = "def solution(heights: list[list[int]]) -> list[list[int]]:"

HINTS = [
    "칸마다 '여기서 출발한 물이 양쪽 바다에 닿는가?' 를 BFS 로 확인하면 칸 R·C 개 × BFS O(R·C) = O((R·C)^2) 입니다.",
    "방향을 뒤집어 보세요. '바다에 닿을 수 있는 칸' = 바다에서 출발해 높이가 같거나 '높아지는' 방향으로 거슬러 올라가며 도달할 수 있는 칸입니다.",
    "태평양 가장자리 칸 전부를 시작점으로 하는 다중 시작점 BFS 한 번, 대서양 가장자리 칸 전부로 한 번. 두 방문 집합의 교집합이 답입니다.",
]

COMPARE = "unordered"

TESTS = [
    {"input": [[[1, 2], [3, 4]]], "output": [[0, 1], [1, 0], [1, 1]]},
    {
        "input": [[[3, 3, 3], [3, 1, 3], [3, 3, 3]]],
        "output": [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]],
    },
    {"input": [[[7]]], "output": [[0, 0]]},
    {"input": [[[1, 2, 3]]], "output": [[0, 0], [0, 1], [0, 2]]},
    {"input": [[[2, 1], [1, 2]]], "output": [[0, 0], [0, 1], [1, 0], [1, 1]]},
    {
        "input": [[[1, 2, 3], [8, 9, 4], [7, 6, 5]]],
        "output": [[0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]],
    },
    {
        "input": [[[1, 2, 2, 3], [3, 2, 3, 4], [2, 4, 5, 3], [6, 7, 1, 4]]],
        "output": [[0, 3], [1, 3], [2, 2], [3, 0], [3, 1]],
    },
]

PERF_LIMIT = 1.0


def perf_case():
    # 가운데가 높은 피라미드 지형(+ 약간의 요철): 물이 넓게 퍼지므로
    # 칸마다 BFS 를 돌리는 풀이는 매번 격자 대부분을 탐색하게 됩니다.
    R = C = 200
    heights = [[2 * min(r, c, R - 1 - r, C - 1 - c) + random.randint(0, 1) for c in range(C)] for r in range(R)]
    return {"input": [heights], "output": None}


EXPLANATION = """
핵심: "각 칸에서 바다로 내려갈 수 있나?" 를 칸마다 묻는 대신,
"바다에서 거꾸로 올라가면 어디까지 갈 수 있나?" 를 바다마다 한 번씩만 묻습니다.

거꾸로 이동 규칙: (r, c) → 이웃 (nr, nc) 는 heights[nr][nc] >= heights[r][c] 일 때 가능

heights        Pacific 도달(P)   Atlantic 도달(A)   교집합
1 2 3          P P P             . . A              . . ✔
8 9 4          P P P             A A A              ✔ ✔ ✔
7 6 5          P P P             A A A              ✔ ✔ ✔
(나선형 지형이라 태평양은 1→2→3→4→... 순서로 거슬러 올라가 전체에 닿음)

1. pac = 위쪽 행 + 왼쪽 열 칸들, atl = 아래쪽 행 + 오른쪽 열 칸들 을 각각 시작점으로
2. 각각 다중 시작점 BFS: 이웃이 더 높거나 같고 미방문이면 방문
3. 두 방문 집합에 모두 있는 칸을 반환

시간 O(R · C) — BFS 두 번
공간 O(R · C)

면접 포인트
- "역방향 탐색(reverse search)" 은 목표가 소수이고 출발 후보가 많을 때의 표준 기법입니다.
  (예: 모든 칸 → 출구 거리 = 출구에서 한 번 BFS)
- 높이가 같은 칸끼리도 흐를 수 있다는 조건(>=)을 놓치지 마세요.
- brute_force 는 칸마다 BFS 를 돌리는 O((R·C)^2) 풀이로, 정답이지만 효율성 테스트에서 시간 초과입니다.
"""


def reference(heights):
    from collections import deque

    R, C = len(heights), len(heights[0])

    def bfs(starts):
        seen = set(starts)
        queue = deque(starts)
        while queue:
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if (0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen
                        and heights[nr][nc] >= heights[r][c]):     # 거꾸로: 같거나 높은 곳으로
                    seen.add((nr, nc))
                    queue.append((nr, nc))
        return seen

    pacific = bfs([(0, c) for c in range(C)] + [(r, 0) for r in range(1, R)])
    atlantic = bfs([(R - 1, c) for c in range(C)] + [(r, C - 1) for r in range(R - 1)])
    return [[r, c] for r, c in sorted(pacific & atlantic)]


def brute_force(heights):
    # 칸마다 물이 흘러갈 수 있는 곳을 BFS 로 확인: O((R·C)^2)
    from collections import deque

    R, C = len(heights), len(heights[0])
    result = []
    for sr in range(R):
        for sc in range(C):
            seen = {(sr, sc)}
            queue = deque([(sr, sc)])
            pac = atl = False
            while queue and not (pac and atl):
                r, c = queue.popleft()
                if r == 0 or c == 0:
                    pac = True
                if r == R - 1 or c == C - 1:
                    atl = True
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if (0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen
                            and heights[nr][nc] <= heights[r][c]):
                        seen.add((nr, nc))
                        queue.append((nr, nc))
            if pac and atl:
                result.append([sr, sc])
    return result
