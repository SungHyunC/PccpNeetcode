import heapq
import random
from bisect import insort

TITLE = "Find Median from Data Stream (데이터 스트림의 중앙값)"
LEVEL = "Hard"
SOURCE = "LeetCode 295"
PATTERN = "두 개의 힙 (작은 절반 = 최대 힙, 큰 절반 = 최소 힙)"

DESCRIPTION = """
숫자가 하나씩 들어올 때, 지금까지 들어온 숫자들의 중앙값(median)을 언제든 빠르게 알려 주는 클래스를 설계하세요.
중앙값은 정렬했을 때 가운데 값이며, 개수가 짝수면 가운데 두 값의 평균입니다.
예) [2, 3, 4] → 3.0,  [2, 3] → 2.5

- MedianFinder(): 빈 상태로 시작합니다.
- addNum(num): num 을 추가합니다. 반환값 없음.
- findMedian(): 지금까지의 중앙값을 실수(float)로 반환합니다.

[채점 방식] 클래스 설계 문제를 solution(commands, values) 로 바꿨습니다.
commands[i] 는 호출할 이름, values[i] 는 그 인자 리스트입니다.
각 호출의 반환값을 순서대로 담은 리스트를 return 하세요 (생성자와 addNum 은 None).

제한사항
- -10^5 ≤ num ≤ 10^5
- findMedian 은 숫자가 1개 이상 있을 때만 호출됩니다.
- 호출 횟수 ≤ 100,000 (효율성 테스트 있음)

입출력 예
commands = ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
values   = [[], [1], [2], [], [3], []]
→ [None, None, None, 1.5, None, 2.0]
"""

SIGNATURE = "def solution(commands: list[str], values: list[list]) -> list:"

HINTS = [
    "findMedian 마다 정렬하면 O(n log n) 입니다. 중앙값은 '작은 절반의 최댓값'과 '큰 절반의 최솟값'만 알면 구할 수 있습니다.",
    "작은 절반은 최대 힙(부호 반전), 큰 절반은 최소 힙에 넣으세요. 두 힙의 루트가 가운데 두 값입니다.",
    "addNum: 일단 작은 쪽(최대 힙)에 넣고, 그 최댓값을 큰 쪽으로 옮긴 뒤, 큰 쪽이 더 많아지면 큰 쪽 최솟값을 다시 작은 쪽으로 옮깁니다. 이렇게 하면 '작은 쪽 크기 = 큰 쪽 크기 또는 +1' 이 유지됩니다.",
    "findMedian: 작은 쪽이 더 크면 -small[0], 크기가 같으면 (-small[0] + large[0]) / 2.",
]

TESTS = [
    {
        "input": [
            ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"],
            [[], [1], [2], [], [3], []],
        ],
        "output": [None, None, None, 1.5, None, 2.0],
    },
    {
        "input": [["MedianFinder", "addNum", "findMedian"], [[], [5], []]],
        "output": [None, None, 5.0],
    },
    {
        "input": [
            ["MedianFinder", "addNum", "findMedian", "addNum", "findMedian", "addNum", "findMedian",
             "addNum", "findMedian", "addNum", "findMedian"],
            [[], [-1], [], [-2], [], [-3], [], [-4], [], [-5], []],
        ],
        "output": [None, None, -1.0, None, -1.5, None, -2.0, None, -2.5, None, -3.0],
    },
    {
        "input": [
            ["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"],
            [[], [2], [2], [], [2], []],
        ],
        "output": [None, None, None, 2.0, None, 2.0],
    },
    {
        "input": [
            ["MedianFinder"] + ["addNum", "findMedian"] * 10,
            [[]] + [x for v in [6, 10, 2, 6, 5, 0, 6, 3, 1, 0] for x in ([v], [])],
        ],
        "output": [None] + [x for m in [6.0, 8.0, 6.0, 6.0, 6.0, 5.5, 6.0, 5.5, 5.0, 4.0] for x in (None, m)],
    },
    {
        "input": [
            ["MedianFinder", "addNum", "addNum", "findMedian", "findMedian"],
            [[], [100000], [-100000], [], []],
        ],
        "output": [None, None, None, 0.0, 0.0],
    },
]

