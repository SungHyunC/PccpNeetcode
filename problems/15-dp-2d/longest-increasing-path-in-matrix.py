TITLE = "Longest Increasing Path in a Matrix (행렬의 최장 증가 경로)"
LEVEL = "Hard"
SOURCE = "LeetCode 329"
PATTERN = "DFS + 메모이제이션 (DAG 위의 DP) / 값 순서 정렬 바텀업"

DESCRIPTION = """
정수로 채워진 rows × cols 행렬 matrix 가 주어집니다.
한 칸에서 상하좌우로 인접한 칸으로 이동할 수 있는데, 반드시 지금보다 '큰' 값으로만 이동할 수 있습니다.
(대각선 이동, 행렬 밖으로 나가기, 같은 값으로의 이동은 불가)
이렇게 만들 수 있는 경로 중 가장 긴 경로에 포함된 칸의 수를 return 하세요.

제한사항
- 1 ≤ rows, cols ≤ 200
- 0 ≤ matrix[i][j] ≤ 2^31 - 1

입출력 예
matrix = [[9, 9, 4],
          [6, 6, 8],
          [2, 1, 1]]  →  4   (1 → 2 → 6 → 9)

matrix = [[3, 4, 5],
          [3, 2, 6],
          [2, 2, 1]]  →  4   (3 → 4 → 5 → 6)
"""

SIGNATURE = "def solution(matrix: list[list[int]]) -> int:"

HINTS = [
    "모든 칸에서 DFS 로 갈 수 있는 경로를 전부 탐색하면 경로 수가 지수적으로 늘어 시간 초과입니다.",
    "'큰 값으로만 이동' 하므로 같은 칸을 두 번 방문하는 사이클이 없습니다(DAG). 그래서 visited 배열이 필요 없고, 칸마다 답이 하나로 정해집니다.",
    "memo[r][c] = (r, c) 에서 시작하는 최장 경로 길이 = 1 + max(memo[이웃]) (이웃 값 > 현재 값). 재귀 + 메모로 각 칸을 한 번만 계산하면 O(rows × cols).",
    "재귀 깊이가 걱정되면: 칸들을 값 내림차순으로 정렬해서 처리하면 이웃(더 큰 값)의 답이 항상 먼저 계산되어 있으므로 반복문으로 같은 DP 를 할 수 있습니다.",
]

TESTS = [
    {"input": [[[9, 9, 4], [6, 6, 8], [2, 1, 1]]], "output": 4},
    {"input": [[[3, 4, 5], [3, 2, 6], [2, 2, 1]]], "output": 4},
    {"input": [[[1]]], "output": 1},
    {"input": [[[7, 7], [7, 7]]], "output": 1},
    {"input": [[[1, 2, 3], [6, 5, 4], [7, 8, 9]]], "output": 9},
    {"input": [[[1, 2]]], "output": 2},
    {"input": [[[0], [1], [5], [5]]], "output": 3},
    {"input": [[[1, 2, 3, 4], [12, 13, 14, 5], [11, 16, 15, 6], [10, 9, 8, 7]]], "output": 16},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    rows = cols = 200
    # 오른쪽·아래로 갈수록 커지는 값 + 약간의 잡음 → 단조 경로가 매우 많아 메모 없는 DFS 는 폭발
    matrix = [[(r + c) * 10 + random.randint(0, 5) for c in range(cols)] for r in range(rows)]
    return {"input": [matrix], "output": None}


EXPLANATION = """
아이디어
- "더 큰 값으로만 이동" → 이동 그래프에 사이클이 없습니다(DAG, 방향 비순환 그래프).
- DAG 에서는 각 칸의 '여기서 시작하는 최장 경로' 가 이웃들의 답만으로 결정되므로 DP 가 됩니다.
- 순수 DFS 는 같은 칸을 수없이 다시 탐색 → 메모이제이션으로 칸마다 한 번만 계산.

DP 레시피
1. 상태 정의: L[r][c] = (r, c) 에서 시작하는 최장 증가 경로의 칸 수
2. 점화식:   L[r][c] = 1 + max(L[nr][nc] for 이웃 (nr, nc) if matrix[nr][nc] > matrix[r][c])  (없으면 1)
3. 초기값:   더 큰 이웃이 없는 칸(지역 최댓값) = 1
4. 계산 순서: 더 큰 값의 칸이 먼저 계산되어야 함
             → 재귀 + 메모(alternative)가 자동으로 맞춰 주거나, 값 내림차순 정렬(reference)
5. 답:       max(L[r][c])

  matrix          L (각 칸에서 시작하는 최장 길이)
  9  9  4         1  1  2
  6  6  8         2  2  1
  2  1  1         3  4  2      ← 1(2,1) → 2 → 6 → 9 : 길이 4

두 가지 구현
- 메모 DFS (alternative): 면접에서 가장 많이 쓰는 형태. 코드가 짧고 직관적.
  단점: 경로가 길면(예: 200×200 뱀 모양 → 깊이 40,000) 파이썬 재귀 한도를 넘거나 스택이 터질 수 있습니다.
- 값 정렬 바텀업 (reference): 모든 칸을 값 내림차순으로 정렬 후 순서대로 L 을 계산.
  더 큰 이웃은 항상 먼저 처리되어 있으므로 재귀가 필요 없습니다. (위상 정렬 순서와 같음)

복잡도
- 메모 DFS: 시간 O(R × C), 공간 O(R × C) (+ 재귀 스택)
- 정렬 바텀업: 시간 O(R × C × log(R × C)), 공간 O(R × C)
- (참고) 진입 차수 기반 위상 정렬(Kahn)로 BFS 레벨 수를 세는 방법도 O(R × C).

면접 포인트
- "왜 visited 가 필요 없는가?" → 값이 엄격하게 증가하므로 같은 칸으로 돌아올 수 없다(DAG).
- 메모 DFS 를 먼저 제시하고, 재귀 깊이 문제와 반복형 대안(정렬/위상 정렬)을 언급하면 Hard 문제 답변으로 충분합니다.
"""


def reference(matrix):
    rows, cols = len(matrix), len(matrix[0])
    L = [[1] * cols for _ in range(rows)]
    # 값이 큰 칸부터 처리 → 더 큰 이웃의 L 값이 항상 먼저 확정됨
    cells = sorted(((matrix[r][c], r, c) for r in range(rows) for c in range(cols)), reverse=True)
    best = 1
    for v, r, c in cells:
        cur = 1
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > v:
                if L[nr][nc] + 1 > cur:
                    cur = L[nr][nc] + 1
        L[r][c] = cur
        if cur > best:
            best = cur
    return best


def alternative(matrix):
    # 메모이제이션 DFS (면접 정석). 경로가 매우 길면 재귀 한도 주의
    import sys
    from functools import lru_cache

    rows, cols = len(matrix), len(matrix[0])
    sys.setrecursionlimit(max(10_000, rows * cols + 100))

    @lru_cache(maxsize=None)
    def dfs(r, c):
        best = 1
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))
        return best

    return max(dfs(r, c) for r in range(rows) for c in range(cols))
