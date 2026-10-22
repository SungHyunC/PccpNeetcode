TITLE = "Rotate Image (행렬 90도 회전)"
LEVEL = "Medium"
SOURCE = "LeetCode 48"
PATTERN = "전치(transpose) + 각 행 뒤집기 / zip(*m[::-1])"

DESCRIPTION = """
n × n 정수 행렬 matrix 가 주어집니다. 행렬을 시계 방향으로 90도 회전한 결과를 return 하세요.
(원래 LeetCode 문제는 제자리(in-place) 수정이지만, 여기서는 회전된 행렬을 return 합니다.
면접처럼 추가 행렬 없이 제자리에서 바꾼 뒤 그 행렬을 return 해 보는 것을 권장합니다.)

제한사항
- 1 ≤ n ≤ 20
- -1,000 ≤ matrix[i][j] ≤ 1,000

입출력 예
matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]
→ [[7, 4, 1],
   [8, 5, 2],
   [9, 6, 3]]
"""

SIGNATURE = "def solution(matrix: list[list[int]]) -> list[list[int]]:"

HINTS = [
    "새 행렬을 만든다면: 원래 (r, c) 칸은 회전 후 (c, n - 1 - r) 로 갑니다.",
    "제자리 회전 = 두 단계로 분해: 주대각선 기준 전치(transpose: m[i][j] ↔ m[j][i]) 후 각 행을 좌우로 뒤집기.",
    "파이썬 한 줄: [list(row) for row in zip(*matrix[::-1])] — 위아래를 뒤집은 뒤 열을 행으로 읽습니다.",
]

TESTS = [
    {"input": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], "output": [[7, 4, 1], [8, 5, 2], [9, 6, 3]]},
    {"input": [[[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]],
     "output": [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]},
    {"input": [[[42]]], "output": [[42]]},
    {"input": [[[1, 2], [3, 4]]], "output": [[3, 1], [4, 2]]},
    {"input": [[[-1, 0], [0, -1]]], "output": [[0, -1], [-1, 0]]},
    {"input": [[[1, 1, 1], [0, 0, 0], [0, 0, 0]]], "output": [[0, 0, 1], [0, 0, 1], [0, 0, 1]]},
]

EXPLANATION = """
핵심: 90도 시계 회전 = 전치(transpose) + 좌우 반전. 둘 다 제자리 swap 으로 가능합니다.

  원본          전치(i,j ↔ j,i)    행마다 뒤집기
  1 2 3         1 4 7              7 4 1
  4 5 6   →     2 5 8       →      8 5 2
  7 8 9         3 6 9              9 6 3

좌표 공식: (r, c) → (c, n - 1 - r)

1. i < j 인 칸만 m[i][j], m[j][i] = m[j][i], m[i][j] (대각선 아래위를 한 번씩만 교환)
2. 각 행 row.reverse()

다른 회전도 같은 방식으로:
- 반시계 90도: 전치 + 위아래 반전  ↔ [list(r) for r in zip(*m)][::-1]
- 180도: 위아래 반전 + 각 행 반전  ↔ [row[::-1] for row in m[::-1]]
- 시계 90도 한 줄: [list(r) for r in zip(*m[::-1])]

시간 O(n^2), 공간 O(1) (제자리)
실전 포인트: PCCP/카카오 '자물쇠와 열쇠' 처럼 회전을 4번 시도하는 문제에서 zip(*m[::-1]) 한 줄이 시간을 크게 아껴 줍니다.
직사각형(rows ≠ cols) 행렬은 회전 후 크기가 cols × rows 가 되므로 제자리 방법을 쓸 수 없고 zip 방식이 안전합니다.
"""


def reference(matrix):
    n = len(matrix)
    # 1) 전치: 대각선 기준 대칭 교환
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # 2) 각 행 좌우 반전
    for row in matrix:
        row.reverse()
    return matrix


def alternative(matrix):
    # 위아래를 뒤집고(m[::-1]) 열을 행으로 읽기(zip(*...))
    return [list(row) for row in zip(*matrix[::-1])]


def brute_force(matrix):
    n = len(matrix)
    result = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            result[c][n - 1 - r] = matrix[r][c]  # (r, c) → (c, n-1-r)
    return result
