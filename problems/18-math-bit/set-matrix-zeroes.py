TITLE = "Set Matrix Zeroes (0 이 있는 행과 열 지우기)"
LEVEL = "Medium"
SOURCE = "LeetCode 73"
PATTERN = "표시 먼저, 수정은 나중에 / 첫 행·첫 열을 표시용으로 재사용"

DESCRIPTION = """
m × n 정수 행렬 matrix 가 주어집니다. 원래 행렬에서 값이 0 인 칸이 있으면,
그 칸이 속한 행 전체와 열 전체를 0 으로 바꿉니다. 모든 0 에 대해 이 작업을 한 뒤의 행렬을 return 하세요.

주의: '원래' 0 이었던 칸만 기준입니다. 작업 중에 새로 0 이 된 칸 때문에 다시 행/열을 지우면 안 됩니다.
(원래 LeetCode 문제는 제자리 수정입니다. 추가 공간 O(1) 에도 도전해 보세요.)

제한사항
- 1 ≤ m, n ≤ 200
- -2^31 ≤ matrix[i][j] ≤ 2^31 - 1

입출력 예
matrix = [[1, 1, 1],
          [1, 0, 1],
          [1, 1, 1]]          →  [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

matrix = [[0, 1, 2, 0],
          [3, 4, 5, 2],
          [1, 3, 1, 5]]       →  [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]
"""

SIGNATURE = "def solution(matrix: list[list[int]]) -> list[list[int]]:"

HINTS = [
    "0 을 발견하는 즉시 행/열을 지우면, 새로 생긴 0 때문에 모든 칸이 0 이 될 수 있습니다. '표시' 와 '수정' 을 분리하세요.",
    "1단계로 0 이 있는 행 번호, 열 번호를 set 에 모으고, 2단계로 해당 칸을 0 으로 바꾸면 O(m + n) 공간입니다.",
    "O(1) 공간: 첫 행과 첫 열을 표시판으로 씁니다. matrix[i][0] = 0 은 'i 행 지움', matrix[0][j] = 0 은 'j 열 지움'. 단, 첫 행/첫 열 자체에 원래 0 이 있었는지는 변수 두 개로 따로 기억해야 합니다.",
]

TESTS = [
    {"input": [[[1, 1, 1], [1, 0, 1], [1, 1, 1]]], "output": [[1, 0, 1], [0, 0, 0], [1, 0, 1]]},
    {"input": [[[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]], "output": [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]},
    {"input": [[[5]]], "output": [[5]]},
    {"input": [[[0]]], "output": [[0]]},
    {"input": [[[1, 0, 3]]], "output": [[0, 0, 0]]},
    {"input": [[[1], [0], [3]]], "output": [[0], [0], [0]]},
    {"input": [[[1, 2], [3, 4]]], "output": [[1, 2], [3, 4]]},
    {"input": [[[1, 2, 3], [4, 5, 6], [7, 8, 0]]], "output": [[1, 2, 0], [4, 5, 0], [0, 0, 0]]},
    {"input": [[[-1, 2, 3], [4, 0, -6], [7, 8, 9], [0, 1, 1]]], "output": [[0, 0, 3], [0, 0, 0], [0, 0, 9], [0, 0, 0]]},
]

EXPLANATION = """
핵심: '어디를 지울지 표시' 와 '실제로 지우기' 를 두 번의 순회로 분리합니다.

[O(m + n) 공간] zero_rows, zero_cols 집합에 기록 → 다시 돌며 r in zero_rows or c in zero_cols 이면 0

[O(1) 공간] 첫 행·첫 열을 표시판으로 재사용
  1. first_row_zero = 첫 행에 0 이 있었나?, first_col_zero = 첫 열에 0 이 있었나?
  2. 나머지 칸 (1.., 1..) 에서 matrix[i][j] == 0 이면 matrix[i][0] = 0, matrix[0][j] = 0
  3. 나머지 칸 (1.., 1..) 을 matrix[i][0] == 0 or matrix[0][j] == 0 이면 0 으로
  4. first_row_zero 면 첫 행 전체 0, first_col_zero 면 첫 열 전체 0 (반드시 마지막에!)

  원본            표시 후(첫 행/열)     결과
  0 1 2 0         0 1 2 0               0 0 0 0
  3 4 5 2   →     3 4 5 2        →      0 4 5 0
  1 3 1 5         1 3 1 5               0 3 1 0
  (첫 행에 원래 0 이 있음 → 4단계에서 첫 행 전체 0, 열 0·3 은 첫 행 표시로 지움)

시간 O(m·n), 공간 O(1)
면접 포인트: O(mn) 복사 → O(m+n) 집합 → O(1) 첫 행/열 재사용 순서로 개선을 설명하세요.
첫 행/열을 먼저 지워 버리면 표시 정보가 사라지는 함정이 있습니다.
"""


def reference(matrix):
    rows, cols = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][c] == 0 for c in range(cols))
    first_col_zero = any(matrix[r][0] == 0 for r in range(rows))
    # 1) 나머지 영역의 0 을 첫 행/첫 열에 표시
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][c] == 0:
                matrix[r][0] = 0
                matrix[0][c] = 0
    # 2) 표시를 보고 나머지 영역을 0 으로
    for r in range(1, rows):
        for c in range(1, cols):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
    # 3) 첫 행/첫 열은 마지막에 처리 (표시판이므로)
    if first_row_zero:
        for c in range(cols):
            matrix[0][c] = 0
    if first_col_zero:
        for r in range(rows):
            matrix[r][0] = 0
    return matrix


def alternative(matrix):
    zero_rows, zero_cols = set(), set()
    for r, row in enumerate(matrix):
        for c, v in enumerate(row):
            if v == 0:
                zero_rows.add(r)
                zero_cols.add(c)
    return [
        [0 if r in zero_rows or c in zero_cols else v for c, v in enumerate(row)]
        for r, row in enumerate(matrix)
    ]
