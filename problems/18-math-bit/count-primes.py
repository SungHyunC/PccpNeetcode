TITLE = "Count Primes (소수 개수 세기)"
LEVEL = "Medium"
SOURCE = "LeetCode 204"
PATTERN = "에라토스테네스의 체 (sieve of Eratosthenes)"

DESCRIPTION = """
정수 n 이 주어집니다. n 보다 작은(엄격히 작은) 소수의 개수를 return 하세요.
소수는 1 과 자기 자신만을 약수로 갖는 2 이상의 정수입니다.

제한사항
- 0 ≤ n ≤ 5,000,000

입출력 예
n = 10  →  4   (2, 3, 5, 7)
n = 0   →  0
n = 1   →  0
n = 3   →  1   (2 만 해당, 3 은 n 보다 작지 않음)
"""

SIGNATURE = "def solution(n: int) -> int:"

HINTS = [
    "각 수마다 √k 까지 나눠 보는 소수 판별은 O(n√n) 입니다. n = 5,000,000 이면 시간 초과입니다.",
    "에라토스테네스의 체: 2 부터 보면서 아직 지워지지 않은 수 p 는 소수이고, p 의 배수를 모두 지웁니다.",
    "p 의 배수는 p*p 부터 지우면 됩니다 (그보다 작은 배수는 더 작은 소수가 이미 지웠음). p 는 √n 까지만 보면 충분합니다.",
    "파이썬에서는 bytearray 와 슬라이스 대입 is_prime[p*p::p] = bytes(len(range(p*p, n, p))) 가 이중 for 문보다 훨씬 빠릅니다.",
]

TESTS = [
    {"input": [10], "output": 4},
    {"input": [0], "output": 0},
    {"input": [1], "output": 0},
    {"input": [2], "output": 0},
    {"input": [3], "output": 1},
    {"input": [100], "output": 25},
    {"input": [1000], "output": 168},
    {"input": [100_000], "output": 9592},
]

PERF_LIMIT = 2.0


def perf_case():
    return {"input": [5_000_000], "output": 348513}


EXPLANATION = """
핵심: 소수를 '판별' 하지 말고, 합성수를 '지워 나갑니다'. (에라토스테네스의 체)

  n = 30,  □ = 남은 수(소수 후보), × = 지움
  p=2: 4 6 8 10 12 ... 지움
  p=3: 9 15 21 27 지움 (6, 12... 는 이미 지워짐 → 3*3=9 부터)
  p=5: 25 지움
  p=6 → 6*6=36 > 30 이므로 종료.  남은 수: 2 3 5 7 11 13 17 19 23 29 → 10개

1. n < 3 이면 0
2. is_prime = [1] * n, is_prime[0] = is_prime[1] = 0
3. p = 2 .. √n: is_prime[p] 이면 p*p, p*p+p, ... 를 0 으로
4. return sum(is_prime)

시간 O(n log log n), 공간 O(n)
파이썬 실전 팁:
- bytearray + 슬라이스 대입은 C 레벨에서 동작해 일반 리스트 이중 for 문보다 10배 이상 빠릅니다.
- 소수 판별을 여러 번 하거나 범위 안 소수 목록이 필요하면 체를 한 번 만들어 두고 재사용하세요.
- 수 하나만 판별할 때는 √k 까지 나누기(O(√k))가 간단합니다. PCCP 의 'k진수에서 소수 개수 구하기' 처럼
  수가 매우 크고 개수가 적을 때는 체 대신 √k 판별을 씁니다.
"""


def reference(n):
    if n < 3:
        return 0
    is_prime = bytearray([1]) * n  # 0 ~ n-1
    is_prime[0] = is_prime[1] = 0
    p = 2
    while p * p < n:
        if is_prime[p]:
            # p*p 부터 p 간격으로 모두 지움 (슬라이스 대입으로 빠르게)
            is_prime[p * p :: p] = bytes(len(range(p * p, n, p)))
        p += 1
    return sum(is_prime)


def alternative(n):
    # 리스트 + 이중 for 문 버전 (원리는 같지만 파이썬에서는 느림)
    if n < 3:
        return 0
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            for multiple in range(p * p, n, p):
                is_prime[multiple] = False
    return sum(is_prime)


def brute_force(n):
    # 수마다 √k 까지 나눠 보는 판별: O(n√n)
    def is_prime(k):
        if k < 2:
            return False
        d = 2
        while d * d <= k:
            if k % d == 0:
                return False
            d += 1
        return True

    return sum(1 for k in range(n) if is_prime(k))
