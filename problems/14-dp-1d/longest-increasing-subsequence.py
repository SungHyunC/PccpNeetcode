TITLE = "Longest Increasing Subsequence (최장 증가 부분 수열)"
LEVEL = "Medium"
SOURCE = "LeetCode 300"
PATTERN = "O(n^2) DP → tails 배열 + 이분 탐색(bisect) O(n log n)"

DESCRIPTION = """
정수 배열 nums 가 주어집니다.
원소의 순서를 유지한 채 일부를 골라(연속일 필요 없음) 만든 수열 중
값이 '엄격하게' 증가하는 가장 긴 수열의 길이를 return 하세요.

제한사항
- 1 ≤ len(nums) ≤ 100,000
- -10^9 ≤ nums[i] ≤ 10^9

입출력 예
nums = [10, 9, 2, 5, 3, 7, 101, 18]  →  4   (예: 2, 3, 7, 18)
nums = [0, 1, 0, 3, 2, 3]            →  4   (0, 1, 2, 3)
nums = [7, 7, 7, 7]                  →  1   (같은 값은 증가가 아님)
"""

SIGNATURE = "def solution(nums: list[int]) -> int:"

HINTS = [
    "먼저 O(n^2) DP: dp[i] = nums[i] 로 끝나는 LIS 의 길이 = 1 + max(dp[j]) (j < i 이고 nums[j] < nums[i]).",
    "n = 100,000 이면 O(n^2) 는 시간 초과입니다. '길이 k 인 증가 수열의 마지막 값 중 가장 작은 값' 을 tails[k-1] 에 저장해 보세요.",
    "tails 는 항상 오름차순입니다. 새 값 x 에 대해 bisect_left(tails, x) 위치를 x 로 교체하거나(같거나 큰 첫 값), 끝이면 append. 답은 len(tails).",
]

TESTS = [
    {"input": [[10, 9, 2, 5, 3, 7, 101, 18]], "output": 4},
    {"input": [[0, 1, 0, 3, 2, 3]], "output": 4},
    {"input": [[7, 7, 7, 7]], "output": 1},
    {"input": [[5]], "output": 1},
    {"input": [[1, 2, 3, 4, 5]], "output": 5},
    {"input": [[5, 4, 3, 2, 1]], "output": 1},
    {"input": [[-2, -1, -5, 0]], "output": 3},
    {"input": [[4, 10, 4, 3, 8, 9]], "output": 3},
    {"input": [[1, 3, 6, 7, 9, 4, 10, 5, 6]], "output": 6},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    nums = [random.randint(-10**9, 10**9) for _ in range(100_000)]
    return {"input": [nums], "output": None}


EXPLANATION = """
아이디어 1 — O(n^2) DP (brute_force)
1. 상태 정의: dp[i] = nums[i] 로 '끝나는' 가장 긴 증가 부분 수열의 길이
2. 점화식:   dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i])  (없으면 1)
3. 초기값:   dp[i] = 1
4. 계산 순서: i = 0 → n-1
5. 답:       max(dp)   ← dp[n-1] 이 아님에 주의!

아이디어 2 — tails + 이분 탐색 O(n log n) (reference)
- tails[k] = 길이 k+1 인 증가 수열들이 가질 수 있는 '가장 작은 마지막 값'
- 끝값이 작을수록 뒤에 더 많은 수를 붙일 수 있으므로 작은 값이 유리합니다.
- tails 는 항상 오름차순 → 새 값 x 의 자리를 bisect_left 로 O(log n) 에 찾습니다.
  - x 가 모든 값보다 크면 append (LIS 길이 +1)
  - 아니면 x 이상인 첫 값을 x 로 교체 (같은 길이를 더 작은 끝값으로 갱신)

  nums = [10, 9, 2, 5, 3, 7, 101, 18]
  x=10  → [10]
  x=9   → [9]            (10 을 9 로 교체)
  x=2   → [2]
  x=5   → [2, 5]
  x=3   → [2, 3]
  x=7   → [2, 3, 7]
  x=101 → [2, 3, 7, 101]
  x=18  → [2, 3, 7, 18]  → 길이 4

  주의: tails 자체는 실제 LIS 가 아닐 수 있습니다. 길이만 정확합니다.

복잡도
- O(n^2) DP: 시간 O(n^2), 공간 O(n) → n = 100,000 이면 약 50억 번 비교로 시간 초과
- tails + bisect: 시간 O(n log n), 공간 O(n)

면접 포인트
- O(n^2) DP 를 먼저 말하고 "n 이 크면 이분 탐색으로 최적화" 하는 흐름이 정석입니다.
- 엄격한 증가 → bisect_left, 비감소(같은 값 허용) → bisect_right. 이 차이를 설명할 수 있어야 합니다.
- 실제 수열을 복원하려면 각 원소가 들어간 위치와 이전 원소 인덱스(parent)를 기록합니다.
"""


def reference(nums):
    from bisect import bisect_left

    tails = []  # tails[k] = 길이 k+1 증가 수열의 최소 끝값
    for x in nums:
        i = bisect_left(tails, x)  # x 이상인 첫 위치 (엄격한 증가)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)


def brute_force(nums):
    # O(n^2) DP: dp[i] = nums[i] 로 끝나는 LIS 길이
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
