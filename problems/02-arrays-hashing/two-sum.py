TITLE = "Two Sum (두 수의 합)"
LEVEL = "Easy"
SOURCE = "LeetCode 1"
PATTERN = "해시맵으로 짝(보수) 찾기"

DESCRIPTION = """
정수 배열 nums 와 정수 target 이 주어집니다.
더해서 target 이 되는 두 원소의 인덱스 [i, j] (i < j) 를 return 하세요.
답은 항상 정확히 하나 존재하며, 같은 원소를 두 번 쓸 수 없습니다.

제한사항
- 2 ≤ len(nums) ≤ 100,000
- -10^9 ≤ nums[i], target ≤ 10^9

입출력 예
nums = [2, 7, 11, 15], target = 9  →  [0, 1]
nums = [3, 2, 4],      target = 6  →  [1, 2]
"""

SIGNATURE = "def solution(nums: list[int], target: int) -> list[int]:"

HINTS = [
    "이중 for 문은 O(n^2) 입니다. n = 100,000 이면 약 50억 번 → 시간 초과.",
    "nums[j] 를 볼 때 필요한 짝은 target - nums[j] 입니다. 그 값을 '이미 본 적 있는지' 빠르게 알 수 있다면?",
    "값 → 인덱스 를 저장하는 dict 를 만들고, 한 번만 훑으면서 짝을 찾으세요. (짝을 먼저 확인한 뒤 자기 자신을 저장)",
]

TESTS = [
    {"input": [[2, 7, 11, 15], 9], "output": [0, 1]},
    {"input": [[3, 2, 4], 6], "output": [1, 2]},
    {"input": [[3, 3], 6], "output": [0, 1]},
    {"input": [[-1, -2, -3, -4, -5], -8], "output": [2, 4]},
    {"input": [[0, 4, 3, 0], 0], "output": [0, 3]},
    {"input": [[1, 5, 1_000_000_000, -1_000_000_000], 0], "output": [2, 3]},
]


def check(result, expected, nums, target):
    return result is not None and sorted(result) == expected


PERF_LIMIT = 1.0


def perf_case():
    n = 100_000
    nums = list(range(1, n + 1))
    return {"input": [nums, (n - 1) + n], "output": [n - 2, n - 1]}


EXPLANATION = """
핵심: "x 와 짝이 되는 값(target - x)을 이미 봤는가?" 를 O(1)에 확인 → 해시맵.

1. seen = {} (값 → 인덱스)
2. 왼쪽부터 보며 need = target - x 가 seen 에 있으면 [seen[need], i] 반환
3. 없으면 seen[x] = i 저장 (먼저 확인하고 저장해야 같은 원소를 두 번 쓰지 않음)

시간 O(n), 공간 O(n)
면접 포인트: 브루트포스 O(n^2) → 정렬 + 투 포인터 O(n log n) (단, 인덱스를 잃음) → 해시맵 O(n) 순서로 개선 과정을 말해 보세요.
"""


def reference(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []


def brute_force(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
