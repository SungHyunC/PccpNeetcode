TITLE = "Permutation in String (문자열 속 순열)"
LEVEL = "Medium"
SOURCE = "LeetCode 567"
PATTERN = "고정 길이 슬라이딩 윈도우 + 문자 빈도 비교"

DESCRIPTION = """
두 문자열 s1, s2 가 주어집니다.
s1 의 글자 순서를 바꾼 것(순열, 즉 같은 글자를 같은 개수만큼 가진 문자열) 중 하나가
s2 안에 '연속된' 부분 문자열로 들어 있으면 True, 아니면 False 를 return 하세요.

제한사항
- 1 ≤ len(s1), len(s2) ≤ 100,000
- s1, s2 는 영어 소문자로만 이루어져 있습니다.

입출력 예
s1 = "ab", s2 = "eidbaooo"  →  True   ("ba" 가 들어 있음)
s1 = "ab", s2 = "eidboaoo"  →  False
"""

SIGNATURE = "def solution(s1: str, s2: str) -> bool:"

HINTS = [
    "s1 의 순열인지 확인하는 것 = 두 문자열의 '글자별 개수' 가 같은지 확인하는 것입니다. (정렬할 필요 없음)",
    "확인할 부분 문자열의 길이는 항상 len(s1) 입니다. 길이가 고정된 윈도우를 s2 위에서 한 칸씩 밀어 보세요.",
    "윈도우를 한 칸 밀 때는 들어오는 글자 +1, 나가는 글자 -1 만 하면 됩니다. 길이 26 배열 두 개를 비교하면 한 번에 O(26) 입니다.",
    "더 빠르게: '개수가 일치하는 글자 종류 수(matches)' 를 관리하면 비교도 O(1) 이 됩니다. matches == 26 이면 True.",
]

TESTS = [
    {"input": ["ab", "eidbaooo"], "output": True},
    {"input": ["ab", "eidboaoo"], "output": False},
    {"input": ["a", "a"], "output": True},
    {"input": ["abc", "ab"], "output": False},
    {"input": ["adc", "dcda"], "output": True},
    {"input": ["hello", "ooolleoooleh"], "output": False},
    {"input": ["aab", "ba"], "output": False},
    {"input": ["abc", "cbaebabacd"], "output": True},
    {"input": ["aa", "ababab"], "output": False},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    s1 = "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(5_000))
    s2 = "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(100_000))
    return {"input": [s1, s2], "output": False}


EXPLANATION = """
핵심: 순열 판정 = 글자 빈도가 같은지. 길이 len(s1) 인 고정 윈도우를 s2 위에서 밀면서 빈도를 갱신합니다.

1. len(s1) > len(s2) 면 False
2. need = s1 의 글자 개수(길이 26), window = s2 의 앞 len(s1) 글자 개수
3. window == need 이면 True
4. i = len(s1) .. len(s2)-1: window[s2[i]] += 1, window[s2[i - len(s1)]] -= 1, 비교
5. 끝까지 없으면 False

시간 O(26 · n) (배열 비교) 또는 matches 기법으로 O(n), 공간 O(26)
면접 포인트: 윈도우마다 Counter 를 새로 만들거나 정렬하면 O(n · m) 입니다. "들어오는 것 +1, 나가는 것 -1" 로
윈도우 상태를 O(1) 에 갱신하는 것이 슬라이딩 윈도우의 본질입니다. LeetCode 438(Find All Anagrams)도 같은 코드입니다.
"""


def reference(s1, s2):
    m, n = len(s1), len(s2)
    if m > n:
        return False
    need = [0] * 26
    window = [0] * 26
    for i in range(m):
        need[ord(s1[i]) - 97] += 1
        window[ord(s2[i]) - 97] += 1
    if need == window:
        return True
    for i in range(m, n):
        window[ord(s2[i]) - 97] += 1       # 들어오는 글자
        window[ord(s2[i - m]) - 97] -= 1   # 나가는 글자
        if need == window:
            return True
    return False


def brute_force(s1, s2):
    target = sorted(s1)
    m = len(s1)
    for i in range(len(s2) - m + 1):
        if sorted(s2[i:i + m]) == target:
            return True
    return False
