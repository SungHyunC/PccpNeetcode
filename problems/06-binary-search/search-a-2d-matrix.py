TITLE = "Search a 2D Matrix (2차원 행렬 탐색)"
LEVEL = "Medium"
SOURCE = "LeetCode 74"
PATTERN = "2차원 행렬을 길이 m·n 인 1차원 정렬 배열로 보고 이분 탐색"

DESCRIPTION = """
m × n 정수 행렬 matrix 와 정수 target 이 주어집니다. matrix 는 다음 성질을 가집니다.
- 각 행은 왼쪽에서 오른쪽으로 오름차순(같은 값 없음) 정렬되어 있습니다.
- 각 행의 첫 번째 값은 바로 윗 행의 마지막 값보다 큽니다.
target 이 matrix 안에 있으면 True, 없으면 False 를 return 하세요. O(log(m·n)) 을 목표로 하세요.

제한사항
- 1 ≤ m, n ≤ 100
- -10^4 ≤ matrix[i][j], target ≤ 10^4

입출력 예
matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], target = 3   →  True
matrix = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], target = 13  →  False
"""

SIGNATURE = "def solution(matrix: list[list[int]], target: int) -> bool:"

HINTS = [
    "행을 순서대로 이어 붙이면 어떤 배열이 될까요? 성질 두 개를 합치면 전체가 하나의 정렬된 배열입니다.",
    "1차원 인덱스 k (0 ≤ k < m·n) 는 행렬의 (k // n, k % n) 위치입니다. 실제로 이어 붙이지 않고 인덱스만 변환하세요.",
    "lo = 0, hi = m·n - 1 로 일반 이분 탐색을 하되, 값은 matrix[mid // n][mid % n] 으로 읽습니다.",
]

TESTS = [
    {"input": [[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3], "output": True},
    {"input": [[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13], "output": False},
    {"input": [[[1]], 1], "output": True},
    {"input": [[[1]], 2], "output": False},
    {"input": [[[1, 3]], 3], "output": True},
    {"input": [[[1], [3], [5]], 5], "output": True},
    {"input": [[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 60], "output": True},
    {"input": [[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 0], "output": False},
    {"input": [[[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 61], "output": False},
    {"input": [[[-10, -5], [-2, 0]], -2], "output": True},
]

EXPLANATION = """
핵심: 두 성질 덕분에 행렬을 행 순서대로 펼치면 하나의 정렬된 배열이 됩니다. 펼치지 않고 인덱스만 변환해서 이분 탐색합니다.

1. m, n = 행 수, 열 수. lo, hi = 0, m * n - 1
2. while lo <= hi:
     mid = (lo + hi) // 2, v = matrix[mid // n][mid % n]
     v == target → True / v < target → lo = mid + 1 / v > target → hi = mid - 1
3. False

시간 O(log(m·n)), 공간 O(1)
다른 방법: (1) 각 행의 첫 값으로 행을 이분 탐색 → 그 행 안에서 이분 탐색 (O(log m + log n), 같은 복잡도)
          (2) 오른쪽 위 모서리에서 출발해 크면 왼쪽, 작으면 아래로 이동 O(m + n) — LeetCode 240(행·열만 정렬된 행렬)의 풀이
면접 포인트: 1차원 ↔ 2차원 인덱스 변환 (k // n, k % n) 에서 나누는 수가 '열 수 n' 이라는 것을 정확히 말하세요.
"""


def reference(matrix, target):
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = matrix[mid // n][mid % n]  # 1차원 인덱스 → (행, 열)
        if v == target:
            return True
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


def alternative(matrix, target):
    # 오른쪽 위 모서리에서 출발하는 계단식 탐색 O(m + n)
    r, c = 0, len(matrix[0]) - 1
    while r < len(matrix) and c >= 0:
        v = matrix[r][c]
        if v == target:
            return True
        if v > target:
            c -= 1  # 이 열의 아래는 모두 더 크다
        else:
            r += 1  # 이 행의 왼쪽은 모두 더 작다
    return False
