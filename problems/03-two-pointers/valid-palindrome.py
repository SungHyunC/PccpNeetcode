TITLE = "Valid Palindrome (유효한 팰린드롬)"
LEVEL = "Easy"
SOURCE = "LeetCode 125"
PATTERN = "양 끝에서 안쪽으로 좁혀 오는 투 포인터"

DESCRIPTION = """
문자열 s 가 주어집니다.
영문자와 숫자만 남기고(공백·문장부호 등은 무시), 대문자는 소문자로 바꿨을 때
앞에서 읽으나 뒤에서 읽으나 같으면 True, 아니면 False 를 return 하세요.
영문자·숫자가 하나도 없으면 빈 문자열이므로 True 입니다.

제한사항
- 1 ≤ len(s) ≤ 200,000
- s 는 출력 가능한 ASCII 문자로만 이루어져 있습니다.

입출력 예
s = "A man, a plan, a canal: Panama"  →  True   ("amanaplanacanalpanama")
s = "race a car"                      →  False  ("raceacar")
s = " "                               →  True
"""

SIGNATURE = "def solution(s: str) -> bool:"

HINTS = [
    "가장 쉬운 방법: 영문자·숫자만 골라 소문자로 만든 새 문자열 t 를 만들고 t == t[::-1] 을 확인합니다. 이것도 O(n) 입니다.",
    "면접에서는 '추가 메모리 O(1)' 을 요구하는 경우가 많습니다. 새 문자열 없이 양 끝에서 비교할 수 있을까요?",
    "l = 0, r = len(s) - 1 에서 시작해, 영문자·숫자가 아닌 문자는 건너뛰고(l += 1 / r -= 1), 두 문자를 lower() 로 비교한 뒤 둘 다 한 칸씩 안쪽으로 옮깁니다.",
]

TESTS = [
    {"input": ["A man, a plan, a canal: Panama"], "output": True},
    {"input": ["race a car"], "output": False},
    {"input": [" "], "output": True},
    {"input": ["0P"], "output": False},
    {"input": ["a."], "output": True},
    {"input": ["ab_a"], "output": True},
    {"input": [".,"], "output": True},
    {"input": ["No 'x' in Nixon"], "output": True},
    {"input": ["1a2"], "output": False},
]

PERF_LIMIT = 1.0


def perf_case():
    half = "".join(chr(ord("a") + (i * 7) % 26) + ("," if i % 3 == 0 else "") for i in range(50_000))
    s = half + " " + half[::-1].upper()
    return {"input": [s], "output": True}


EXPLANATION = """
핵심: 팰린드롬은 "i 번째 글자 == 뒤에서 i 번째 글자" 입니다. 양 끝 포인터를 안쪽으로 좁히며 비교하면 됩니다.

1. l = 0, r = len(s) - 1
2. s[l] 이 영문자·숫자가 아니면 l += 1, s[r] 이 아니면 r -= 1 (건너뛰기)
3. 둘 다 유효하면 소문자로 비교 → 다르면 False, 같으면 l += 1, r -= 1
4. l >= r 이 되면 끝까지 문제없었으므로 True

시간 O(n), 공간 O(1)
면접 포인트: "정제한 문자열을 뒤집어 비교" 는 공간 O(n) 입니다. 면접관이 "추가 메모리 없이?" 라고 물으면
투 포인터로 바꾸세요. 건너뛰는 while 문 안에서도 l < r 조건을 꼭 확인해야 인덱스가 엇갈리지 않습니다.
"""


def reference(s):
    l, r = 0, len(s) - 1
    while l < r:
        # 영문자/숫자가 아닌 문자는 건너뛴다 (l < r 을 계속 확인)
        while l < r and not s[l].isalnum():
            l += 1
        while l < r and not s[r].isalnum():
            r -= 1
        if s[l].lower() != s[r].lower():
            return False
        l += 1
        r -= 1
    return True


def alternative(s):
    # 정제한 문자열을 뒤집어 비교 (공간 O(n))
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]