PERF_LIMIT = 1.0


def perf_case():
    commands, values = ["MedianFinder"], [[]]
    for _ in range(50_000):
        commands += ["addNum", "findMedian"]
        values += [[random.randint(-10**5, 10**5)], []]
    return {"input": [commands, values], "output": None}


EXPLANATION = """
핵심: 정렬된 숫자들을 가운데에서 둘로 자른다고 생각합니다.
- small: 작은 절반 → 최대 힙 (파이썬은 부호 반전)   루트 = 작은 절반의 최댓값
- large: 큰 절반   → 최소 힙                         루트 = 큰 절반의 최솟값
두 힙의 크기를 같게(또는 small 이 1개 더 많게) 유지하면 중앙값은 두 루트만 보면 됩니다.

  지금까지: 1 2 3 5 8 9
   small(최대 힙) = {1, 2, 3}  |  large(최소 힙) = {5, 8, 9}
                    루트 3     |  루트 5          → 중앙값 (3 + 5) / 2 = 4.0

addNum(num)
1. small 에 넣고 (heappush(small, -num))
2. small 의 최댓값을 large 로 옮김 → "small 의 모든 값 ≤ large 의 모든 값" 보장
3. large 가 small 보다 커지면 large 의 최솟값을 small 로 옮김 → 크기 균형

findMedian
- len(small) > len(large) 이면 -small[0]
- 같으면 (-small[0] + large[0]) / 2

시간: addNum O(log n), findMedian O(1)   공간 O(n)
면접 포인트: "두 힙" 패턴의 대표 문제입니다. 불변식(invariant) 두 가지 — 순서(small ≤ large)와 크기(차이 ≤ 1) — 를 명확히 말하세요.
bisect.insort 로 정렬 리스트를 유지하는 풀이(alternative)는 탐색은 O(log n) 이지만 삽입이 O(n) 입니다
(파이썬에서는 memmove 가 빨라 실제로는 꽤 빠르지만, 면접에서는 O(log n) 풀이를 기대합니다).
후속 질문: "값의 범위가 0~100 이라면?" → 카운팅 배열로 O(100). "슬라이딩 윈도우 중앙값이라면?" → 두 힙 + 지연 삭제(lazy deletion).
"""


def reference(commands, values):
    class MedianFinder:
        def __init__(self):
            self.small = []  # 작은 절반: 최대 힙 (값에 - 를 붙여 저장)
            self.large = []  # 큰 절반: 최소 힙

        def addNum(self, num):
            heapq.heappush(self.small, -num)
            heapq.heappush(self.large, -heapq.heappop(self.small))  # small 의 최댓값을 large 로
            if len(self.large) > len(self.small):                   # 크기 균형: small 이 같거나 1 많게
                heapq.heappush(self.small, -heapq.heappop(self.large))

        def findMedian(self):
            if len(self.small) > len(self.large):
                return float(-self.small[0])
            return (-self.small[0] + self.large[0]) / 2

    out, obj = [], None
    for cmd, args in zip(commands, values):
        if cmd == "MedianFinder":
            obj = MedianFinder()
            out.append(None)
        else:
            out.append(getattr(obj, cmd)(*args))
    return out


def alternative(commands, values):
    # 정렬 리스트 + bisect.insort: 삽입 O(n), 중앙값 O(1)
    out, data = [], []
    for cmd, args in zip(commands, values):
        if cmd == "MedianFinder":
            data = []
            out.append(None)
        elif cmd == "addNum":
            insort(data, args[0])
            out.append(None)
        else:
            mid = len(data) // 2
            out.append(float(data[mid]) if len(data) % 2 else (data[mid - 1] + data[mid]) / 2)
    return out


def brute_force(commands, values):
    # findMedian 마다 정렬: O(n log n) → 효율성 실패
    out, data = [], []
    for cmd, args in zip(commands, values):
        if cmd == "MedianFinder":
            data = []
            out.append(None)
        elif cmd == "addNum":
            data.append(args[0])
            out.append(None)
        else:
            s = sorted(data)
            mid = len(s) // 2
            out.append(float(s[mid]) if len(s) % 2 else (s[mid - 1] + s[mid]) / 2)
    return out
