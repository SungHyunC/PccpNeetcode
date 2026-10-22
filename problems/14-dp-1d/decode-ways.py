TITLE = "Decode Ways (숫자 암호 해독 경우의 수)"
LEVEL = "Medium"
SOURCE = "LeetCode 91"
PATTERN = "한 글자/두 글자 끊기 DP (조건부 피보나치)"

DESCRIPTION = """
알파벳 대문자를 숫자로 바꾸는 암호가 있습니다: A → "1", B → "2", ..., Z → "26".
여러 글자를 바꾼 숫자들을 이어 붙인 문자열 s 가 주어질 때,
s 를 원래 글자들로 되돌리는(끊어 읽는) 방법의 수를 return 하세요.
"06" 처럼 0으로 시작하는 조각은 어떤 글자에도 대응하지 않으므로 사용할 수 없습니다.
해독할 수 없으면 0 을 return 합니다.

제한사항
- 1 ≤ len(s) ≤ 100
- s 는 숫자('0'~'9')로만 이루어져 있으며, 0 으로 시작할 수도 있습니다.

입출력 예
s = "12"   →  2   ("1"+"2" = AB, "12" = L)
s = "226"  →  3   (2|2|6, 22|6, 2|26)
s = "06"   →  0
"""

SIGNATURE = "def solution(s: str) -> int:"

HINTS = [
    "앞에서부터 i 글자까지 해독하는 방법의 수를 생각하세요. 마지막 조각은 1글자 또는 2글자입니다.",
    "마지막 1글자 s[i-1] 이 '1'~'9' 이면 dp[i-1] 을 더하고, 마지막 2글자 s[i-2:i] 가 '10'~'26' 이면 dp[i-2] 를 더합니다.",
    "dp[0] = 1 (빈 문자열을 해독하는 방법 1가지). '0' 은 단독으로 못 쓰고 '10', '20' 의 일부로만 쓸 수 있다는 점이 핵심 함정입니다.",
]

TESTS = [
    {"input": ["12"], "output": 2},
    {"input": ["226"], "output": 3},
    {"input": ["06"], "output": 0},
    {"input": ["0"], "output": 0},
    {"input": ["1"], "output": 1},
    {"input": ["10"], "output": 1},
    {"input": ["2101"], "output": 1},
    {"input": ["11106"], "output": 2},
    {"input": ["27"], "output": 1},
    {"input": ["100"], "output": 0},
    {"input": ["1" * 40], "output": 165580141},
]

EXPLANATION = """
아이디어
- s[:i] 를 해독하는 마지막 조각은 '1글자' 또는 '2글자' 입니다 → 계단 오르기와 같은 구조.
- 단, 조각이 유효할 때만 더합니다: 1글자는 '1'~'9', 2글자는 '10'~'26'.

DP 레시피
1. 상태 정의: dp[i] = 앞 i 글자 s[:i] 를 해독하는 방법의 수
2. 점화식:
     dp[i] = (dp[i-1] if s[i-1] != '0' else 0)
           + (dp[i-2] if i >= 2 and 10 <= int(s[i-2:i]) <= 26 else 0)
3. 초기값:   dp[0] = 1 (빈 문자열)
4. 계산 순서: i = 1 → n
5. 답:       dp[n]

  s  = "2 2 6"
  i  : 0  1  2  3
  dp : 1  1  2  3      dp[3] = dp[2]('6' 유효) + dp[1]('26' 유효) = 2 + 1

복잡도: 시간 O(n), 공간 O(1) (직전 두 값만 사용)

면접 포인트
- "0" 처리 질문을 먼저 하세요: '0' 단독 불가, '30'/'00' 불가, '10'/'20' 만 가능.
- 중간에 dp 값이 0 이 되면 이후 전부 0 이 되므로 일찍 return 해도 됩니다.
- top-down(재귀 + 메모)로 먼저 설명하고 바텀업으로 바꾸는 흐름도 좋습니다. (alternative 참고)
"""


def reference(s):
    # prev2 = dp[i-2], prev1 = dp[i-1]
    prev2, prev1 = 0, 1  # dp[-1] 은 쓰이지 않음, dp[0] = 1
    for i in range(1, len(s) + 1):
        cur = 0
        if s[i - 1] != "0":  # 마지막 1글자가 유효
            cur += prev1
        if i >= 2 and 10 <= int(s[i - 2:i]) <= 26:  # 마지막 2글자가 유효
            cur += prev2
        prev2, prev1 = prev1, cur
    return prev1


def alternative(s):
    # top-down: ways(i) = s[i:] 를 해독하는 방법의 수
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def ways(i):
        if i == len(s):
            return 1
        if s[i] == "0":
            return 0
        total = ways(i + 1)
        if i + 1 < len(s) and int(s[i:i + 2]) <= 26:
            total += ways(i + 2)
        return total

    return ways(0)
