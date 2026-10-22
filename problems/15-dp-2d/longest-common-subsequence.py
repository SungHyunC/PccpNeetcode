TITLE = "Longest Common Subsequence (최장 공통 부분 수열)"
LEVEL = "Medium"
SOURCE = "LeetCode 1143"
PATTERN = "두 문자열 2차원 DP: 같으면 대각선 + 1, 다르면 max(위, 왼쪽)"

DESCRIPTION = """
두 문자열 text1, text2 가 주어집니다.
각 문자열에서 글자 몇 개를 지워(순서는 유지) 만들 수 있는 문자열을 부분 수열이라고 합니다.
두 문자열에 공통으로 존재하는 부분 수열 중 가장 긴 것의 길이를 return 하세요.
공통 부분 수열이 없으면 0 을 return 합니다.

제한사항
- 0 ≤ len(text1), len(text2) ≤ 1,000
- 영어 대소문자로만 이루어져 있음

입출력 예
text1 = "abcde", text2 = "ace"  →  3   ("ace")
text1 = "abc",   text2 = "abc"  →  3
text1 = "abc",   text2 = "def"  →  0
"""

SIGNATURE = "def solution(text1: str, text2: str) -> int:"

HINTS = [
    "두 문자열의 '앞부분' 끼리의 답을 생각하세요: dp[i][j] = text1[:i] 와 text2[:j] 의 LCS 길이.",
    "마지막 글자 text1[i-1] 과 text2[j-1] 이 같으면 그 글자를 LCS 에 넣을 수 있습니다 → dp[i-1][j-1] + 1.",
    "다르면 둘 중 하나의 마지막 글자는 버려야 합니다 → max(dp[i-1][j], dp[i][j-1]). (n+1)×(m+1) 표, 0행·0열은 0.",
]

TESTS = [
    {"input": ["abcde", "ace"], "output": 3},
    {"input": ["abc", "abc"], "output": 3},
    {"input": ["abc", "def"], "output": 0},
    {"input": ["a", "a"], "output": 1},
    {"input": ["", "abc"], "output": 0},
    {"input": ["bsbininm", "jmjkbkjkv"], "output": 1},
    {"input": ["AGGTAB", "GXTXAYB"], "output": 4},
    {"input": ["ezupkr", "ubmrapg"], "output": 2},
    {"input": ["aaaa", "aa"], "output": 2},
]

EXPLANATION = """
아이디어
- 두 문자열의 '마지막 글자' 를 비교해서 문제를 한 글자씩 줄입니다.
  - 같다 → 그 글자는 LCS 의 마지막 글자로 쓸 수 있음 → 둘 다 한 글자 줄인 문제 + 1
  - 다르다 → 둘 중 하나는 LCS 에 못 들어감 → 한쪽만 줄인 두 문제 중 큰 값

DP 레시피
1. 상태 정의: dp[i][j] = text1[:i] 와 text2[:j] 의 LCS 길이
2. 점화식:
     text1[i-1] == text2[j-1] → dp[i][j] = dp[i-1][j-1] + 1      (↖ 대각선 + 1)
     그 외                    → dp[i][j] = max(dp[i-1][j], dp[i][j-1])  (↑ 또는 ←)
3. 초기값:   dp[0][*] = dp[*][0] = 0 (빈 문자열과의 LCS)
4. 계산 순서: i = 1 → n, j = 1 → m
5. 답:       dp[n][m]

  text1 = "abcde" (행), text2 = "ace" (열)
          ""   a   c   e
     ""    0   0   0   0
     a     0  ↖1   1   1
     b     0   1   1   1
     c     0   1  ↖2   2
     d     0   1   2   2
     e     0   1   2  ↖3   ← 답 3

복잡도: 시간 O(n × m), 공간 O(n × m) → 두 줄(이전 행, 현재 행)만 쓰면 O(min(n, m))

면접 포인트
- 실제 LCS 문자열 복원: dp[n][m] 에서 출발해 같으면 ↖, 아니면 큰 쪽(↑/←)으로 거슬러 올라가며 글자를 모읍니다.
- 응용: Edit Distance, 최장 팰린드롬 부분 수열(= LCS(s, s[::-1])), 두 문자열을 같게 만드는 최소 삭제 수(n + m - 2·LCS), diff 도구.
- 부분 수열(subsequence, 비연속) vs 부분 문자열(substring, 연속)을 구분하세요.
  최장 공통 '부분 문자열' 은 다르면 0 으로 리셋하는 다른 점화식입니다.
"""


def reference(text1, text2):
    n, m = len(text1), len(text2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        a = text1[i - 1]
        row, prev = dp[i], dp[i - 1]
        for j in range(1, m + 1):
            if a == text2[j - 1]:
                row[j] = prev[j - 1] + 1  # 같은 글자: 대각선 + 1
            else:
                row[j] = max(prev[j], row[j - 1])  # 위 / 왼쪽 중 큰 값
    return dp[n][m]


def alternative(text1, text2):
    # top-down: lcs(i, j) = text1[i:] 와 text2[j:] 의 LCS 길이
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def lcs(i, j):
        if i == len(text1) or j == len(text2):
            return 0
        if text1[i] == text2[j]:
            return lcs(i + 1, j + 1) + 1
        return max(lcs(i + 1, j), lcs(i, j + 1))

    return lcs(0, 0)
