TITLE = "Longest Repeating Character Replacement (문자 바꿔서 가장 긴 반복 만들기)"
LEVEL = "Medium"
SOURCE = "LeetCode 424"
PATTERN = "가변 윈도우: (윈도우 길이 - 최다 문자 개수) ≤ k 유지"

DESCRIPTION = """
영어 대문자로 이루어진 문자열 s 와 정수 k 가 주어집니다.
s 의 아무 문자나 다른 대문자로 바꾸는 연산을 최대 k 번 할 수 있습니다.
연산 후 같은 문자로만 이루어진 '연속된' 부분 문자열의 최대 길이를 return 하세요.

제한사항
- 1 ≤ len(s) ≤ 100,000
- s 는 'A'~'Z' 로만 이루어져 있습니다.
- 0 ≤ k ≤ len(s)

입출력 예
s = "ABAB",    k = 2  →  4   (A 두 개를 B 로 → "BBBB")
s = "AABABBA", k = 1  →  4   (가운데 A 하나를 B 로 → "AABBBBA")
"""

SIGNATURE = "def solution(s: str, k: int) -> int:"

HINTS = [
    "어떤 구간을 전부 같은 문자로 만들려면 몇 번 바꿔야 할까요? 그 구간에서 가장 많은 문자는 그대로 두고 나머지만 바꾸면 됩니다.",
    "필요한 변경 횟수 = (구간 길이) - (구간에서 가장 많이 나온 문자의 개수). 이 값이 k 이하인 가장 긴 구간을 찾으면 됩니다.",
    "윈도우 [l, r] 의 문자 개수를 dict(또는 길이 26 배열)로 관리합니다. r 을 늘리다가 (r - l + 1) - max_count > k 가 되면 l 을 한 칸 줄입니다.",
    "최적화: max_count 는 줄어들 때 갱신하지 않아도 답이 틀리지 않습니다. 답은 max_count 가 커질 때만 커지기 때문입니다.",
]

TESTS = [
    {"input": ["ABAB", 2], "output": 4},
    {"input": ["AABABBA", 1], "output": 4},
    {"input": ["A", 0], "output": 1},
    {"input": ["AAAA", 0], "output": 4},
    {"input": ["ABCDE", 1], "output": 2},
    {"input": ["ABBB", 2], "output": 4},
    {"input": ["ABAA", 0], "output": 2},
    {"input": ["ABCDE", 5], "output": 5},
    {"input": ["BAAAB", 2], "output": 5},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    s = "".join(random.choice("AB") for _ in range(100_000))
    return {"input": [s, 30_000], "output": None}


EXPLANATION = """
핵심: 구간을 한 문자로 통일하는 비용 = 길이 - 최다 문자 개수. 이 비용이 k 이하인 가장 긴 윈도우를 찾습니다.

1. count = {} , l = 0, max_count = 0, best = 0
2. r 을 오른쪽으로 늘리며 count[s[r]] += 1, max_count = max(max_count, count[s[r]])
3. (r - l + 1) - max_count > k 이면 count[s[l]] -= 1, l += 1  (윈도우를 한 칸 밀기)
4. best = max(best, r - l + 1)

왜 max_count 를 줄이지 않아도 되나? 윈도우 길이는 한 번에 최대 1 만 줄고(if 한 번),
답(best)은 max_count 가 이전 최고치를 넘을 때만 커질 수 있습니다. 오래된 max_count 때문에 윈도우가 잠시 '유효하지 않게'
남아 있어도 길이가 줄어들지 않을 뿐 best 를 잘못 키우지는 않습니다.

시간 O(n), 공간 O(26)
면접 포인트: 처음에는 매번 max(count.values()) 로 다시 계산하는 O(26n) 풀이를 설명하고,
그다음 "max_count 를 줄이지 않아도 되는 이유" 를 최적화로 제시하면 좋습니다.
"""


def reference(s, k):
    count = {}
    l = 0
    max_count = 0  # 윈도우 안에서 가장 많이 나온 문자의 개수(역대 최대)
    best = 0
    for r, c in enumerate(s):
        count[c] = count.get(c, 0) + 1
        max_count = max(max_count, count[c])
        # 바꿔야 하는 문자 수가 k 를 넘으면 왼쪽을 한 칸 줄인다
        if (r - l + 1) - max_count > k:
            count[s[l]] -= 1
            l += 1
        best = max(best, r - l + 1)
    return best


def alternative(s, k):
    # max_count 를 매번 다시 계산하는 정직한 버전 (O(26n))
    count = [0] * 26
    l = best = 0
    for r, c in enumerate(s):
        count[ord(c) - 65] += 1
        while (r - l + 1) - max(count) > k:
            count[ord(s[l]) - 65] -= 1
            l += 1
        best = max(best, r - l + 1)
    return best


def brute_force(s, k):
    n = len(s)
    best = 0
    for i in range(n):
        count = [0] * 26
        top = 0
        for j in range(i, n):
            count[ord(s[j]) - 65] += 1
            top = max(top, count[ord(s[j]) - 65])
            if (j - i + 1) - top <= k:
                best = max(best, j - i + 1)
    return best
