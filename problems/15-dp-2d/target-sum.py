TITLE = "Target Sum (부호 붙여 목표 합 만들기)"
LEVEL = "Medium"
SOURCE = "LeetCode 494 (프로그래머스 Lv.2 '타겟 넘버' 의 DP 버전)"
PATTERN = "+/- 선택 → 부분집합 합 개수 DP (P = (total + target) / 2)"

DESCRIPTION = """
음이 아닌 정수 배열 nums 와 정수 target 이 주어집니다.
nums 의 각 수 앞에 '+' 또는 '-' 를 하나씩 붙인 뒤 순서대로 모두 더해 식을 만듭니다.
계산 결과가 target 이 되는 식의 개수를 return 하세요.
(값이 같은 원소라도 위치가 다르면 다른 원소로 취급합니다.)

제한사항
- 1 ≤ len(nums) ≤ 40
- 0 ≤ nums[i] ≤ 500
- -20,000 ≤ target ≤ 20,000

입출력 예
nums = [1, 1, 1, 1, 1], target = 3  →  5   (-1+1+1+1+1, +1-1+1+1+1, ... 5가지)
nums = [1], target = 1              →  1
"""

SIGNATURE = "def solution(nums: list[int], target: int) -> int:"

HINTS = [
    "모든 부호 조합을 보면 2^n. n = 40 이면 1조 개가 넘습니다. 하지만 '지금까지의 합' 이 가질 수 있는 값의 종류는 많지 않습니다.",
    "dict 로 {현재 합: 그 합을 만드는 방법 수} 를 관리하며 원소를 하나씩 반영해 보세요. (상태 = (인덱스, 현재 합))",
    "더 나아가: + 를 붙인 수들의 합을 P 라 하면 P - (total - P) = target → P = (total + target) / 2. 결국 '합이 P 인 부분집합의 개수' 를 0/1 배낭(역순 루프)으로 세면 됩니다. (total + target) 이 홀수이거나 |target| > total 이면 0.",
]

TESTS = [
    {"input": [[1, 1, 1, 1, 1], 3], "output": 5},
    {"input": [[1], 1], "output": 1},
    {"input": [[1], 2], "output": 0},
    {"input": [[0, 0, 0], 0], "output": 8},
    {"input": [[1, 2, 1], 0], "output": 2},
    {"input": [[2, 3, 5], 0], "output": 2},
    {"input": [[100], -200], "output": 0},
    {"input": [[1, 0], 1], "output": 2},
    {"input": [[7, 9, 3, 8, 0, 2, 4, 8, 3, 9], 0], "output": 0},
    {"input": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5], "output": 39},
    {"input": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 6], "output": 0},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    nums = [random.randint(0, 500) for _ in range(40)]
    target = sum(nums) // 3
    if (sum(nums) + target) % 2:
        target += 1
    return {"input": [nums, target], "output": None}


EXPLANATION = """
아이디어 1 — (인덱스, 현재 합) 상태 DP (alternative)
- 2^n 개의 부호 조합도 '현재 합' 기준으로 묶으면 상태는 n × (가능한 합의 개수) 뿐입니다.
- dict 에 {합: 방법 수} 를 저장하고 원소마다 +x, -x 로 퍼뜨립니다.

아이디어 2 — 부분집합 합으로 변환 (reference)
- + 를 붙인 집합의 합 = P, - 를 붙인 집합의 합 = N 이라 하면
  P + N = total,  P - N = target  →  P = (total + target) / 2
- 즉 "합이 P 인 부분집합의 개수" 를 세는 0/1 배낭 경우의 수 문제가 됩니다.
- (total + target) 이 홀수이거나 |target| > total 이면 답은 0.

DP 레시피 (reference)
1. 상태 정의: dp[s] = 지금까지 본 원소 중 일부를 골라 합 s 를 만드는 방법 수
2. 점화식:   원소 x 마다 s = P → x (역순) 로 dp[s] += dp[s - x]
3. 초기값:   dp[0] = 1
4. 계산 순서: 원소 바깥, 합은 역순 (각 원소 한 번만)
5. 답:       dp[P]

  nums = [1, 1, 1, 1, 1], target = 3 → total = 5, P = 4
  s →        0  1  2  3  4
  초기        1  0  0  0  0
  x=1        1  1  0  0  0
  x=1        1  2  1  0  0
  x=1        1  3  3  1  0
  x=1        1  4  6  4  1
  x=1        1  5 10 10  5   ← 답 5  (= C(5, 4))

0 의 처리: x = 0 이면 dp[s] += dp[s] 로 모든 값이 두 배 → +0, -0 을 서로 다른 식으로 세는 것과 일치합니다.

복잡도
- 부분집합 변환: 시간 O(n × P), 공간 O(P)
- dict 상태 DP: 시간 O(n × 합의 범위), 공간 O(합의 범위)
- 완전 탐색(brute_force): O(2^n)

면접 포인트
- 프로그래머스 '타겟 넘버' 는 n ≤ 20 이라 DFS 완전 탐색(2^20 ≈ 100만)으로도 통과하지만,
  n 이 커지면 이 변환이 필요합니다. "왜 DFS 로 되는지 / 언제 안 되는지" 를 입력 크기로 설명하세요.
- 대수적 변환(P = (total + target) / 2)을 떠올리는 과정 자체가 면접관이 보고 싶은 부분입니다.
"""


def reference(nums, target):
    total = sum(nums)
    if abs(target) > total or (total + target) % 2:
        return 0
    P = (total + target) // 2  # + 를 붙일 수들의 합
    dp = [0] * (P + 1)
    dp[0] = 1
    for x in nums:
        for s in range(P, x - 1, -1):  # 역순: 각 원소는 한 번만
            dp[s] += dp[s - x]
    return dp[P]


def alternative(nums, target):
    # {현재 합: 방법 수} 를 원소마다 갱신
    from collections import defaultdict

    ways = {0: 1}
    for x in nums:
        nxt = defaultdict(int)
        for s, cnt in ways.items():
            nxt[s + x] += cnt
            nxt[s - x] += cnt
        ways = nxt
    return ways.get(target, 0)


def brute_force(nums, target):
    # 모든 부호 조합: O(2^n)
    def go(i, s):
        if i == len(nums):
            return 1 if s == target else 0
        return go(i + 1, s + nums[i]) + go(i + 1, s - nums[i])

    return go(0, 0)
