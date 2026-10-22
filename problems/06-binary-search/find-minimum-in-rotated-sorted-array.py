TITLE = "Find Minimum in Rotated Sorted Array (회전된 정렬 배열의 최솟값)"
LEVEL = "Medium"
SOURCE = "LeetCode 153"
PATTERN = "nums[mid] 와 nums[hi] 를 비교해 최솟값(회전 지점)이 있는 쪽 남기기"

DESCRIPTION = """
서로 다른 정수로 이루어진 오름차순 배열을 어떤 지점에서 잘라 앞부분을 뒤로 옮긴(회전한) 배열 nums 가 주어집니다.
예: [0, 1, 2, 4, 5, 6, 7] → [4, 5, 6, 7, 0, 1, 2]  (회전하지 않았을 수도 있습니다)
nums 의 최솟값을 O(log n) 시간에 찾아 return 하세요.

제한사항
- 1 ≤ len(nums) ≤ 5,000
- -5,000 ≤ nums[i] ≤ 5,000, 모든 값은 서로 다름

입출력 예
nums = [3, 4, 5, 1, 2]           →  1
nums = [4, 5, 6, 7, 0, 1, 2]     →  0
nums = [11, 13, 15, 17]          →  11  (회전하지 않음)
"""

SIGNATURE = "def solution(nums: list[int]) -> int:"

HINTS = [
    "회전된 배열은 '큰 값들의 정렬 구간' 뒤에 '작은 값들의 정렬 구간' 이 붙은 모양입니다. 최솟값은 두 번째 구간의 시작입니다.",
    "nums[mid] 를 맨 오른쪽 값 nums[hi] 와 비교해 보세요. nums[mid] > nums[hi] 라면 mid 는 어느 구간에 속할까요?",
    "nums[mid] > nums[hi] → 최솟값은 mid 오른쪽에 있음 → lo = mid + 1. 아니면 mid 가 최솟값일 수도 있으므로 hi = mid. while lo < hi, 답은 nums[lo].",
]

TESTS = [
    {"input": [[3, 4, 5, 1, 2]], "output": 1},
    {"input": [[4, 5, 6, 7, 0, 1, 2]], "output": 0},
    {"input": [[11, 13, 15, 17]], "output": 11},
    {"input": [[1]], "output": 1},
    {"input": [[2, 1]], "output": 1},
    {"input": [[1, 2]], "output": 1},
    {"input": [[5, 1, 2, 3, 4]], "output": 1},
    {"input": [[2, 3, 4, 5, 1]], "output": 1},
    {"input": [[-2, -1, -5, -4, -3]], "output": -5},
]

EXPLANATION = """
핵심: 회전 배열 = [큰 쪽 정렬 구간][작은 쪽 정렬 구간]. 맨 오른쪽 값 nums[hi] 는 항상 '작은 쪽 구간' 에 속합니다
(회전이 없으면 전체가 하나의 구간). 그래서 nums[mid] 를 nums[hi] 와 비교하면 mid 가 어느 구간인지 알 수 있습니다.

1. lo, hi = 0, n - 1
2. while lo < hi:
     mid = (lo + hi) // 2
     nums[mid] > nums[hi] → mid 는 큰 쪽 구간 → 최솟값은 mid 오른쪽 → lo = mid + 1
     그 외                → mid 는 작은 쪽 구간 → 최솟값은 mid 이하 → hi = mid
3. nums[lo] return

시간 O(log n), 공간 O(1)
면접 포인트: nums[lo] 와 비교하면 회전이 없는 경우를 따로 처리해야 해서 헷갈립니다. nums[hi] 와 비교하는 쪽이 깔끔합니다.
hi = mid - 1 이 아니라 hi = mid 인 이유(mid 자체가 답일 수 있음)를 설명하세요.
중복 값이 허용되면(LeetCode 154) nums[mid] == nums[hi] 일 때 hi -= 1 로 한 칸만 줄여야 하고 최악 O(n) 이 됩니다.
"""


def reference(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1  # mid 는 '큰 쪽' 구간 → 최솟값은 오른쪽
        else:
            hi = mid      # mid 는 '작은 쪽' 구간 → mid 가 답일 수도 있다
    return nums[lo]


def brute_force(nums):
    return min(nums)
