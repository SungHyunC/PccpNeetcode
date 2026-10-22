TITLE = "Longest Substring Without Repeating Characters (중복 없는 가장 긴 부분 문자열)"
LEVEL = "Medium"
SOURCE = "LeetCode 3"
PATTERN = "가변 슬라이딩 윈도우 + 문자의 마지막 위치 해시맵"

DESCRIPTION = """
문자열 s 가 주어집니다.
같은 문자가 두 번 이상 나오지 않는 '연속된' 부분 문자열 중 가장 긴 것의 길이를 return 하세요.

제한사항
- 0 ≤ len(s) ≤ 100,000
- s 는 영문자, 숫자, 기호, 공백, 한글 등 임의의 문자로 이루어질 수 있습니다.

입출력 예
s = "abcabcbb"  →  3   ("abc")
s = "bbbbb"     →  1   ("b")
s = "pwwkew"    →  3   ("wke". "pwke" 는 연속이 아니므로 부분 문자열이 아님)
"""

SIGNATURE = "def solution(s: str) -> int:"

HINTS = [
    "모든 시작점에서 중복이 나올 때까지 늘려 보는 방법은 최악 O(n^2) 입니다.",
    "윈도우 [l, r] 안에는 중복이 없다고 유지합시다. r 을 한 칸 늘렸을 때 s[r] 이 윈도우 안에 이미 있다면 l 을 어디로 옮겨야 할까요?",
    "dict 에 '문자 → 마지막으로 나온 인덱스' 를 저장하세요. s[r] 의 마지막 위치가 l 이상이면 l = last[s[r]] + 1 로 점프합니다.",
    "주의: 마지막 위치가 l 보다 왼쪽(이미 윈도우 밖)이면 l 을 뒤로 되돌리면 안 됩니다. 예: 'abba'",
]

TESTS = [
    {"input": ["abcabcbb"], "output": 3},
    {"input": ["bbbbb"], "output": 1},
    {"input": ["pwwkew"], "output": 3},
    {"input": [""], "output": 0},
    {"input": [" "], "output": 1},
    {"input": ["abba"], "output": 2},
    {"input": ["dvdf"], "output": 3},
    {"input": ["tmmzuxt"], "output": 5},
    {"input": ["가나다가라"], "output": 4},
    {"input": ["a b c a"], "output": 3},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    # 서로 다른 20,000 글자 블록을 반복 → 중복 없는 구간이 매우 길다
    block = [chr(0x4E00 + c) for c in random.sample(range(20_000), 20_000)]
    s = "".join(block * 5)
    return {"input": [s], "output": 20_000}


EXPLANATION = """
핵심: 윈도우 [l, r] 에 중복이 없도록 유지하면서 r 을 하나씩 늘립니다.
중복이 생기면 l 을 "그 문자가 마지막으로 나온 위치 + 1" 로 한 번에 점프합니다.

1. last = {} (문자 → 마지막 인덱스), l = 0, best = 0
2. r = 0..n-1:
   - c = s[r] 이 last 에 있고 last[c] >= l 이면 l = last[c] + 1
   - last[c] = r
   - best = max(best, r - l + 1)
3. best return

시간 O(n) (l, r 모두 앞으로만 움직임), 공간 O(min(n, 문자 종류))
면접 포인트: set 으로 윈도우를 관리하며 "중복이 사라질 때까지 l 을 한 칸씩 옮기는" 풀이도 O(n) 입니다(각 문자는 최대 한 번 들어오고 한 번 나감).
'abba' 처럼 last[c] 가 윈도우 밖에 있을 때 l 을 뒤로 되돌리는 버그를 조심하세요.
"""


def reference(s):
    last = {}  # 문자 -> 마지막으로 나온 인덱스
    l = 0
    best = 0
    for r, c in enumerate(s):
        if c in last and last[c] >= l:
            l = last[c] + 1  # 중복 문자의 바로 다음 칸으로 점프
        last[c] = r
        best = max(best, r - l + 1)
    return best


def alternative(s):
    # set + while 로 l 을 한 칸씩 줄이는 형태 (역시 O(n))
    window = set()
    l = best = 0
    for r, c in enumerate(s):
        while c in window:
            window.remove(s[l])
            l += 1
        window.add(c)
        best = max(best, r - l + 1)
    return best


def brute_force(s):
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
        best = max(best, len(seen))
    return best
