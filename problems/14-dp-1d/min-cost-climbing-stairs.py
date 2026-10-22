TITLE = "Min Cost Climbing Stairs (최소 비용으로 계단 오르기)"
LEVEL = "Easy"
SOURCE = "LeetCode 746"
PATTERN = "dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])"

DESCRIPTION = """
계단의 각 칸에는 통행료가 있습니다. i 번 칸을 밟으면 cost[i] 를 내야 합니다.
처음에는 0번 칸 또는 1번 칸 중 원하는 곳에서 출발할 수 있고(출발한 칸의 통행료도 냅니다),
통행료를 낸 뒤에는 1칸 또는 2칸 위로 올라갈 수 있습니다.
꼭대기는 마지막 칸의 바로 다음 위치(인덱스 len(cost))이며, 꼭대기에는 통행료가 없습니다.
꼭대기에 도착하기 위한 최소 비용을 return 하세요.

제한사항
- 2 ≤ len(cost) ≤ 1,000
- 0 ≤ cost[i] ≤ 999

입출력 예
cost = [10, 15, 20]                         →  15  (1번 칸에서 출발, 15 내고 2칸 점프)
cost = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1] →  6
"""

SIGNATURE = "def solution(cost: list[int]) -> int:"

HINTS = [
    "꼭대기(인덱스 n)에 도착하기 직전에는 n-1 번 칸 또는 n-2 번 칸에 있었습니다.",
    "dp[i] = 'i 번 위치에 도착하기까지 낸 최소 비용' 으로 정의해 보세요. (i 번 칸 통행료는 아직 안 냄)",
    "dp[0] = dp[1] = 0 (공짜로 출발), dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2]). 답은 dp[n]. 변수 두 개면 충분합니다.",
]

TESTS = [
    {"input": [[10, 15, 20]], "output": 15},
    {"input": [[1, 100, 1, 1, 1, 100, 1, 1, 100, 1]], "output": 6},
    {"input": [[0, 0]], "output": 0},
    {"input": [[5, 3]], "output": 3},
    {"input": [[1, 2, 3]], "output": 2},
    {"input": [[0, 1, 2, 2]], "output": 2},
    {"input": [[7, 7, 7, 7, 7, 7]], "output": 21},
]

EXPLANATION = """
아이디어
- 위치 i 에 오는 마지막 동작은 'i-1 칸을 밟고(통행료 지불) 1칸' 또는 'i-2 칸을 밟고 2칸' 입니다.
- 두 경우 중 더 싼 쪽을 고르면 됩니다 → 최솟값 DP.

DP 레시피
1. 상태 정의: dp[i] = i 번 위치에 '도착' 하기까지 낸 최소 비용 (i 번 칸의 통행료는 미포함)
2. 점화식:   dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])
3. 초기값:   dp[0] = dp[1] = 0  (0번, 1번 칸은 출발점이라 도착 비용 0)
4. 계산 순서: i = 2 → n
5. 답:       dp[n]  (n = len(cost), 꼭대기)

  cost = [10, 15, 20]
  i   : 0   1   2              3(꼭대기)
  dp  : 0   0   min(0+15,0+10)=10   min(10+20, 0+15)=15

복잡도: 시간 O(n), 공간 O(1)

면접 포인트
- 상태 정의를 "i 칸을 밟을 때까지의 비용(통행료 포함)" 으로 잡아도 됩니다. 그때는 답이 min(dp[n-1], dp[n-2]) 로 바뀝니다.
  → 상태 정의가 달라지면 초기값과 답의 위치가 함께 바뀐다는 점을 명확히 말하세요.
- 꼭대기가 '마지막 칸' 이 아니라 '그 다음 위치' 라는 문제 조건을 확인하는 질문(clarifying question)을 먼저 하세요.
"""


def reference(cost):
    n = len(cost)
    prev2, prev1 = 0, 0  # dp[i-2], dp[i-1]  (dp[0] = dp[1] = 0)
    for i in range(2, n + 1):
        cur = min(prev1 + cost[i - 1], prev2 + cost[i - 2])
        prev2, prev1 = prev1, cur
    return prev1


def alternative(cost):
    # top-down: arrive(i) = i 번 위치에 도착하는 최소 비용
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def arrive(i):
        if i <= 1:
            return 0
        return min(arrive(i - 1) + cost[i - 1], arrive(i - 2) + cost[i - 2])

    return arrive(len(cost))
