TITLE = "House Robber (집 도둑)"
LEVEL = "Medium"
SOURCE = "LeetCode 198"
PATTERN = "고른다/안 고른다 선택 DP: dp[i] = max(dp[i-1], dp[i-2] + nums[i])"

DESCRIPTION = """
일렬로 늘어선 집들에 각각 nums[i] 만큼의 돈이 있습니다.
도둑은 집을 골라 돈을 훔치려 하지만, 바로 옆에 붙은 두 집을 모두 털면 경보가 울립니다.
경보를 울리지 않고 훔칠 수 있는 돈의 최댓값을 return 하세요.

제한사항
- 1 ≤ len(nums) ≤ 100,000
- 0 ≤ nums[i] ≤ 1,000

입출력 예
nums = [1, 2, 3, 1]     →  4   (0번 + 2번 = 1 + 3)
nums = [2, 7, 9, 3, 1]  →  12  (0번 + 2번 + 4번 = 2 + 9 + 1)
"""

SIGNATURE = "def solution(nums: list[int]) -> int:"

HINTS = [
    "큰 값부터 욕심내서 고르는 그리디는 틀립니다. 예: [2, 1, 1, 2] → 답은 4 (양 끝).",
    "i 번 집에서 할 수 있는 선택은 두 가지: 턴다(그러면 i-1 은 못 턺) / 안 턴다.",
    "dp[i] = 0..i 번 집까지 봤을 때의 최대 금액 = max(dp[i-1], dp[i-2] + nums[i]). 직전 두 값만 필요하니 변수 두 개로 굴리세요.",
]

TESTS = [
    {"input": [[1, 2, 3, 1]], "output": 4},
    {"input": [[2, 7, 9, 3, 1]], "output": 12},
    {"input": [[5]], "output": 5},
    {"input": [[2, 1]], "output": 2},
    {"input": [[0, 0, 0]], "output": 0},
    {"input": [[2, 1, 1, 2]], "output": 4},
    {"input": [[1, 3, 1, 3, 100]], "output": 103},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    nums = [random.randint(0, 1000) for _ in range(100_000)]
    return {"input": [nums], "output": None}


EXPLANATION = """
아이디어
- i 번 집 앞에서의 선택: 턴다 → 이전 최선은 i-2 까지의 답 / 안 턴다 → i-1 까지의 답 그대로.
- 모든 부분집합(2^n)을 보는 대신, "i 까지의 최선" 하나만 기억하면 됩니다(최적 부분 구조).

DP 레시피
1. 상태 정의: dp[i] = 0..i 번 집만 고려했을 때 훔칠 수 있는 최대 금액
2. 점화식:   dp[i] = max(dp[i-1], dp[i-2] + nums[i])
3. 초기값:   dp[-1] = dp[-2] = 0 (집이 없으면 0) → 변수 prev2 = prev1 = 0 으로 시작
4. 계산 순서: i = 0 → n-1
5. 답:       dp[n-1]

  nums : 2   7   9   3   1
  dp   : 2   7   11  11  12

복잡도: 시간 O(n), 공간 O(1)

면접 포인트
- 브루트포스(각 집을 턴다/안 턴다 재귀)는 O(2^n). 같은 i 에 대한 부분 문제가 반복되므로 메모하면 O(n).
- n 이 100,000 이면 top-down 재귀는 RecursionError 위험 → 바텀업 + 변수 두 개가 안전합니다.
- 후속 문제: 집이 원형이면? → House Robber II (첫 집/마지막 집 중 하나를 빼고 두 번 계산).
"""


def reference(nums):
    prev2, prev1 = 0, 0  # dp[i-2], dp[i-1]
    for x in nums:
        # 이번 집을 털면 prev2 + x, 안 털면 prev1
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1


def brute_force(nums):
    # 각 집마다 턴다/안 턴다를 모두 시도: O(2^n)
    def go(i):
        if i >= len(nums):
            return 0
        return max(go(i + 1), nums[i] + go(i + 2))

    return go(0)
