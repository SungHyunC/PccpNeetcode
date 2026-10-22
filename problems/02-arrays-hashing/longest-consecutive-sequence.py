TITLE = "Longest Consecutive Sequence (가장 긴 연속 수열)"
LEVEL = "Medium"
SOURCE = "LeetCode 128"
PATTERN = "set 에서 수열의 시작점만 확장"

DESCRIPTION = """
정렬되지 않은 정수 배열 nums 가 주어집니다. 값이 1씩 연속으로 이어지는 수들의 최대 길이를 return 하세요.
(배열 안에서의 위치는 상관없습니다.) O(n) 풀이를 목표로 하세요.

제한사항
- 0 ≤ len(nums) ≤ 100,000
- -10^9 ≤ nums[i] ≤ 10^9

입출력 예
[100, 4, 200, 1, 3, 2]           →  4   (1, 2, 3, 4)
[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]   →  9
"""

SIGNATURE = "def solution(nums: list[int]) -> int:"

HINTS = [
    "정렬하면 O(n log n) 에 풀 수 있습니다. O(n) 은?",
    "모든 값을 set 에 넣으면 'x+1 이 있는가' 를 O(1) 에 알 수 있습니다.",
    "x-1 이 set 에 없는 x 만 '수열의 시작' 입니다. 시작점에서만 x+1, x+2 ... 를 세면 각 원소를 최대 두 번만 봅니다.",
]

TESTS = [
    {"input": [[100, 4, 200, 1, 3, 2]], "output": 4},
    {"input": [[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]], "output": 9},
    {"input": [[]], "output": 0},
    {"input": [[5]], "output": 1},
    {"input": [[1, 2, 0, 1]], "output": 3},
    {"input": [[-3, -2, -1, 10, 11]], "output": 3},
    {"input": [[9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6]], "output": 7},
]

PERF_LIMIT = 1.0


def perf_case():
    nums = list(range(0, 200_000, 2)) + list(range(50_001, 60_000, 2))
    import random
    random.shuffle(nums)
    return {"input": [nums], "output": None}


EXPLANATION = """
아이디어: 수열은 '시작점' 에서만 세면 됩니다. x-1 이 없으면 x 가 시작점.

  set = {1, 2, 3, 4, 100, 200}
  1   : 0 없음 → 시작! 1,2,3,4 → 길이 4
  2,3,4: 앞 숫자가 있으므로 건너뜀
  100 : 시작 → 길이 1

각 원소는 '시작 여부 확인' 1번 + '확장' 최대 1번 → 시간 O(n), 공간 O(n)
면접 포인트: while 문이 for 문 안에 있어도 전체 O(n) 인 이유(상각 분석)를 설명할 수 있어야 합니다.
"""


def reference(nums):
    num_set = set(nums)
    best = 0
    for x in num_set:
        if x - 1 not in num_set:  # x 가 수열의 시작점
            length = 1
            while x + length in num_set:
                length += 1
            best = max(best, length)
    return best


def alternative(nums):
    # 정렬 풀이: O(n log n)
    if not nums:
        return 0
    nums = sorted(set(nums))
    best = cur = 1
    for a, b in zip(nums, nums[1:]):
        cur = cur + 1 if b == a + 1 else 1
        best = max(best, cur)
    return best
