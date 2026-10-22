TITLE = "GCD and LCM of Array (배열의 최대공약수와 최소공배수)"
LEVEL = "Easy"
SOURCE = "프로그래머스 Lv.2 'N개의 최소공배수' 유형"
PATTERN = "유클리드 호제법 gcd(a, b) = gcd(b, a % b), lcm = a * b // gcd"

DESCRIPTION = """
양의 정수 배열 nums 가 주어집니다. nums 에 있는 모든 수의 최대공약수(GCD)와 최소공배수(LCM)를 구해
[gcd, lcm] 형태로 return 하세요.

제한사항
- 1 ≤ len(nums) ≤ 100
- 1 ≤ nums[i] ≤ 100
- 파이썬 정수는 크기 제한이 없으므로 LCM 이 아무리 커도 그대로 return 하면 됩니다.

입출력 예
nums = [2, 6, 8, 14]  →  [2, 168]
nums = [1, 2, 3]      →  [1, 6]
nums = [7]            →  [7, 7]
"""

SIGNATURE = "def solution(nums: list[int]) -> list[int]:"

HINTS = [
    "여러 수의 GCD/LCM 은 두 수씩 차례로 합치면 됩니다: gcd(a, b, c) = gcd(gcd(a, b), c).",
    "유클리드 호제법: gcd(a, b) = gcd(b, a % b), b 가 0 이 되면 a 가 답입니다.",
    "lcm(a, b) = a * b // gcd(a, b). (a // gcd * b 순서로 계산하면 중간값이 작아집니다.) 실전에서는 math.gcd 를 쓰세요.",
]

TESTS = [
    {"input": [[2, 6, 8, 14]], "output": [2, 168]},
    {"input": [[1, 2, 3]], "output": [1, 6]},
    {"input": [[7]], "output": [7, 7]},
    {"input": [[12, 18, 24]], "output": [6, 72]},
    {"input": [[5, 5, 5]], "output": [5, 5]},
    {"input": [[1]], "output": [1, 1]},
    {"input": [[97, 89, 83]], "output": [1, 716539]},
    {"input": [[100, 75, 50, 25]], "output": [25, 300]},
    {"input": [list(range(1, 21))], "output": [1, 232792560]},
]

EXPLANATION = """
핵심: 유클리드 호제법(Euclidean algorithm)으로 두 수의 GCD 를 O(log min(a, b)) 에 구하고, 배열 전체로 확장합니다.

  gcd(48, 18)
  = gcd(18, 48 % 18 = 12)
  = gcd(12, 18 % 12 = 6)
  = gcd(6, 12 % 6 = 0)
  = 6

  lcm(a, b) = a * b // gcd(a, b)   → lcm(48, 18) = 48 * 18 // 6 = 144

1. g = nums[0], l = nums[0]
2. 나머지 x 마다: g = gcd(g, x), l = l * x // gcd(l, x)
3. return [g, l]

시간 O(n log M) (M = 값의 크기), 공간 O(1)
실전 포인트:
- math.gcd(a, b) 는 3.5+, 여러 인자 math.gcd(*nums) 와 math.lcm(*nums) 는 3.9+ 에서 지원됩니다.
- functools.reduce(math.gcd, nums) 로 한 줄에 끝낼 수도 있습니다.
- C++/Java 는 lcm 계산 중 a * b 가 오버플로할 수 있어 a / gcd * b 순서로 계산합니다.
- 분수 약분, 격자 위 선분이 지나는 점 개수(gcd(dx, dy)), 주기 맞추기 등에 자주 나옵니다.
"""


def reference(nums):
    def gcd(a, b):
        while b:
            a, b = b, a % b  # 유클리드 호제법
        return a

    g = l = nums[0]
    for x in nums[1:]:
        g = gcd(g, x)
        l = l // gcd(l, x) * x  # 나눗셈을 먼저 해서 중간값을 줄임
    return [g, l]


def alternative(nums):
    import math
    from functools import reduce
    g = reduce(math.gcd, nums)
    l = reduce(lambda a, b: a * b // math.gcd(a, b), nums)
    return [g, l]
