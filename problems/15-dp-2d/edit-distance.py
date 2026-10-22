TITLE = "Edit Distance (편집 거리)"
LEVEL = "Medium"
SOURCE = "LeetCode 72"
PATTERN = "두 문자열 2차원 DP: 같으면 대각선, 다르면 1 + min(삽입, 삭제, 교체)"

DESCRIPTION = """
두 문자열 word1, word2 가 주어집니다. word1 에 다음 세 가지 연산을 적용할 수 있습니다.
- 삽입: 아무 위치에 글자 하나를 넣는다
- 삭제: 글자 하나를 지운다
- 교체: 글자 하나를 다른 글자로 바꾼다
word1 을 word2 로 바꾸는 데 필요한 연산 횟수의 최솟값을 return 하세요.

제한사항
- 0 ≤ len(word1), len(word2) ≤ 500
- 영어 소문자로만 이루어져 있음

입출력 예
word1 = "horse",     word2 = "ros"        →  3   (h→r 교체, r 삭제, e 삭제)
word1 = "intention", word2 = "execution"  →  5
word1 = "",          word2 = "abc"        →  3   (삽입 3번)
"""

SIGNATURE = "def solution(word1: str, word2: str) -> int:"

HINTS = [
    "dp[i][j] = word1[:i] 를 word2[:j] 로 바꾸는 최소 연산 수. 빈 문자열과의 거리는 길이 그 자체입니다: dp[i][0] = i, dp[0][j] = j.",
    "마지막 글자가 같으면 연산이 필요 없습니다 → dp[i-1][j-1].",
    "다르면 세 연산 중 최선: 교체 dp[i-1][j-1] + 1, 삭제 dp[i-1][j] + 1, 삽입 dp[i][j-1] + 1. 표의 ↖, ↑, ← 세 칸에 대응합니다.",
]

TESTS = [
    {"input": ["horse", "ros"], "output": 3},
    {"input": ["intention", "execution"], "output": 5},
    {"input": ["", "abc"], "output": 3},
    {"input": ["abc", ""], "output": 3},
    {"input": ["", ""], "output": 0},
    {"input": ["same", "same"], "output": 0},
    {"input": ["kitten", "sitting"], "output": 3},
    {"input": ["a", "b"], "output": 1},
    {"input": ["abcdef", "azced"], "output": 3},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    a = "".join(random.choice("abcd") for _ in range(400))
    b = "".join(random.choice("abcd") for _ in range(400))
    return {"input": [a, b], "output": None}


EXPLANATION = """
아이디어
- 두 문자열의 마지막 글자를 맞추는 방법을 생각합니다.
  - 같다      → 그대로 두고 앞부분만 해결: dp[i-1][j-1]
  - 교체      → word1[i-1] 을 word2[j-1] 로 바꿈: dp[i-1][j-1] + 1  (↖)
  - 삭제      → word1[i-1] 을 지움:                dp[i-1][j]   + 1  (↑)
  - 삽입      → word2[j-1] 을 word1 끝에 넣음:     dp[i][j-1]   + 1  (←)

DP 레시피
1. 상태 정의: dp[i][j] = word1[:i] → word2[:j] 최소 연산 수
2. 점화식:   같으면 dp[i-1][j-1], 다르면 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])
3. 초기값:   dp[i][0] = i (전부 삭제), dp[0][j] = j (전부 삽입)
4. 계산 순서: i = 1 → n, j = 1 → m
5. 답:       dp[n][m]

  word1 = "horse" (행), word2 = "ros" (열)
           ""   r   o   s
     ""     0   1   2   3
     h      1   1   2   3
     o      2   2   1   2
     r      3   2   2   2
     s      4   3   3   2
     e      5   4   4   3   ← 답 3

복잡도: 시간 O(n × m), 공간 O(n × m) → 두 행만 쓰면 O(m)

면접 포인트
- 세 연산이 표의 어느 방향(↖ ↑ ←)에 대응하는지 그림으로 설명하면 가장 명확합니다.
- LCS 와 같은 틀(두 문자열의 접두사 쌍)이라는 점을 언급하세요. 삽입·삭제만 허용하면 n + m - 2 × LCS.
- 실무 응용: 맞춤법 교정, DNA 서열 정렬, diff.
"""


def reference(word1, word2):
    n, m = len(word1), len(word2)
    prev = list(range(m + 1))  # dp[0][j] = j
    for i in range(1, n + 1):
        cur = [i] + [0] * m  # dp[i][0] = i
        for j in range(1, m + 1):
            if word1[i - 1] == word2[j - 1]:
                cur[j] = prev[j - 1]  # 같은 글자: 비용 없음
            else:
                cur[j] = 1 + min(prev[j - 1],  # 교체 ↖
                                 prev[j],      # 삭제 ↑
                                 cur[j - 1])   # 삽입 ←
        prev = cur
    return prev[m]


def alternative(word1, word2):
    # top-down: dist(i, j) = word1[i:] → word2[j:] 최소 연산 수
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dist(i, j):
        if i == len(word1):
            return len(word2) - j  # 남은 글자 삽입
        if j == len(word2):
            return len(word1) - i  # 남은 글자 삭제
        if word1[i] == word2[j]:
            return dist(i + 1, j + 1)
        return 1 + min(dist(i + 1, j + 1), dist(i + 1, j), dist(i, j + 1))

    return dist(0, 0)
