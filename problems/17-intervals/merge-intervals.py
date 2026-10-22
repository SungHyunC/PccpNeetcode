TITLE = "Merge Intervals (겹치는 구간 합치기)"
LEVEL = "Medium"
SOURCE = "LeetCode 56"
PATTERN = "시작 기준 정렬 후 마지막 구간과 비교하며 병합"

DESCRIPTION = """
구간 목록 intervals 가 주어집니다. intervals[i] = [start, end] (start ≤ end) 입니다.
겹치는 구간을 모두 하나로 합친 뒤, 서로 겹치지 않는 구간들을 시작 값 오름차순으로 return 하세요.

두 구간이 한 점이라도 공유하면 겹치는 것으로 봅니다. ([1, 4] 와 [4, 5] → [1, 5])

제한사항
- 1 ≤ len(intervals) ≤ 10,000
- 0 ≤ start ≤ end ≤ 10,000
- intervals 는 정렬되어 있지 않을 수 있습니다.

입출력 예
intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]  →  [[1, 6], [8, 10], [15, 18]]
intervals = [[1, 4], [4, 5]]                     →  [[1, 5]]
intervals = [[1, 4], [0, 0]]                     →  [[0, 0], [1, 4]]
"""

SIGNATURE = "def solution(intervals: list[list[int]]) -> list[list[int]]:"

HINTS = [
    "정렬하지 않으면 어떤 구간과 어떤 구간이 합쳐질지 알기 어렵습니다. 무엇을 기준으로 정렬할까요?",
    "시작 값으로 정렬하면, 새 구간은 '지금까지 만든 결과의 마지막 구간' 하고만 겹칠 수 있습니다.",
    "정렬 후 merged 리스트를 만들며: 현재 start ≤ merged[-1][1] 이면 merged[-1][1] = max(merged[-1][1], end), 아니면 새로 append.",
]

TESTS = [
    {"input": [[[1, 3], [2, 6], [8, 10], [15, 18]]], "output": [[1, 6], [8, 10], [15, 18]]},
    {"input": [[[1, 4], [4, 5]]], "output": [[1, 5]]},
    {"input": [[[1, 4], [0, 0]]], "output": [[0, 0], [1, 4]]},
    {"input": [[[5, 7]]], "output": [[5, 7]]},
    {"input": [[[1, 10], [2, 3], [4, 5], [6, 7]]], "output": [[1, 10]]},
    {"input": [[[6, 8], [1, 9], [2, 4], [4, 7]]], "output": [[1, 9]]},
    {"input": [[[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]]], "output": [[1, 10]]},
    {"input": [[[1, 2], [3, 4], [5, 6]]], "output": [[1, 2], [3, 4], [5, 6]]},
    {"input": [[[3, 3], [3, 3], [1, 2]]], "output": [[1, 2], [3, 3]]},
]

EXPLANATION = """
핵심: 시작 값으로 정렬하면 병합 후보는 항상 '결과의 마지막 구간' 하나뿐입니다.

1. intervals.sort()  (start 기준)
2. merged = [] 를 두고 각 구간 [s, e] 에 대해
   - merged 가 비었거나 s > merged[-1][1] → 겹치지 않음, 새로 추가
   - 아니면 겹침 → merged[-1][1] = max(merged[-1][1], e)
     (max 를 써야 [1,10] 뒤의 [2,3] 처럼 안쪽에 포함된 구간을 처리할 수 있음)

  정렬 후:  [1,3] [2,6] [8,10] [15,18]
  merged:   [1,3] → [1,6] → [1,6],[8,10] → [1,6],[8,10],[15,18]

시간 O(n log n), 공간 O(n) (결과)
면접 포인트: "끝 값을 그냥 e 로 덮어쓰면 안 되는 반례" ([1,10],[2,3]) 를 직접 말해 보세요.
닿기만 하는 구간([1,4],[4,5])을 합칠지 여부는 문제마다 다르니 비교 연산자(< vs ≤)를 꼭 확인합니다.
"""


def reference(intervals):
    intervals = sorted(intervals)  # 시작 값 기준 정렬
    merged = []
    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])  # 겹치지 않으면 새 구간 시작
        else:
            merged[-1][1] = max(merged[-1][1], end)  # 겹치면 끝을 늘림
    return merged


def alternative(intervals):
    # 좌표 범위가 작을 때: 차분 배열(difference array)로 '덮인 칸' 을 표시하는 방법
    # 점 하나짜리 구간 [3,3] 도 표현하려고 좌표를 2배로 늘립니다.
    size = 2 * max(e for _, e in intervals) + 2
    diff = [0] * (size + 1)
    for s, e in intervals:
        diff[2 * s] += 1
        diff[2 * e + 1] -= 1
    result, cover, start = [], 0, None
    for x in range(size + 1):
        cover += diff[x]
        if cover > 0 and start is None:
            start = x
        elif cover == 0 and start is not None:
            result.append([start // 2, (x - 1) // 2])
            start = None
    return result
