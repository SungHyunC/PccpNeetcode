TITLE = "Subarray Sum Equals K (합이 K인 부분 배열 개수)"
LEVEL = "Medium"
SOURCE = "LeetCode 560"
PATTERN = "누적합(prefix sum) + 해시맵"

DESCRIPTION = """
정수 배열 nums 와 정수 k 가 주어집니다. 합이 정확히 k 인 연속 부분 배열의 개수를 return 하세요.

제한사항
- 1 ≤ len(nums) ≤ 20,000
- -1,000 ≤ nums[i] ≤ 1,000 (음수 가능 → 슬라이딩 윈도우 불가)
- -10^7 ≤ k ≤ 10^7

입출력 예
nums = [1, 1, 1], k = 2  →  2
nums = [1, 2, 3], k = 3  →  2   ([1,2], [3])
"""

SIGNATURE = "def solution(nums: list[int], k: int) -> int:"

HINTS = [
    "구간 [i, j] 의 합 = prefix[j+1] - prefix[i] 입니다.",
    "prefix[j+1] - prefix[i] == k  ⇔  prefix[i] == prefix[j+1] - k",
    "지금까지 나온 누적합의 등장 횟수를 dict 에 세면서, 현재 누적합 - k 가 몇 번 나왔는지 더하세요. 시작 전에 {0: 1} 을 넣어 두는 것을 잊지 마세요.",
]

TESTS = [
    {"input": [[1, 1, 1], 2], "output": 2},
    {"input": [[1, 2, 3], 3], "output": 2},
    {"input": [[1], 0], "output": 0},
    {"input": [[0, 0, 0], 0], "output": 6},
    {"input": [[1, -1, 0], 0], "output": 3},
    {"input": [[3, 4, 7, 2, -3, 1, 4, 2], 7], "output": 4},
    {"input": [[-1, -1, 1], 0], "output": 1},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    nums = [random.randint(-5, 5) for _ in range(20_000)]
    return {"input": [nums, 3], "output": None}


EXPLANATION = """
누적합 S(j) = nums[0] + ... + nums[j-1]. 구간 (i, j] 의 합 = S(j) - S(i).
오른쪽 끝 j 를 고정하면 S(i) == S(j) - k 인 i 의 개수가 곧 답에 더해질 값입니다.

  nums = [1, 1, 1], k = 2
  누적합:    0  1  2  3
  count = {0:1} → 1 (1-2=-1 없음) → 2 (0 있음 +1) → 3 (1 있음 +1)  ⇒ 2

시간 O(n), 공간 O(n)
면접 포인트: 음수가 있으면 슬라이딩 윈도우가 안 되는 이유(윈도우를 늘려도 합이 커진다는 보장이 없음)를 설명하세요.
PCCP 에서도 '연속 부분 수열의 합' 문제가 자주 나옵니다.
"""


def reference(nums, k):
    from collections import defaultdict
    count = defaultdict(int)
    count[0] = 1  # 아무것도 고르지 않은 누적합 0
    prefix = 0
    answer = 0
    for x in nums:
        prefix += x
        answer += count[prefix - k]
        count[prefix] += 1
    return answer


def brute_force(nums, k):
    n = len(nums)
    answer = 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s == k:
                answer += 1
    return answer
