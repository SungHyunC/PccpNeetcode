TITLE = "Valid Parentheses (올바른 괄호)"
LEVEL = "Easy"
SOURCE = "LeetCode 20 · 프로그래머스 Lv.2 '올바른 괄호' 유형"
PATTERN = "여는 괄호는 push, 닫는 괄호는 top 과 짝이 맞는지 확인 후 pop"

DESCRIPTION = """
'(', ')', '{', '}', '[', ']' 로만 이루어진 문자열 s 가 주어집니다.
다음 조건을 모두 만족하면 True, 아니면 False 를 return 하세요.
- 여는 괄호는 반드시 같은 종류의 닫는 괄호로 닫혀야 합니다.
- 괄호는 올바른 순서로 닫혀야 합니다. (나중에 연 괄호를 먼저 닫음)
- 모든 닫는 괄호에는 대응하는 여는 괄호가 있어야 합니다.

제한사항
- 1 ≤ len(s) ≤ 100,000

입출력 예
s = "()[]{}"  →  True
s = "(]"      →  False
s = "([)]"    →  False   (안쪽 '[' 보다 ')' 가 먼저 닫힘)
s = "{[]}"    →  True
"""

SIGNATURE = "def solution(s: str) -> bool:"

HINTS = [
    "괄호는 '가장 나중에 연 것' 을 '가장 먼저' 닫아야 합니다. 이런 LIFO(후입선출) 구조에 맞는 자료구조는?",
    "여는 괄호를 만나면 스택에 push 합니다. 닫는 괄호를 만나면 스택 top 이 짝이 맞는 여는 괄호인지 확인하고 pop 합니다.",
    "닫는 괄호를 만났는데 스택이 비어 있으면 False. 문자열을 다 본 뒤 스택이 비어 있지 않아도 False 입니다. (짝 매핑은 {')': '(', ...} dict 로)",
]

TESTS = [
    {"input": ["()"], "output": True},
    {"input": ["()[]{}"], "output": True},
    {"input": ["(]"], "output": False},
    {"input": ["([)]"], "output": False},
    {"input": ["{[]}"], "output": True},
    {"input": ["("], "output": False},
    {"input": [")"], "output": False},
    {"input": ["(("], "output": False},
    {"input": ["){"], "output": False},
    {"input": ["([]{[()]})"], "output": True},
]

PERF_LIMIT = 1.0


def perf_case():
    s = "([{" * 16_000 + "}])" * 16_000
    return {"input": [s], "output": True}


EXPLANATION = """
핵심: 괄호 짝 맞추기는 "가장 최근에 열린 괄호" 와 비교해야 하므로 스택(stack)입니다.

1. pair = {')': '(', ']': '[', '}': '{'}, stack = []
2. 각 문자 c:
   - 여는 괄호면 push
   - 닫는 괄호면 stack 이 비었거나 stack[-1] != pair[c] 이면 False, 아니면 pop
3. 끝나고 stack 이 비어 있으면 True

시간 O(n), 공간 O(n)
면접 포인트: 괄호가 한 종류뿐이면 스택 없이 '열린 개수' 카운터 하나로 충분합니다(프로그래머스 '올바른 괄호').
여러 종류일 때는 순서 정보가 필요해서 스택이 필요하다는 차이를 설명할 수 있어야 합니다.
"""


def reference(s):
    pair = {")": "(", "]": "[", "}": "{"}
    stack = []
    for c in s:
        if c in pair:  # 닫는 괄호
            if not stack or stack[-1] != pair[c]:
                return False
            stack.pop()
        else:          # 여는 괄호
            stack.append(c)
    return not stack


def brute_force(s):
    # 짝이 맞는 '()' '[]' '{}' 를 더 이상 없을 때까지 지우기 (최악 O(n^2))
    prev = None
    while prev != s:
        prev = s
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""
