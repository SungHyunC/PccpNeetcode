TITLE = "Number of 1 Bits (1 비트 개수)"
LEVEL = "Easy"
SOURCE = "LeetCode 191"
PATTERN = "n & (n - 1) 로 가장 낮은 1 비트 지우기"

DESCRIPTION = """
음이 아닌 정수 n 이 주어집니다. n 을 2진수로 나타냈을 때 1 인 비트의 개수(해밍 무게, Hamming weight)를 return 하세요.

제한사항
- 0 ≤ n ≤ 2^32 - 1

입출력 예
n = 11 (2진수 1011)          →  3
n = 128 (2진수 10000000)     →  1
n = 4294967293 (2진수 11111111111111111111111111111101)  →  31
"""

SIGNATURE = "def solution(n: int) -> int:"

HINTS = [
    "가장 쉬운 방법: bin(n).count('1'). 면접에서는 비트 연산으로 직접 구현해 보라고 합니다.",
    "n & 1 은 가장 낮은 비트, n >>= 1 은 오른쪽으로 한 칸 밀기입니다. 이것으로 32번 반복할 수 있습니다.",
    "더 빠른 방법: n & (n - 1) 은 n 의 가장 낮은 1 비트 하나를 0 으로 만듭니다. n 이 0 이 될 때까지 몇 번 반복되는지 세세요.",
]

TESTS = [
    {"input": [11], "output": 3},
    {"input": [128], "output": 1},
    {"input": [4294967293], "output": 31},
    {"input": [0], "output": 0},
    {"input": [1], "output": 1},
    {"input": [4294967295], "output": 32},
    {"input": [2147483648], "output": 1},
    {"input": [255], "output": 8},
]

EXPLANATION = """
핵심: n & (n - 1) 은 n 의 '가장 낮은 1 비트' 를 지웁니다.

  n       = 1011 1000
  n - 1   = 1011 0111   (가장 낮은 1 이 0 이 되고, 그 아래 0 들은 1 이 됨)
  n & n-1 = 1011 0000   → 가장 낮은 1 하나가 사라짐

1. count = 0
2. while n: n &= n - 1; count += 1
3. return count

반복 횟수 = 1 비트 개수 (최대 32번)

시간 O(1의 개수) ≤ O(32), 공간 O(1)
면접 포인트:
- 시프트 방식(n & 1, n >>= 1)은 항상 비트 길이만큼 돌고, n & (n-1) 방식은 1 의 개수만큼만 돕니다.
- 파이썬에서는 bin(n).count("1") 이나 n.bit_count() (3.10+) 가 실전에서 가장 빠르고 간단합니다.
- n & (n - 1) == 0 이면 n 은 2의 거듭제곱(n > 0 일 때)이라는 것도 같이 기억하세요.
- C++/Java 에서는 음수 입력이 2의 보수로 들어오지만, 파이썬 정수는 무한 비트라 음수면 n & 0xFFFFFFFF 로 32비트로 잘라야 합니다.
"""


def reference(n):
    count = 0
    while n:
        n &= n - 1  # 가장 낮은 1 비트 제거
        count += 1
    return count


def alternative(n):
    # 한 비트씩 확인하는 방법
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


def brute_force(n):
    return bin(n).count("1")
