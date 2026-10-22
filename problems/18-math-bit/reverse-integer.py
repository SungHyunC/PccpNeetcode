TITLE = "Reverse Integer (정수 뒤집기)"
LEVEL = "Medium"
SOURCE = "LeetCode 7"
PATTERN = "자릿수 분해(% 10, // 10) + 32비트 범위 검사"

DESCRIPTION = """
32비트 부호 있는 정수 x 가 주어집니다. x 의 숫자 자릿수를 거꾸로 뒤집은 값을 return 하세요.
부호는 그대로 유지합니다. 뒤집은 결과가 32비트 부호 있는 정수 범위 [-2^31, 2^31 - 1] 을 벗어나면 0 을 return 하세요.

(C++/Java 처럼 64비트 정수를 쓸 수 없는 환경을 가정한 문제입니다. 파이썬은 정수에 크기 제한이 없으므로
범위를 직접 검사해야 합니다.)

제한사항
- -2^31 ≤ x ≤ 2^31 - 1

입출력 예
x = 123          →  321
x = -123         →  -321
x = 120          →  21    (앞자리 0 은 사라짐)
x = 1534236469   →  0     (9646324351 은 2^31 - 1 = 2147483647 보다 큼)
"""

SIGNATURE = "def solution(x: int) -> int:"

HINTS = [
    "부호를 먼저 떼어 내고(sign), 절댓값만 뒤집은 뒤 다시 부호를 붙이면 편합니다.",
    "문자열로 뒤집기: int(str(abs(x))[::-1]). 숫자로 뒤집기: digit = x % 10, x //= 10, rev = rev * 10 + digit.",
    "결과가 -2**31 ≤ rev ≤ 2**31 - 1 인지 확인하세요. (주의: 파이썬에서 음수에 % 와 // 를 쓰면 C 와 결과가 다릅니다. 절댓값으로 처리하세요.)",
]

TESTS = [
    {"input": [123], "output": 321},
    {"input": [-123], "output": -321},
    {"input": [120], "output": 21},
    {"input": [0], "output": 0},
    {"input": [1534236469], "output": 0},
    {"input": [-2147483648], "output": 0},
    {"input": [2147483647], "output": 0},
    {"input": [1463847412], "output": 2147483641},
    {"input": [-1463847412], "output": -2147483641},
    {"input": [-1563847412], "output": 0},
    {"input": [-10], "output": -1},
]

EXPLANATION = """
핵심: 자릿수를 하나씩 떼어(x % 10) 결과의 뒤에 붙이고(rev * 10 + d), 마지막에 32비트 범위를 검사합니다.

  x = 123
  d=3 → rev=3, x=12
  d=2 → rev=32, x=1
  d=1 → rev=321, x=0

1. sign = -1 if x < 0 else 1, x = abs(x)
2. while x: rev = rev * 10 + x % 10; x //= 10
3. rev *= sign
4. 범위 [-2^31, 2^31-1] 밖이면 0

경계값: 2^31 - 1 = 2147483647, -2^31 = -2147483648
  -2147483648 을 뒤집으면 -8463847412 → 범위 밖 → 0
  1463847412 를 뒤집으면 2147483641 → 범위 안 (경계 바로 아래)

시간 O(자릿수) = O(log10 x), 공간 O(1)
면접 포인트:
- 64비트를 못 쓰는 환경이라면 rev * 10 + d 를 하기 '전에' rev > (2^31-1) // 10 인지 미리 검사해 오버플로를 막아야 합니다.
- 파이썬의 음수 나머지: -123 % 10 == 7, -123 // 10 == -13 (내림). C/Java 는 -3, -12 (0 방향 버림). 그래서 절댓값으로 처리합니다.
"""

def reference(x):
    sign = -1 if x < 0 else 1
    x = abs(x)  # 파이썬 음수 % 는 C 와 달라서 절댓값으로 처리
    rev = 0
    while x:
        rev = rev * 10 + x % 10  # 마지막 자리를 떼어 뒤에 붙임
        x //= 10
    rev *= sign
    return rev if -(2**31) <= rev <= 2**31 - 1 else 0


def alternative(x):
    # 32비트 환경 흉내: 곱하기 전에 오버플로를 미리 검사 (양수 기준으로 처리)
    limit = 2**31 - 1 if x >= 0 else 2**31  # 음수 쪽은 절댓값 2^31 까지 허용
    sign = -1 if x < 0 else 1
    x = abs(x)
    rev = 0
    while x:
        d = x % 10
        if rev > (limit - d) // 10:  # rev * 10 + d > limit 이면 넘침
            return 0
        rev = rev * 10 + d
        x //= 10
    return sign * rev


def brute_force(x):
    s = str(abs(x))[::-1]
    rev = int(s) * (-1 if x < 0 else 1)
    return rev if -(2**31) <= rev <= 2**31 - 1 else 0
