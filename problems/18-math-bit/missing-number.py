TITLE = "Missing Number (빠진 숫자)"
LEVEL = "Easy"
SOURCE = "LeetCode 268"
PATTERN = "가우스 합 공식 / XOR 로 짝 지우기"

DESCRIPTION = """
0 부터 n 까지의 서로 다른 정수 n + 1 개 중 딱 하나가 빠진, 길이 n 인 배열 nums 가 주어집니다.
빠진 정수를 return 하세요. (nums 는 정렬되어 있지 않습니다.)

추가 조건: 추가 공간 O(1), 시간 O(n) 으로 풀어 보세요.

제한사항
- 1 ≤ n = len(nums) ≤ 10,000
- 0 ≤ nums[i] ≤ n, 모든 값은 서로 다름

입출력 예
nums = [3, 0, 1]                     →  2
nums = [0, 1]                        →  2
nums = [9, 6, 4, 2, 3, 5, 7, 0, 1]   →  8
"""

SIGNATURE = "def solution(nums: list[int]) -> int:"

HINTS = [
    "set 에 넣고 0..n 을 확인하면 O(n) 공간입니다. 공간 없이 '빠진 것' 을 알아내려면?",
    "0 + 1 + ... + n = n(n+1)/2 입니다. 실제 합과의 차이는?",
    "XOR 방법: 0..n 의 모든 인덱스와 nums 의 모든 값을 XOR 하면 짝이 있는 값은 지워지고 빠진 값만 남습니다.",
]

TESTS = [
    {"input": [[3, 0, 1]], "output": 2},
    {"input": [[0, 1]], "output": 2},
    {"input": [[9, 6, 4, 2, 3, 5, 7, 0, 1]], "output": 8},
    {"input": [[0]], "output": 1},
    {"input": [[1]], "output": 0},
    {"input": [[1, 2, 3, 4]], "output": 0},
    {"input": [[2, 0, 3, 1, 5]], "output": 4},
]

EXPLANATION = """
핵심: 있어야 할 것(0..n)과 실제 있는 것(nums)의 '차이' 가 답입니다.

[방법 1] 합 공식
  기대 합 = n(n+1)/2, 답 = 기대 합 - sum(nums)
  nums = [3, 0, 1], n = 3 → 6 - 4 = 2

[방법 2] XOR
  result = n, 그리고 i = 0..n-1 에 대해 result ^= i ^ nums[i]
  0..n 과 nums 를 모두 XOR 하면 둘 다에 있는 값은 두 번 등장해 지워지고, 빠진 값만 한 번 남습니다.

시간 O(n), 공간 O(1)
면접 포인트: C++/Java 에서는 합 공식이 오버플로 위험이 있어 XOR 방법을 선호한다는 점을 언급하세요.
파이썬은 정수 크기 제한이 없어 합 공식도 안전합니다. 정렬 O(n log n), set O(n) 공간 방법과 비교해 보세요.
"""


def reference(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)  # 기대 합 - 실제 합


def alternative(nums):
    result = len(nums)
    for i, x in enumerate(nums):
        result ^= i ^ x  # 인덱스와 값이 짝지어 지워짐
    return result


def brute_force(nums):
    seen = set(nums)
    for x in range(len(nums) + 1):
        if x not in seen:
            return x
