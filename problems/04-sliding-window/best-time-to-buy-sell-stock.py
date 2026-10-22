TITLE = "Best Time to Buy and Sell Stock (주식을 사고팔기 가장 좋은 때)"
LEVEL = "Easy"
SOURCE = "LeetCode 121"
PATTERN = "지금까지의 최저가를 기억하며 한 번 훑기 (가변 윈도우의 가장 단순한 형태)"

DESCRIPTION = """
prices[i] 는 i 번째 날의 주식 가격입니다.
어느 하루에 한 주를 사고, 그보다 뒤의 다른 하루에 팔 수 있습니다. (거래는 한 번만)
얻을 수 있는 최대 이익을 return 하세요. 이익을 낼 수 없으면 0 을 return 합니다.

제한사항
- 1 ≤ len(prices) ≤ 100,000
- 0 ≤ prices[i] ≤ 10,000

입출력 예
prices = [7, 1, 5, 3, 6, 4]  →  5   (2일째 1에 사서 5일째 6에 팔기)
prices = [7, 6, 4, 3, 1]     →  0   (계속 떨어지므로 거래하지 않음)
"""

SIGNATURE = "def solution(prices: list[int]) -> int:"

HINTS = [
    "모든 (사는 날, 파는 날) 쌍을 보면 O(n^2) 입니다. n = 100,000 이면 시간 초과입니다.",
    "파는 날을 j 로 고정하면, 가장 좋은 사는 날은 j 이전의 '최저가' 날입니다.",
    "왼쪽부터 훑으면서 min_price = 지금까지의 최저가 를 유지하고, best = max(best, price - min_price) 를 갱신하세요.",
]

TESTS = [
    {"input": [[7, 1, 5, 3, 6, 4]], "output": 5},
    {"input": [[7, 6, 4, 3, 1]], "output": 0},
    {"input": [[1]], "output": 0},
    {"input": [[1, 2]], "output": 1},
    {"input": [[2, 4, 1]], "output": 2},
    {"input": [[3, 3, 3]], "output": 0},
    {"input": [[3, 2, 6, 5, 0, 3]], "output": 4},
    {"input": [[0, 10000]], "output": 10000},
]

PERF_LIMIT = 1.0


def perf_case():
    n = 100_000
    prices = [10_000 - i // 10 for i in range(n)]  # 계속 떨어지는 가격
    return {"input": [prices], "output": 0}


EXPLANATION = """
핵심: 파는 날을 오른쪽으로 옮기면서 "그 전까지의 최저가" 만 알면 됩니다.
윈도우로 보면 l = 최저가 날, r = 오늘. 더 싼 날이 나오면 l 을 그 날로 점프합니다.

1. min_price = prices[0], best = 0
2. 각 price 에 대해 best = max(best, price - min_price), min_price = min(min_price, price)
3. best return

시간 O(n), 공간 O(1)
면접 포인트: "파는 날을 고정하면 사는 날은 그 이전 최솟값" 이라는 관찰을 말로 설명하세요.
후속 질문(거래 여러 번 = LeetCode 122, 수수료/쿨다운 = DP)으로 이어지는 경우가 많습니다.
"""


def reference(prices):
    min_price = prices[0]  # 지금까지 본 최저가 (= 윈도우의 왼쪽 끝)
    best = 0
    for price in prices:
        best = max(best, price - min_price)
        min_price = min(min_price, price)
    return best


def brute_force(prices):
    best = 0
    n = len(prices)
    for i in range(n):
        for j in range(i + 1, n):
            best = max(best, prices[j] - prices[i])
    return best
