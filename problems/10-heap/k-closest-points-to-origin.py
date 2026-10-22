import heapq

TITLE = "K Closest Points to Origin (원점에 가까운 K개의 점)"
LEVEL = "Medium"
SOURCE = "LeetCode 973"
PATTERN = "크기 k 최대 힙(거리 부호 반전) / heapq.nsmallest"

DESCRIPTION = """
평면 위의 점 목록 points (points[i] = [x, y]) 와 정수 k 가 주어집니다.
원점 (0, 0) 에서 가장 가까운 점 k 개를 return 하세요. 거리는 유클리드 거리 sqrt(x^2 + y^2) 입니다.
결과의 순서는 상관없습니다. (k 번째와 k+1 번째 점의 거리가 같은 경우는 주어지지 않습니다.)

제한사항
- 1 ≤ k ≤ len(points) ≤ 10,000
- -10^4 ≤ x, y ≤ 10^4

입출력 예
points = [[1, 3], [-2, 2]],          k = 1  →  [[-2, 2]]
points = [[3, 3], [5, -1], [-2, 4]], k = 2  →  [[3, 3], [-2, 4]]
"""

SIGNATURE = "def solution(points: list[list[int]], k: int) -> list[list[int]]:"

HINTS = [
    "거리를 비교만 하면 되므로 sqrt 를 할 필요가 없습니다. x*x + y*y 를 그대로 비교하세요.",
    "전체를 거리순으로 정렬하면 O(n log n) 입니다. k 가 n 보다 훨씬 작다면 더 잘할 수 있습니다.",
    "'가장 가까운 k 개'를 유지하는 크기 k 의 최대 힙을 만드세요. 파이썬에서는 (-거리, x, y) 를 최소 힙에 넣으면 됩니다. 크기가 k 를 넘으면 가장 먼 점(루트)을 버립니다.",
]

TESTS = [
    {"input": [[[1, 3], [-2, 2]], 1], "output": [[-2, 2]]},
    {"input": [[[3, 3], [5, -1], [-2, 4]], 2], "output": [[3, 3], [-2, 4]]},
    {"input": [[[0, 0]], 1], "output": [[0, 0]]},
    {"input": [[[1, 1], [2, 2], [3, 3]], 3], "output": [[1, 1], [2, 2], [3, 3]]},
    {"input": [[[-5, -5], [1, 0], [0, -2], [10, 10]], 2], "output": [[1, 0], [0, -2]]},
    {"input": [[[2, 2], [-1, -1], [0, 3], [1, -1]], 2], "output": [[-1, -1], [1, -1]]},
    {"input": [[[10000, 10000], [-10000, -9999], [0, 1]], 1], "output": [[0, 1]]},
]

COMPARE = "unordered"

EXPLANATION = """
핵심: Top-k "작은" 값 → 크기 k 의 "최대" 힙. 힙의 루트에 '지금까지 고른 k 개 중 가장 먼 점'을 두고,
더 가까운 점이 오면 그 점과 교체합니다.

  k = 2, 점: (3,3)=18  (5,-1)=26  (-2,4)=20
  push (3,3)            힙 {18}
  push (5,-1)           힙 {18, 26}       (루트 = 가장 먼 26)
  (-2,4)=20 < 26 → 교체  힙 {18, 20}      → 답 [(3,3), (-2,4)]

1. heap = [] (원소: (-dist, x, y) → 최소 힙이 최대 힙처럼 동작)
2. 점마다 dist = x*x + y*y
   - 힙 크기 < k 이면 push
   - 아니면 dist < -heap[0][0] 일 때 heapreplace
3. 힙에 남은 점들을 반환

시간 O(n log k), 공간 O(k)
면접 포인트: 세 가지 풀이를 비교할 수 있으면 좋습니다.
- 정렬: O(n log n), 가장 간단 (brute_force)
- 크기 k 힙: O(n log k), 스트림(점이 계속 들어옴)에도 적용 가능 (reference)
- heapq.nsmallest(k, points, key=...): 내부적으로 힙을 쓰는 한 줄 풀이 (alternative)
- 퀵셀렉트(quickselect): 평균 O(n), 최악 O(n^2)
sqrt 를 생략해도 대소 관계가 유지된다는 점, 튜플의 첫 원소로 우선순위를 정한다는 점을 언급하세요.
"""


def reference(points, k):
    heap = []  # (-거리, x, y): 루트가 '가장 먼 점'
    for x, y in points:
        dist = x * x + y * y          # sqrt 불필요
        if len(heap) < k:
            heapq.heappush(heap, (-dist, x, y))
        elif dist < -heap[0][0]:      # 현재 k 개 중 가장 먼 점보다 가까우면 교체
            heapq.heapreplace(heap, (-dist, x, y))
    return [[x, y] for _, x, y in heap]


def alternative(points, k):
    return heapq.nsmallest(k, points, key=lambda p: p[0] * p[0] + p[1] * p[1])


def brute_force(points, k):
    return sorted(points, key=lambda p: p[0] * p[0] + p[1] * p[1])[:k]
