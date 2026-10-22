TITLE = "Climbing Stairs (계단 오르기)"
LEVEL = "Easy"
SOURCE = "LeetCode 70"
PATTERN = "dp[i] = dp[i-1] + dp[i-2] (피보나치형 1차원 DP)"

DESCRIPTION = """
n 개의 칸으로 이루어진 계단의 맨 아래(0번 칸)에 서 있습니다.
한 번에 1칸 또는 2칸씩 올라갈 수 있을 때, 정확히 n 번 칸(꼭대기)에 도착하는
서로 다른 방법의 수를 return 하세요.
오르는 순서가 다르면 다른 방법으로 셉니다. (1+2 와 2+1 은 서로 다른 방법)

제한사항
- 1 ≤ n ≤ 45

입출력 예
n = 2  →  2   (1+1, 2)
n = 3  →  3   (1+1+1, 1+2, 2+1)
n = 5  →  8
"""

SIGNATURE = "def solution(n: int) -> int:"

HINTS = [
    "n 번 칸에 도착하기 직전에는 어디에 있었을까요? 마지막 한 걸음은 1칸 아니면 2칸입니다.",
    "ways(n) = ways(n-1) + ways(n-2). 하지만 이걸 그대로 재귀로 짜면 같은 값을 수없이 다시 계산해서 O(2^n) 입니다.",
    "작은 i 부터 차례로 채우면 O(n). 직전 두 값만 쓰므로 배열 대신 변수 두 개(prev2, prev1)로 충분합니다.",
]

TESTS = [
    {"input": [1], "output": 1},
    {"input": [2], "output": 2},
    {"input": [3], "output": 3},
    {"input": [4], "output": 5},
    {"input": [5], "output": 8},
    {"input": [10], "output": 89},
    {"input": [45], "output": 1836311903},
]

EXPLANATION = """
아이디어
- 꼭대기 i 에 도착하는 마지막 동작은 'i-1 에서 1칸' 또는 'i-2 에서 2칸' 둘 중 하나입니다.
- 두 경우는 겹치지 않으므로(마지막 걸음이 다름) 경우의 수를 더하면 됩니다.

DP 레시피
1. 상태 정의: dp[i] = i 번 칸에 도착하는 방법의 수
2. 점화식:   dp[i] = dp[i-1] + dp[i-2]
3. 초기값:   dp[0] = 1 (아무것도 안 하는 방법 1가지), dp[1] = 1
4. 계산 순서: i = 2 → n (작은 문제부터)
5. 답:       dp[n]

  i  : 0  1  2  3  4  5
  dp : 1  1  2  3  5  8     ← 피보나치 수열

공간 최적화: dp[i] 는 dp[i-1], dp[i-2] 만 보므로 변수 두 개를 굴리면(rolling) O(1) 공간입니다.

복잡도: 시간 O(n), 공간 O(1)  (배열을 쓰면 O(n))

면접 포인트
- "순진한 재귀 O(2^n) → 메모이제이션(top-down) O(n) → 바텀업 O(n) → 공간 O(1)" 의 개선 과정을 말로 설명하세요.
- 후속 질문: 한 번에 1, 2, 3칸을 오를 수 있다면? → dp[i] = dp[i-1] + dp[i-2] + dp[i-3].
- 후속 질문: 오를 수 있는 칸 수가 집합 steps 로 주어지면? → dp[i] = sum(dp[i-s] for s in steps if i >= s).
"""


def reference(n):
    # prev2 = dp[i-2], prev1 = dp[i-1]
    prev2, prev1 = 1, 1  # dp[0] = 1, dp[1] = 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1


def alternative(n):
    # top-down 메모이제이션: 재귀 + 캐시
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def ways(i):
        if i <= 1:
            return 1
        return ways(i - 1) + ways(i - 2)

    return ways(n)
