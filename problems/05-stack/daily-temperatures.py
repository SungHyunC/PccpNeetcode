TITLE = "Daily Temperatures (일일 온도)"
LEVEL = "Medium"
SOURCE = "LeetCode 739 · 프로그래머스 Lv.2 '주식가격' / '뒤에 있는 큰 수 찾기' 유형"
PATTERN = "단조 감소 스택(monotonic stack)으로 '다음 큰 원소' 찾기"

DESCRIPTION = """
매일의 기온을 담은 배열 temperatures 가 주어집니다.
각 날짜 i 에 대해, i 이후 처음으로 기온이 '더 높아지는' 날까지 며칠을 기다려야 하는지 구해
같은 길이의 리스트로 return 하세요. 더 따뜻한 날이 오지 않으면 0 을 넣습니다.

제한사항
- 1 ≤ len(temperatures) ≤ 100,000
- 30 ≤ temperatures[i] ≤ 100

입출력 예
temperatures = [73, 74, 75, 71, 69, 72, 76, 73]  →  [1, 1, 4, 2, 1, 1, 0, 0]
temperatures = [30, 40, 50, 60]                  →  [1, 1, 1, 0]
temperatures = [30, 60, 90]                      →  [1, 1, 0]
"""

SIGNATURE = "def solution(temperatures: list[int]) -> list[int]:"

HINTS = [
    "각 날짜마다 오른쪽을 훑으면 O(n^2) 입니다. 기온이 계속 내려가는 입력에서 n = 100,000 이면 시간 초과입니다.",
    "아직 '더 따뜻한 날' 을 찾지 못한 날들을 모아 두었다가, 따뜻한 날이 오면 한꺼번에 답을 정해 줄 수 있을까요?",
    "스택에 '답이 정해지지 않은 날의 인덱스' 를 넣습니다. 이 스택의 기온은 위로 갈수록 낮아집니다(단조 감소).",
    "오늘 기온이 스택 top 날의 기온보다 높으면 pop 하고 answer[top] = i - top. 더 이상 높지 않을 때까지 반복한 뒤 오늘을 push 합니다.",
]

TESTS = [
    {"input": [[73, 74, 75, 71, 69, 72, 76, 73]], "output": [1, 1, 4, 2, 1, 1, 0, 0]},
    {"input": [[30, 40, 50, 60]], "output": [1, 1, 1, 0]},
    {"input": [[30, 60, 90]], "output": [1, 1, 0]},
    {"input": [[50]], "output": [0]},
    {"input": [[90, 80, 70, 60]], "output": [0, 0, 0, 0]},
    {"input": [[70, 70, 70, 71]], "output": [3, 2, 1, 0]},
    {"input": [[55, 38, 53, 81, 61, 93, 97, 32, 43, 78]], "output": [3, 1, 1, 2, 1, 1, 0, 1, 1, 0]},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    # 계속 내려가거나 같은 기온 → 브루트포스는 매번 끝까지 훑는다
    temps = sorted((random.randint(30, 100) for _ in range(100_000)), reverse=True)
    return {"input": [temps], "output": None}


EXPLANATION = """
핵심: "다음으로 큰 원소(next greater element)" 문제는 단조 스택의 대표 유형입니다.
스택에는 아직 답을 못 찾은 날들이 쌓이고, 그 기온은 위로 갈수록 낮거나 같습니다.

1. answer = [0] * n, stack = [] (인덱스)
2. i = 0..n-1:
   - stack 이 있고 temperatures[stack[-1]] < temperatures[i] 인 동안
     j = stack.pop(), answer[j] = i - j   (j 의 '처음으로 더 따뜻한 날' 이 i)
   - stack.append(i)
3. 스택에 남은 날들은 더 따뜻한 날이 없으므로 0 그대로

시간 O(n) (각 인덱스는 한 번 push, 한 번 pop), 공간 O(n)
면접 포인트: 이중 루프 같아 보여도 while 의 총 실행 횟수가 n 이하라서 O(n) 이라는 분할 상환(amortized) 분석을 설명하세요.
같은 기온은 '더 높은' 것이 아니므로 비교는 < 입니다. 프로그래머스 '주식가격', '뒤에 있는 큰 수 찾기' 도 같은 틀입니다.
"""


def reference(temperatures):
    n = len(temperatures)
    answer = [0] * n
    stack = []  # 아직 더 따뜻한 날을 못 찾은 날의 인덱스 (기온은 단조 감소)
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            answer[j] = i - j
        stack.append(i)
    return answer


def brute_force(temperatures):
    n = len(temperatures)
    answer = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if temperatures[j] > temperatures[i]:
                answer[i] = j - i
                break
    return answer
