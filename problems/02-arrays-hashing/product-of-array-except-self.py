TITLE = "Product of Array Except Self (자신을 제외한 곱)"
LEVEL = "Medium"
SOURCE = "LeetCode 238"
PATTERN = "누적곱 (prefix · suffix)"

DESCRIPTION = """
정수 배열 nums 가 주어집니다. answer[i] 가 nums[i] 를 제외한 나머지 모든 원소의 곱이 되는 배열을 return 하세요.
나눗셈을 쓰지 말고 O(n) 에 해결하세요.

제한사항
- 2 ≤ len(nums) ≤ 100,000
- -30 ≤ nums[i] ≤ 30 (0 이 들어올 수 있음)

입출력 예
[1, 2, 3, 4]       →  [24, 12, 8, 6]
[-1, 1, 0, -3, 3]  →  [0, 0, 9, 0, 0]
"""

SIGNATURE = "def solution(nums: list[int]) -> list[int]:"

HINTS = [
    "전체 곱 / nums[i] 는 0 이 있으면 깨집니다. 나눗셈 없이 생각해 보세요.",
    "answer[i] = (i 왼쪽 원소들의 곱) × (i 오른쪽 원소들의 곱)",
    "왼쪽에서 오른쪽으로 prefix 곱을 채우고, 오른쪽에서 왼쪽으로 suffix 곱을 곱해 주면 추가 배열 없이 됩니다.",
]

TESTS = [
    {"input": [[1, 2, 3, 4]], "output": [24, 12, 8, 6]},
    {"input": [[-1, 1, 0, -3, 3]], "output": [0, 0, 9, 0, 0]},
    {"input": [[2, 3]], "output": [3, 2]},
    {"input": [[0, 0]], "output": [0, 0]},
    {"input": [[1, 1, 1, 1]], "output": [1, 1, 1, 1]},
    {"input": [[-2, -3, 4]], "output": [-12, -8, 6]},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    return {"input": [[random.choice([-1, 1, 1, 2]) for _ in range(20_000)]], "output": None}


EXPLANATION = """
answer[i] = prefix[i] × suffix[i]

  nums   =  [ 1,  2,  3,  4 ]
  prefix =  [ 1,  1,  2,  6 ]   (i 왼쪽의 곱)
  suffix =  [24, 12,  4,  1 ]   (i 오른쪽의 곱)
  answer =  [24, 12,  8,  6 ]

1. answer 를 prefix 곱으로 채웁니다.
2. 오른쪽부터 running suffix 를 곱해 줍니다.

시간 O(n), 추가 공간 O(1) (출력 배열 제외)
면접 포인트: prefix/suffix 아이디어는 '구간 합(prefix sum)' 과 같은 계열입니다. 0 이 있는 경우를 직접 예로 들어 보세요.
"""


def reference(nums):
    n = len(nums)
    answer = [1] * n
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]
    return answer


def brute_force(nums):
    n = len(nums)
    answer = []
    for i in range(n):
        p = 1
        for j in range(n):
            if j != i:
                p *= nums[j]
        answer.append(p)
    return answer
