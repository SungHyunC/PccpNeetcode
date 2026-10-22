TITLE = "Maximum Subarray (최대 부분 배열 합)"
LEVEL = "Medium"
SOURCE = "LeetCode 53"
PATTERN = "카데인(Kadane): 누적합이 음수면 버리고 새로 시작"

DESCRIPTION = """
정수 배열 nums 가 주어집니다.
비어 있지 않은 연속 부분 배열 중 원소의 합이 가장 큰 것을 찾아 그 합을 return 하세요.

제한사항
- 1 ≤ len(nums) ≤ 100,000
- -10,000 ≤ nums[i] ≤ 10,000

입출력 예
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]  →  6    ([4, -1, 2, 1])
nums = [5, 4, -1, 7, 8]                 →  23   (전체)
nums = [-3, -1, -2]                     →  -1   (원소 하나만 골라야 함)
"""

SIGNATURE = "def solution(nums: list[int]) -> int:"

HINTS = [
    "모든 (시작, 끝) 쌍을 보면 O(n^2) 입니다. n = 100,000 이면 50억 번 → 시간 초과.",
    "i 에서 끝나는 최대 부분 배열은 'i-1 에서 끝나는 최대 부분 배열에 nums[i] 를 붙이기' 또는 'nums[i] 혼자' 둘 중 하나입니다.",
    "cur = max(x, cur + x), best = max(best, cur). 즉 지금까지의 누적합이 음수라면 앞부분을 버리는 게 항상 이득입니다. 모든 원소가 음수일 때를 위해 best 의 초기값은 nums[0]!",
]

TESTS = [
    {"input": [[-2, 1, -3, 4, -1, 2, 1, -5, 4]], "output": 6},
    {"input": [[1]], "output": 1},
    {"input": [[5, 4, -1, 7, 8]], "output": 23},
    {"input": [[-3, -1, -2]], "output": -1},
    {"input": [[0, 0]], "output": 0},
    {"input": [[-1]], "output": -1},
    {"input": [[2, -1, 2]], "output": 3},
    {"input": [[8, -19, 5, -4, 20]], "output": 21},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    nums = [random.randint(-10_000, 10_000) for _ in range(100_000)]
    return {"input": [nums], "output": None}


EXPLANATION = """
아이디어 (Kadane 알고리즘)
- 왼쪽부터 보면서 "지금 위치에서 끝나는 최대 합" cur 를 유지합니다.
- cur 가 음수라면 앞부분을 이어 붙이는 것은 손해 → 버리고 현재 원소부터 새로 시작합니다.
- 이것은 그리디처럼 보이지만 정확히는 1차원 DP 입니다: dp[i] = max(nums[i], dp[i-1] + nums[i]).

단계
1. cur = best = nums[0]
2. 다음 원소 x 마다: cur = max(x, cur + x)  (이어 붙이기 vs 새로 시작)
3. best = max(best, cur)

  nums : -2   1  -3   4  -1   2   1  -5   4
  cur  : -2   1  -2   4   3   5   6   1   5
  best : -2   1   1   4   4   5   6   6   6   → 6

왜 맞는가 (교환 논법 스케치)
- 최적 부분 배열 [l..r] 이 있을 때, 그 앞부분 nums[l..k] 의 합이 음수라면 그 부분을 빼면 더 커지므로 모순.
  즉 최적해의 모든 접두사 합은 0 이상 → "누적합이 음수가 되면 끊는다" 가 최적해를 잃지 않습니다.

복잡도: 시간 O(n), 공간 O(1)

면접 포인트
- 브루트포스 O(n^2) (누적합 사용) → Kadane O(n) 순서로 개선 과정을 말하세요.
- 함정: best = 0 으로 시작하면 모든 원소가 음수일 때 0 을 반환합니다(빈 배열은 불가).
- 후속 질문: 부분 배열의 시작/끝 인덱스 반환 → cur 를 새로 시작할 때 start 를 기록.
- 후속 질문: 분할 정복 O(n log n) 풀이, 원형 배열 버전(LeetCode 918: 전체합 - 최소 부분합).
"""


def reference(nums):
    cur = best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)  # 앞부분을 이어 붙일지, 여기서 새로 시작할지
        if cur > best:
            best = cur
    return best


def brute_force(nums):
    # 모든 시작점에서 누적합: O(n^2)
    best = nums[0]
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            best = max(best, s)
    return best
