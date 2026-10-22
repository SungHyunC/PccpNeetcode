TITLE = "Jump Game II (최소 점프 횟수)"
LEVEL = "Medium"
SOURCE = "LeetCode 45"
PATTERN = "구간 단위 BFS 그리디: 현재 점프로 닿는 구간 끝에서 점프 횟수 +1"

DESCRIPTION = """
정수 배열 nums 가 주어집니다. 처음에는 0번 칸에 서 있습니다.
i 번 칸에서는 오른쪽으로 1칸 이상 nums[i] 칸 이하만큼 점프할 수 있습니다.
마지막 칸(인덱스 n-1)에 도착하기 위한 최소 점프 횟수를 return 하세요.
마지막 칸에는 항상 도착할 수 있는 입력만 주어집니다.

제한사항
- 1 ≤ len(nums) ≤ 100,000
- 0 ≤ nums[i] ≤ 100,000

입출력 예
nums = [2, 3, 1, 1, 4]  →  2   (0 → 1 → 4)
nums = [2, 3, 0, 1, 4]  →  2
nums = [0]              →  0   (이미 마지막 칸)
"""

SIGNATURE = "def solution(nums: list[int]) -> int:"

HINTS = [
    "dp[j] = j 까지의 최소 점프 수로 두면 각 i 에서 최대 nums[i] 칸을 갱신 → 최악 O(n^2).",
    "BFS 를 떠올려 보세요. 점프 0번으로 닿는 칸 = [0, 0], 1번으로 닿는 칸 = [1, nums[0]], ... 각 '층' 은 연속 구간입니다.",
    "현재 층의 끝(cur_end)과 다음 층의 끝(farthest)을 관리하세요. i 를 왼쪽부터 보며 farthest = max(farthest, i + nums[i]), i == cur_end 가 되면 jumps += 1, cur_end = farthest. 마지막 칸은 순회에서 제외(range(n-1)).",
]

TESTS = [
    {"input": [[2, 3, 1, 1, 4]], "output": 2},
    {"input": [[2, 3, 0, 1, 4]], "output": 2},
    {"input": [[0]], "output": 0},
    {"input": [[1, 1, 1, 1]], "output": 3},
    {"input": [[10, 1, 1]], "output": 1},
    {"input": [[1, 2]], "output": 1},
    {"input": [[1, 2, 1, 1, 1]], "output": 3},
    {"input": [[3, 1, 1, 1, 5, 1, 1, 1, 1]], "output": 3},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    n = 100_000
    nums = [random.randint(1, 5_000) for _ in range(n)]
    return {"input": [nums], "output": None}


EXPLANATION = """
아이디어
- 점프 횟수로 층을 나누는 BFS 를 생각합니다. k 번 점프로 닿을 수 있는 칸은 항상 '연속 구간' 입니다.
- 그래서 큐 없이 구간의 끝 두 개만 관리하면 됩니다.
  - cur_end : 지금까지의 점프 수로 닿을 수 있는 가장 먼 칸 (현재 층의 끝)
  - farthest: 현재 층의 칸들에서 한 번 더 뛰면 닿는 가장 먼 칸 (다음 층의 끝)

단계
1. jumps = 0, cur_end = 0, farthest = 0
2. i = 0 → n-2 (마지막 칸에서는 뛸 필요 없음):
   - farthest = max(farthest, i + nums[i])
   - i == cur_end 이면 현재 층을 다 봤으므로 jumps += 1, cur_end = farthest
3. return jumps

  nums = [2, 3, 1, 1, 4]
  층 0 : [0]        → 다음 층 끝 = 0 + 2 = 2         jumps = 1
  층 1 : [1, 2]     → 다음 층 끝 = max(1+3, 2+1) = 4  jumps = 2  (4 = 마지막 칸)

왜 그리디가 맞는가
- BFS 는 가중치 없는 그래프에서 최단 거리를 보장합니다. 이 풀이는 BFS 의 층을 구간으로 압축한 것뿐입니다.
- "각 층에서 가장 멀리 가는 칸을 고른다" 는 선택이 다음 층을 최대로 넓히므로 손해가 없습니다.

복잡도: 시간 O(n), 공간 O(1)

면접 포인트
- 루프를 n-1 까지만 돌아야 합니다. 마지막 칸에서 i == cur_end 가 되면 불필요하게 jumps 가 1 늘어납니다.
- DP O(n^2) → BFS → 구간 그리디 O(n) 의 연결 고리를 설명하면 좋습니다.
"""


def reference(nums):
    jumps = 0
    cur_end = 0  # 현재 점프 횟수로 닿는 구간의 끝
    farthest = 0  # 한 번 더 뛰면 닿는 가장 먼 칸
    for i in range(len(nums) - 1):  # 마지막 칸은 제외
        farthest = max(farthest, i + nums[i])
        if i == cur_end:  # 현재 층을 다 봤다 → 한 번 더 점프
            jumps += 1
            cur_end = farthest
    return jumps


def brute_force(nums):
    # DP: dp[j] = j 까지의 최소 점프 수. 최악 O(n^2)
    n = len(nums)
    INF = float("inf")
    dp = [INF] * n
    dp[0] = 0
    for i in range(n):
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            dp[j] = min(dp[j], dp[i] + 1)
    return dp[-1]
