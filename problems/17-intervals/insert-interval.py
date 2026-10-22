TITLE = "Insert Interval (구간 삽입)"
LEVEL = "Medium"
SOURCE = "LeetCode 57"
PATTERN = "왼쪽 / 겹침 / 오른쪽 세 구역으로 나눠 한 번 훑기"

DESCRIPTION = """
서로 겹치지 않고 시작 값 오름차순으로 정렬된 구간 목록 intervals 와 새 구간 new_interval 이 주어집니다.
new_interval 을 끼워 넣은 뒤, 겹치는 구간을 합쳐 여전히 '겹치지 않고 정렬된' 구간 목록을 return 하세요.

한 점이라도 공유하면 겹치는 것으로 보고 합칩니다. ([1, 2] 와 [2, 3] → [1, 3])

제한사항
- 0 ≤ len(intervals) ≤ 10,000
- intervals[i] = [start, end], 0 ≤ start ≤ end ≤ 100,000
- intervals 는 start 오름차순이며 서로 겹치지 않습니다.
- new_interval = [start, end], 0 ≤ start ≤ end ≤ 100,000

입출력 예
intervals = [[1, 3], [6, 9]],                         new_interval = [2, 5]   →  [[1, 5], [6, 9]]
intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], new_interval = [4, 8]   →  [[1, 2], [3, 10], [12, 16]]
intervals = [],                                       new_interval = [5, 7]   →  [[5, 7]]
"""

SIGNATURE = "def solution(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:"

HINTS = [
    "이미 정렬되어 있으니 다시 정렬할 필요가 없습니다. O(n) 한 번 훑기로 충분합니다.",
    "기존 구간은 세 종류로 나뉩니다: 새 구간보다 완전히 왼쪽(end < new.start), 겹치는 것, 완전히 오른쪽(start > new.end).",
    "왼쪽 것들은 그대로 담고, 겹치는 것들은 new = [min(시작들), max(끝들)] 로 흡수한 뒤 한 번 담고, 오른쪽 것들은 그대로 담으세요.",
]

TESTS = [
    {"input": [[[1, 3], [6, 9]], [2, 5]], "output": [[1, 5], [6, 9]]},
    {"input": [[[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]], "output": [[1, 2], [3, 10], [12, 16]]},
    {"input": [[], [5, 7]], "output": [[5, 7]]},
    {"input": [[[3, 5]], [0, 1]], "output": [[0, 1], [3, 5]]},
    {"input": [[[3, 5]], [7, 9]], "output": [[3, 5], [7, 9]]},
    {"input": [[[1, 2], [5, 6]], [3, 4]], "output": [[1, 2], [3, 4], [5, 6]]},
    {"input": [[[1, 2], [3, 4], [5, 6]], [0, 10]], "output": [[0, 10]]},
    {"input": [[[1, 2], [5, 6]], [2, 5]], "output": [[1, 6]]},
    {"input": [[[1, 5]], [2, 3]], "output": [[1, 5]]},
]

EXPLANATION = """
핵심: 입력이 이미 정렬·비중첩이므로 '왼쪽 → 겹침 → 오른쪽' 세 구역을 순서대로 지나가며 한 번에 처리합니다.

1. end < new.start 인 구간들 → 그대로 result 에 추가 (완전히 왼쪽)
2. start ≤ new.end 인 구간들 → 겹침. new = [min(new.start, start), max(new.end, end)] 로 흡수
3. 흡수가 끝난 new 를 result 에 추가
4. 남은 구간들(완전히 오른쪽) → 그대로 추가

  intervals: [1,2] [3,5] [6,7] [8,10] [12,16],  new = [4,8]
  왼쪽: [1,2]
  겹침: [3,5] [6,7] [8,10]  → new = [3,10]
  오른쪽: [12,16]
  결과: [1,2] [3,10] [12,16]

시간 O(n), 공간 O(n)
면접 포인트: "그냥 append 하고 Merge Intervals 를 다시 돌리면 O(n log n)" 이라는 쉬운 답을 먼저 말한 뒤,
정렬되어 있다는 조건을 활용해 O(n) 으로 줄이는 흐름이 좋습니다. 이진 탐색(bisect)으로 삽입 위치를 찾을 수도 있지만
결과 리스트를 만드는 데 어차피 O(n) 이 듭니다.
"""


def reference(intervals, new_interval):
    result = []
    i, n = 0, len(intervals)
    new_start, new_end = new_interval
    # 1) 새 구간보다 완전히 왼쪽
    while i < n and intervals[i][1] < new_start:
        result.append(intervals[i])
        i += 1
    # 2) 겹치는 구간들을 새 구간에 흡수
    while i < n and intervals[i][0] <= new_end:
        new_start = min(new_start, intervals[i][0])
        new_end = max(new_end, intervals[i][1])
        i += 1
    result.append([new_start, new_end])
    # 3) 나머지(완전히 오른쪽)
    result.extend(intervals[i:])
    return result


def alternative(intervals, new_interval):
    # 쉬운 방법: 넣고 정렬한 뒤 Merge Intervals. O(n log n)
    merged = []
    for s, e in sorted(intervals + [new_interval]):
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return merged
