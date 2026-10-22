TITLE = "Jump Game (점프 게임)"
LEVEL = "Medium"
SOURCE = "LeetCode 55"
PATTERN = "도달 가능한 최대 위치(farthest)를 갱신하는 그리디"

DESCRIPTION = """
정수 배열 nums 가 주어집니다. 처음에는 0번 칸에 서 있습니다.
i 번 칸에서는 오른쪽으로 1칸 이상 nums[i] 칸 이하만큼 점프할 수 있습니다. (nums[i] 가 0 이면 점프 불가)
마지막 칸에 도착할 수 있으면 True, 없으면 False 를 return 하세요.

제한사항
- 1 ≤ len(nums) ≤ 100,000
- 0 ≤ nums[i] ≤ 100,000

입출력 예
nums = [2, 3, 1, 1, 4]  →  True   (0 → 1 → 4)
nums = [3, 2, 1, 0, 4]  →  False  (어떻게 가도 3번 칸(값 0)에 갇힘)
"""

SIGNATURE = "def solution(nums: list[int]) -> bool:"

HINTS = [
    "dp[i] = i 번 칸에 도달 가능한가? 로 풀면 각 칸에서 최대 nums[i] 칸을 표시해야 해서 최악 O(n^2) 입니다.",
    "실제로 필요한 정보는 '지금까지 도달 가능한 가장 먼 위치' 하나뿐입니다. 그보다 앞의 칸은 모두 도달 가능하니까요.",
    "farthest = 0 으로 시작해 i = 0..n-1 을 보며, i > farthest 면 False (여기에 올 수 없음). 아니면 farthest = max(farthest, i + nums[i]).",
]

TESTS = [
    {"input": [[2, 3, 1, 1, 4]], "output": True},
    {"input": [[3, 2, 1, 0, 4]], "output": False},
    {"input": [[0]], "output": True},
    {"input": [[1, 0]], "output": True},
    {"input": [[0, 1]], "output": False},
    {"input": [[2, 0, 0]], "output": True},
    {"input": [[1, 1, 0, 1]], "output": False},
    {"input": [[5, 0, 0, 0, 0, 0, 1]], "output": False},
]

PERF_LIMIT = 1.0


def perf_case():
    n = 100_000
    # 모든 칸이 n-2 까지만 닿는다 → 마지막 칸은 도달 불가. O(n^2) 표시 방식은 시간 초과
    nums = [n - 2 - i for i in range(n - 1)] + [0]
    return {"input": [nums], "output": False}


EXPLANATION = """
아이디어
- "i 번 칸까지 도달 가능" 하다면 0..i 의 모든 칸도 도달 가능합니다(앞 칸에서 더 짧게 뛰면 되므로).
- 따라서 도달 가능 영역은 항상 [0, farthest] 구간 하나 → farthest 하나만 관리하면 됩니다.

단계
1. farthest = 0
2. i = 0 → n-1:
   - i > farthest 이면 i 에 올 수 없음 → False
   - farthest = max(farthest, i + nums[i])
   - farthest ≥ n-1 이면 일찍 True
3. 끝까지 오면 True

  nums     : 3  2  1  0  4
  i+nums[i]: 3  3  3  3  -
  farthest : 3  3  3  3  → i = 4 > 3 → False

왜 그리디가 맞는가
- 각 칸에서 '어디로 뛸지' 고르지 않고, 도달 가능한 구간 전체를 한 번에 넓혀 갑니다.
  어떤 경로로 가든 도달 가능한 칸의 집합은 같으므로 선택을 잘못할 위험이 없습니다.

복잡도: 시간 O(n), 공간 O(1)

면접 포인트
- DP(O(n^2)) → 그리디(O(n)) 로 개선하는 흐름이 좋습니다.
- 뒤에서부터 보는 방법도 있습니다: goal = n-1, i 가 goal 에 닿으면(i + nums[i] ≥ goal) goal = i. 마지막에 goal == 0.
- 최소 점프 횟수를 묻는 Jump Game II 와 함께 나오는 경우가 많습니다.
"""


def reference(nums):
    farthest = 0  # 지금까지 도달 가능한 가장 먼 인덱스
    last = len(nums) - 1
    for i, step in enumerate(nums):
        if i > farthest:  # i 번 칸에는 올 수 없음
            return False
        farthest = max(farthest, i + step)
        if farthest >= last:
            return True
    return True


def brute_force(nums):
    # DP: reach[i] = i 에 도달 가능한가. 최악 O(n^2)
    n = len(nums)
    reach = [False] * n
    reach[0] = True
    for i in range(n):
        if not reach[i]:
            continue
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            reach[j] = True
    return reach[-1]
