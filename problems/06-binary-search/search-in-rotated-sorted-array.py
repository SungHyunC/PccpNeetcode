TITLE = "Search in Rotated Sorted Array (회전된 정렬 배열에서 찾기)"
LEVEL = "Medium"
SOURCE = "LeetCode 33"
PATTERN = "mid 기준으로 '정렬된 절반' 을 찾고, target 이 그 안에 있는지로 방향 결정"

DESCRIPTION = """
서로 다른 정수로 이루어진 오름차순 배열을 어떤 지점에서 회전한 배열 nums 와 정수 target 이 주어집니다.
예: [0, 1, 2, 4, 5, 6, 7] → [4, 5, 6, 7, 0, 1, 2]  (회전하지 않았을 수도 있습니다)
nums 에서 target 의 인덱스를 찾아 return 하고, 없으면 -1 을 return 하세요. O(log n) 시간이어야 합니다.

제한사항
- 1 ≤ len(nums) ≤ 5,000
- -10^4 ≤ nums[i], target ≤ 10^4, nums 의 값은 모두 서로 다름

입출력 예
nums = [4, 5, 6, 7, 0, 1, 2], target = 0  →  4
nums = [4, 5, 6, 7, 0, 1, 2], target = 3  →  -1
nums = [1],                   target = 0  →  -1
"""

SIGNATURE = "def solution(nums: list[int], target: int) -> int:"

HINTS = [
    "회전된 배열을 mid 에서 둘로 나누면, 적어도 한쪽 절반은 반드시 '제대로 정렬된' 상태입니다.",
    "nums[lo] <= nums[mid] 이면 왼쪽 절반 [lo, mid] 가 정렬되어 있습니다. 아니면 오른쪽 절반 [mid, hi] 가 정렬되어 있습니다.",
    "정렬된 절반은 양 끝 값만 보면 target 이 그 안에 있는지 바로 알 수 있습니다. 있으면 그쪽으로, 없으면 반대쪽으로 좁히세요.",
    "왼쪽이 정렬: nums[lo] <= target < nums[mid] 이면 hi = mid - 1, 아니면 lo = mid + 1. 오른쪽이 정렬: nums[mid] < target <= nums[hi] 이면 lo = mid + 1, 아니면 hi = mid - 1.",
]

TESTS = [
    {"input": [[4, 5, 6, 7, 0, 1, 2], 0], "output": 4},
    {"input": [[4, 5, 6, 7, 0, 1, 2], 3], "output": -1},
    {"input": [[1], 0], "output": -1},
    {"input": [[1], 1], "output": 0},
    {"input": [[3, 1], 1], "output": 1},
    {"input": [[1, 3], 3], "output": 1},
    {"input": [[5, 1, 3], 5], "output": 0},
    {"input": [[4, 5, 6, 7, 8, 1, 2, 3], 8], "output": 4},
    {"input": [[1, 2, 3, 4, 5, 6], 4], "output": 3},
    {"input": [[6, 7, 1, 2, 3, 4, 5], 6], "output": 0},
]

EXPLANATION = """
핵심: mid 로 나눈 두 절반 중 적어도 하나는 정렬되어 있습니다. 정렬된 쪽은 범위 확인이 쉬우므로
"target 이 정렬된 쪽 범위 안인가?" 로 방향을 정합니다.

1. lo, hi = 0, n - 1
2. while lo <= hi:
     mid = (lo + hi) // 2, 같으면 mid 반환
     nums[lo] <= nums[mid] (왼쪽 정렬):
         nums[lo] <= target < nums[mid] 이면 hi = mid - 1, 아니면 lo = mid + 1
     그 외 (오른쪽 정렬):
         nums[mid] < target <= nums[hi] 이면 lo = mid + 1, 아니면 hi = mid - 1
3. -1 반환

시간 O(log n), 공간 O(1)
다른 방법: Find Minimum 으로 회전 지점(최솟값 위치)을 먼저 찾고, target 이 있는 쪽 구간에서 일반 이분 탐색 (역시 O(log n)).
면접 포인트: nums[lo] <= nums[mid] 에서 = 를 빼먹으면 lo == mid 인 경우(원소 2개)에서 틀립니다. 경계 조건을 작은 예([3, 1])로 손으로 확인하세요.
"""


def reference(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:  # 왼쪽 [lo, mid] 가 정렬되어 있다
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                      # 오른쪽 [mid, hi] 가 정렬되어 있다
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


def alternative(nums, target):
    # 1) 회전 지점(최솟값 위치) 찾기 → 2) 해당 구간에서 bisect
    from bisect import bisect_left

    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    pivot = lo
    if pivot > 0 and target >= nums[0]:
        left, right = 0, pivot           # 큰 쪽 구간 [0, pivot)
    else:
        left, right = pivot, len(nums)   # 작은 쪽 구간 [pivot, n)
    i = bisect_left(nums, target, left, right)
    return i if i < right and nums[i] == target else -1
