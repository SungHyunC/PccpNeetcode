TITLE = "Coin Change II (동전 교환 - 경우의 수)"
LEVEL = "Medium"
SOURCE = "LeetCode 518"
PATTERN = "완전 배낭 경우의 수: 동전 바깥 루프 + 금액 정순 루프 (조합)"

DESCRIPTION = """
동전 액면가 목록 coins 와 금액 amount 가 주어집니다. 각 동전은 개수 제한 없이 쓸 수 있습니다.
amount 를 만드는 '조합' 의 개수를 return 하세요.
사용한 동전의 종류와 개수가 같으면 순서가 달라도 같은 방법으로 셉니다. (1+2 와 2+1 은 같은 방법)
만들 수 없으면 0 을 return 합니다.

제한사항
- 1 ≤ len(coins) ≤ 300, 1 ≤ coins[i] ≤ 5,000, 액면가는 서로 다름
- 0 ≤ amount ≤ 10,000
- 답이 매우 클 수 있지만 파이썬 정수는 크기 제한이 없으므로 그대로 return 하세요.

입출력 예
coins = [1, 2, 5], amount = 5  →  4   (5 / 2+2+1 / 2+1+1+1 / 1+1+1+1+1)
coins = [2],       amount = 3  →  0
coins = [10],      amount = 10 →  1
"""

SIGNATURE = "def solution(coins: list[int], amount: int) -> int:"

HINTS = [
    "dp[a] = a 원을 만드는 방법 수라고 두고 'for a: for c: dp[a] += dp[a-c]' 로 짜면 1+2 와 2+1 을 따로 세게 됩니다(순열).",
    "중복을 없애려면 동전을 '종류 순서대로' 쓰도록 강제하세요. dp[i][a] = 앞의 i 종류 동전만으로 a 를 만드는 조합 수.",
    "1차원으로: 동전 c 를 바깥 루프, 금액 a = c → amount 를 안쪽 정순 루프로 돌며 dp[a] += dp[a - c]. dp[0] = 1. 정순이라 같은 동전을 여러 번 쓸 수 있습니다.",
]

TESTS = [
    {"input": [[1, 2, 5], 5], "output": 4},
    {"input": [[2], 3], "output": 0},
    {"input": [[10], 10], "output": 1},
    {"input": [[1, 2], 0], "output": 1},
    {"input": [[1, 2, 3], 4], "output": 4},
    {"input": [[2, 3], 7], "output": 1},
    {"input": [[5, 7], 1], "output": 0},
    {"input": [[3, 5, 7, 8, 9, 10, 11], 500], "output": 35502874},
]

PERF_LIMIT = 1.0


def perf_case():
    coins = [3, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    return {"input": [coins, 10_000], "output": None}


EXPLANATION = """
아이디어
- 경우의 수 DP 에서 '조합(순서 무관)' 과 '순열(순서 구분)' 은 루프 순서로 갈립니다.
  - 동전 바깥, 금액 안쪽  → 각 조합을 '동전 종류 순서' 로 한 번만 셈 → 조합 (이 문제)
  - 금액 바깥, 동전 안쪽  → 마지막 동전이 무엇이었는지로 나눔      → 순열 (LeetCode 377)

DP 레시피 (2차원으로 생각 → 1차원으로 구현)
1. 상태 정의: dp[i][a] = 앞의 i 종류 동전만 써서 a 원을 만드는 조합 수
2. 점화식:   dp[i][a] = dp[i-1][a]  (i 번째 동전 안 씀)
                      + dp[i][a - c_i]  (i 번째 동전을 한 개 이상 씀 → 같은 행!)
3. 초기값:   dp[*][0] = 1 (아무것도 안 내는 방법 1가지)
4. 계산 순서: 동전 순서대로, 금액은 작은 쪽부터(같은 행의 왼쪽 값을 쓰므로 정순)
5. 답:       dp[n][amount]

  coins = [1, 2, 5], amount = 5
  a →          0  1  2  3  4  5
  동전 없음     1  0  0  0  0  0
  +1           1  1  1  1  1  1
  +2           1  1  2  2  3  3
  +5           1  1  2  2  3  4   ← 답 4

  순열로 잘못 세면 (금액 바깥 루프): coins = [1, 2, 3], amount = 4 → 7 (정답 4)

배낭 계열 루프 방향 정리
- 0/1 배낭(각 물건 1번): 1차원에서 용량 '역순'
- 완전 배낭(무한 사용): 1차원에서 용량 '정순'  ← 이 문제

복잡도: 시간 O(len(coins) × amount), 공간 O(amount)

면접 포인트
- "루프 두 줄의 순서를 바꾸면 조합 ↔ 순열이 바뀐다" 를 예시와 함께 설명하면 강한 인상을 줍니다.
- Coin Change(최소 개수)는 min, 이 문제는 + 입니다. 같은 표 모양, 다른 연산.
"""


def reference(coins, amount):
    dp = [0] * (amount + 1)
    dp[0] = 1  # 0원을 만드는 방법: 아무 동전도 안 씀
    for c in coins:  # 동전 종류가 바깥 → 조합으로 셈
        for a in range(c, amount + 1):  # 정순 → 같은 동전 여러 번 사용 가능
            dp[a] += dp[a - c]
    return dp[amount]


def alternative(coins, amount):
    # 2차원 표: dp[i][a] = 앞의 i 종류 동전으로 a 를 만드는 조합 수
    n = len(coins)
    dp = [[0] * (amount + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = 1
    for i in range(1, n + 1):
        c = coins[i - 1]
        for a in range(1, amount + 1):
            dp[i][a] = dp[i - 1][a]
            if a >= c:
                dp[i][a] += dp[i][a - c]
    return dp[n][amount]
