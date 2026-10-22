TITLE = "Single Number (혼자인 숫자)"
LEVEL = "Easy"
SOURCE = "LeetCode 136"
PATTERN = "XOR 성질: x ^ x = 0, x ^ 0 = x"

DESCRIPTION = """
정수 배열 nums 에서 딱 하나의 원소만 한 번 등장하고, 나머지 원소는 모두 정확히 두 번씩 등장합니다.
한 번만 등장하는 원소를 return 하세요.

추가 조건: 선형 시간 O(n), 추가 공간 O(1) 로 풀어 보세요.

제한사항
- 1 ≤ len(nums) ≤ 30,000 (항상 홀수)
- -30,000 ≤ nums[i] ≤ 30,000

입출력 예
nums = [2, 2, 1]        →  1
nums = [4, 1, 2, 1, 2]  →  4
nums = [7]              →  7
"""

SIGNATURE = "def solution(nums: list[int]) -> int:"

HINTS = [
    "Counter 나 set 을 쓰면 O(n) 시간이지만 O(n) 공간이 듭니다. 공간 O(1) 이 되려면?",
    "비트 연산 XOR(^) 의 성질을 떠올려 보세요: a ^ a = 0, a ^ 0 = a, 그리고 교환·결합 법칙이 성립합니다.",
    "모든 원소를 XOR 하면 짝을 이룬 값은 서로 지워지고 혼자인 값만 남습니다.",
]

TESTS = [
    {"input": [[2, 2, 1]], "output": 1},
    {"input": [[4, 1, 2, 1, 2]], "output": 4},
    {"input": [[7]], "output": 7},
    {"input": [[-1, 5, 5]], "output": -1},
    {"input": [[0, 3, 3]], "output": 0},
    {"input": [[30000, -30000, -30000, 9, 9]], "output": 30000},
    {"input": [[1, 2, 3, 4, 3, 2, 1]], "output": 4},
]

EXPLANATION = """
핵심: XOR 은 같은 값끼리 지워지는(a ^ a = 0) 연산이고 순서와 무관합니다.

  4 ^ 1 ^ 2 ^ 1 ^ 2
= 4 ^ (1 ^ 1) ^ (2 ^ 2)
= 4 ^ 0 ^ 0
= 4

1. result = 0
2. 모든 x 에 대해 result ^= x
3. return result

비트 단위로 보면: 각 비트 자리마다 1 의 개수를 2 로 나눈 나머지가 남습니다.
짝으로 나온 값은 각 자리에 1 을 짝수 번 더하므로 사라집니다. 음수도 파이썬에서 그대로 동작합니다.

시간 O(n), 공간 O(1)
면접 포인트: Counter(O(n) 공간) → 합 트릭 2*sum(set) - sum(nums) (O(n) 공간) → XOR (O(1) 공간) 순서로 개선을 말하세요.
변형: '나머지는 세 번씩 등장' (LeetCode 137) 이면 비트 자리별 개수를 3 으로 나눈 나머지를 씁니다.
"""


def reference(nums):
    result = 0
    for x in nums:
        result ^= x  # 짝을 이룬 값은 서로 지워짐
    return result


def alternative(nums):
    # 합 트릭: 모든 값이 두 번씩 있다면 합은 2 * sum(set) 이 됨
    return 2 * sum(set(nums)) - sum(nums)


def brute_force(nums):
    from collections import Counter
    for x, c in Counter(nums).items():
        if c == 1:
            return x
