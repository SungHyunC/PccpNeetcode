TITLE = "Counting Bits (0 부터 n 까지 1 비트 개수)"
LEVEL = "Easy"
SOURCE = "LeetCode 338"
PATTERN = "비트 DP: bits[i] = bits[i >> 1] + (i & 1)"

DESCRIPTION = """
정수 n 이 주어집니다. 0 이상 n 이하의 모든 정수 i 에 대해 i 를 2진수로 썼을 때 1 의 개수를 구해,
길이 n + 1 인 리스트로 return 하세요. (answer[i] = i 의 1 비트 개수)

추가 조건: 각 수마다 비트를 하나씩 세지 말고 O(n) 에 풀어 보세요.

제한사항
- 0 ≤ n ≤ 100,000

입출력 예
n = 2  →  [0, 1, 1]
n = 5  →  [0, 1, 1, 2, 1, 2]
"""

SIGNATURE = "def solution(n: int) -> list[int]:"

HINTS = [
    "각 수마다 Number of 1 Bits 를 따로 구하면 O(n log n) 입니다. 이전에 구한 값을 재사용할 수 없을까요?",
    "i >> 1 (i // 2) 은 i 에서 가장 낮은 비트 하나만 뗀 수이고, 이미 계산되어 있습니다.",
    "bits[i] = bits[i >> 1] + (i & 1). 또는 bits[i] = bits[i & (i - 1)] + 1 도 됩니다.",
]

TESTS = [
    {"input": [2], "output": [0, 1, 1]},
    {"input": [5], "output": [0, 1, 1, 2, 1, 2]},
    {"input": [0], "output": [0]},
    {"input": [1], "output": [0, 1]},
    {"input": [8], "output": [0, 1, 1, 2, 1, 2, 2, 3, 1]},
    {"input": [16], "output": [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1]},
]

EXPLANATION = """
핵심: 동적 계획법(DP). 오른쪽으로 한 칸 민 수(i >> 1)의 답은 이미 알고 있습니다.

  i      2진수    i >> 1   i & 1   bits[i]
  5      101      10 (2)    1      bits[2] + 1 = 2
  6      110      11 (3)    0      bits[3] + 0 = 2
  7      111      11 (3)    1      bits[3] + 1 = 3

1. bits = [0] * (n + 1)
2. i = 1..n: bits[i] = bits[i >> 1] + (i & 1)
3. return bits

시간 O(n), 공간 O(n) (결과 제외 O(1))
면접 포인트: 두 가지 점화식을 모두 설명할 수 있으면 좋습니다.
- bits[i >> 1] + (i & 1): 맨 아래 비트를 떼어 냄
- bits[i & (i - 1)] + 1: 가장 낮은 1 비트를 지움
"""


def reference(n):
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)  # 아래 비트 하나를 뗀 수의 답 + 그 비트
    return bits


def alternative(n):
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i & (i - 1)] + 1  # 가장 낮은 1 비트를 지운 수 + 1
    return bits


def brute_force(n):
    return [bin(i).count("1") for i in range(n + 1)]
