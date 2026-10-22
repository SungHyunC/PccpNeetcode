TITLE = "Grid Paths with Puddles (웅덩이를 피하는 최단 경로의 수)"
LEVEL = "Medium"
SOURCE = "PCCP 기출 유형 (프로그래머스 Lv.3 '등굣길' 유형)"
PATTERN = "장애물 격자 DP + 나머지 연산(mod 1,000,000,007)"

DESCRIPTION = """
m 행 n 열의 동네 지도가 있습니다. 집은 (1, 1) (맨 왼쪽 위), 도서관은 (m, n) (맨 오른쪽 아래)에 있습니다.
비가 와서 몇몇 칸에 물웅덩이가 생겼고, 웅덩이 칸은 지나갈 수 없습니다.
웅덩이 위치는 puddles 에 [행, 열] (1부터 시작) 형태로 주어집니다.
오른쪽 또는 아래쪽으로만 한 칸씩 이동할 때, 집에서 도서관까지 가는 경로의 수를
1,000,000,007 로 나눈 나머지를 return 하세요.

제한사항
- 1 ≤ m, n ≤ 100
- 0 ≤ len(puddles) ≤ 10
- 집과 도서관 칸은 웅덩이가 아니며, 같은 웅덩이가 중복으로 주어지지 않음
- 주의: 좌표 순서는 [행, 열] 입니다. (원본 '등굣길' 은 [열(가로), 행(세로)] 순서이니 실전에서는 꼭 확인!)

입출력 예
m = 3, n = 4, puddles = [[2, 2]]          →  4
m = 2, n = 2, puddles = [[1, 2], [2, 1]]  →  0
m = 3, n = 3, puddles = []                →  6
"""

SIGNATURE = "def solution(m: int, n: int, puddles: list[list[int]]) -> int:"

HINTS = [
    "웅덩이가 없다면 Unique Paths 와 같습니다: dp[r][c] = dp[r-1][c] + dp[r][c-1].",
    "웅덩이 칸은 경로 수를 0 으로 고정하면 됩니다. 그러면 그 칸을 거치는 경로가 자연스럽게 사라집니다.",
    "첫 행/첫 열을 1 로 미리 채우면 안 됩니다! 웅덩이 뒤쪽은 0 이어야 하니까요. (m+1)×(n+1) 패딩 배열에 dp[1][1] = 1 로 시작하고, 더할 때마다 % 1,000,000,007.",
]

TESTS = [
    {"input": [3, 4, [[2, 2]]], "output": 4},
    {"input": [2, 2, [[1, 2], [2, 1]]], "output": 0},
    {"input": [3, 3, []], "output": 6},
    {"input": [1, 1, []], "output": 1},
    {"input": [1, 5, [[1, 3]]], "output": 0},
    {"input": [3, 3, [[2, 2]]], "output": 2},
    {"input": [4, 4, [[1, 3], [3, 1]]], "output": 12},
    {"input": [100, 100, []], "output": 690285631},
    {"input": [100, 100, [[50, 50], [2, 1], [1, 2]]], "output": 0},
]

EXPLANATION = """
아이디어
- Unique Paths 에 '막힌 칸은 0' 규칙만 추가하면 됩니다.
- 첫 행/첫 열을 무조건 1 로 채우는 실수를 피하려고, 1-indexed 패딩 배열(0행·0열은 모두 0)을 씁니다.

DP 레시피
1. 상태 정의: dp[r][c] = 집에서 (r, c) 까지 가는 경로 수 (mod P)
2. 점화식:   웅덩이면 dp[r][c] = 0, 아니면 dp[r][c] = (dp[r-1][c] + dp[r][c-1]) % P
3. 초기값:   dp[1][1] = 1, 패딩(0행·0열) = 0
4. 계산 순서: r = 1 → m, c = 1 → n
5. 답:       dp[m][n]

  m = 3, n = 4, puddles = [[2, 2]]   (X = 웅덩이)
        c=1  c=2  c=3  c=4
  r=1    1    1    1    1
  r=2    1    X0   1    2
  r=3    1    1    2    4    ← 답 4

  첫 행/첫 열에 웅덩이가 있으면 그 뒤로는 전부 0:
  m = 1, n = 5, puddles = [[1, 3]] → 1  1  X0  0  0

복잡도: 시간 O(m × n), 공간 O(m × n) (한 줄 배열로 O(n) 가능)

면접/시험 포인트
- 프로그래머스 '등굣길' 은 m 이 가로(열), n 이 세로(행), puddles 가 [x, y] = [열, 행] 입니다.
  좌표 순서를 뒤집어 읽어 틀리는 경우가 정말 많으니, 문제의 좌표계를 첫 줄에 주석으로 적어 두세요.
- 나머지 연산은 더할 때마다 하세요. 파이썬은 큰 수도 다루지만, 수백 자리 정수 덧셈은 느려지고 다른 언어에서는 overflow 입니다.
- 웅덩이 판정은 set 에 튜플로 넣어 O(1) 로 확인합니다.
"""

MOD = 1_000_000_007


def reference(m, n, puddles):
    blocked = {(r, c) for r, c in puddles}
    dp = [[0] * (n + 1) for _ in range(m + 1)]  # 0행·0열은 패딩(항상 0)
    dp[1][1] = 1
    for r in range(1, m + 1):
        for c in range(1, n + 1):
            if (r, c) == (1, 1):
                continue
            if (r, c) in blocked:
                dp[r][c] = 0  # 웅덩이는 지나갈 수 없음
            else:
                dp[r][c] = (dp[r - 1][c] + dp[r][c - 1]) % MOD
    return dp[m][n]


def alternative(m, n, puddles):
    # top-down: ways(r, c) = (r, c) 에서 도서관까지 가는 경로 수. 깊이는 최대 m + n
    from functools import lru_cache

    blocked = {(r, c) for r, c in puddles}

    @lru_cache(maxsize=None)
    def ways(r, c):
        if r > m or c > n or (r, c) in blocked:
            return 0
        if (r, c) == (m, n):
            return 1
        return (ways(r + 1, c) + ways(r, c + 1)) % 1_000_000_007

    return ways(1, 1)
