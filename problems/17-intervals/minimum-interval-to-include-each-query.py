TITLE = "Minimum Interval to Include Each Query (각 질의를 포함하는 최소 구간)"
LEVEL = "Hard"
SOURCE = "LeetCode 1851"
PATTERN = "구간·질의 오프라인 정렬 + 최소 힙"

DESCRIPTION = """
구간 목록 intervals 와 정수 질의 목록 queries 가 주어집니다.
intervals[i] = [left, right] 는 left 이상 right 이하의 정수를 모두 포함하는 닫힌 구간이며,
크기는 right - left + 1 입니다.

각 질의 q 에 대해, q 를 포함하는(left ≤ q ≤ right) 구간들 중 크기가 가장 작은 구간의 크기를 구하세요.
그런 구간이 없으면 -1 입니다. 결과를 queries 와 같은 순서의 리스트로 return 하세요.

제한사항
- 1 ≤ len(intervals) ≤ 100,000
- 1 ≤ len(queries) ≤ 100,000
- 1 ≤ left ≤ right ≤ 10^7
- 1 ≤ queries[j] ≤ 10^7
- queries 는 정렬되어 있지 않으며 중복이 있을 수 있습니다.

입출력 예
intervals = [[1, 4], [2, 4], [3, 6], [4, 4]], queries = [2, 3, 4, 5]  →  [3, 3, 1, 4]
intervals = [[2, 3], [2, 5], [1, 8], [20, 25]], queries = [2, 19, 5, 22]  →  [2, -1, 4, 6]
"""

SIGNATURE = "def solution(intervals: list[list[int]], queries: list[int]) -> list[int]:"

HINTS = [
    "질의마다 모든 구간을 보면 O(N·Q) = 10^10 → 시간 초과. 질의를 '작은 값부터' 처리하면 무엇이 좋아질까요?",
    "질의를 오름차순으로 처리하면, left ≤ q 인 구간들은 한 번 '후보' 가 되면 다음 질의에서도 left 조건을 계속 만족합니다. (구간도 left 기준 정렬)",
    "후보들을 (크기, right) 최소 힙에 넣으세요. 힙 맨 위 구간의 right < q 이면 앞으로도 쓸모없으므로 pop 합니다.",
    "결과는 원래 순서로 돌려줘야 하므로 sorted(range(len(queries)), key=...) 처럼 인덱스를 함께 정렬하세요. 같은 값의 질의는 dict 로 캐시해도 됩니다.",
]

TESTS = [
    {"input": [[[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]], "output": [3, 3, 1, 4]},
    {"input": [[[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]], "output": [2, -1, 4, 6]},
    {"input": [[[5, 5]], [5, 4, 6]], "output": [1, -1, -1]},
    {"input": [[[1, 10]], [10, 1, 10, 11]], "output": [10, 10, 10, -1]},
    {"input": [[[1, 3], [5, 7], [9, 11]], [4, 8, 12, 2]], "output": [-1, -1, -1, 3]},
    {"input": [[[1, 100], [40, 60], [45, 55], [50, 50]], [50, 45, 40, 1, 100]], "output": [1, 11, 21, 100, 100]},
    {"input": [[[4, 5], [5, 8], [1, 9], [8, 10], [1, 6]], [7, 9, 3, 9, 3]], "output": [4, 3, 6, 3, 6]},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    n = 50_000
    intervals = []
    for _ in range(n):
        left = random.randint(1, 10**7 - 10**5)
        intervals.append([left, left + random.randint(0, 10**5)])
    queries = [random.randint(1, 10**7) for _ in range(n)]
    return {"input": [intervals, queries], "output": None}


EXPLANATION = """
핵심: 질의를 정렬해서 오프라인(offline)으로 처리하고, '현재 질의를 포함할 수도 있는 구간' 을 크기 기준 최소 힙으로 관리합니다.

1. intervals 를 left 기준 정렬, 질의 인덱스를 질의 값 기준 정렬
2. 작은 질의 q 부터:
   a. left ≤ q 인 구간을 모두 힙에 push: (크기, right)
   b. 힙 맨 위의 right < q 이면 pop (q 를 포함하지 않고, 더 큰 질의도 포함 못 함 → 영원히 버림)
   c. 힙이 비었으면 -1, 아니면 heap[0][0] 이 답
3. 원래 인덱스 위치에 답을 기록

  intervals(정렬): [1,4] [2,4] [3,6] [4,4]     queries(정렬): 2 3 4 5
  q=2: push [1,4](4),[2,4](3)            → heap top (3, 4) → 3
  q=3: push [3,6](4)                     → top (3, 4) → 3
  q=4: push [4,4](1)                     → top (1, 4) → 1
  q=5: top (1,4) right 4<5 pop, (3,4) pop → top (4, 6) → 4

'게으른 삭제(lazy deletion)': 힙 안쪽에 만료된 구간이 남아 있어도 맨 위에 올라올 때만 버리면 충분합니다.

시간 O(N log N + Q log Q), 공간 O(N + Q)
면접 포인트: '질의를 정렬해도 되는가?' → 답만 원래 순서로 돌려주면 되므로 오프라인 처리 가능.
온라인(질의가 하나씩 들어옴)이면 세그먼트 트리 등이 필요하다는 점도 언급하면 좋습니다.
"""


def reference(intervals, queries):
    import heapq
    intervals = sorted(intervals)  # left 기준
    order = sorted(range(len(queries)), key=lambda j: queries[j])
    answer = [-1] * len(queries)
    heap = []  # (크기, right)
    i = 0
    for j in order:
        q = queries[j]
        # left ≤ q 인 구간을 후보로 추가
        while i < len(intervals) and intervals[i][0] <= q:
            left, right = intervals[i]
            heapq.heappush(heap, (right - left + 1, right))
            i += 1
        # q 를 포함하지 못하는(이미 끝난) 구간은 버림
        while heap and heap[0][1] < q:
            heapq.heappop(heap)
        if heap:
            answer[j] = heap[0][0]
    return answer


def brute_force(intervals, queries):
    answer = []
    for q in queries:
        best = -1
        for left, right in intervals:
            if left <= q <= right:
                size = right - left + 1
                if best == -1 or size < best:
                    best = size
        answer.append(best)
    return answer
