TITLE = "Unique Paths (격자 경로의 수)"
LEVEL = "Medium"
SOURCE = "LeetCode 62"
PATTERN = "격자 DP: dp[r][c] = dp[r-1][c] + dp[r][c-1]"

DESCRIPTION = """
m 행 n 열의 격자가 있습니다. 로봇은 맨 왼쪽 위 칸에서 출발해 맨 오른쪽 아래 칸으로 가려고 합니다.
로봇은 한 번에 오른쪽 또는 아래쪽으로 한 칸씩만 움직일 수 있습니다.
도착 칸까지 가는 서로 다른 경로의 수를 return 하세요.

제한사항
- 1 ≤ m, n ≤ 100
- 답은 2 × 10^9 이하입니다.

입출력 예
m = 3, n = 7  →  28
m = 3, n = 2  →  3   (오→아→아, 아→오→아, 아→아→오)
"""

SIGNATURE = "def solution(m: int, n: int) -> int:"

HINTS = [
    "어떤 칸 (r, c) 에 들어오는 마지막 이동은 위에서 아래로, 또는 왼쪽에서 오른쪽으로 둘 중 하나입니다.",
    "dp[r][c] = dp[r-1][c] + dp[r][c-1]. 첫 행과 첫 열은 가는 방법이 한 가지뿐이라 모두 1 입니다.",
    "한 행만 기억해도 됩니다: row[c] += row[c-1] 를 왼쪽부터 돌리면 row[c] 에는 '위(이전 행 값)' 가 이미 들어 있습니다. (조합으로 C(m+n-2, m-1) 도 가능)",
]

TESTS = [
    {"input": [3, 7], "output": 28},
    {"input": [3, 2], "output": 3},
    {"input": [1, 1], "output": 1},
    {"input": [1, 10], "output": 1},
    {"input": [10, 1], "output": 1},
    {"input": [7, 3], "output": 28},
    {"input": [10, 10], "output": 48620},
    {"input": [23, 12], "output": 193536720},
]

EXPLANATION = """
아이디어
- (r, c) 에 도착하는 경로는 '(r-1, c) 에서 내려온 것' 과 '(r, c-1) 에서 온 것' 으로 겹치지 않게 나뉩니다.

DP 레시피
1. 상태 정의: dp[r][c] = 출발점에서 (r, c) 까지 가는 경로 수
2. 점화식:   dp[r][c] = dp[r-1][c] + dp[r][c-1]
3. 초기값:   첫 행, 첫 열은 모두 1
4. 계산 순서: 위 → 아래, 왼쪽 → 오른쪽 (행 우선)
5. 답:       dp[m-1][n-1]

  m = 3, n = 4
       c=0  c=1  c=2  c=3
  r=0   1    1    1    1
  r=1   1    2    3    4
  r=2   1    3    6   10    ← 답 10

공간 최적화: 한 줄짜리 row 배열로 row[c] = row[c] (위) + row[c-1] (왼쪽)

복잡도: 시간 O(m × n), 공간 O(n)

수학 풀이
- 총 (m-1) 번 아래, (n-1) 번 오른쪽 이동을 나열하는 방법 = C(m+n-2, m-1). (alternative)

면접 포인트
- 조합 공식으로 O(min(m, n)) 에 풀 수 있다고 언급하면 좋지만, 장애물이 생기는 변형(Unique Paths II)에서는
  DP 만 통한다는 점도 함께 말하세요.
"""


def reference(m, n):
    row = [1] * n  # 첫 행은 모두 1
    for _ in range(1, m):
        for c in range(1, n):
            row[c] += row[c - 1]  # 위(row[c]) + 왼쪽(row[c-1])
    return row[-1]


def alternative(m, n):
    from math import comb

    return comb(m + n - 2, m - 1)
