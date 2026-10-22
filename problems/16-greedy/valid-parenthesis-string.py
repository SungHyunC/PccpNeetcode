TITLE = "Valid Parenthesis String (와일드카드 괄호 검사)"
LEVEL = "Medium"
SOURCE = "LeetCode 678"
PATTERN = "열린 괄호 개수의 범위 [lo, hi] 를 유지하는 그리디"

DESCRIPTION = """
'(' , ')' , '*' 세 종류의 문자로 이루어진 문자열 s 가 주어집니다.
'*' 는 '(' 또는 ')' 또는 빈 문자열 중 무엇으로든 바꿀 수 있습니다.
'*' 를 적절히 바꿔서 s 를 올바른 괄호 문자열로 만들 수 있으면 True, 없으면 False 를 return 하세요.
올바른 괄호 문자열은 모든 '(' 가 그보다 뒤에 있는 ')' 와 하나씩 짝지어지는 문자열이며, 빈 문자열도 올바릅니다.

제한사항
- 0 ≤ len(s) ≤ 100,000
- s[i] 는 '(' , ')' , '*' 중 하나

입출력 예
s = "()"    →  True
s = "(*)"   →  True
s = "(*))"  →  True   ('*' 를 '(' 로)
s = ")("    →  False
"""

SIGNATURE = "def solution(s: str) -> bool:"

HINTS = [
    "'*' 가 없다면 열린 괄호 개수(balance)를 세다가 음수가 되면 False, 끝에서 0 이면 True 입니다.",
    "'*' 때문에 balance 가 한 값이 아니라 여러 값이 될 수 있습니다. 가능한 balance 의 최솟값 lo 와 최댓값 hi 만 추적해 보세요.",
    "'(' → lo+1, hi+1 / ')' → lo-1, hi-1 / '*' → lo-1, hi+1. hi < 0 이면 False(닫는 괄호가 너무 많음). lo 는 0 아래로 내려가지 않게 max(lo, 0). 끝에서 lo == 0 이면 True.",
]

TESTS = [
    {"input": ["()"], "output": True},
    {"input": ["(*)"], "output": True},
    {"input": ["(*))"], "output": True},
    {"input": [""], "output": True},
    {"input": ["("], "output": False},
    {"input": [")("], "output": False},
    {"input": ["*"], "output": True},
    {"input": ["(((**"], "output": False},
    {"input": ["**(("], "output": False},
    {"input": ["(*()"], "output": True},
    {"input": ["((*)(*))((*"], "output": False},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    n = 100_000
    s = "".join(random.choice("(*)") for _ in range(n))
    return {"input": [s], "output": None}


EXPLANATION = """
아이디어
- '*' 가 있으면 "지금까지 열려 있는 '(' 의 개수(balance)" 가 하나로 정해지지 않고 여러 값이 가능합니다.
- 가능한 balance 들은 항상 연속 구간 [lo, hi] 를 이룹니다. 그러니 양 끝만 관리하면 됩니다.
  - lo: '*' 를 최대한 ')' 로 썼을 때 (단, 0 미만은 의미 없음 → 0 으로 자름)
  - hi: '*' 를 최대한 '(' 로 썼을 때

단계
1. lo = hi = 0
2. 문자마다
   - '(' : lo += 1, hi += 1
   - ')' : lo -= 1, hi -= 1
   - '*' : lo -= 1, hi += 1
   - hi < 0 → False  ('*' 를 전부 '(' 로 써도 ')' 가 너무 많음)
   - lo = max(lo, 0)  (balance 는 음수가 될 수 없으므로 불가능한 경우를 버림)
3. 끝에서 lo == 0 이면 True (balance 0 이 가능한 범위 안에 있음)

  s  :  (   *   )   )
  lo :  1   0   0   0      ('*' 를 ')' 로 → 0, 이후 max(…,0))
  hi :  1   2   1   0      → hi ≥ 0 유지, 끝에서 lo == 0 → True

복잡도: 시간 O(n), 공간 O(1)

다른 풀이
- DP: dp[i][b] = i 글자까지 보고 balance 가 b 일 수 있는가 → O(n^2).
- 스택 두 개: '(' 인덱스 스택과 '*' 인덱스 스택. ')' 는 '(' 를 먼저, 없으면 '*' 를 소비.
  끝에서 남은 '(' 마다 그보다 뒤에 있는 '*' 와 짝지음 → O(n).
- 완전 탐색(brute_force): '*' 마다 3가지 → O(3^k).

면접 포인트
- "가능한 상태의 집합이 구간이라서 양 끝만 관리하면 된다" 는 관찰이 핵심입니다. 이걸 말로 설명하세요.
- max(lo, 0) 을 빼먹으면 "(*)" 같은 입력에서 틀립니다.
  ( → [1,1], * → [0,2], ) → [-1,1] 이 되어 끝에서 lo == -1 → False 로 잘못 판정. (정답은 True)
"""


def reference(s):
    lo = hi = 0  # 가능한 '열린 괄호 수' 의 최솟값, 최댓값
    for ch in s:
        if ch == "(":
            lo += 1
            hi += 1
        elif ch == ")":
            lo -= 1
            hi -= 1
        else:  # '*' 는 ')' (lo 쪽) 또는 '(' (hi 쪽) 또는 빈 문자
            lo -= 1
            hi += 1
        if hi < 0:  # '*' 를 모두 '(' 로 써도 닫는 괄호가 많음
            return False
        lo = max(lo, 0)  # 음수 balance 는 불가능하므로 버림
    return lo == 0


def brute_force(s):
    # '*' 를 세 가지로 모두 바꿔 보기: O(3^k * n)
    from itertools import product

    stars = [i for i, ch in enumerate(s) if ch == "*"]
    for choice in product(["(", ")", ""], repeat=len(stars)):  # '*' 가 없으면 빈 튜플 하나
        chars = list(s)
        for idx, c in zip(stars, choice):
            chars[idx] = c
        bal = 0
        ok = True
        for ch in "".join(chars):
            bal += 1 if ch == "(" else -1
            if bal < 0:
                ok = False
                break
        if ok and bal == 0:
            return True
    return False
