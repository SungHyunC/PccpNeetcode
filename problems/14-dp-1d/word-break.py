TITLE = "Word Break (단어 나누기)"
LEVEL = "Medium"
SOURCE = "LeetCode 139"
PATTERN = "접두사 가능 여부 DP: dp[i] = any(dp[j] and s[j:i] in words)"

DESCRIPTION = """
문자열 s 와 단어 목록 word_dict 가 주어집니다.
s 를 하나 이상의 조각으로 끊었을 때 모든 조각이 word_dict 에 있는 단어가 되도록
만들 수 있으면 True, 없으면 False 를 return 하세요.
같은 단어를 여러 번 써도 됩니다.

제한사항
- 1 ≤ len(s) ≤ 1,000
- 1 ≤ len(word_dict) ≤ 1,000, 1 ≤ 각 단어의 길이 ≤ 20
- s 와 단어는 영어 소문자로만 이루어져 있고, word_dict 의 단어는 서로 다름

입출력 예
s = "leetcode",      word_dict = ["leet", "code"]                     →  True
s = "applepenapple", word_dict = ["apple", "pen"]                     →  True  (apple 재사용)
s = "catsandog",     word_dict = ["cats", "dog", "sand", "and", "cat"] →  False
"""

SIGNATURE = "def solution(s: str, word_dict: list[str]) -> bool:"

HINTS = [
    "앞에서부터 단어를 하나씩 떼어 보는 백트래킹은 \"aaaa...ab\" 같은 입력에서 지수 시간이 걸립니다. 같은 위치를 반복해서 다시 탐색하기 때문입니다.",
    "dp[i] = s 의 앞 i 글자 s[:i] 를 단어들로 나눌 수 있는가? 로 정의해 보세요. dp[0] = True.",
    "dp[i] = True ⇔ 어떤 j < i 에 대해 dp[j] 가 True 이고 s[j:i] 가 사전에 있음. 단어 길이가 최대 20 이므로 j 는 i-20..i-1 만 보면 충분합니다. word_dict 는 set 으로!",
]

TESTS = [
    {"input": ["leetcode", ["leet", "code"]], "output": True},
    {"input": ["applepenapple", ["apple", "pen"]], "output": True},
    {"input": ["catsandog", ["cats", "dog", "sand", "and", "cat"]], "output": False},
    {"input": ["a", ["a"]], "output": True},
    {"input": ["a", ["b"]], "output": False},
    {"input": ["cars", ["car", "ca", "rs"]], "output": True},
    {"input": ["aaaaaaaaaaaaaaaaaaaaaaaaaaaaab", ["a", "aa", "aaa", "aaaa"]], "output": False},
    {"input": ["goalspecial", ["go", "goal", "goals", "special"]], "output": True},
]

PERF_LIMIT = 1.0


def perf_case():
    s = "a" * 600 + "b"
    words = ["a" * k for k in range(1, 11)]
    return {"input": [s, words], "output": False}


EXPLANATION = """
아이디어
- "s[:i] 를 나눌 수 있는가" 는 "마지막 단어 s[j:i] 가 사전에 있고, 그 앞 s[:j] 를 나눌 수 있는가" 로 쪼개집니다.
- 백트래킹은 같은 j 위치를 여러 경로로 반복 방문 → 지수 시간. 결과를 dp 에 기록하면 각 위치를 한 번만 계산합니다.

DP 레시피
1. 상태 정의: dp[i] = s[:i] 를 사전 단어로 나눌 수 있으면 True
2. 점화식:   dp[i] = any(dp[i - L] and s[i-L:i] in words  for L in 단어 길이들)
3. 초기값:   dp[0] = True (빈 문자열)
4. 계산 순서: i = 1 → n
5. 답:       dp[n]

  s = "leetcode", words = {leet, code}
  i  : 0 1 2 3 4 5 6 7 8
  dp : T F F F T F F F T
               ↑ "leet"   ↑ dp[4] and "code"

복잡도
- 단어 길이 집합을 L 이라 하면 시간 O(n × |L| × 최대 단어 길이) (슬라이스 비용 포함), 공간 O(n)
- 모든 j < i 를 보는 단순 DP 는 O(n^2 × n) 이지만 n ≤ 1,000 이면 보통 충분합니다.

면접 포인트
- word_dict 를 list 로 두고 `in` 을 쓰면 매번 O(단어 수) → 반드시 set 으로 바꾸세요.
- top-down(dfs(i) + 메모)으로 설명해도 동일한 복잡도입니다. (alternative 참고)
- 후속 문제 Word Break II(가능한 모든 문장 출력)는 출력 자체가 지수적일 수 있어 백트래킹 + 메모가 필요합니다.
- 트라이(trie)로 s[i:] 에서 시작하는 단어를 한 번에 따라가면 슬라이스 비용을 줄일 수 있습니다.
"""


def reference(s, word_dict):
    words = set(word_dict)
    lengths = sorted({len(w) for w in words})
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True  # 빈 문자열은 항상 나눌 수 있음
    for i in range(1, n + 1):
        for L in lengths:
            if L > i:
                break
            # 마지막 단어가 s[i-L:i] 이고, 그 앞부분이 나눌 수 있는 경우
            if dp[i - L] and s[i - L:i] in words:
                dp[i] = True
                break
    return dp[n]


def alternative(s, word_dict):
    # top-down: can(i) = s[i:] 를 나눌 수 있는가
    from functools import lru_cache

    words = set(word_dict)
    max_len = max(len(w) for w in words)

    @lru_cache(maxsize=None)
    def can(i):
        if i == len(s):
            return True
        for j in range(i + 1, min(len(s), i + max_len) + 1):
            if s[i:j] in words and can(j):
                return True
        return False

    return can(0)
