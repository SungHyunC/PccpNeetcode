TITLE = "Pow(x, n) (빠른 거듭제곱)"
LEVEL = "Medium"
SOURCE = "LeetCode 50"
PATTERN = "분할 정복 거듭제곱 (exponentiation by squaring)"

DESCRIPTION = """
실수 x 와 정수 n 이 주어질 때 x 의 n 제곱(x^n)을 계산해 return 하세요.
단, 연습을 위해 ** 연산자, pow(), math.pow() 를 쓰지 말고 직접 구현하세요.

n 이 음수이면 x^n = 1 / x^(-n) 입니다. 결과는 실수(float)이며 상대 오차 10^-6 이내면 정답입니다.

제한사항
- -100.0 < x < 100.0
- -2^31 ≤ n ≤ 2^31 - 1
- n < 0 이면 x ≠ 0
- 결과의 절댓값은 10^4 이하이거나 0 에 매우 가깝습니다.

입출력 예
x = 2.0, n = 10   →  1024.0
x = 2.1, n = 3    →  9.261
x = 2.0, n = -2   →  0.25
x = 1.0, n = -2147483648  →  1.0   (n 번 곱하면 시간 초과!)
"""

SIGNATURE = "def solution(x: float, n: int) -> float:"

COMPARE = "float"

HINTS = [
    "x 를 n 번 곱하면 O(n) 입니다. n 이 20억이면 시간 초과입니다.",
    "x^10 = (x^5)^2, x^5 = x · (x^2)^2. 지수를 반으로 줄이면 O(log n) 이 됩니다.",
    "반복문 버전: n 을 2진수로 보고, 맨 아래 비트가 1 이면 result *= x, 매 단계 x *= x, n >>= 1.",
    "음수 n 은 x = 1 / x, n = -n 으로 바꿔서 처리하세요. (파이썬은 -(-2^31) 도 오버플로가 없습니다.)",
]

TESTS = [
    {"input": [2.0, 10], "output": 1024.0},
    {"input": [2.1, 3], "output": 9.261},
    {"input": [2.0, -2], "output": 0.25},
    {"input": [1.0, -2147483648], "output": 1.0},
    {"input": [-1.0, 2147483647], "output": -1.0},
    {"input": [5.0, 0], "output": 1.0},
    {"input": [0.0, 5], "output": 0.0},
    {"input": [-2.0, 3], "output": -8.0},
    {"input": [0.5, -3], "output": 8.0},
    {"input": [1.00001, 123456], "output": 3.4368447520907104},
]

PERF_LIMIT = 1.0


def perf_case():
    # 약 2억 번 곱하는 O(n) 풀이는 시간 초과, O(log n) 은 즉시 끝남
    return {"input": [1.00000001, 200_000_000], "output": None}


EXPLANATION = """
핵심: 지수를 반씩 줄이는 분할 정복. x^n 을 O(log n) 번의 곱셈으로 계산합니다.

  n 이 짝수: x^n = (x^2)^(n/2)
  n 이 홀수: x^n = x · (x^2)^((n-1)/2)

반복문(2진수) 관점: n = 13 = 1101(2) 이면 x^13 = x^8 · x^4 · x^1
  비트    x 의 거듭제곱    result
  1       x^1             x
  0       x^2             x        (곱하지 않음)
  1       x^4             x^5
  1       x^8             x^13

1. n < 0 이면 x = 1/x, n = -n
2. result = 1.0
3. while n: (n & 1 이면 result *= x), x *= x, n >>= 1
4. return result

시간 O(log n), 공간 O(1) (재귀 버전은 O(log n) 스택)
면접 포인트:
- Java/C++ 에서는 n = -2^31 을 -n 하면 오버플로 → long 으로 바꿔야 함. 파이썬은 문제없음.
- 같은 원리로 모듈러 거듭제곱 pow(a, b, m), 행렬 거듭제곱(피보나치 O(log n))을 구현합니다.
"""


def reference(x, n):
    if n < 0:
        x, n = 1 / x, -n  # 음수 지수 → 역수의 양수 지수
    result = 1.0
    while n:
        if n & 1:  # 현재 비트가 1 이면 지금의 x(= 원래 x 의 2^k 제곱)를 곱함
            result *= x
        x *= x  # x^(2^k) → x^(2^(k+1))
        n >>= 1
    return result


def alternative(x, n):
    # 재귀 분할 정복: half 를 한 번만 계산하는 것이 핵심 (두 번 부르면 O(n))
    def power(base, e):
        if e == 0:
            return 1.0
        half = power(base, e // 2)
        return half * half if e % 2 == 0 else half * half * base

    if n < 0:
        return 1 / power(x, -n)
    return power(x, n)
