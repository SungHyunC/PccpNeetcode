TITLE = "String Compression (단위 길이별 문자열 압축)"
LEVEL = "Medium"
SOURCE = "PCCP 기출 유형 (프로그래머스 '문자열 압축' 유형)"
PATTERN = "모든 단위 길이 완전 탐색 + 연속 같은 조각 묶기"

DESCRIPTION = """
로그 저장 공간을 아끼기 위해 문자열을 다음 규칙으로 압축하려고 합니다.

1. 단위 길이 k 를 하나 정하고, 문자열을 맨 앞부터 k 글자씩 잘라 조각으로 나눕니다.
   (마지막 조각은 k 보다 짧을 수 있으며, 그대로 둡니다.)
2. 바로 이어서 같은 조각이 m 번(m ≥ 2) 반복되면 "m" + 조각 으로 줄여 씁니다.
   한 번만 나오는 조각은 숫자 없이 그대로 씁니다.

예: s = "aabbaccc", k = 1 → a a b b a c c c → "2a2ba3c" (길이 7)
    s = "abcabcdede", k = 3 → abc abc ded e → "2abcdede" (길이 8)
    s = "abcabcdede", k = 2 → ab ca bc de de → "abcabc2de" (길이 9)

반드시 앞에서부터 같은 길이로만 자를 수 있습니다. 가능한 모든 k 중에서
압축 결과가 가장 짧을 때의 길이를 return 하세요. (압축하지 않는 것도 k = len(s) 로 볼 수 있습니다.)

제한사항
- 1 ≤ len(s) ≤ 1,000
- s 는 알파벳 소문자로만 이루어져 있습니다.
- 반복 횟수가 10 이상이면 숫자도 두 자리 이상을 차지합니다. (예: "10a" 는 길이 3)

입출력 예
s = "aabbaccc"            →  7
s = "abcabcdede"          →  8
s = "xyzxyzxyzxyzq"       →  5     ("4xyzq")
s = "a"                   →  1
"""

SIGNATURE = "def solution(s: str) -> int:"

HINTS = [
    "len(s) ≤ 1,000 이므로 모든 단위 길이 k = 1 .. len(s)//2 를 직접 다 해 봐도 됩니다. (k > len(s)//2 는 반복이 생길 수 없음)",
    "k 를 정하면 조각 목록은 [s[i:i+k] for i in range(0, len(s), k)] 입니다.",
    "조각 목록을 앞에서부터 보며 '이전 조각과 같으면 count += 1, 다르면 지금까지의 묶음을 결과 길이에 반영' 하세요. 마지막 묶음 반영을 잊지 마세요.",
    "묶음 하나의 길이 = len(조각) + (len(str(count)) if count > 1 else 0). 숫자 자릿수 처리를 꼭 str 로 하세요(10 이상 반복).",
]

TESTS = [
    {"input": ["aabbaccc"], "output": 7},
    {"input": ["abcabcdede"], "output": 8},
    {"input": ["xyzxyzxyzxyzq"], "output": 5},
    {"input": ["a"], "output": 1},
    {"input": ["ab"], "output": 2},
    {"input": ["zz"], "output": 2},
    {"input": ["aaaaaaaaaa"], "output": 3},
    {"input": ["abababababababababab"], "output": 4},
    {"input": ["qabcabcabcabc"], "output": 8},
    {"input": ["qabcabc"], "output": 7},
    {"input": ["abcabcabcdddddddddddd"], "output": 8},
    {"input": ["pqpqrpqpqr"], "output": 6},
]

EXPLANATION = """
핵심: 입력이 작으므로(1,000) 모든 단위 길이를 완전 탐색합니다. 어려운 것은 '압축 규칙 구현' 입니다.

  s = "abcabcdede"
  k=1: a b c a b c d e d e     → 압축 없음, 10
  k=2: ab ca bc de de          → "abcabc2de", 9
  k=3: abc abc ded e           → "2abcdede", 8   ← 최소
  k=4: abca bcde de            → 10
  k=5: abcab cdede             → 10

단위 k 하나에 대해:
1. 조각 목록 chunks 를 만들고, prev = chunks[0], count = 1
2. 다음 조각이 prev 와 같으면 count += 1
   다르면 length += 묶음 길이(prev, count) 후 prev 갱신, count = 1
3. 마지막 묶음도 반영
4. 모든 k 의 최솟값

복잡도: k 마다 O(n) 개의 조각을 비교(조각 비교 O(k)) → 전체 O(n^2) 정도. n = 1,000 이면 충분.
실전 포인트:
- len(s) == 1 일 때 range(1, len(s)//2 + 1) 이 비어 있으므로 기본값 answer = len(s) 를 꼭 두세요.
- 반복 횟수가 두 자리(10 이상)가 되면 len(str(count)) 로 자릿수를 세야 합니다. 많이 틀리는 포인트입니다.
- 앞에서부터만 자른다는 조건 때문에 "qabcabc" 처럼 맨 앞에 한 글자가 끼면 "abc" 반복이 있어도 압축이 전혀 안 됩니다.
  (k=3: qab cab c → 반복 없음). 반대로 "qabcabcabcabc" 는 k=3 에서 qab 3cab c → 8 로 줄어듭니다.
"""


def reference(s):
    n = len(s)
    answer = n  # 압축하지 않은 경우 (n == 1 일 때도 안전)
    for k in range(1, n // 2 + 1):
        length = 0
        prev, count = s[:k], 1
        for i in range(k, n, k):
            chunk = s[i : i + k]
            if chunk == prev:
                count += 1
            else:
                # 지금까지의 묶음 반영: 숫자(2회 이상일 때) + 조각
                length += len(prev) + (len(str(count)) if count > 1 else 0)
                prev, count = chunk, 1
        length += len(prev) + (len(str(count)) if count > 1 else 0)  # 마지막 묶음
        answer = min(answer, length)
    return answer


def alternative(s):
    # itertools.groupby 로 연속 같은 조각 묶기 + 실제 압축 문자열을 만들어 길이 비교
    from itertools import groupby
    best = len(s)
    for k in range(1, len(s) // 2 + 1):
        chunks = [s[i : i + k] for i in range(0, len(s), k)]
        parts = []
        for chunk, group in groupby(chunks):
            cnt = len(list(group))
            parts.append((str(cnt) if cnt > 1 else "") + chunk)
        best = min(best, len("".join(parts)))
    return best
