TITLE = "Longest Palindromic Substring (가장 긴 팰린드롬 부분 문자열)"
LEVEL = "Medium"
SOURCE = "LeetCode 5"
PATTERN = "중심 확장(expand around center) / 구간 DP is_pal[i][j]"

DESCRIPTION = """
문자열 s 가 주어집니다.
s 의 연속된 부분 문자열 중 앞에서 읽으나 뒤에서 읽으나 같은(팰린드롬) 가장 긴 것을 return 하세요.
길이가 같은 답이 여러 개라면 그중 아무거나 return 해도 됩니다.

제한사항
- 1 ≤ len(s) ≤ 1,000
- s 는 영어 대소문자와 숫자로만 이루어져 있음

입출력 예
s = "babad"  →  "bab"   ("aba" 도 정답)
s = "cbbd"   →  "bb"
s = "a"      →  "a"
"""

SIGNATURE = "def solution(s: str) -> str:"

HINTS = [
    "모든 부분 문자열(O(n^2))을 만들어 팰린드롬인지 검사(O(n))하면 O(n^3) 입니다. 검사 결과를 재활용할 방법이 있을까요?",
    "팰린드롬은 가운데에서 바깥으로 대칭입니다. s[i..j] 가 팰린드롬 ⇔ s[i] == s[j] 이고 s[i+1..j-1] 이 팰린드롬.",
    "각 위치를 중심으로 양쪽으로 넓혀 가세요. 중심은 홀수 길이(i, i)와 짝수 길이(i, i+1) 두 종류가 있습니다. 총 O(n^2), 추가 공간 O(1).",
]

TESTS = [
    {"input": ["babad"], "output": "bab"},
    {"input": ["cbbd"], "output": "bb"},
    {"input": ["a"], "output": "a"},
    {"input": ["ac"], "output": "a"},
    {"input": ["forgeeksskeegfor"], "output": "geeksskeeg"},
    {"input": ["aaaa"], "output": "aaaa"},
    {"input": ["abacdfgdcaba"], "output": "aba"},
    {"input": ["racecarXY"], "output": "racecar"},
]


def check(result, expected, s):
    # 같은 길이의 팰린드롬이면서 s 의 부분 문자열이면 정답
    return (
        isinstance(result, str)
        and len(result) == len(expected)
        and result in s
        and result == result[::-1]
    )


EXPLANATION = """
아이디어 1 — 중심 확장 (reference)
- 모든 팰린드롬에는 중심이 있습니다. 홀수 길이는 글자 하나, 짝수 길이는 글자 사이.
- 중심 후보는 2n - 1 개. 각 중심에서 s[l] == s[r] 인 동안 l -= 1, r += 1 로 넓힙니다.

  s = "b a b a d"   (인덱스 0 1 2 3 4)
  중심 1('a') : (1,1) → (0,2) 'b'=='b' → (-1,3) 범위 밖에서 멈춤 → s[0..2] = "bab"
  중심 2('b') : (2,2) → (1,3) 'a'=='a' → (0,4) 'b'!='d' 에서 멈춤 → s[1..3] = "aba"
  중심 (1,2)  : 'a'!='b' → 짝수 길이 팰린드롬 없음

아이디어 2 — 구간 DP (alternative)
1. 상태 정의: is_pal[i][j] = s[i..j] 가 팰린드롬인가
2. 점화식:   is_pal[i][j] = (s[i] == s[j]) and (j - i < 2 or is_pal[i+1][j-1])
3. 초기값:   길이 1 은 모두 True
4. 계산 순서: is_pal[i+1][j-1] 이 먼저 필요 → i 를 n-1 → 0 으로(또는 길이 순으로)
5. 답:       True 인 칸 중 j - i 가 최대인 구간

         j→ b  a  b  a  d
     i↓ b   T  F  T  F  F
        a      T  F  T  F
        b         T  F  F
        a            T  F
        d               T

복잡도
- 중심 확장: 시간 O(n^2), 공간 O(1)
- 구간 DP:   시간 O(n^2), 공간 O(n^2)
- (참고) Manacher 알고리즘은 O(n) 이지만 면접에서는 중심 확장이면 충분합니다.

면접 포인트
- 짝수 길이 중심을 빠뜨리는 실수가 가장 흔합니다 ("cbbd" → "bb").
- 구간 DP 를 설명할 때 "짧은 구간이 먼저 계산되어야 한다" 는 계산 순서를 꼭 언급하세요.
- 부분 문자열(substring, 연속)과 부분 수열(subsequence, 비연속) 문제를 구분하세요.
  최장 팰린드롬 부분 '수열' 은 LCS(s, reversed(s)) 로 풀 수 있는 다른 문제입니다.
"""


def reference(s):
    n = len(s)
    best_l, best_r = 0, 0  # 가장 긴 팰린드롬 구간 [best_l, best_r]

    def expand(l, r):
        # s[l..r] 이 팰린드롬인 동안 양쪽으로 넓힌 뒤, 마지막으로 유효한 구간 반환
        while l >= 0 and r < n and s[l] == s[r]:
            l -= 1
            r += 1
        return l + 1, r - 1

    for center in range(n):
        for l, r in (expand(center, center), expand(center, center + 1)):  # 홀수, 짝수
            if r - l > best_r - best_l:
                best_l, best_r = l, r
    return s[best_l:best_r + 1]


def alternative(s):
    # 구간 DP: is_pal[i][j] = s[i..j] 가 팰린드롬인가
    n = len(s)
    is_pal = [[False] * n for _ in range(n)]
    best_l, best_r = 0, 0
    for i in range(n - 1, -1, -1):  # i+1 행이 먼저 계산되도록 아래에서 위로
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1]):
                is_pal[i][j] = True
                if j - i > best_r - best_l:
                    best_l, best_r = i, j
    return s[best_l:best_r + 1]
