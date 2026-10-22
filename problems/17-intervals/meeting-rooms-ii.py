TITLE = "Meeting Rooms II (필요한 최소 회의실 수)"
LEVEL = "Medium"
SOURCE = "LeetCode 253"
PATTERN = "최소 힙으로 끝나는 시각 관리 / 스위프 라인(sweep line)"

DESCRIPTION = """
회의 일정 intervals 가 주어집니다. intervals[i] = [start, end] 는 i 번째 회의가 start 에 시작해 end 에 끝난다는 뜻입니다.
모든 회의를 진행하는 데 필요한 회의실의 최소 개수를 return 하세요.

어떤 회의가 끝나는 시각에 다른 회의가 바로 그 방을 쓸 수 있습니다. ([1, 5] 와 [5, 8] 은 같은 방 사용 가능)

제한사항
- 0 ≤ len(intervals) ≤ 100,000
- 0 ≤ start < end ≤ 10^9

입출력 예
intervals = [[0, 30], [5, 10], [15, 20]]  →  2
intervals = [[7, 10], [2, 4]]             →  1
intervals = [[1, 5], [5, 8], [2, 6]]      →  2
"""

SIGNATURE = "def solution(intervals: list[list[int]]) -> int:"

HINTS = [
    "답은 '어떤 순간에 동시에 진행 중인 회의 수' 의 최댓값과 같습니다.",
    "시작 시각 순으로 회의를 배정하면서, 지금 쓰는 방들 중 '가장 빨리 비는 방' 만 알면 됩니다. 어떤 자료구조가 최솟값을 빠르게 줄까요?",
    "방법 1: 시작 기준 정렬 + 끝 시각 최소 힙. heap[0] ≤ start 면 heappop 후 재사용, 매번 heappush(end). 답은 힙 크기의 최댓값.",
    "방법 2 (스위프 라인): (start, +1), (end, -1) 이벤트를 만들어 정렬하고 누적합의 최댓값을 구하세요. 같은 시각이면 -1(끝)을 먼저 처리해야 합니다.",
]

TESTS = [
    {"input": [[[0, 30], [5, 10], [15, 20]]], "output": 2},
    {"input": [[[7, 10], [2, 4]]], "output": 1},
    {"input": [[[1, 5], [5, 8], [2, 6]]], "output": 2},
    {"input": [[]], "output": 0},
    {"input": [[[1, 2]]], "output": 1},
    {"input": [[[1, 10], [1, 10], [1, 10]]], "output": 3},
    {"input": [[[1, 3], [3, 5], [5, 7], [7, 9]]], "output": 1},
    {"input": [[[9, 10], [4, 9], [4, 17]]], "output": 2},
    {"input": [[[2, 15], [36, 45], [9, 29], [16, 23], [4, 9]]], "output": 2},
    {"input": [[[1, 4], [2, 5], [3, 6], [4, 7], [5, 8]]], "output": 3},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    intervals = []
    for _ in range(100_000):
        s = random.randint(0, 10**9 - 10**6)
        intervals.append([s, s + random.randint(1, 10**6)])
    return {"input": [intervals], "output": None}


EXPLANATION = """
핵심: 필요한 방 수 = 동시에 진행 중인 회의 수의 최댓값.

[방법 1] 최소 힙 (min-heap)
1. 시작 시각 기준 정렬
2. heap 에는 '사용 중인 방들의 끝나는 시각' 을 넣음
3. 새 회의 [s, e]: heap[0] ≤ s 면 그 방이 비었으므로 heappop (재사용)
4. heappush(heap, e). 마지막 힙 크기 = 지금까지 동시에 쓴 방 수의 최댓값
   (pop 은 push 직전에 최대 1번만 하므로 힙 크기는 줄지 않고, 최종 크기가 곧 답)

[방법 2] 스위프 라인 (sweep line)
  시간축을 왼쪽에서 오른쪽으로 쓸며 시작 +1, 끝 -1.

  시간:   0    5    10   15   20   30
  이벤트: +1   +1   -1   +1   -1   -1
  진행중:  1    2    1    2    1    0   → 최댓값 2

  같은 시각에 끝(-1)과 시작(+1)이 있으면 끝을 먼저 처리해야 [1,5],[5,8] 이 방 1개로 계산됩니다.
  (time, delta) 튜플 정렬 시 -1 < +1 이므로 자동으로 끝이 먼저 옵니다.

시간 O(n log n), 공간 O(n)
면접 포인트: 두 방법 모두 말할 수 있으면 좋습니다. 힙 방법은 '어느 방에 배정되는지' 까지 확장하기 쉽고,
스위프 라인은 '동시 접속자 수', '가장 붐비는 시간대' 같은 변형에 바로 쓰입니다.
"""


def reference(intervals):
    import heapq
    intervals = sorted(intervals)  # 시작 시각 순
    ends = []  # 사용 중인 방들의 끝나는 시각 (최소 힙)
    for start, end in intervals:
        if ends and ends[0] <= start:
            heapq.heappop(ends)  # 가장 빨리 끝나는 방을 재사용
        heapq.heappush(ends, end)
    return len(ends)


def alternative(intervals):
    # 스위프 라인: 시작 +1, 끝 -1 이벤트를 정렬해 누적합의 최댓값
    events = []
    for start, end in intervals:
        events.append((start, 1))
        events.append((end, -1))
    events.sort()  # 같은 시각이면 -1(끝) 이 +1(시작) 보다 먼저
    rooms = best = 0
    for _, delta in events:
        rooms += delta
        best = max(best, rooms)
    return best


def brute_force(intervals):
    # 모든 시작 시각에서 진행 중인 회의 수를 센다: O(n^2)
    best = 0
    for s, _ in intervals:
        best = max(best, sum(1 for a, b in intervals if a <= s < b))
    return best
