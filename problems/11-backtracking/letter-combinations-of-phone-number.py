TITLE = "Letter Combinations of a Phone Number (전화번호 문자 조합)"
LEVEL = "Medium"
SOURCE = "LeetCode 17"
PATTERN = "백트래킹: 자리마다 후보 문자 하나씩 (데카르트 곱)"

DESCRIPTION = """
옛날 휴대폰 키패드에서 숫자 2~9 에는 다음 문자들이 적혀 있습니다.

  2: abc   3: def   4: ghi   5: jkl
  6: mno   7: pqrs  8: tuv   9: wxyz

숫자 2~9 로 이루어진 문자열 digits 가 주어질 때, 각 숫자에서 문자를 하나씩 골라 만들 수 있는
모든 문자열을 return 하세요. 결과의 순서는 상관없습니다.
digits 가 빈 문자열이면 빈 리스트를 return 합니다.

제한사항
- 0 ≤ len(digits) ≤ 4
- digits[i] 는 '2' ~ '9' 중 하나입니다.

입출력 예
digits = "23"  →  ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
digits = ""    →  []
digits = "7"   →  ["p", "q", "r", "s"]
"""

SIGNATURE = "def solution(digits: str) -> list[str]:"

HINTS = [
    "숫자 개수만큼 for 문을 중첩하면 되지만, 숫자 개수가 입력마다 다르므로 중첩 깊이를 고정할 수 없습니다. → 재귀!",
    "dfs(i, path): i 번째 숫자에 해당하는 문자들을 하나씩 path 에 붙여 dfs(i + 1) 을 호출합니다. i == len(digits) 이면 완성.",
    "빈 문자열 입력은 [''] 이 아니라 [] 를 return 해야 합니다. 맨 처음에 따로 처리하세요. (PCCP 라면 itertools.product 로 한 줄에 풀 수도 있습니다.)",
]

COMPARE = "unordered"

TESTS = [
    {"input": ["23"], "output": ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]},
    {"input": [""], "output": []},
    {"input": ["2"], "output": ["a", "b", "c"]},
    {"input": ["7"], "output": ["p", "q", "r", "s"]},
    {
        "input": ["79"],
        "output": ["pw", "px", "py", "pz", "qw", "qx", "qy", "qz", "rw", "rx", "ry", "rz", "sw", "sx", "sy", "sz"],
    },
    {"input": ["22"], "output": ["aa", "ab", "ac", "ba", "bb", "bc", "ca", "cb", "cc"]},
    {
        "input": ["234"],
        "output": [
            "adg", "adh", "adi", "aeg", "aeh", "aei", "afg", "afh", "afi",
            "bdg", "bdh", "bdi", "beg", "beh", "bei", "bfg", "bfh", "bfi",
            "cdg", "cdh", "cdi", "ceg", "ceh", "cei", "cfg", "cfh", "cfi",
        ],
    },
]

EXPLANATION = """
핵심: 자리(숫자)마다 후보 문자를 하나씩 고르는 결정 트리 = 데카르트 곱(Cartesian product).

digits = "23"
            ""
     /      |      \\
    a       b       c        ← '2' 의 후보
  / | \\   / | \\   / | \\
 ad ae af bd be bf cd ce cf  ← '3' 의 후보 (리프 = 결과)

1. digits == "" 이면 [] 반환 (빈 곱은 [""] 가 아님에 주의)
2. dfs(i): i == len(digits) 면 path 를 문자열로 저장
3. keypad[digits[i]] 의 각 문자 ch: path.append(ch) → dfs(i+1) → path.pop()

시간 O(4^n · n) — 숫자당 최대 4개 후보, 결과 문자열 만들기 O(n)
공간 O(n) 재귀 깊이

면접 포인트
- 가지치기가 없는 "순수한" 백트래킹입니다. 모든 리프가 정답이라 결과 개수만큼의 시간이 하한입니다.
- PCCP 에서는 itertools.product(*[keypad[d] for d in digits]) 로 바로 만들 수 있습니다 (alternative).
- BFS 처럼 한 자리씩 결과 리스트를 확장하는 반복문 풀이도 가능합니다: res = [p + ch for p in res for ch in letters].
"""

def reference(digits):
    keypad = {
        "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
    }
    if not digits:
        return []
    result = []
    path = []

    def dfs(i):
        if i == len(digits):
            result.append("".join(path))
            return
        for ch in keypad[digits[i]]:
            path.append(ch)         # 선택
            dfs(i + 1)              # 다음 숫자로
            path.pop()              # 취소

    dfs(0)
    return result


def alternative(digits):
    from itertools import product

    keypad = {
        "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
    }
    if not digits:
        return []
    return ["".join(p) for p in product(*(keypad[d] for d in digits))]
