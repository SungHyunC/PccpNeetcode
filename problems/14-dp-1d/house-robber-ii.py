TITLE = "House Robber II (원형 집 도둑)"
LEVEL = "Medium"
SOURCE = "LeetCode 213"
PATTERN = "원형 → 첫 집 제외 / 마지막 집 제외 두 번의 선형 DP"

DESCRIPTION = """
집들이 원형으로 둘러앉아 있어서 첫 번째 집과 마지막 집도 서로 이웃입니다.
각 집에는 nums[i] 만큼의 돈이 있고, 이웃한 두 집을 모두 털면 경보가 울립니다.
경보를 울리지 않고 훔칠 수 있는 돈의 최댓값을 return 하세요.

제한사항
- 1 ≤ len(nums) ≤ 100,000
- 0 ≤ nums[i] ≤ 1,000

입출력 예
nums = [2, 3, 2]     →  3   (0번과 2번은 이웃이라 함께 털 수 없음)
nums = [1, 2, 3, 1]  →  4   (0번 + 2번)
"""

SIGNATURE = "def solution(nums: list[int]) -> int:"

HINTS = [
    "원형이라는 조건 때문에 생기는 제약은 단 하나: 첫 집과 마지막 집을 동시에 털 수 없다는 것뿐입니다.",
    "그렇다면 '첫 집을 털지 않는 경우' 와 '마지막 집을 털지 않는 경우' 로 나누면 각각은 일렬(House Robber I) 문제가 됩니다.",
    "answer = max(rob(nums[1:]), rob(nums[:-1])). 단, 집이 1채면 nums[0] 을 그대로 return 해야 합니다.",
]

TESTS = [
    {"input": [[2, 3, 2]], "output": 3},
    {"input": [[1, 2, 3, 1]], "output": 4},
    {"input": [[1, 2, 3]], "output": 3},
    {"input": [[5]], "output": 5},
    {"input": [[1, 1]], "output": 1},
    {"input": [[200, 3, 140, 20, 10]], "output": 340},
    {"input": [[2, 7, 9, 3, 1]], "output": 11},
    {"input": [[0, 0, 0, 0]], "output": 0},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    nums = [random.randint(0, 1000) for _ in range(100_000)]
    return {"input": [nums], "output": None}


EXPLANATION = """
아이디어
- 원형 조건 = "0번과 n-1번을 동시에 고르지 않는다" 하나뿐입니다.
- 최적해는 반드시 (0번을 안 고름) 또는 (n-1번을 안 고름) 중 적어도 하나에 속합니다.
  → nums[1:] 과 nums[:-1] 에 대해 일렬 집 도둑 DP를 각각 돌려 큰 값을 고릅니다.

단계
1. n == 1 이면 nums[0] (nums[1:], nums[:-1] 이 둘 다 비어서 0이 나오는 함정 주의)
2. rob(arr): prev2, prev1 = 0, 0 → prev2, prev1 = prev1, max(prev1, prev2 + x)
3. max(rob(nums[1:]), rob(nums[:-1]))

점화식 (각 선형 구간에서)
- dp[i] = max(dp[i-1], dp[i-2] + nums[i])

복잡도: 시간 O(n), 공간 O(n) (슬라이스 복사) — 인덱스 범위만 넘기면 O(1)

면접 포인트
- "원형(circular) → 경계 하나를 끊어 선형 문제 두 개로 만든다" 는 일반적인 기법입니다.
  (원형 배열의 최대 부분합, 원형 순회 문제 등에서도 같은 발상)
- n == 1 경계값을 먼저 언급하면 꼼꼼하다는 인상을 줍니다.
"""


def reference(nums):
    def rob(lo, hi):
        # nums[lo..hi] 구간에 대한 일렬 집 도둑 DP
        prev2, prev1 = 0, 0
        for i in range(lo, hi + 1):
            prev2, prev1 = prev1, max(prev1, prev2 + nums[i])
        return prev1

    n = len(nums)
    if n == 1:
        return nums[0]
    # 마지막 집 제외 vs 첫 집 제외
    return max(rob(0, n - 2), rob(1, n - 1))


def brute_force(nums):
    # 모든 부분집합 중 (원형으로) 이웃이 없는 것의 최대 합: O(2^n * n)
    n = len(nums)
    best = 0
    for mask in range(1 << n):
        ok = True
        for i in range(n):
            j = (i + 1) % n
            if i != j and (mask >> i) & 1 and (mask >> j) & 1:
                ok = False
                break
        if ok:
            best = max(best, sum(nums[i] for i in range(n) if (mask >> i) & 1))
    return best
