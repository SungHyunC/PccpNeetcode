import heapq
import random

TITLE = "Mix Spicy Food (매운 음식 섞기)"
LEVEL = "Medium"
SOURCE = "PCCP 기출 유형 (프로그래머스 '더 맵게' 유형)"
PATTERN = "최소 힙으로 가장 작은 두 값을 반복해서 꺼내 합치기"

DESCRIPTION = """
분식집 사장님은 모든 소스의 매운맛 지수를 K 이상으로 만들고 싶습니다.
매운맛이 가장 약한 소스 두 개를 골라 아래 방식으로 섞으면 새 소스 하나가 됩니다.

  섞은 소스의 지수 = (가장 약한 소스의 지수) + 2 x (두 번째로 약한 소스의 지수)

섞은 두 소스는 사라지고 새 소스가 추가됩니다. 모든 소스의 지수가 K 이상이 될 때까지 이 과정을 반복합니다.
섞어야 하는 최소 횟수를 return 하세요. 소스가 하나만 남았는데도 K 미만이라 불가능하면 -1 을 return 하세요.
처음부터 모든 소스가 K 이상이면 0 입니다.

제한사항
- 1 ≤ len(scoville) ≤ 200,000
- 0 ≤ scoville[i] ≤ 1,000,000
- 0 ≤ K ≤ 1,000,000,000
- 효율성 테스트가 있습니다.

입출력 예
scoville = [1, 3, 2, 8, 11], K = 10  →  3
  1 + 2x2 = 5   → [3, 5, 8, 11]
  3 + 2x5 = 13  → [8, 11, 13]
  8 + 2x11 = 30 → [13, 30]   모두 10 이상
scoville = [0, 0, 0], K = 1  →  -1
"""

SIGNATURE = "def solution(scoville: list[int], K: int) -> int:"

HINTS = [
    "매번 '가장 작은 두 값'이 필요합니다. 매번 정렬하거나 min() 을 두 번 하면 O(n^2) 이상입니다.",
    "가장 작은 값을 반복해서 꺼내고 새 값을 넣는 작업 → 최소 힙(heapq). heapify 로 O(n) 에 힙을 만드세요.",
    "while heap[0] < K: 원소가 1개뿐이면 -1, 아니면 a = heappop, b = heappop, heappush(a + 2*b), count += 1. 루프가 끝나면 count.",
]

TESTS = [
    {"input": [[1, 3, 2, 8, 11], 10], "output": 3},
    {"input": [[0, 0, 0], 1], "output": -1},
    {"input": [[10, 12, 15], 10], "output": 0},
    {"input": [[5], 7], "output": -1},
    {"input": [[7], 7], "output": 0},
    {"input": [[0, 0], 0], "output": 0},
    {"input": [[1, 1], 3], "output": 1},
    {"input": [[4, 1, 1, 2, 9, 0], 20], "output": 5},
    {"input": [[1, 2, 3, 9, 10, 12], 7], "output": 2},
]

PERF_LIMIT = 1.0


def perf_case():
    scoville = [random.randint(0, 1000) for _ in range(100_000)]
    return {"input": [scoville, 1_000_000], "output": None}


EXPLANATION = """
핵심: "가장 작은 두 개를 꺼내 합쳐서 다시 넣기" 의 반복 → 최소 힙. (허프만 코딩과 같은 구조)

  heap = [1, 2, 3, 8, 11], K = 10
  pop 1, pop 2 → push 1 + 2*2 = 5    heap = [3, 5, 8, 11]     1회
  pop 3, pop 5 → push 3 + 2*5 = 13   heap = [8, 11, 13]       2회
  pop 8, pop 11 → push 30            heap = [13, 30]          3회
  heap[0] = 13 ≥ 10 → 종료, 답 3

1. heapq.heapify(scoville)   ← O(n)
2. while heap[0] < K:
   - len(heap) < 2 이면 -1 (더 섞을 수 없음)
   - a = heappop, b = heappop, heappush(a + 2*b), count += 1
3. count 반환

시간 O(n log n) (섞을 때마다 원소가 1개 줄어 최대 n - 1 번), 공간 O(1) 추가 (입력을 힙으로 사용)
면접 포인트(PCCP): 프로그래머스 '더 맵게' 와 같은 유형으로, 효율성 테스트 때문에 힙이 필수입니다.
- heap[0] 이 최솟값이라는 점을 이용해 "모두 K 이상인가?" 를 O(1) 에 확인합니다 (all() 로 매번 확인하면 느림).
- 원소가 1개 남았을 때의 -1 처리, 처음부터 조건을 만족하는 0 처리를 잊지 마세요.
- 매번 정렬하는 brute_force 는 효율성 테스트에서 실패합니다.
"""


def reference(scoville, K):
    heap = list(scoville)
    heapq.heapify(heap)                  # O(n) 으로 최소 힙 만들기
    count = 0
    while heap[0] < K:                   # 가장 약한 소스가 K 미만인 동안
        if len(heap) < 2:
            return -1                    # 섞을 상대가 없음
        a = heapq.heappop(heap)          # 가장 약한 소스
        b = heapq.heappop(heap)          # 두 번째로 약한 소스
        heapq.heappush(heap, a + 2 * b)
        count += 1
    return count


def brute_force(scoville, K):
    # 매번 정렬: O(n^2 log n) → 효율성 실패
    foods = list(scoville)
    count = 0
    while True:
        foods.sort()
        if foods[0] >= K:
            return count
        if len(foods) < 2:
            return -1
        a, b = foods[0], foods[1]
        foods = foods[2:] + [a + 2 * b]
        count += 1
