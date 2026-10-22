TITLE = "Koko Eating Bananas (바나나 먹는 코코)"
LEVEL = "Medium"
SOURCE = "LeetCode 875"
PATTERN = "파라메트릭 서치: '속도 k 로 h 시간 안에 가능한가?' 를 이분 탐색"

DESCRIPTION = """
바나나 더미 n 개가 있고, i 번 더미에는 piles[i] 개의 바나나가 있습니다.
코코는 시간당 먹는 속도 k (정수) 를 정해, 매 시간 한 더미를 골라 최대 k 개를 먹습니다.
더미에 k 개보다 적게 남아 있으면 그 더미를 다 먹고 그 시간에는 더 먹지 않습니다.
h 시간 안에 모든 바나나를 먹을 수 있는 가장 작은 k 를 return 하세요.

제한사항
- 1 ≤ len(piles) ≤ 10,000
- len(piles) ≤ h ≤ 1,000,000,000
- 1 ≤ piles[i] ≤ 1,000,000,000

입출력 예
piles = [3, 6, 7, 11],        h = 8  →  4    (1 + 2 + 2 + 3 = 8 시간)
piles = [30, 11, 23, 4, 20],  h = 5  →  30   (더미 5개를 5시간에 → 가장 큰 더미를 한 번에)
piles = [30, 11, 23, 4, 20],  h = 6  →  23
"""

SIGNATURE = "def solution(piles: list[int], h: int) -> int:"

HINTS = [
    "속도 k 가 정해지면 걸리는 시간은 바로 계산됩니다: 각 더미마다 ceil(pile / k) 시간 → 합계. 그러면 '이 k 로 가능한가?' 는 O(n) 에 판정됩니다.",
    "k 가 커지면 걸리는 시간은 줄어듭니다(단조성). 즉 '가능/불가능' 이 어떤 경계를 기준으로 [불가능 ... 불가능, 가능 ... 가능] 으로 나뉩니다.",
    "k 의 범위는 1 ~ max(piles) 입니다. 이 범위에서 '가능한 가장 작은 k' 를 이분 탐색하세요. ceil(p / k) 는 (p + k - 1) // k 로 정수 계산합니다.",
    "lo, hi = 1, max(piles). while lo < hi: mid = (lo + hi) // 2; 가능하면 hi = mid (mid 도 후보), 불가능하면 lo = mid + 1. 답은 lo.",
]

TESTS = [
    {"input": [[3, 6, 7, 11], 8], "output": 4},
    {"input": [[30, 11, 23, 4, 20], 5], "output": 30},
    {"input": [[30, 11, 23, 4, 20], 6], "output": 23},
    {"input": [[1], 1], "output": 1},
    {"input": [[1000000000], 2], "output": 500000000},
    {"input": [[1000000000], 1000000000], "output": 1},
    {"input": [[312884470], 312884469], "output": 2},
    {"input": [[2, 2], 4], "output": 1},
    {"input": [[5, 5, 5], 3], "output": 5},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    piles = [random.randint(1, 1_000_000_000) for _ in range(10_000)]
    return {"input": [piles, 15_000], "output": None}


EXPLANATION = """
핵심(파라메트릭 서치, parametric search): "최소 k 는?" 이라는 최적화 문제를
"k 로 가능한가?" 라는 예/아니오 문제로 바꾸고, 그 답이 k 에 대해 단조(불가능…불가능 가능…가능)이므로 경계를 이분 탐색합니다.

1. can(k) = sum((p + k - 1) // k for p in piles) <= h      ← O(n)
2. lo, hi = 1, max(piles)   (max(piles) 면 더미마다 1시간이므로 h ≥ n 이라 항상 가능)
3. while lo < hi:
     mid = (lo + hi) // 2
     can(mid) 이면 hi = mid      (mid 도 답 후보이므로 남김)
     아니면     lo = mid + 1
4. lo return (lo == hi 가 '처음으로 가능한 k')

시간 O(n log M) (M = max(piles) ≤ 10^9 → 약 30 번 × n), 공간 O(1)
면접 포인트: k 를 1 부터 하나씩 늘리면(선형 탐색) O(n · M) 으로 시간 초과입니다. 예: piles = [10^9], h = 2 이면 k 를 5억 번 시도해야 합니다.
"답의 범위가 크고, 답을 정하면 판정이 쉽고, 판정이 단조적이다" → 파라메트릭 서치 라는 신호를 설명하세요.
math.ceil(p / k) 는 큰 수에서 부동소수점 오차가 날 수 있으므로 (p + k - 1) // k 또는 -(-p // k) 를 씁니다.
"""


def reference(piles, h):
    def can(k):
        # 속도 k 로 모든 더미를 먹는 데 걸리는 시간이 h 이하인가?
        return sum((p + k - 1) // k for p in piles) <= h

    lo, hi = 1, max(piles)  # 답은 반드시 이 범위 안에 있다
    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid):
            hi = mid      # mid 도 가능 → 더 작은 쪽을 찾아본다 (mid 포함)
        else:
            lo = mid + 1  # mid 는 불가능 → mid 보다 커야 한다
    return lo

