TITLE = "Minimum Window Substring (모든 문자를 포함하는 최소 구간)"
LEVEL = "Hard"
SOURCE = "LeetCode 76"
PATTERN = "가변 윈도우: 오른쪽으로 늘려 조건을 만족시키고, 왼쪽을 최대한 줄이기"

DESCRIPTION = """
문자열 s 와 t 가 주어집니다.
t 의 모든 글자를 (같은 글자가 여러 번 있으면 그 개수만큼) 포함하는 s 의 '연속된' 부분 문자열 중
가장 짧은 것을 return 하세요. 그런 부분 문자열이 없으면 빈 문자열 "" 을 return 합니다.
답이 존재하면 가장 짧은 것은 유일하도록 입력이 주어집니다.

제한사항
- 1 ≤ len(s), len(t) ≤ 100,000
- s, t 는 영어 대소문자로 이루어져 있습니다. (대소문자 구분)

입출력 예
s = "ADOBECODEBANC", t = "ABC"  →  "BANC"
s = "a",             t = "a"    →  "a"
s = "a",             t = "aa"   →  ""     (a 가 두 개 필요)
"""

SIGNATURE = "def solution(s: str, t: str) -> str:"

HINTS = [
    "모든 (시작, 끝) 쌍을 확인하면 O(n^2) 이상입니다. 윈도우를 '늘리는 단계' 와 '줄이는 단계' 로 나눠 생각해 보세요.",
    "r 을 늘려 윈도우가 t 를 모두 포함하게 되면, 그 상태를 유지하는 한 l 을 최대한 오른쪽으로 당겨 최소 길이를 갱신합니다.",
    "need = Counter(t). '조건을 만족한 글자 종류 수' have 를 관리하면 윈도우가 유효한지 O(1) 에 알 수 있습니다. window[c] == need[c] 가 되는 순간 have += 1.",
    "l 을 줄일 때 window[s[l]] 이 need 보다 작아지는 순간 have -= 1. have == len(need) 인 동안만 줄이고, 그때마다 최소 구간을 기록하세요.",
]

TESTS = [
    {"input": ["ADOBECODEBANC", "ABC"], "output": "BANC"},
    {"input": ["a", "a"], "output": "a"},
    {"input": ["a", "aa"], "output": ""},
    {"input": ["ab", "b"], "output": "b"},
    {"input": ["abc", "d"], "output": ""},
    {"input": ["bba", "ab"], "output": "ba"},
    {"input": ["aaflslflsldkalskaaa", "aaa"], "output": "aaa"},
    {"input": ["cabwefgewcwaefgcf", "cae"], "output": "cwae"},
    {"input": ["aA", "A"], "output": "A"},
    {"input": ["abc", "cba"], "output": "abc"},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    # 'y' 는 맨 앞, 'z' 는 맨 뒤에만 있음 → 답은 문자열 전체
    middle = "".join(random.choice("ab") for _ in range(100_000))
    s = "y" + middle + "z"
    return {"input": [s, "zay"], "output": s}


EXPLANATION = """
핵심: "늘려서 만족시키고, 줄여서 최소화" 하는 가변 슬라이딩 윈도우의 대표 문제입니다.

1. need = Counter(t), required = len(need) (필요한 글자 종류 수), have = 0
2. r 을 0..n-1 로 늘리며 window[s[r]] += 1
   - s[r] 이 need 에 있고 window[s[r]] == need[s[r]] 이 되는 순간 have += 1
3. have == required 인 동안(윈도우가 유효한 동안):
   - 현재 길이 r - l + 1 이 최소면 기록
   - window[s[l]] -= 1, 그로 인해 window[s[l]] < need[s[l]] 이면 have -= 1
   - l += 1
4. 기록한 구간을 return (없으면 "")

시간 O(|s| + |t|) (l, r 각각 최대 |s| 번 이동), 공간 O(문자 종류)
면접 포인트: 윈도우가 유효한지 매번 두 Counter 를 비교하면 O(52 · n) 이 됩니다. have/required 카운터로 O(1) 판정하는 것을 설명하세요.
"t 에 중복 글자가 있으면?", "답이 없으면?" 같은 경계 조건을 먼저 질문하는 것도 좋은 인상을 줍니다.
"""


def reference(s, t):
    from collections import Counter

    need = Counter(t)
    required = len(need)  # 조건을 채워야 하는 글자 종류 수
    window = {}
    have = 0
    best_len, best_l = float("inf"), 0
    l = 0
    for r, c in enumerate(s):
        window[c] = window.get(c, 0) + 1
        if c in need and window[c] == need[c]:
            have += 1
        # 유효한 동안 왼쪽을 최대한 줄인다
        while have == required:
            if r - l + 1 < best_len:
                best_len, best_l = r - l + 1, l
            left = s[l]
            window[left] -= 1
            if left in need and window[left] < need[left]:
                have -= 1
            l += 1
    return "" if best_len == float("inf") else s[best_l:best_l + best_len]


def brute_force(s, t):
    from collections import Counter

    need = Counter(t)
    best = ""
    for i in range(len(s)):
        window = Counter()
        for j in range(i, len(s)):
            window[s[j]] += 1
            if all(window[c] >= k for c, k in need.items()):
                if best == "" or j - i + 1 < len(best):
                    best = s[i:j + 1]
                break
    return best
