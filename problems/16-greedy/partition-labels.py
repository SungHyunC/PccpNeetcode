TITLE = "Partition Labels (글자가 겹치지 않게 문자열 나누기)"
LEVEL = "Medium"
SOURCE = "LeetCode 763"
PATTERN = "각 글자의 마지막 위치로 구간 끝을 늘려 가는 그리디"

DESCRIPTION = """
영어 소문자로 이루어진 문자열 s 가 주어집니다.
s 를 가능한 한 많은 조각으로 나누되, 어떤 글자든 최대 한 조각에만 등장하도록 나누려고 합니다.
조각들을 순서대로 이어 붙이면 원래 s 가 되어야 합니다.
각 조각의 길이를 앞에서부터 순서대로 담은 리스트를 return 하세요.

제한사항
- 1 ≤ len(s) ≤ 500,000
- s 는 영어 소문자로만 이루어져 있음

입출력 예
s = "ababcbacadefegdehijhklij"  →  [9, 7, 8]   ("ababcbaca", "defegde", "hijhklij")
s = "eccbbbbdec"                →  [10]
"""

SIGNATURE = "def solution(s: str) -> list[int]:"

HINTS = [
    "첫 글자 s[0] 이 들어간 조각은 적어도 s[0] 이 마지막으로 등장하는 위치까지는 이어져야 합니다.",
    "먼저 각 글자의 마지막 등장 위치 last[ch] 를 구해 두세요.",
    "왼쪽부터 보며 end = max(end, last[s[i]]) 로 현재 조각의 끝을 늘려 가다가, i == end 가 되는 순간 조각을 끊으면(길이 기록) 됩니다.",
]

TESTS = [
    {"input": ["ababcbacadefegdehijhklij"], "output": [9, 7, 8]},
    {"input": ["eccbbbbdec"], "output": [10]},
    {"input": ["a"], "output": [1]},
    {"input": ["abc"], "output": [1, 1, 1]},
    {"input": ["abca"], "output": [4]},
    {"input": ["aabbcc"], "output": [2, 2, 2]},
    {"input": ["caedbdedda"], "output": [1, 9]},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    letters = "abcdefghijklmnopqrstuvwxyz"
    # 앞부분은 글자 블록을 반복 → 여러 조각이 생기도록 구성
    parts = []
    for k in range(26):
        parts.append("".join(random.choice(letters[k]) for _ in range(10_000)))
    return {"input": ["".join(parts) * 1 + "".join(random.choice(letters) for _ in range(100))], "output": None}


EXPLANATION = """
아이디어
- 조각에 글자 c 가 들어가면, c 의 '모든' 등장 위치가 그 조각에 있어야 합니다.
- 그래서 조각의 끝은 "지금까지 본 글자들의 마지막 등장 위치 중 최댓값" 이상이어야 합니다.
- 그 최댓값에 도달하는 순간이 가장 이르게 끊을 수 있는 지점 → 최대한 많이 나누려면 거기서 바로 끊습니다.

단계
1. last = {ch: i for i, ch in enumerate(s)}  (뒤에 나온 i 가 덮어써서 마지막 위치)
2. start = end = 0
3. i 를 왼쪽부터: end = max(end, last[s[i]])
   - i == end 이면 조각 [start, end] 완성 → 길이 end - start + 1 기록, start = i + 1

  s    : a b a b c b a c a | d e f e g d e | h i j h k l i j
  last : a→8 b→5 c→7 d→14 e→15 ...
  end  : 8 8 8 8 8 8 8 8 8 → i=8 에서 끊기 (길이 9)

왜 그리디가 맞는가
- i == end 인 지점보다 일찍 끊으면 어떤 글자가 두 조각에 걸칩니다(불가능).
- i == end 에서 끊지 않고 더 늘리면 조각 수가 줄어듭니다(손해). → 매번 가장 이른 지점에서 끊는 것이 최적.

복잡도: 시간 O(n), 공간 O(1) (알파벳 26개)

면접 포인트
- 이 문제는 "구간 합치기(merge intervals)" 로 볼 수도 있습니다: 각 글자의 [처음, 마지막] 구간을 합친 결과의 길이들.
- 출력 형식(길이 리스트 vs 조각 문자열)을 먼저 확인하세요.
"""


def reference(s):
    last = {ch: i for i, ch in enumerate(s)}  # 각 글자의 마지막 등장 위치
    sizes = []
    start = end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])  # 현재 조각이 최소한 여기까지는 가야 함
        if i == end:  # 조각 안 글자들이 모두 이 안에서 끝남 → 끊기
            sizes.append(end - start + 1)
            start = i + 1
    return sizes


def alternative(s):
    # 구간 합치기 관점: 글자마다 [처음, 마지막] 구간을 만들고 겹치는 구간을 병합
    first, last = {}, {}
    for i, ch in enumerate(s):
        first.setdefault(ch, i)
        last[ch] = i
    intervals = sorted((first[ch], last[ch]) for ch in first)
    merged = []
    for a, b in intervals:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    return [b - a + 1 for a, b in merged]
