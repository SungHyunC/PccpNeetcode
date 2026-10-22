TITLE = "Min Stack (최솟값 스택)"
LEVEL = "Medium"
SOURCE = "LeetCode 155"
PATTERN = "원소마다 '그 시점까지의 최솟값' 을 함께 저장하는 스택 설계"

DESCRIPTION = """
다음 연산을 모두 O(1) 에 처리하는 스택 MinStack 을 설계하세요.
- MinStack()  : 빈 스택을 만듭니다.
- push(val)   : val 을 넣습니다.
- pop()       : 맨 위 원소를 제거합니다. (return 값 없음)
- top()       : 맨 위 원소를 return 합니다.
- getMin()    : 스택 안의 최솟값을 return 합니다.

이 저장소에서는 LeetCode 의 설계 문제 형식을 함수 하나로 바꿔 출제합니다.
commands[i] 는 i 번째로 호출할 연산 이름, values[i] 는 그 연산의 인자 리스트입니다.
각 연산의 결과를 차례대로 담은 리스트를 return 하세요. 반환값이 없는 연산(생성자, push, pop)은 None 을 넣습니다.
(풀이 함수 안에 class MinStack 을 정의해서 사용해도 됩니다.)

제한사항
- commands[0] 은 항상 "MinStack" 입니다.
- 1 ≤ len(commands) ≤ 100,000
- -2^31 ≤ val ≤ 2^31 - 1
- pop, top, getMin 은 스택이 비어 있지 않을 때만 호출됩니다.

입출력 예
commands = ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"]
values   = [[],         [-2],   [0],    [-3],   [],       [],    [],    []]
→ [None, None, None, None, -3, None, 0, -2]
"""

SIGNATURE = "def solution(commands: list[str], values: list[list]) -> list:"

HINTS = [
    "push/pop/top 은 리스트로 바로 됩니다. 문제는 getMin 입니다. 매번 min(stack) 을 하면 O(n) 입니다.",
    "pop 으로 최솟값이 빠져나가면 '그 다음 최솟값' 을 알아야 합니다. 최솟값의 '이력' 을 어떻게 저장할 수 있을까요?",
    "원소를 넣을 때 (값, 그 시점까지의 최솟값) 을 함께 push 하세요. 그러면 getMin 은 stack[-1][1] 입니다.",
    "명령 처리: result 리스트를 만들고, commands 를 순회하며 이름에 따라 메서드를 호출해 반환값(없으면 None)을 append 합니다.",
]

TESTS = [
    {
        "input": [["MinStack", "push", "push", "getMin", "pop", "top"], [[], [-2], [0], [], [], []]],
        "output": [None, None, None, -2, None, -2],
    },
    {
        "input": [
            ["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"],
            [[], [-2], [0], [-3], [], [], [], []],
        ],
        "output": [None, None, None, None, -3, None, 0, -2],
    },
    {
        "input": [["MinStack", "push", "top", "getMin"], [[], [5], [], []]],
        "output": [None, None, 5, 5],
    },
    {
        "input": [
            ["MinStack", "push", "push", "push", "getMin", "pop", "getMin", "pop", "getMin"],
            [[], [1], [1], [1], [], [], [], [], []],
        ],
        "output": [None, None, None, None, 1, None, 1, None, 1],
    },
    {
        "input": [
            ["MinStack", "push", "push", "getMin", "pop", "getMin", "push", "getMin"],
            [[], [3], [1], [], [], [], [2], []],
        ],
        "output": [None, None, None, 1, None, 3, None, 2],
    },
    {
        "input": [
            ["MinStack", "push", "push", "push", "getMin", "pop", "getMin", "top"],
            [[], [2147483647], [-2147483648], [0], [], [], [], []],
        ],
        "output": [None, None, None, None, -2147483648, None, -2147483648, -2147483648],
    },
    {
        "input": [
            ["MinStack", "push", "pop", "push", "getMin", "top"],
            [[], [10], [], [20], [], []],
        ],
        "output": [None, None, None, None, 20, 20],
    },
]

PERF_LIMIT = 1.0


def perf_case():
    n = 40_000
    commands = ["MinStack"] + ["push"] * n + ["getMin"] * n
    values = [[]] + [[n - i] for i in range(n)] + [[] for _ in range(n)]
    return {"input": [commands, values], "output": None}


EXPLANATION = """
핵심: 스택은 위에서만 넣고 빼므로, 각 원소가 들어간 시점의 최솟값은 그 원소가 빠질 때까지 변하지 않습니다.
그래서 원소마다 "그 시점까지의 최솟값" 을 함께 저장하면 getMin 이 O(1) 입니다.

1. stack = [] 에 (val, cur_min) 튜플을 저장
2. push(val): cur_min = val if 비었으면 else min(val, stack[-1][1]) → append
3. pop(): stack.pop()
4. top(): stack[-1][0],  getMin(): stack[-1][1]

시간: 모든 연산 O(1), 공간 O(n)
면접 포인트: "최솟값 전용 보조 스택(min stack)에 val <= 현재 최솟값일 때만 push" 하는 공간 최적화 버전도 설명할 수 있으면 좋습니다
(같은 값이 여러 번 들어올 때 < 가 아니라 <= 로 넣어야 하는 이유까지).
설계 문제에서는 각 연산의 시간 복잡도를 먼저 말하고 시작하세요.
"""


def reference(commands, values):
    class MinStack:
        def __init__(self):
            self.stack = []  # (값, 이 원소까지의 최솟값)

        def push(self, val):
            cur_min = val if not self.stack else min(val, self.stack[-1][1])
            self.stack.append((val, cur_min))

        def pop(self):
            self.stack.pop()

        def top(self):
            return self.stack[-1][0]

        def getMin(self):
            return self.stack[-1][1]

    result = []
    obj = None
    for cmd, args in zip(commands, values):
        if cmd == "MinStack":
            obj = MinStack()
            result.append(None)
        else:
            result.append(getattr(obj, cmd)(*args))  # push/pop 은 None 을 반환
    return result


def brute_force(commands, values):
    # getMin 을 매번 min() 으로 계산 (O(n))
    stack = []
    result = []
    for cmd, args in zip(commands, values):
        out = None
        if cmd == "push":
            stack.append(args[0])
        elif cmd == "pop":
            stack.pop()
        elif cmd == "top":
            out = stack[-1]
        elif cmd == "getMin":
            out = min(stack)
        result.append(out)
    return result
