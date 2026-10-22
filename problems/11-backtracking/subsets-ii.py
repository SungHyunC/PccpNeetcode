TITLE = "Subsets II (중복 원소가 있는 부분집합)"
LEVEL = "Medium"
SOURCE = "LeetCode 90"
PATTERN = "정렬 + 같은 레벨에서 같은 값 건너뛰기"

DESCRIPTION = """
정수 배열 nums 가 주어집니다. nums 에는 같은 값이 여러 번 들어 있을 수 있습니다.
nums 로 만들 수 있는 모든 부분집합을 return 하되, 같은 부분집합은 한 번만 포함하세요.
(원소의 구성이 같으면 같은 부분집합입니다. 예: nums = [2, 1, 2] 에서 [1, 2] 는 한 번만)
부분집합끼리의 순서, 부분집합 안의 원소 순서는 상관없습니다.

제한사항
- 1 ≤ len(nums) ≤ 12
- -10 ≤ nums[i] ≤ 10

입출력 예
nums = [1, 2, 2]  →  [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]
nums = [0]        →  [[], [0]]
"""

SIGNATURE = "def solution(nums: list[int]) -> list[list[int]]:"

HINTS = [
    "모든 부분집합을 만든 뒤 set 으로 중복을 제거해도 정답은 나옵니다. 하지만 처음부터 중복을 만들지 않는 방법이 정석입니다.",
    "먼저 nums 를 정렬하면 같은 값이 서로 붙어 있게 됩니다.",
    "dfs(start) 의 for j 루프에서 j > start 이고 nums[j] == nums[j - 1] 이면 continue 하세요. '같은 자리(레벨)에 같은 값을 두 번 놓지 않는다' 는 뜻입니다.",
]

COMPARE = "unordered_nested"

TESTS = [
    {"input": [[1, 2, 2]], "output": [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]},
    {"input": [[0]], "output": [[], [0]]},
    {"input": [[1, 1]], "output": [[], [1], [1, 1]]},
    {"input": [[2, 1, 2]], "output": [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]},
    {"input": [[-1, -1, 0]], "output": [[], [-1], [-1, -1], [0], [-1, 0], [-1, -1, 0]]},
    {
        "input": [[4, 4, 4, 1, 4]],
        "output": [
            [], [4], [4, 4], [4, 4, 4], [4, 4, 4, 4],
            [1], [1, 4], [1, 4, 4], [1, 4, 4, 4], [1, 4, 4, 4, 4],
        ],
    },
    {"input": [[1, 2, 3]], "output": [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]},
]

EXPLANATION = """
핵심: 정렬한 뒤, 결정 트리의 "같은 레벨(같은 for 루프)" 에서 같은 값을 두 번 고르지 않습니다.

nums = [1, 2, 2] (정렬됨, 두 2 를 2a, 2b 라 하면)
              []
       /       |        \\
     [1]     [2a]      [2b]  ← 같은 레벨에서 2 를 또 고름 → 건너뜀 ✂
    /   \\      |
[1,2a] [1,2b]✂ [2a,2b]
   |
[1,2a,2b]

조건이 j > start 인 이유: 같은 레벨의 "첫 번째" 2 는 골라야 합니다.
깊이 방향으로 [2a, 2b] 처럼 연속으로 고르는 것은 허용됩니다 (j == start 인 경우).

1. nums.sort()
2. dfs(start): path[:] 저장
3. j = start..n-1: j > start and nums[j] == nums[j-1] 이면 continue, 아니면 choose → dfs(j+1) → unchoose

시간 O(n · 2^n), 공간 O(n)

면접 포인트
- "중복 제거를 set 으로 하면 안 되나요?" → 가능하지만 중복 부분집합까지 다 만든 뒤 버리므로 낭비. 정렬 + skip 이 정석.
- 이 skip 규칙은 Combination Sum II, Permutations II, 3Sum 등에서도 똑같이 쓰입니다.
"""


def reference(nums):
    nums = sorted(nums)
    result = []
    path = []

    def dfs(start):
        result.append(path[:])
        for j in range(start, len(nums)):
            if j > start and nums[j] == nums[j - 1]:
                continue                # 같은 레벨에서 같은 값은 한 번만
            path.append(nums[j])
            dfs(j + 1)
            path.pop()

    dfs(0)
    return result


def brute_force(nums):
    # 모든 부분집합을 만든 뒤 (정렬된 튜플) 집합으로 중복 제거
    nums = sorted(nums)
    n = len(nums)
    seen = set()
    for mask in range(1 << n):
        seen.add(tuple(nums[i] for i in range(n) if mask >> i & 1))
    return [list(t) for t in seen]
