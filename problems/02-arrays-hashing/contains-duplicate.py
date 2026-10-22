TITLE = "Contains Duplicate (중복 원소 찾기)"
LEVEL = "Easy"
SOURCE = "LeetCode 217"
PATTERN = "set 으로 이미 본 값 기록"

DESCRIPTION = """
정수 배열 nums 에 같은 값이 두 번 이상 등장하면 True, 모든 값이 서로 다르면 False 를 return 하세요.

제한사항
- 0 ≤ len(nums) ≤ 100,000
- -10^9 ≤ nums[i] ≤ 10^9

입출력 예
[1, 2, 3, 1]  →  True
[1, 2, 3, 4]  →  False
"""

SIGNATURE = "def solution(nums: list[int]) -> bool:"

HINTS = [
    "모든 쌍을 비교하면 O(n^2) 입니다. 더 빠른 방법은?",
    "정렬하면 같은 값이 붙어 있게 됩니다 → O(n log n).",
    "set 은 '있는지 확인' 을 평균 O(1) 에 합니다. 한 번 훑으면서 이미 본 값인지 확인하세요. (한 줄 풀이: len(set(nums)) != len(nums))",
]

TESTS = [
    {"input": [[1, 2, 3, 1]], "output": True},
    {"input": [[1, 2, 3, 4]], "output": False},
    {"input": [[]], "output": False},
    {"input": [[7]], "output": False},
    {"input": [[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]], "output": True},
    {"input": [[-1, 1, 0, -1]], "output": True},
]

PERF_LIMIT = 1.0


def perf_case():
    return {"input": [list(range(100_000))], "output": False}


EXPLANATION = """
아이디어: 지금까지 본 값을 set 에 넣어 두고, 새 값이 이미 set 에 있으면 중복입니다.

- 시간 O(n), 공간 O(n)
- 정렬 풀이: 시간 O(n log n), 추가 공간 O(1) (정렬을 제자리에서 할 수 있다면)
면접 포인트: "시간 vs 공간" 트레이드오프를 말해 보세요. 메모리가 아주 제한되면 정렬 풀이가 낫습니다.
"""


def reference(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


def alternative(nums):
    # 파이썬다운 한 줄 풀이
    return len(set(nums)) != len(nums)
