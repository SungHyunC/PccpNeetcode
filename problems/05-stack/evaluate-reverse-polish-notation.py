TITLE = "Evaluate Reverse Polish Notation (후위 표기식 계산)"
LEVEL = "Medium"
SOURCE = "LeetCode 150"
PATTERN = "숫자는 push, 연산자를 만나면 두 개 pop 해서 계산 후 push"

DESCRIPTION = """
후위 표기법(역폴란드 표기법, Reverse Polish Notation)으로 쓰인 수식이 토큰 리스트 tokens 로 주어집니다.
후위 표기법은 연산자를 두 피연산자 '뒤에' 씁니다. 예: (2 + 1) * 3 → ["2", "1", "+", "3", "*"]
수식을 계산한 정수 결과를 return 하세요.

- 연산자는 '+', '-', '*', '/' 네 가지입니다.
- 나눗셈은 소수점 아래를 버리고 0 쪽으로 자릅니다. (예: 7 / -2 = -3, -7 / 2 = -3)
- 0 으로 나누는 경우는 없으며, 항상 올바른 수식만 주어집니다.

제한사항
- 1 ≤ len(tokens) ≤ 10,000
- 숫자 토큰은 -200 이상 200 이하의 정수입니다. (음수는 "-11" 처럼 주어짐)
- 중간 계산과 결과는 32비트 정수 범위 안에 있습니다.

입출력 예
tokens = ["2", "1", "+", "3", "*"]   →  9    ((2 + 1) * 3)
tokens = ["4", "13", "5", "/", "+"]  →  6    (4 + (13 / 5) = 4 + 2)
"""

SIGNATURE = "def solution(tokens: list[str]) -> int:"

HINTS = [
    "연산자를 만났을 때 필요한 두 피연산자는 '가장 최근에 나온 두 값' 입니다. 어떤 자료구조가 어울릴까요?",
    "숫자는 int 로 바꿔 스택에 push 합니다. 연산자를 만나면 b = pop(), a = pop() 순서로 꺼내 a (연산자) b 를 계산해 다시 push 합니다. (순서 주의: 먼저 꺼낸 것이 오른쪽 피연산자)",
    "파이썬의 // 는 음의 무한대 쪽으로 내림합니다(-7 // 2 == -4). 0 쪽으로 자르려면 int(a / b) 를 쓰세요.",
    "'-11' 같은 음수 토큰을 연산자 '-' 로 착각하지 않도록, 토큰이 정확히 '+', '-', '*', '/' 인지로 판단하세요.",
]

TESTS = [
    {"input": [["2", "1", "+", "3", "*"]], "output": 9},
    {"input": [["4", "13", "5", "/", "+"]], "output": 6},
    {"input": [["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]], "output": 22},
    {"input": [["42"]], "output": 42},
    {"input": [["-7", "2", "/"]], "output": -3},
    {"input": [["7", "-2", "/"]], "output": -3},
    {"input": [["3", "-4", "*"]], "output": -12},
    {"input": [["5", "8", "-"]], "output": -3},
    {"input": [["0", "3", "/"]], "output": 0},
    {"input": [["-200"]], "output": -200},
]

EXPLANATION = """
핵심: 후위 표기식은 왼쪽부터 읽으며 스택만으로 계산할 수 있습니다. 연산자는 항상 "가장 최근 두 값" 에 적용됩니다.

1. stack = []
2. 각 토큰 t:
   - t 가 연산자면 b = stack.pop(), a = stack.pop(), stack.append(a op b)
   - 아니면 stack.append(int(t))
3. stack[0] 을 return

나눗셈 주의: 파이썬 // 는 바닥 나눗셈(floor)이라 -7 // 2 == -4 입니다. 0 쪽 자르기는 int(a / b).
(값이 매우 크면 float 오차가 생길 수 있으므로 그때는 abs 로 나눈 뒤 부호를 붙이는 방식이 안전합니다.)

시간 O(n), 공간 O(n)
면접 포인트: a, b 를 꺼내는 순서(빼기·나누기는 교환법칙이 안 됨)와 파이썬 나눗셈 동작 차이를 먼저 짚으세요.
후속 질문으로 "중위 표기식을 후위로 바꾸기(Shunting-yard)" 나 Basic Calculator(LeetCode 224, 227)가 나올 수 있습니다.
"""


def reference(tokens):
    stack = []
    for t in tokens:
        if t in ("+", "-", "*", "/"):
            b = stack.pop()  # 오른쪽 피연산자
            a = stack.pop()  # 왼쪽 피연산자
            if t == "+":
                stack.append(a + b)
            elif t == "-":
                stack.append(a - b)
            elif t == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))  # 0 쪽으로 자르기 (// 는 내림이라 다름)
        else:
            stack.append(int(t))
    return stack[0]
