import heapq
from collections import Counter, deque

TITLE = "Task Scheduler (작업 스케줄러)"
LEVEL = "Medium"
SOURCE = "LeetCode 621"
PATTERN = "남은 개수 최대 힙 + 쿨다운 큐 (또는 수학 공식)"

DESCRIPTION = """
CPU 가 처리할 작업 목록 tasks 가 주어집니다. 각 작업은 대문자 한 글자로 표시되며, 같은 글자는 같은 종류의 작업입니다.
CPU 는 단위 시간마다 작업 하나를 처리하거나, 아무것도 하지 않고 쉴(idle) 수 있습니다.
단, 같은 종류의 작업을 다시 처리하려면 그 사이에 최소 n 단위 시간이 지나야 합니다.
(즉, 같은 글자 두 개 사이에 다른 작업이나 idle 이 n 개 이상 있어야 합니다.)

작업 순서는 자유롭게 정할 수 있을 때, 모든 작업을 끝내는 데 필요한 최소 시간을 return 하세요.

제한사항
- 1 ≤ len(tasks) ≤ 10,000
- tasks[i] 는 'A' ~ 'Z'
- 0 ≤ n ≤ 100

입출력 예
tasks = ["A", "A", "A", "B", "B", "B"], n = 2  →  8   (A B idle A B idle A B)
tasks = ["A", "C", "A", "B", "D", "B"], n = 1  →  6   (A B C A B D 등)
tasks = ["A", "A", "A", "B", "B", "B"], n = 0  →  6
"""

SIGNATURE = "def solution(tasks: list[str], n: int) -> int:"

HINTS = [
    "작업 이름은 중요하지 않고 종류별 개수만 중요합니다. Counter 로 세어 보세요.",
    "매 시점에는 '지금 실행할 수 있는 작업 중 남은 개수가 가장 많은 것'을 실행하는 것이 유리합니다 (많이 남은 작업일수록 나중에 idle 을 만들기 때문). → 최대 힙.",
    "실행한 작업은 (남은 개수, 다시 실행 가능한 시각) 으로 큐에 넣어 두고, 그 시각이 되면 힙으로 되돌립니다. 힙이 비어 있으면 큐의 맨 앞 시각까지 시간을 건너뛰세요.",
    "수학 풀이: 가장 많은 작업의 개수를 m, 개수가 m 인 작업 종류 수를 c 라 하면 답 = max(len(tasks), (m - 1) * (n + 1) + c).",
]

TESTS = [
    {"input": [["A", "A", "A", "B", "B", "B"], 2], "output": 8},
    {"input": [["A", "C", "A", "B", "D", "B"], 1], "output": 6},
    {"input": [["A", "A", "A", "B", "B", "B"], 3], "output": 10},
    {"input": [["A", "A", "A", "B", "B", "B"], 0], "output": 6},
    {"input": [["A"], 5], "output": 1},
    {"input": [["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2], "output": 16},
    {"input": [["A", "A", "B", "B", "C", "C", "D", "D"], 1], "output": 8},
    {"input": [["Z", "Z", "Z"], 100], "output": 203},
]

EXPLANATION = """
핵심(시뮬레이션): 매 순간 "지금 실행 가능한 작업 중 가장 많이 남은 것"을 실행합니다 (그리디).
최대 힙에는 실행 가능한 작업의 남은 개수, 큐에는 쿨다운 중인 작업 (남은 개수, 다시 가능한 시각) 을 둡니다.

  A x3, B x3, n = 2
  t=1 A (A 남음 2, t=4 부터 가능)     t=2 B (B 남음 2, t=5 부터)
  t=3 실행 가능한 작업 없음 → idle  (힙이 비면 t=4 로 건너뜀)
  t=4 A   t=5 B   t=6 idle   t=7 A   t=8 B   → 8

1. heap = [-개수 ...] (최대 힙), q = deque(), time = 0
2. while heap or q:
   - time += 1
   - 힙이 비어 있으면 time = q[0] 의 가능 시각 (idle 구간 건너뛰기)
   - 가능 시각이 된 작업을 큐에서 힙으로 이동
   - 힙에서 하나 꺼내 실행, 남은 개수가 있으면 (남은 개수, time + n + 1) 을 큐에 추가
3. time 반환

시간 O(T log 26) = O(T) (T = 작업 수), 공간 O(26)

수학 풀이(alternative): 가장 많은 작업 A 가 m 번 있으면 "A _ _ A _ _ A" 처럼 (m - 1) 개의 칸(각 n + 1 길이)과
마지막 줄이 필요합니다. 마지막 줄에는 개수가 m 인 작업들(c 개)이 놓이므로 (m - 1)(n + 1) + c.
작업 종류가 많아 칸이 넘치면 idle 이 필요 없으므로 len(tasks) 와 max.

면접 포인트: 힙 시뮬레이션을 먼저 설명하고, 공식으로 O(T) 최적화를 덧붙이면 좋습니다.
같은 "쿨다운 + 우선순위" 구조는 Reorganize String (LeetCode 767) 에도 쓰입니다.
"""


def reference(tasks, n):
    heap = [-c for c in Counter(tasks).values()]   # 남은 개수 최대 힙
    heapq.heapify(heap)
    cooldown = deque()                              # (남은 개수(음수), 다시 가능한 시각)
    time = 0
    while heap or cooldown:
        time += 1
        if not heap:
            time = max(time, cooldown[0][1])        # 할 일이 없으면 idle 구간 건너뛰기
        while cooldown and cooldown[0][1] <= time:
            heapq.heappush(heap, cooldown.popleft()[0])
        remaining = heapq.heappop(heap) + 1         # 하나 실행 (음수이므로 +1)
        if remaining:
            cooldown.append((remaining, time + n + 1))
    return time


def alternative(tasks, n):
    counts = Counter(tasks).values()
    m = max(counts)
    c = sum(1 for v in counts if v == m)
    return max(len(tasks), (m - 1) * (n + 1) + c)
