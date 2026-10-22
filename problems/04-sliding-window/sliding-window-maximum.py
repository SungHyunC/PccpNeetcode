TITLE = "Sliding Window Maximum (슬라이딩 윈도우 최댓값)"
LEVEL = "Hard"
SOURCE = "LeetCode 239"
PATTERN = "단조 감소 덱(monotonic deque)에 인덱스 저장"

DESCRIPTION = """
정수 배열 nums 와 윈도우 크기 k 가 주어집니다.
길이 k 인 윈도우를 맨 왼쪽부터 한 칸씩 오른쪽으로 밀 때,
각 위치에서 윈도우 안의 최댓값을 차례대로 담은 리스트를 return 하세요.

제한사항
- 1 ≤ len(nums) ≤ 100,000
- -10,000 ≤ nums[i] ≤ 10,000
- 1 ≤ k ≤ len(nums)

입출력 예
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3  →  [3, 3, 5, 5, 6, 7]
  [1  3  -1] -3  5  3  6  7   → 3
   1 [3  -1  -3] 5  3  6  7   → 3
   1  3 [-1  -3  5] 3  6  7   → 5
   1  3  -1 [-3  5  3] 6  7   → 5
   1  3  -1  -3 [5  3  6] 7   → 6
   1  3  -1  -3  5 [3  6  7]  → 7
nums = [1], k = 1  →  [1]
"""

SIGNATURE = "def solution(nums: list[int], k: int) -> list[int]:"

HINTS = [
    "윈도우마다 max() 를 구하면 O(n·k) 입니다. n = 100,000, k = 50,000 이면 시간 초과입니다.",
    "윈도우 안에서 '어떤 원소의 오른쪽에 그보다 크거나 같은 원소가 있다면' 그 원소는 앞으로 절대 최댓값이 될 수 없습니다. 이런 원소는 버려도 됩니다.",
    "deque 에 인덱스를 넣되, 값이 '감소하는 순서' 를 유지하세요. 새 값이 들어오면 뒤에서부터 자기보다 작거나 같은 값을 모두 pop 합니다.",
    "덱의 맨 앞 인덱스가 윈도우를 벗어났으면(i - k 이하) popleft. i ≥ k - 1 부터 nums[dq[0]] 을 결과에 추가합니다.",
]

TESTS = [
    {"input": [[1, 3, -1, -3, 5, 3, 6, 7], 3], "output": [3, 3, 5, 5, 6, 7]},
    {"input": [[1], 1], "output": [1]},
    {"input": [[1, -1], 1], "output": [1, -1]},
    {"input": [[9, 11], 2], "output": [11]},
    {"input": [[4, -2], 2], "output": [4]},
    {"input": [[7, 2, 4], 2], "output": [7, 4]},
    {"input": [[1, 3, 1, 2, 0, 5], 3], "output": [3, 3, 2, 5]},
    {"input": [[5, 4, 3, 2, 1], 5], "output": [5]},
    {"input": [[2, 2, 2, 2], 2], "output": [2, 2, 2]},
    {"input": [[-7, -8, 7, 5, 7, 1, 6, 0], 4], "output": [7, 7, 7, 7, 7]},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    nums = [random.randint(-10_000, 10_000) for _ in range(100_000)]
    return {"input": [nums, 50_000], "output": None}


EXPLANATION = """
핵심: 덱에는 "앞으로 최댓값이 될 가능성이 있는 후보" 의 인덱스만, 값이 감소하는 순서로 남깁니다.
그러면 덱의 맨 앞이 항상 현재 윈도우의 최댓값입니다.

1. dq = deque() (인덱스 저장, nums[dq] 는 감소)
2. i = 0..n-1:
   - dq[0] <= i - k 이면 popleft (윈도우 밖으로 나감)
   - nums[dq[-1]] <= nums[i] 인 동안 pop (새 값보다 작은 후보는 영원히 최댓값이 될 수 없음)
   - dq.append(i)
   - i >= k - 1 이면 결과에 nums[dq[0]] 추가
3. 결과 return

시간 O(n) (각 인덱스는 덱에 한 번 들어가고 한 번 나감 → 분할 상환 amortized O(1)), 공간 O(k)
면접 포인트: "왜 작은 값을 버려도 되는가" (나보다 오른쪽에 있고 크거나 같은 값이 있으면 나는 그보다 먼저 윈도우를 떠남)
를 설명하세요. 힙(heap)으로 O(n log n) 풀이(값, 인덱스를 넣고 맨 위가 윈도우 밖이면 버리기)도 대안으로 언급하면 좋습니다.
"""


def reference(nums, k):
    from collections import deque

    dq = deque()  # 인덱스. nums[dq[0]] > nums[dq[1]] > ... (감소)
    res = []
    for i, x in enumerate(nums):
        if dq and dq[0] <= i - k:
            dq.popleft()  # 윈도우를 벗어난 최댓값 후보 제거
        while dq and nums[dq[-1]] <= x:
            dq.pop()  # x 보다 작거나 같은 후보는 다시는 최댓값이 될 수 없다
        dq.append(i)
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res


def alternative(nums, k):
    # 힙 풀이 O(n log n): (-값, 인덱스) 를 넣고 맨 위가 윈도우 밖이면 버린다
    import heapq

    heap = []
    res = []
    for i, x in enumerate(nums):
        heapq.heappush(heap, (-x, i))
        if i >= k - 1:
            while heap[0][1] <= i - k:
                heapq.heappop(heap)
            res.append(-heap[0][0])
    return res


def brute_force(nums, k):
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]
