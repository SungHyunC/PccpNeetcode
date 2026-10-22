TITLE = "Non-overlapping Intervals (겹치지 않게 최소 제거)"
LEVEL = "Medium"
SOURCE = "LeetCode 435"
PATTERN = "끝 기준 정렬 그리디 (활동 선택 문제)"

DESCRIPTION = """
구간 목록 intervals 가 주어집니다. intervals[i] = [start, end] (start < end).
일부 구간을 지워서 남은 구간들이 서로 겹치지 않게 만들려고 합니다.
지워야 하는 구간 개수의 최솟값을 return 하세요.

끝과 시작이 맞닿는 것은 겹치지 않는 것으로 봅니다. ([1, 2] 와 [2, 3] 은 공존 가능)

제한사항
- 1 ≤ len(intervals) ≤ 100,000
- -50,000 ≤ start < end ≤ 50,000

입출력 예
intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]  →  1   ([1, 3] 을 지움)
intervals = [[1, 2], [1, 2], [1, 2]]          →  2
intervals = [[1, 2], [2, 3]]                  →  0
"""

SIGNATURE = "def solution(intervals: list[list[int]]) -> int:"

HINTS = [
    "'최소 몇 개를 지울까' 는 '최대 몇 개를 겹치지 않게 남길까' 와 같은 질문입니다. (답 = n - 최대로 남길 수 있는 개수)",
    "회의실 하나에 회의를 최대한 많이 넣는 문제(활동 선택)와 같습니다. 어떤 회의를 먼저 고르는 것이 항상 이득일까요?",
    "가장 빨리 끝나는 구간을 고르면 뒤에 남는 시간이 가장 많습니다. end 로 정렬하고, start ≥ 마지막으로 고른 end 이면 고르고 아니면 지우세요.",
]

TESTS = [
    {"input": [[[1, 2], [2, 3], [3, 4], [1, 3]]], "output": 1},
    {"input": [[[1, 2], [1, 2], [1, 2]]], "output": 2},
    {"input": [[[1, 2], [2, 3]]], "output": 0},
    {"input": [[[5, 9]]], "output": 0},
    {"input": [[[1, 100], [11, 22], [1, 11], [2, 12]]], "output": 2},
    {"input": [[[-5, -1], [-3, 2], [0, 4], [3, 6]]], "output": 2},
    {"input": [[[0, 10], [1, 2], [3, 4], [5, 6], [7, 8]]], "output": 1},
    {"input": [[[1, 3], [2, 4], [3, 5], [4, 6]]], "output": 2},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    intervals = []
    for _ in range(100_000):
        s = random.randint(-50_000, 49_000)
        intervals.append([s, s + random.randint(1, 1000)])
    return {"input": [intervals], "output": None}


EXPLANATION = """
핵심: 활동 선택 문제(activity selection). '끝나는 시간이 가장 빠른 구간' 부터 욕심내서 고르면
남길 수 있는 구간 수가 최대가 됩니다. 답 = 전체 - 남긴 개수.

1. end 기준 오름차순 정렬
2. last_end = -무한대, kept = 0
3. 각 [s, e] 에 대해 s ≥ last_end 이면 남김(kept += 1, last_end = e), 아니면 지움
4. return n - kept

왜 끝 기준인가?
  가장 먼저 끝나는 구간 A 를 포함하는 최적해가 항상 존재합니다.
  어떤 최적해의 첫 구간 B 를 A 로 바꿔도 A.end ≤ B.end 라서 뒤 구간과 겹치지 않기 때문입니다(교환 논증).

  시작 기준으로 정렬하면 틀리는 예:  [1,100] [11,22] [1,11] [2,12]
  끝 기준 정렬: [1,11] [2,12] [11,22] [1,100]
    [1,11] 남김 → [2,12] 지움 → [11,22] 남김 (11 ≥ 11) → [1,100] 지움  ⇒ 2개 제거

시간 O(n log n), 공간 O(1) (정렬 제외)
면접 포인트: 그리디가 왜 맞는지 '교환 논증(exchange argument)' 으로 한 문장 설명할 수 있어야 합니다.
O(n^2) DP(LIS 와 비슷한 형태)도 가능하지만 n = 100,000 에서는 시간 초과입니다.
"""


def reference(intervals):
    intervals = sorted(intervals, key=lambda x: x[1])  # 끝 기준 정렬
    kept = 0
    last_end = float("-inf")
    for start, end in intervals:
        if start >= last_end:  # 겹치지 않으면 남긴다
            kept += 1
            last_end = end
        # 겹치면 지운다 (끝이 더 늦은 현재 구간을 버리는 셈)
    return len(intervals) - kept


def alternative(intervals):
    # 시작 기준 정렬도 가능: 겹치면 '끝이 더 큰 쪽' 을 지운다
    intervals = sorted(intervals)
    removed = 0
    prev_end = intervals[0][1]
    for start, end in intervals[1:]:
        if start < prev_end:
            removed += 1
            prev_end = min(prev_end, end)  # 더 일찍 끝나는 쪽을 남김
        else:
            prev_end = end
    return removed


def brute_force(intervals):
    # O(n^2) DP: dp[i] = i 번째(시작 정렬)로 끝나는 겹치지 않는 최대 개수
    intervals = sorted(intervals)
    n = len(intervals)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if intervals[j][1] <= intervals[i][0]:
                dp[i] = max(dp[i], dp[j] + 1)
    return n - max(dp)
