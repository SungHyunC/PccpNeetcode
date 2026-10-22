TITLE = "Coin Change (동전 교환 - 최소 개수)"
LEVEL = "Medium"
SOURCE = "LeetCode 322"
PATTERN = "완전 배낭(unbounded) 최솟값 DP: dp[a] = min(dp[a - c] + 1)"

DESCRIPTION = """
여러 종류의 동전 액면가 coins 와 만들어야 하는 금액 amount 가 주어집니다.
각 동전은 개수 제한 없이 몇 번이든 사용할 수 있습니다.
amount 를 정확히 만들기 위해 필요한 동전 개수의 최솟값을 return 하세요.
어떤 조합으로도 만들 수 없다면 -1 을 return 합니다.

제한사항
- 1 ≤ len(coins) ≤ 12
- 1 ≤ coins[i] ≤ 2^31 - 1, 액면가는 서로 다름
- 0 ≤ amount ≤ 10,000

입출력 예
coins = [1, 2, 5], amount = 11  →  3   (5 + 5 + 1)
coins = [2],       amount = 3   →  -1
coins = [1],       amount = 0   →  0
"""

SIGNATURE = "def solution(coins: list[int], amount: int) -> int:"

HINTS = [
    "큰 동전부터 최대한 쓰는 그리디는 틀립니다. coins = [1, 3, 4], amount = 6 → 그리디 4+1+1 (3개), 정답 3+3 (2개).",
    "금액 a 를 만드는 마지막 동전이 c 라면, 나머지 a - c 는 '최소 개수' 로 만들어져 있어야 합니다.",
    "dp[a] = a 원을 만드는 최소 동전 수. dp[0] = 0, 나머지는 무한대로 두고 dp[a] = min(dp[a - c] + 1) 을 a = 1..amount 순서로 채우세요. 끝까지 무한대면 -1.",
]

TESTS = [
    {"input": [[1, 2, 5], 11], "output": 3},
    {"input": [[2], 3], "output": -1},
    {"input": [[1], 0], "output": 0},
    {"input": [[1], 2], "output": 2},
    {"input": [[1, 3, 4], 6], "output": 2},
    {"input": [[2, 5, 10, 1], 27], "output": 4},
    {"input": [[186, 419, 83, 408], 6249], "output": 20},
    {"input": [[3, 7], 5], "output": -1},
    {"input": [[2147483647], 2], "output": -1},
]

PERF_LIMIT = 1.0


def perf_case():
    coins = [7, 13, 29, 31, 101, 211, 307, 401, 499, 997]
    return {"input": [coins, 10_000], "output": None}


EXPLANATION = """
아이디어
- 동전 수를 최소화하는 문제는 그리디가 통하지 않는 대표 사례입니다 ([1,3,4], 6).
- 금액 a 의 최적해에서 마지막 동전 c 를 빼면, a - c 의 최적해가 남습니다(최적 부분 구조).
  → 모든 c 에 대해 dp[a - c] + 1 의 최솟값.

DP 레시피
1. 상태 정의: dp[a] = 정확히 a 원을 만드는 최소 동전 수 (불가능하면 INF)
2. 점화식:   dp[a] = min(dp[a - c] + 1  for c in coins if c <= a)
3. 초기값:   dp[0] = 0, 나머지 INF
4. 계산 순서: a = 1 → amount (작은 금액부터)
5. 답:       dp[amount] (INF 면 -1)

  coins = [1, 2, 5], amount = 11
  a  :  0  1  2  3  4  5  6  7  8  9  10  11
  dp :  0  1  1  2  2  1  2  2  3  3   2   3
                        ↑5원 한 개       ↑ dp[11] = dp[6] + 1 = 3

복잡도: 시간 O(amount × len(coins)), 공간 O(amount)

면접 포인트
- 그리디 반례를 먼저 제시하고 DP 로 넘어가면 설득력이 있습니다.
- top-down 으로 짜면 amount = 10,000, coins = [1] 에서 재귀 깊이가 10,000 → RecursionError.
  sys.setrecursionlimit 을 늘리거나 바텀업으로 작성하세요.
- BFS 로도 풀 수 있습니다: 0 에서 출발해 동전만큼 이동하는 최단 거리 = 최소 개수.
- 경우의 수를 묻는 변형(Coin Change II)은 min 대신 + 이고, 루프 순서가 중요해집니다.
"""


def reference(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return dp[amount] if dp[amount] != INF else -1


def alternative(coins, amount):
    # top-down 메모이제이션. 재귀 깊이가 amount / min(coins) 까지 깊어질 수 있음에 주의
    import sys
    from functools import lru_cache

    sys.setrecursionlimit(max(1000, amount + 100))

    @lru_cache(maxsize=None)
    def best(a):
        if a == 0:
            return 0
        res = float("inf")
        for c in coins:
            if c <= a:
                res = min(res, best(a - c) + 1)
        return res

    ans = best(amount)
    return ans if ans != float("inf") else -1
