TITLE = "Meeting Rooms (회의실 배정 가능 여부)"
LEVEL = "Easy"
SOURCE = "LeetCode 252"
PATTERN = "시작 시각으로 정렬 후 이웃끼리 겹침 확인"

DESCRIPTION = """
한 사람이 참석해야 하는 회의 일정 intervals 가 주어집니다.
intervals[i] = [start, end] 는 i 번째 회의가 start 에 시작해 end 에 끝난다는 뜻입니다.
회의는 동시에 두 개를 들을 수 없습니다. 모든 회의에 빠짐없이 참석할 수 있으면 True,
아니면 False 를 return 하세요.

한 회의가 끝나는 시각에 바로 다음 회의가 시작하는 것은 괜찮습니다. ([1, 5] 와 [5, 8] 은 겹치지 않음)

제한사항
- 0 ≤ len(intervals) ≤ 10,000
- 0 ≤ start < end ≤ 1,000,000
- intervals 는 정렬되어 있지 않을 수 있습니다.

입출력 예
intervals = [[0, 30], [5, 10], [15, 20]]  →  False   ([0, 30] 이 나머지와 겹침)
intervals = [[7, 10], [2, 4]]             →  True
intervals = [[1, 5], [5, 8]]              →  True    (끝과 시작이 맞닿는 것은 허용)
"""

SIGNATURE = "def solution(intervals: list[list[int]]) -> bool:"

HINTS = [
    "모든 쌍을 비교하면 O(n^2) 입니다. 회의를 어떤 순서로 늘어놓으면 '바로 옆' 회의만 비교해도 될까요?",
    "시작 시각으로 정렬하면, 겹치는 회의가 있을 경우 반드시 인접한 두 회의 사이에서 겹침이 드러납니다.",
    "정렬 후 i = 1.. 에 대해 intervals[i][0] < intervals[i-1][1] 이면 False. 등호(=)는 겹침이 아닙니다.",
]

TESTS = [
    {"input": [[[0, 30], [5, 10], [15, 20]]], "output": False},
    {"input": [[[7, 10], [2, 4]]], "output": True},
    {"input": [[[1, 5], [5, 8]]], "output": True},
    {"input": [[]], "output": True},
    {"input": [[[3, 4]]], "output": True},
    {"input": [[[1, 5], [4, 6]]], "output": False},
    {"input": [[[9, 10], [1, 3], [6, 9], [3, 6]]], "output": True},
    {"input": [[[1, 10], [2, 3], [10, 11]]], "output": False},
    {"input": [[[5, 8], [5, 8]]], "output": False},
]

EXPLANATION = """
핵심: 시작 시각으로 정렬하면 '앞 회의의 끝 > 다음 회의의 시작' 인 인접 쌍이 있는지만 보면 됩니다.

1. intervals 를 start 기준으로 정렬
2. 인접한 두 회의 prev, cur 에 대해 cur.start < prev.end 이면 겹침 → False
3. 끝까지 문제 없으면 True

왜 인접 쌍만 보면 될까?
  정렬 후 a.start ≤ b.start ≤ c.start 일 때 a 와 c 가 겹친다면 c.start < a.end 이고
  b.start ≤ c.start < a.end 이므로 a 와 b 도 이미 겹칩니다. 즉 첫 번째 겹침은 항상 인접 쌍에서 발견됩니다.

  [0────────────30]
       [5──10]          ← 5 < 30 → 겹침!
                 [15──20]

시간 O(n log n) (정렬), 공간 O(1) ~ O(n) (정렬 방식에 따라)
면접 포인트: 구간 문제에서 가장 먼저 "어떤 기준으로 정렬할까?" 를 질문하세요.
끝과 시작이 같은 경우([1,5],[5,8])를 겹침으로 볼지 면접관에게 꼭 확인합니다.
"""


def reference(intervals):
    intervals = sorted(intervals)  # 시작 시각 기준 정렬
    for i in range(1, len(intervals)):
        # 다음 회의가 앞 회의가 끝나기 전에 시작하면 겹침
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True


def brute_force(intervals):
    n = len(intervals)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = intervals[i], intervals[j]
            # 두 구간이 겹치는 조건: a.start < b.end 이고 b.start < a.end
            if a[0] < b[1] and b[0] < a[1]:
                return False
    return True
