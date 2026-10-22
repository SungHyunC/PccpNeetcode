import heapq
import random

TITLE = "Kth Largest Element in an Array (배열에서 k번째로 큰 값)"
LEVEL = "Medium"
SOURCE = "LeetCode 215"
PATTERN = "크기 k 최소 힙 / 퀵셀렉트"

DESCRIPTION = """
정수 배열 nums 와 정수 k 가 주어집니다. 배열을 정렬했을 때 k 번째로 큰 값을 return 하세요.
'서로 다른 값' 중 k 번째가 아니라, 중복을 포함한 순서에서 k 번째입니다.
예) [3, 3, 2] 에서 2번째로 큰 값은 3

제한사항
- 1 ≤ k ≤ len(nums) ≤ 100,000
- -10^4 ≤ nums[i] ≤ 10^4
- 정렬 없이 풀 수 있을지 생각해 보세요.

입출력 예
nums = [3, 2, 1, 5, 6, 4],          k = 2  →  5
nums = [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4  →  4
"""

SIGNATURE = "def solution(nums: list[int], k: int) -> int:"

HINTS = [
    "정렬하면 sorted(nums)[-k] 로 O(n log n) 입니다. 면접에서는 '정렬 없이' 를 요구하는 경우가 많습니다.",
    "크기 k 의 최소 힙에 '지금까지 본 값 중 큰 k 개'를 유지하면, 힙의 루트가 k 번째로 큰 값입니다. O(n log k).",
    "평균 O(n) 을 원한다면 퀵셀렉트: 피벗을 골라 큰 값 / 같은 값 / 작은 값으로 나누고, k 가 어느 그룹에 속하는지 보고 그쪽만 계속 탐색합니다.",
]

TESTS = [
    {"input": [[3, 2, 1, 5, 6, 4], 2], "output": 5},
    {"input": [[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], "output": 4},
    {"input": [[1], 1], "output": 1},
    {"input": [[2, 2, 2], 2], "output": 2},
    {"input": [[-1, -1], 1], "output": -1},
    {"input": [[7, 6, 5, 4, 3, 2, 1], 7], "output": 1},
    {"input": [[-10000, 10000, 0, 5, -5], 3], "output": 0},
]

EXPLANATION = """
핵심: Top-k 패턴. "큰 값 k 개"만 최소 힙에 남기면, 그중 가장 작은 값(루트)이 k 번째로 큰 값입니다.

  nums = [3, 2, 1, 5, 6, 4], k = 2
  3 → [3]       2 → [2, 3]      1 → 1 < 2 무시
  5 → [3, 5]    6 → [5, 6]      4 → 4 < 5 무시     → heap[0] = 5

1. heap = nums[:k] 로 시작해 heapify
2. 나머지 x 마다 x > heap[0] 이면 heapreplace(heap, x)
3. heap[0] 반환

시간 O(n log k), 공간 O(k)

퀵셀렉트(alternative): 무작위 피벗으로 [큰 값 | 같은 값 | 작은 값] 3분할 → k 가 속한 쪽만 재귀.
평균 O(n), 최악 O(n^2) (무작위 피벗으로 확률적으로 회피). 같은 값이 많을 때 3분할이 중요합니다.

면접 포인트: 정렬 O(n log n) → 힙 O(n log k) → 퀵셀렉트 평균 O(n) 의 순서로 개선을 이야기하고,
각각의 장단점(힙은 스트림에 강하고 최악도 보장, 퀵셀렉트는 평균이 빠르지만 배열 전체가 필요)을 비교하세요.
heapq.nlargest(k, nums)[-1] 도 내부적으로 힙을 쓰는 한 줄 풀이입니다.
"""


def reference(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)            # 처음 k 개로 최소 힙
    for x in nums[k:]:
        if x > heap[0]:            # 상위 k 개 중 최솟값보다 크면 교체
            heapq.heapreplace(heap, x)
    return heap[0]                 # 상위 k 개 중 가장 작은 값


def alternative(nums, k):
    # 퀵셀렉트 (3분할, 반복문): 평균 O(n)
    while True:
        pivot = random.choice(nums)
        bigger = [x for x in nums if x > pivot]
        equal_count = sum(1 for x in nums if x == pivot)
        if k <= len(bigger):
            nums = bigger                       # 답이 큰 쪽에 있음
        elif k <= len(bigger) + equal_count:
            return pivot                        # 답이 피벗
        else:
            k -= len(bigger) + equal_count      # 작은 쪽에서 순위 조정
            nums = [x for x in nums if x < pivot]


def brute_force(nums, k):
    return sorted(nums, reverse=True)[k - 1]
