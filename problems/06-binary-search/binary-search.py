TITLE = "Binary Search (이분 탐색)"
LEVEL = "Easy"
SOURCE = "LeetCode 704"
PATTERN = "닫힌 구간 [lo, hi] 에서 가운데와 비교해 절반씩 버리기"

DESCRIPTION = """
오름차순으로 정렬된 정수 배열 nums (원소는 모두 서로 다름) 와 정수 target 이 주어집니다.
nums 에 target 이 있으면 그 인덱스를, 없으면 -1 을 return 하세요.
O(log n) 시간에 동작하도록 작성해야 합니다.

제한사항
- 1 ≤ len(nums) ≤ 100,000
- -10^9 ≤ nums[i], target ≤ 10^9
- nums 는 오름차순 정렬, 중복 없음

입출력 예
nums = [-1, 0, 3, 5, 9, 12], target = 9  →  4
nums = [-1, 0, 3, 5, 9, 12], target = 2  →  -1
"""

SIGNATURE = "def solution(nums: list[int], target: int) -> int:"

HINTS = [
    "정렬되어 있으므로 가운데 값 하나만 보면, target 이 왼쪽 절반에 있는지 오른쪽 절반에 있는지 알 수 있습니다.",
    "lo = 0, hi = n - 1 (양 끝 포함). while lo <= hi: mid = (lo + hi) // 2",
    "nums[mid] == target 이면 mid 반환, nums[mid] < target 이면 lo = mid + 1, 아니면 hi = mid - 1. 루프가 끝나면 -1.",
]

TESTS = [
    {"input": [[-1, 0, 3, 5, 9, 12], 9], "output": 4},
    {"input": [[-1, 0, 3, 5, 9, 12], 2], "output": -1},
    {"input": [[5], 5], "output": 0},
    {"input": [[5], -5], "output": -1},
    {"input": [[1, 3], 1], "output": 0},
    {"input": [[1, 3], 3], "output": 1},
    {"input": [[1, 3, 5, 7, 9], 10], "output": -1},
    {"input": [[1, 3, 5, 7, 9], 0], "output": -1},
    {"input": [[-1000000000, 0, 1000000000], 1000000000], "output": 2},
]

EXPLANATION = """
핵심: 탐색 구간을 매번 절반으로 줄입니다. n = 100,000 이어도 약 17 번이면 끝납니다.

1. lo, hi = 0, n - 1      ← 닫힌 구간 [lo, hi] 가 '아직 후보인 구간'
2. while lo <= hi:        ← 구간에 원소가 하나라도 있는 동안
     mid = (lo + hi) // 2
     같으면 mid 반환 / 작으면 lo = mid + 1 / 크면 hi = mid - 1
3. -1 반환

시간 O(log n), 공간 O(1)
면접 포인트: 구간 정의(닫힌 [lo, hi] vs 반열린 [lo, hi))와 그에 맞는 while 조건·갱신식을 일관되게 쓰는 것이 핵심입니다.
파이썬은 정수 오버플로가 없지만, 다른 언어에서는 mid = lo + (hi - lo) // 2 로 쓰는 이유도 말할 수 있으면 좋습니다.
실전에서는 bisect.bisect_left 를 써도 됩니다.
"""


def reference(nums, target):
    lo, hi = 0, len(nums) - 1  # 닫힌 구간 [lo, hi]
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1  # mid 와 그 왼쪽은 모두 target 보다 작다
        else:
            hi = mid - 1  # mid 와 그 오른쪽은 모두 target 보다 크다
    return -1


def alternative(nums, target):
    # 표준 라이브러리 bisect 사용
    from bisect import bisect_left

    i = bisect_left(nums, target)
    return i if i < len(nums) and nums[i] == target else -1
