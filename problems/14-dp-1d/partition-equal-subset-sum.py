TITLE = "Partition Equal Subset Sum (합이 같은 두 부분집합으로 나누기)"
LEVEL = "Medium"
SOURCE = "LeetCode 416"
PATTERN = "부분집합 합(subset sum) → 0/1 배낭 불리언 DP (뒤에서부터 갱신)"

DESCRIPTION = """
양의 정수 배열 nums 가 주어집니다.
모든 원소를 두 묶음으로 나누어(각 원소는 정확히 한 묶음에 속함)
두 묶음의 합이 같아지게 할 수 있으면 True, 없으면 False 를 return 하세요.

제한사항
- 1 ≤ len(nums) ≤ 200
- 1 ≤ nums[i] ≤ 100

입출력 예
nums = [1, 5, 11, 5]  →  True   ([1, 5, 5] 와 [11])
nums = [1, 2, 3, 5]   →  False  (합 11 은 홀수)
"""

SIGNATURE = "def solution(nums: list[int]) -> bool:"

HINTS = [
    "전체 합 total 이 홀수면 바로 False. 짝수라면 '합이 total // 2 인 부분집합이 있는가?' 와 같은 질문입니다.",
    "모든 부분집합(2^n)을 보는 대신, '지금까지 본 원소로 만들 수 있는 합' 의 집합을 관리하세요. 합의 범위는 0..total//2 로 작습니다.",
    "dp[t] = 합 t 를 만들 수 있는가. 원소 x 마다 t 를 target 에서 x 까지 '거꾸로' 돌며 dp[t] |= dp[t - x]. 거꾸로 돌아야 x 를 한 번만 씁니다.",
]

TESTS = [
    {"input": [[1, 5, 11, 5]], "output": True},
    {"input": [[1, 2, 3, 5]], "output": False},
    {"input": [[1]], "output": False},
    {"input": [[2, 2]], "output": True},
    {"input": [[1, 2, 5]], "output": False},
    {"input": [[3, 3, 3, 4, 5]], "output": True},
    {"input": [[2, 2, 3, 5]], "output": False},
    {"input": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]], "output": True},
    {"input": [[100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 99]], "output": False},
]

EXPLANATION = """
아이디어
- 두 묶음의 합이 같다 ⇔ 한 묶음의 합이 total / 2.  → 부분집합 합(subset sum) 문제.
- 각 원소를 '넣는다/안 넣는다' 한 번씩 결정 → 0/1 배낭(0/1 knapsack) 의 불리언 버전입니다.

DP 레시피
1. 상태 정의: dp[t] = 지금까지 본 원소 일부로 합 t 를 만들 수 있는가
2. 점화식:   x 를 볼 때 dp[t] = dp[t] or dp[t - x]   (t = target → x, 역순)
3. 초기값:   dp[0] = True (아무것도 안 고름)
4. 계산 순서: 원소 바깥 루프, 합은 큰 쪽에서 작은 쪽으로
5. 답:       dp[target]

  nums = [1, 5, 11, 5], target = 11
  t        : 0 1 2 3 4 5 6 7 8 9 10 11
  초기     : T . . . . . . . . . .  .
  x=1      : T T . . . . . . . . .  .
  x=5      : T T . . . T T . . . .  .
  x=11     : T T . . . T T . . . .  T   ← 이미 성공
  x=5      : T T . . . T T . . . T  T

왜 역순인가?
- 정순(t = x → target)으로 돌면 방금 갱신한 dp[t - x] 를 같은 x 로 다시 써서 x 를 여러 번 쓰게 됩니다.
  (그건 동전처럼 무한히 쓰는 unbounded 배낭)

복잡도: 시간 O(n × total/2), 공간 O(total/2) → 최대 200 × 10,000 = 2,000,000

면접 포인트
- "원소 값의 합이 작다(≤ 20,000)" 는 제한이 DP 를 쓰라는 신호입니다 (의사 다항 시간, pseudo-polynomial).
- 파이썬 정수를 비트셋(bitset)으로 써서 bits |= bits << x 한 줄로 빠르게 풀 수도 있습니다. (alternative)
- dp[target] 이 True 가 되는 순간 일찍 종료해도 됩니다.
"""


def reference(nums):
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        # 역순으로 돌아야 같은 x 를 두 번 쓰지 않음 (0/1 배낭)
        for t in range(target, x - 1, -1):
            if dp[t - x]:
                dp[t] = True
        if dp[target]:
            return True
    return dp[target]


def alternative(nums):
    # 비트셋: bits 의 t 번째 비트 = 합 t 를 만들 수 있는가
    total = sum(nums)
    if total % 2:
        return False
    bits = 1
    for x in nums:
        bits |= bits << x
    return (bits >> (total // 2)) & 1 == 1


def brute_force(nums):
    # 각 원소를 넣는다/안 넣는다: O(2^n)
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2

    def go(i, s):
        if s == target:
            return True
        if i == len(nums) or s > target:
            return False
        return go(i + 1, s + nums[i]) or go(i + 1, s)

    return go(0, 0)
