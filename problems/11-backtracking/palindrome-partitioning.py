TITLE = "Palindrome Partitioning (팰린드롬 분할)"
LEVEL = "Medium"
SOURCE = "LeetCode 131"
PATTERN = "백트래킹: 자를 위치 고르기 + 팰린드롬 DP 표로 가지치기"

DESCRIPTION = """
영어 소문자로 이루어진 문자열 s 가 주어집니다.
s 를 여러 조각으로 잘라, 모든 조각이 팰린드롬(앞뒤가 같은 문자열)이 되게 하는 방법을 모두 구해 return 하세요.
각 방법은 조각 문자열들의 리스트(원래 순서 유지)로 나타냅니다. 방법끼리의 순서는 상관없습니다.

제한사항
- 1 ≤ len(s) ≤ 16
- s 는 영어 소문자로만 이루어져 있습니다.

입출력 예
s = "aab"  →  [["a", "a", "b"], ["aa", "b"]]
s = "efe"  →  [["e", "f", "e"], ["efe"]]
"""

SIGNATURE = "def solution(s: str) -> list[list[str]]:"

HINTS = [
    "첫 조각을 s[0:1], s[0:2], ..., s[0:n] 중 하나로 정하면, 나머지 문자열에 대해 같은 문제가 남습니다.",
    "dfs(start): s[start:] 를 자르는 모든 방법. end = start+1..n 에 대해 s[start:end] 가 팰린드롬일 때만 path 에 넣고 dfs(end) 를 호출하세요.",
    "start == n 이면 path[:] 를 결과에 저장합니다. 팰린드롬 판정은 piece == piece[::-1] 로 충분하고, 더 빠르게 하려면 is_pal[i][j] 표를 DP 로 미리 만들어 두세요.",
]

COMPARE = "unordered"

TESTS = [
    {"input": ["aab"], "output": [["a", "a", "b"], ["aa", "b"]]},
    {"input": ["a"], "output": [["a"]]},
    {"input": ["ab"], "output": [["a", "b"]]},
    {"input": ["efe"], "output": [["e", "f", "e"], ["efe"]]},
    {"input": ["aaa"], "output": [["a", "a", "a"], ["a", "aa"], ["aa", "a"], ["aaa"]]},
    {"input": ["abba"], "output": [["a", "b", "b", "a"], ["a", "bb", "a"], ["abba"]]},
    {"input": ["aabb"], "output": [["a", "a", "b", "b"], ["a", "a", "bb"], ["aa", "b", "b"], ["aa", "bb"]]},
    {
        "input": ["racecar"],
        "output": [
            ["r", "a", "c", "e", "c", "a", "r"],
            ["r", "a", "cec", "a", "r"],
            ["r", "aceca", "r"],
            ["racecar"],
        ],
    },
]

EXPLANATION = """
핵심: "어디서 자를지" 를 앞에서부터 하나씩 정하는 백트래킹. 팰린드롬이 아닌 조각에서 바로 가지치기합니다.

s = "aab"
dfs(0)
├─ "a"  (팰린드롬) → dfs(1)
│   ├─ "a"  → dfs(2)
│   │   └─ "b" → dfs(3) ✔ ["a","a","b"]
│   └─ "ab" ✂ (팰린드롬 아님)
├─ "aa" (팰린드롬) → dfs(2)
│   └─ "b" → dfs(3) ✔ ["aa","b"]
└─ "aab" ✂

팰린드롬 표 (DP): is_pal[i][j] = s[i] == s[j] and (j - i < 2 or is_pal[i+1][j-1])
→ i 를 뒤에서부터 채우면 O(n^2) 에 모든 구간 판정 완료

1. is_pal 표 만들기 (O(n^2))
2. dfs(start): start == n 이면 저장
3. end = start..n-1: is_pal[start][end] 일 때만 choose(s[start:end+1]) → dfs(end+1) → unchoose

시간 O(n · 2^n) — 자를 수 있는 위치가 n-1 개라 분할 방법은 최대 2^(n-1) 개 ("aaaa..." 가 최악)
공간 O(n^2) (팰린드롬 표) + O(n) 재귀

면접 포인트
- 매번 piece == piece[::-1] 로 판정해도 정답이지만(alternative) O(n) 이 곱해집니다. DP 표로 O(1) 판정.
- 분할 방법의 "개수" 나 "최소 분할 횟수" 를 묻는다면 백트래킹 대신 DP (Palindrome Partitioning II) 로 바꿔야 합니다.
"""


def reference(s):
    n = len(s)
    # is_pal[i][j]: s[i..j] 가 팰린드롬인지 (i 를 뒤에서부터 채워야 is_pal[i+1][j-1] 이 준비됨)
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or is_pal[i + 1][j - 1]):
                is_pal[i][j] = True

    result = []
    path = []

    def dfs(start):
        if start == n:
            result.append(path[:])
            return
        for end in range(start, n):
            if is_pal[start][end]:              # 팰린드롬 조각만 계속 탐색 (가지치기)
                path.append(s[start:end + 1])
                dfs(end + 1)
                path.pop()

    dfs(0)
    return result


def alternative(s):
    # 표 없이 슬라이싱으로 바로 판정하는 간단한 버전
    result = []
    path = []

    def dfs(start):
        if start == len(s):
            result.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if piece == piece[::-1]:
                path.append(piece)
                dfs(end)
                path.pop()

    dfs(0)
    return result
