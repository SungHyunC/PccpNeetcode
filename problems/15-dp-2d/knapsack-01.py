TITLE = "0/1 Knapsack (0/1 배낭 문제)"
LEVEL = "Medium"
SOURCE = "프로그래머스·백준 단골 유형 (BOJ 12865 평범한 배낭)"
PATTERN = "0/1 배낭: dp[w] = max(dp[w], dp[w - wt] + val), 용량은 역순 루프"

DESCRIPTION = """
물건이 n 개 있고, i 번 물건의 무게는 weights[i], 가치는 values[i] 입니다.
최대 capacity 무게까지 담을 수 있는 배낭에 물건을 골라 넣으려 합니다.
각 물건은 넣거나 넣지 않거나 둘 중 하나이며(쪼개기 불가, 한 번만 사용),
담은 물건의 무게 합이 capacity 이하일 때 가치 합의 최댓값을 return 하세요.

제한사항
- 1 ≤ n ≤ 100, len(weights) == len(values) == n
- 1 ≤ weights[i] ≤ 100,000
- 0 ≤ values[i] ≤ 1,000
- 0 ≤ capacity ≤ 100,000
- n × capacity ≤ 1,000,000

입출력 예
weights = [1, 3, 4, 5], values = [1, 4, 5, 7], capacity = 7      →  9    (무게 3 + 4)
weights = [10, 20, 30], values = [60, 100, 120], capacity = 50   →  220  (무게 20 + 30)
"""

SIGNATURE = "def solution(weights: list[int], values: list[int], capacity: int) -> int:"

HINTS = [
    "가치/무게 비율이 큰 것부터 담는 그리디는 '쪼갤 수 있는' 배낭에서만 맞습니다. 반례: 무게 [6, 5, 5], 가치 [10, 6, 6], 용량 10.",
    "dp[i][w] = 앞의 i 개 물건만 써서 무게 w 이하로 얻는 최대 가치. i 번째 물건을 넣는 경우와 안 넣는 경우를 비교하세요.",
    "dp[i][w] = max(dp[i-1][w], dp[i-1][w - wt] + val). 이전 행만 쓰므로 1차원 dp[w] 로 줄일 수 있는데, 이때 w 를 capacity → wt 로 '거꾸로' 돌아야 같은 물건을 두 번 넣지 않습니다.",
]

TESTS = [
    {"input": [[1, 3, 4, 5], [1, 4, 5, 7], 7], "output": 9},
    {"input": [[10, 20, 30], [60, 100, 120], 50], "output": 220},
    {"input": [[2, 3, 4, 5], [3, 4, 5, 6], 5], "output": 7},
    {"input": [[5], [10], 4], "output": 0},
    {"input": [[5], [10], 5], "output": 10},
    {"input": [[1, 2, 3], [10, 15, 40], 0], "output": 0},
    {"input": [[1, 1, 1], [10, 20, 30], 2], "output": 50},
    {"input": [[6, 5, 5], [10, 6, 6], 10], "output": 12},
    {"input": [[4, 3, 2, 1], [0, 0, 0, 0], 10], "output": 0},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    n, capacity = 60, 5000
    weights = [random.randint(1, 300) for _ in range(n)]
    values = [random.randint(0, 1000) for _ in range(n)]
    return {"input": [weights, values, capacity], "output": None}


EXPLANATION = """
아이디어
- 물건마다 '넣는다 / 안 넣는다' 두 갈래 → 완전 탐색은 O(2^n).
- 하지만 "앞의 i 개로 무게 w 까지" 라는 상태로 묶으면 상태 수는 n × capacity 뿐입니다.

DP 레시피 (2차원)
1. 상태 정의: dp[i][w] = 앞의 i 개 물건만 고려, 무게 합 ≤ w 일 때 최대 가치
2. 점화식:   dp[i][w] = dp[i-1][w]                                  (i 번째 안 넣음)
                      = max(위 값, dp[i-1][w - wt_i] + val_i)       (넣음, w ≥ wt_i 일 때)
3. 초기값:   dp[0][w] = 0 (물건 없음)
4. 계산 순서: i = 1 → n, w = 0 → capacity
5. 답:       dp[n][capacity]

  weights = [1, 3, 4, 5], values = [1, 4, 5, 7], capacity = 7
  w →         0  1  2  3  4  5  6  7
  물건 없음    0  0  0  0  0  0  0  0
  (1, 1)      0  1  1  1  1  1  1  1
  (3, 4)      0  1  1  4  5  5  5  5
  (4, 5)      0  1  1  4  5  6  6  9
  (5, 7)      0  1  1  4  5  7  8  9   ← 답 9

1차원으로 줄이기 (reference)
- dp[i][*] 는 dp[i-1][*] 만 봅니다 → 배열 하나를 덮어쓰기.
- dp[w - wt] 는 '이전 행' 값이어야 합니다. w 를 큰 쪽에서 작은 쪽으로 돌면
  dp[w - wt] 는 아직 이번 물건으로 갱신되기 전 값이므로 안전합니다.
- 작은 쪽부터 돌면 같은 물건을 여러 번 넣게 됩니다 → 그건 '완전 배낭(unbounded knapsack)'.

복잡도: 시간 O(n × capacity), 공간 O(capacity)  (2차원은 O(n × capacity))

면접 포인트
- O(n × W) 는 W 가 수치이므로 '의사 다항 시간(pseudo-polynomial)' 입니다. W 가 10^9 이면 못 씁니다.
  그때는 가치 기준 DP(dp[가치] = 최소 무게)나 meet-in-the-middle 을 고려합니다.
- 0/1 은 역순, unbounded 는 정순. 이 한 줄 차이를 설명할 수 있으면 배낭 계열은 대부분 해결됩니다.
"""


def reference(weights, values, capacity):
    dp = [0] * (capacity + 1)  # dp[w] = 무게 w 이하로 얻는 최대 가치
    for wt, val in zip(weights, values):
        # 역순: dp[w - wt] 가 '이번 물건을 아직 안 넣은' 값이 되도록
        for w in range(capacity, wt - 1, -1):
            cand = dp[w - wt] + val
            if cand > dp[w]:
                dp[w] = cand
    return dp[capacity]


def alternative(weights, values, capacity):
    # 2차원 표: dp[i][w]
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wt, val = weights[i - 1], values[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]  # 안 넣는 경우
            if w >= wt:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - wt] + val)  # 넣는 경우
    return dp[n][capacity]


def brute_force(weights, values, capacity):
    # 모든 부분집합: O(2^n)
    n = len(weights)

    def go(i, room):
        if i == n:
            return 0
        best = go(i + 1, room)
        if weights[i] <= room:
            best = max(best, values[i] + go(i + 1, room - weights[i]))
        return best

    return go(0, capacity)
