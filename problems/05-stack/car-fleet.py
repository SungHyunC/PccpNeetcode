TITLE = "Car Fleet (자동차 무리)"
LEVEL = "Medium"
SOURCE = "LeetCode 853"
PATTERN = "목적지에 가까운 차부터 도착 시간을 스택에 쌓아 무리 세기"

DESCRIPTION = """
한 줄로 된 도로 위에 차 n 대가 같은 목적지 target 을 향해 달립니다.
i 번 차는 위치 position[i] 에서 시속 speed[i] 로 출발합니다. 모든 위치는 서로 다릅니다.
차는 앞차를 추월할 수 없습니다. 뒤차가 앞차를 따라잡으면 앞차의 속도로 바로 뒤에 붙어 함께 달리며,
이렇게 함께 달리는 차들을 하나의 '무리(fleet)' 라고 합니다. (차 한 대도 무리 하나입니다)
목적지에 정확히 도착하는 순간 따라잡는 경우도 같은 무리로 봅니다.
목적지에 도착하는 무리의 수를 return 하세요.

제한사항
- 1 ≤ n ≤ 100,000
- 0 < target ≤ 1,000,000
- 0 ≤ position[i] < target, position 의 값은 모두 다름
- 0 < speed[i] ≤ 1,000,000

입출력 예
target = 12, position = [10, 8, 0, 5, 3], speed = [2, 4, 1, 1, 3]  →  3
  10, 8 에서 출발한 차는 12 에서 만나 한 무리, 0 에서 출발한 차는 혼자,
  5, 3 에서 출발한 차는 6 에서 만나 한 무리 → 총 3
target = 10, position = [3], speed = [3]  →  1
"""

SIGNATURE = "def solution(target: int, position: list[int], speed: list[int]) -> int:"

HINTS = [
    "추월이 불가능하므로 순서는 바뀌지 않습니다. 목적지에 가까운 차(앞차)부터 생각해 보세요.",
    "각 차가 '혼자 달린다면' 도착하는 시간은 (target - position) / speed 입니다.",
    "앞차보다 도착 시간이 같거나 짧은 뒤차는 앞차를 따라잡아 같은 무리가 됩니다. 이때 무리의 도착 시간은 앞차의 시간입니다.",
    "위치 내림차순으로 정렬하고, 도착 시간을 스택에 쌓되 '스택 top 보다 오래 걸리는 차' 만 새 무리로 push 하세요. 답은 스택 길이입니다.",
]

TESTS = [
    {"input": [12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]], "output": 3},
    {"input": [10, [3], [3]], "output": 1},
    {"input": [100, [0, 2, 4], [4, 2, 1]], "output": 1},
    {"input": [10, [6, 8], [3, 2]], "output": 2},
    {"input": [10, [0, 4, 2], [2, 1, 3]], "output": 1},
    {"input": [10, [8, 3, 7, 4, 6, 5], [4, 4, 4, 4, 4, 4]], "output": 6},
    {"input": [10, [0, 5], [2, 1]], "output": 1},
    {"input": [20, [6, 2, 17], [3, 9, 2]], "output": 2},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    n = 50_000
    position = random.sample(range(1_000_000), n)
    speed = [random.randint(1, 1_000_000) for _ in range(n)]
    return {"input": [1_000_000, position, speed], "output": None}


EXPLANATION = """
핵심: 추월이 없으니 앞차(목적지에 가까운 차)가 뒤차의 상한선이 됩니다.
위치 내림차순으로 보면서 "혼자 달렸을 때 도착 시간" 을 비교하면 무리를 셀 수 있습니다.

1. cars = (position, speed) 를 위치 내림차순 정렬
2. stack = [] (각 무리의 도착 시간)
3. 각 차에 대해 time = (target - p) / s
   - stack 이 비었거나 time > stack[-1] 이면 앞 무리를 따라잡지 못함 → 새 무리, push
   - 아니면 (time <= stack[-1]) 앞 무리에 합류 → 아무것도 하지 않음
4. len(stack) return

시간 O(n log n) (정렬), 공간 O(n)
면접 포인트: 실제로 시뮬레이션하지 않고 "도착 시간" 으로 문제를 바꾸는 관점 전환이 핵심입니다.
스택 대신 '마지막 무리의 시간' 변수 하나로도 풀 수 있다는 것(공간 O(1), 정렬 제외)도 언급해 보세요.
시간을 실수로 비교하는 것이 걱정되면 (target - p) * s2 와 (target - p2) * s 처럼 정수 곱으로 비교할 수 있습니다.
"""


def reference(target, position, speed):
    cars = sorted(zip(position, speed), reverse=True)  # 목적지에 가까운 차부터
    stack = []  # 각 무리의 도착 시간
    for p, s in cars:
        time = (target - p) / s
        if not stack or time > stack[-1]:
            stack.append(time)  # 앞 무리를 못 따라잡음 → 새 무리
        # time <= stack[-1] 이면 앞 무리에 합류 (도착 시간은 앞 무리 기준)
    return len(stack)


def alternative(target, position, speed):
    # 분수 비교를 정수 곱으로: t1 > t2  <=>  d1 * s2 > d2 * s1
    cars = sorted(zip(position, speed), reverse=True)
    fleets = 0
    last_d, last_s = 0, 1  # 마지막 무리의 (남은 거리, 속도), 시간 0 으로 시작
    for p, s in cars:
        d = target - p
        if fleets == 0 or d * last_s > last_d * s:
            fleets += 1
            last_d, last_s = d, s
    return fleets
