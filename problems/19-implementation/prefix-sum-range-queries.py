TITLE = "Prefix Sum Range Queries (누적합으로 구간 합 질의)"
LEVEL = "Easy"
SOURCE = "PCCP 기출 유형 (구간 합 구하기)"
PATTERN = "누적합(prefix sum): 구간 합 = prefix[r+1] - prefix[l]"

DESCRIPTION = """
매장의 일별 매출 nums 와 질의 목록 queries 가 주어집니다.
queries[j] = [l, r] 은 l 번째 날부터 r 번째 날까지(0부터 시작, 양 끝 포함) 매출의 합을 묻는 질의입니다.
모든 질의의 답을 순서대로 담은 리스트를 return 하세요.

제한사항
- 1 ≤ len(nums) ≤ 100,000
- -10,000 ≤ nums[i] ≤ 10,000 (환불로 음수 매출이 있을 수 있음)
- 1 ≤ len(queries) ≤ 100,000
- 0 ≤ l ≤ r < len(nums)
- 효율성 테스트: 질의마다 구간을 직접 더하면 최악 O(N · Q) = 10^10 으로 시간 초과입니다.

입출력 예
nums = [3, -1, 4, 1, 5], queries = [[0, 2], [1, 3], [4, 4], [0, 4]]  →  [6, 4, 5, 12]
"""

SIGNATURE = "def solution(nums: list[int], queries: list[list[int]]) -> list[int]:"

HINTS = [
    "같은 배열에 대해 구간 합을 여러 번 묻는다면, 미리 한 번 계산해 둔 것을 재사용할 수 있습니다.",
    "prefix[i] = nums[0] + ... + nums[i-1] (prefix[0] = 0, 길이 n+1) 을 만들어 두세요.",
    "[l, r] 의 합 = prefix[r + 1] - prefix[l]. itertools.accumulate(nums, initial=0) 으로 한 줄에 만들 수 있습니다.",
]

TESTS = [
    {"input": [[3, -1, 4, 1, 5], [[0, 2], [1, 3], [4, 4], [0, 4]]], "output": [6, 4, 5, 12]},
    {"input": [[7], [[0, 0]]], "output": [7]},
    {"input": [[-5, -5, -5], [[0, 2], [1, 1], [0, 1]]], "output": [-15, -5, -10]},
    {"input": [[0, 0, 0, 0], [[0, 3], [2, 3]]], "output": [0, 0]},
    {"input": [[10000, -10000, 10000], [[0, 1], [1, 2], [0, 2], [2, 2]]], "output": [0, 0, 10000, 10000]},
    {"input": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [[0, 9], [9, 9], [3, 6], [0, 0], [4, 5]]], "output": [55, 10, 22, 1, 11]},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    n = q = 100_000
    nums = [random.randint(-10_000, 10_000) for _ in range(n)]
    queries = []
    for _ in range(q):
        l = random.randint(0, 1000)
        queries.append([l, random.randint(n - 1000, n - 1)])  # 긴 구간 위주
    return {"input": [nums, queries], "output": None}


EXPLANATION = """
핵심: 누적합(prefix sum)을 O(N) 에 한 번 만들어 두면 모든 구간 합을 O(1) 에 답할 수 있습니다.

  nums   =     3  -1   4   1   5
  prefix =  0  3   2   6   7  12        (prefix[i] = 앞의 i 개 합)
  [1, 3] 의 합 = prefix[4] - prefix[1] = 7 - 3 = 4   (-1 + 4 + 1)

1. prefix = [0] * (n + 1);  prefix[i + 1] = prefix[i] + nums[i]
2. 각 질의 [l, r] → prefix[r + 1] - prefix[l]

시간 O(N + Q), 공간 O(N)    (직접 더하기는 O(N · Q))
실전 포인트:
- prefix 를 길이 n+1 로 만들고 맨 앞에 0 을 두면 l = 0 인 경우를 따로 처리하지 않아도 됩니다.
- 2차원 누적합: P[r+1][c+1] = P[r][c+1] + P[r+1][c] - P[r][c] + a[r][c],
  (r1,c1)~(r2,c2) 의 합 = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]
- 반대로 '구간 갱신이 많고 조회는 마지막' 이면 차분 배열(누적합의 역연산)을 씁니다.
- 갱신과 조회가 섞여 있으면 펜윅 트리(Fenwick tree)나 세그먼트 트리가 필요합니다.
"""


def reference(nums, queries):
    prefix = [0] * (len(nums) + 1)
    for i, x in enumerate(nums):
        prefix[i + 1] = prefix[i] + x  # 앞의 i+1 개 합
    return [prefix[r + 1] - prefix[l] for l, r in queries]


def alternative(nums, queries):
    from itertools import accumulate
    prefix = list(accumulate(nums, initial=0))  # [0, a0, a0+a1, ...] (3.8+)
    return [prefix[r + 1] - prefix[l] for l, r in queries]


def brute_force(nums, queries):
    return [sum(nums[l : r + 1]) for l, r in queries]
