TITLE = "Spiral Matrix (나선형 순회)"
LEVEL = "Medium"
SOURCE = "LeetCode 54"
PATTERN = "네 경계(top/bottom/left/right) 좁히기 / 방향 전환 시뮬레이션"

DESCRIPTION = """
m × n 정수 행렬 matrix 가 주어집니다. 왼쪽 위에서 시작해 시계 방향 나선 모양으로
모든 원소를 방문한 순서대로 담은 리스트를 return 하세요.

제한사항
- 1 ≤ m, n ≤ 10
- -100 ≤ matrix[i][j] ≤ 100

입출력 예
matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]                       →  [1, 2, 3, 6, 9, 8, 7, 4, 5]

matrix = [[1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12]]                 →  [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
"""

SIGNATURE = "def solution(matrix: list[list[int]]) -> list[int]:"

HINTS = [
    "아직 방문하지 않은 영역은 항상 직사각형입니다. 그 경계를 top, bottom, left, right 네 변수로 관리해 보세요.",
    "한 바퀴: 위쪽 행(왼→오) 후 top += 1, 오른쪽 열(위→아래) 후 right -= 1, 아래쪽 행(오→왼) 후 bottom -= 1, 왼쪽 열(아래→위) 후 left += 1.",
    "한 줄짜리(1×n, m×1) 가 남았을 때 같은 칸을 두 번 넣지 않도록, 아래 행/왼쪽 열을 돌기 전에 top ≤ bottom, left ≤ right 를 다시 확인하세요.",
    "다른 방법: 방향 벡터 dr/dc 를 두고 '범위를 벗어나거나 이미 방문한 칸' 이면 시계 방향으로 회전하는 시뮬레이션.",
]

TESTS = [
    {"input": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], "output": [1, 2, 3, 6, 9, 8, 7, 4, 5]},
    {"input": [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]], "output": [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]},
    {"input": [[[7]]], "output": [7]},
    {"input": [[[1, 2, 3, 4]]], "output": [1, 2, 3, 4]},
    {"input": [[[1], [2], [3]]], "output": [1, 2, 3]},
    {"input": [[[1, 2], [3, 4]]], "output": [1, 2, 4, 3]},
    {"input": [[[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]], "output": [1, 2, 3, 6, 9, 12, 11, 10, 7, 4, 5, 8]},
    {"input": [[[-1, -2], [-3, -4], [-5, -6]]], "output": [-1, -2, -4, -6, -5, -3]},
]

EXPLANATION = """
핵심: 남은 영역의 네 경계를 좁혀 가며 바깥 테두리부터 한 겹씩 벗깁니다.

  top=0   → 1  2  3  4
            5  6  7  8   ← right=3
  bottom=2→ 9 10 11 12
            ↑ left=0

  1) top 행:    1 2 3 4        top=1
  2) right 열:  8 12           right=2
  3) bottom 행: 11 10 9        bottom=1   (top ≤ bottom 확인)
  4) left 열:   5              left=1     (left ≤ right 확인)
  다음 바퀴: top 행(1행, 1~2열): 6 7 ...

시간 O(m·n), 공간 O(1) (결과 제외)
실전 포인트:
- 3, 4 단계 전에 경계를 다시 확인하지 않으면 1×n, m×1 에서 중복이 생깁니다. 가장 흔한 버그입니다.
- 방향 벡터 방식(dr = [0, 1, 0, -1], dc = [1, 0, -1, 0], d = (d + 1) % 4)은 PCCP 시뮬레이션 문제의 기본기입니다.
  '삼각 달팽이', 'Spiral Matrix II(번호 채우기)' 에 그대로 응용됩니다.
"""


def reference(matrix):
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):  # 위쪽 행: 왼 → 오
            result.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):  # 오른쪽 열: 위 → 아래
            result.append(matrix[r][right])
        right -= 1
        if top <= bottom:  # 남은 행이 있을 때만
            for c in range(right, left - 1, -1):  # 아래쪽 행: 오 → 왼
                result.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:  # 남은 열이 있을 때만
            for r in range(bottom, top - 1, -1):  # 왼쪽 열: 아래 → 위
                result.append(matrix[r][left])
            left += 1
    return result


def alternative(matrix):
    # 방향 벡터 시뮬레이션: 막히면 시계 방향으로 회전
    rows, cols = len(matrix), len(matrix[0])
    dr, dc = [0, 1, 0, -1], [1, 0, -1, 0]  # 오, 아래, 왼, 위
    visited = [[False] * cols for _ in range(rows)]
    r = c = d = 0
    result = []
    for _ in range(rows * cols):
        result.append(matrix[r][c])
        visited[r][c] = True
        nr, nc = r + dr[d], c + dc[d]
        if not (0 <= nr < rows and 0 <= nc < cols) or visited[nr][nc]:
            d = (d + 1) % 4  # 시계 방향 회전
            nr, nc = r + dr[d], c + dc[d]
        r, c = nr, nc
    return result


def brute_force(matrix):
    # 파이썬 트릭: 첫 행을 떼어 내고, 남은 행렬을 반시계로 회전하기를 반복
    m = [list(row) for row in matrix]
    result = []
    while m:
        result += m.pop(0)
        m = [list(row) for row in zip(*m)][::-1]  # 반시계 90도 회전
    return result
