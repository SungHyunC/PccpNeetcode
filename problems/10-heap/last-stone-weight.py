import heapq
import random

TITLE = "Last Stone Weight (마지막 돌의 무게)"
LEVEL = "Easy"
SOURCE = "LeetCode 1046"
PATTERN = "최대 힙(부호 뒤집기)으로 가장 큰 두 개 반복 추출"

DESCRIPTION = """
돌들의 무게가 담긴 정수 배열 stones 가 주어집니다.
매 차례 가장 무거운 돌 두 개 x ≥ y 를 골라 부딪칩니다.
- x == y 이면 두 돌 모두 사라집니다.
- x > y 이면 무게 y 인 돌은 사라지고, 무게 x 인 돌은 무게 x - y 인 돌이 됩니다.
돌이 1개 이하로 남을 때까지 반복한 뒤, 남은 돌의 무게(없으면 0)를 return 하세요.

제한사항
- 1 ≤ len(stones) ≤ 100,000
- 1 ≤ stones[i] ≤ 10^9
- 효율성 테스트가 있습니다 (매번 정렬하면 시간 초과).

입출력 예
stones = [2, 7, 4, 1, 8, 1]  →  1
  8, 7 → 1 남음  [2, 4, 1, 1, 1]
  4, 2 → 2 남음  [2, 1, 1, 1]
  2, 1 → 1 남음  [1, 1, 1]
  1, 1 → 둘 다 사라짐 [1]  → 1
stones = [1]  →  1
stones = [2, 2]  →  0
"""

SIGNATURE = "def solution(stones: list[int]) -> int:"

HINTS = [
    "매 차례 정렬해서 가장 큰 두 개를 고르면 O(n^2 log n) 입니다. '가장 큰 값을 반복해서 꺼내고 새 값을 넣는' 작업에 맞는 자료구조는?",
    "파이썬 heapq 는 최소 힙(min-heap)만 제공합니다. 값에 -1 을 곱해서 넣으면 최대 힙처럼 쓸 수 있습니다.",
    "heap = [-s for s in stones]; heapify(heap). 원소가 2개 이상인 동안 x = -heappop, y = -heappop, x != y 면 heappush(heap, -(x - y)). 마지막에 -heap[0] 또는 0.",
]

TESTS = [
    {"input": [[2, 7, 4, 1, 8, 1]], "output": 1},
    {"input": [[1]], "output": 1},
    {"input": [[2, 2]], "output": 0},
    {"input": [[10, 4]], "output": 6},
    {"input": [[3, 7, 2]], "output": 2},
    {"input": [[5, 5, 5]], "output": 5},
    {"input": [[1, 1, 1, 1]], "output": 0},
    {"input": [[1_000_000_000, 1, 1]], "output": 999_999_998},
]

PERF_LIMIT = 1.0


def perf_case():
    return {"input": [[random.randint(1, 10**9) for _ in range(100_000)]], "output": None}


EXPLANATION = """
핵심: "가장 큰 것 꺼내기"를 반복 → 최대 힙. 파이썬은 최소 힙뿐이므로 부호를 뒤집어 넣습니다.

  stones = [2, 7, 4, 1, 8, 1]
  heap(부호 반전) = [-8, -7, -4, -1, -2, -1]   heap[0] = -8 → 실제 최댓값 8
  pop -8, pop -7 → 차이 1 → push -1
  ...

1. heap = [-s for s in stones]; heapq.heapify(heap)   ← O(n)
2. len(heap) > 1 동안: x = -heappop, y = -heappop (x ≥ y), x > y 면 heappush(heap, -(x - y))
3. heap 이 있으면 -heap[0], 없으면 0

시간 O(n log n) (매 차례 pop 2번 + push 1번, 차례는 최대 n - 1번), 공간 O(n)
면접 포인트: heapify 는 O(n) 이고, n 번 push 하는 것(O(n log n))보다 빠릅니다.
"최대 힙은 부호 반전" 은 파이썬 코딩 테스트의 필수 관용구입니다.
매번 정렬하는 brute_force 는 O(n^2 log n) 이라 효율성 테스트에서 실패합니다.
"""


def reference(stones):
    heap = [-s for s in stones]   # 부호를 뒤집어 최대 힙처럼 사용
    heapq.heapify(heap)           # O(n)
    while len(heap) > 1:
        x = -heapq.heappop(heap)  # 가장 무거운 돌
        y = -heapq.heappop(heap)  # 두 번째로 무거운 돌
        if x != y:
            heapq.heappush(heap, -(x - y))
    return -heap[0] if heap else 0


def brute_force(stones):
    # 매번 정렬: O(n^2 log n) → 효율성 실패
    stones = list(stones)
    while len(stones) > 1:
        stones.sort()
        x, y = stones.pop(), stones.pop()
        if x != y:
            stones.append(x - y)
    return stones[0] if stones else 0
