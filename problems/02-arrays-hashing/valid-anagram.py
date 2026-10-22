TITLE = "Valid Anagram (애너그램 판별)"
LEVEL = "Easy"
SOURCE = "LeetCode 242"
PATTERN = "문자 빈도수 세기 (Counter)"

DESCRIPTION = """
두 문자열 s, t 가 주어집니다. t 가 s 의 글자 순서만 바꾼 문자열(애너그램)이면 True, 아니면 False 를 return 하세요.

제한사항
- 0 ≤ len(s), len(t) ≤ 50,000
- s, t 는 영어 소문자로만 이루어져 있습니다.

입출력 예
s = "anagram", t = "nagaram"  →  True
s = "rat",     t = "car"      →  False
"""

SIGNATURE = "def solution(s: str, t: str) -> bool:"

HINTS = [
    "길이가 다르면 바로 False 입니다.",
    "각 글자가 몇 번 나오는지(빈도수)가 같으면 애너그램입니다.",
    "collections.Counter(s) == Counter(t) 또는 길이 26 배열로 세어 보세요.",
]

TESTS = [
    {"input": ["anagram", "nagaram"], "output": True},
    {"input": ["rat", "car"], "output": False},
    {"input": ["", ""], "output": True},
    {"input": ["a", "ab"], "output": False},
    {"input": ["aacc", "ccac"], "output": False},
    {"input": ["listen", "silent"], "output": True},
]

EXPLANATION = """
아이디어: 애너그램 ⇔ 모든 글자의 등장 횟수가 같다.

1. 길이가 다르면 False
2. 크기 26 배열에 s 의 글자는 +1, t 의 글자는 -1
3. 모두 0 이면 True

시간 O(n), 공간 O(1) (알파벳 26개 고정)
대안: sorted(s) == sorted(t) → O(n log n)
면접 포인트: "유니코드 문자가 들어오면?" 이라는 후속 질문 → 배열 대신 해시맵(Counter) 사용.
"""


def reference(s, t):
    if len(s) != len(t):
        return False
    count = [0] * 26
    for a, b in zip(s, t):
        count[ord(a) - ord("a")] += 1
        count[ord(b) - ord("a")] -= 1
    return all(c == 0 for c in count)


def alternative(s, t):
    from collections import Counter
    return Counter(s) == Counter(t)
