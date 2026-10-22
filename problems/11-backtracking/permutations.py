TITLE = "Permutations (순열)"
LEVEL = "Medium"
SOURCE = "LeetCode 46"
PATTERN = "백트래킹: used 배열로 아직 안 쓴 원소만 고르기"

DESCRIPTION = """
서로 다른 정수가 담긴 배열 nums 가 주어집니다.
nums 의 원소를 모두 한 번씩 사용해 만들 수 있는 모든 순열(permutation)을 return 하세요.
순열끼리의 순서는 상관없지만, 각 순열 안의 순서는 의미가 있습니다.

제한사항
- 1 ≤ len(nums) ≤ 8
- -10 ≤ nums[i] ≤ 10
- nums 의 원소는 모두 다릅니다.

입출력 예
nums = [1, 2, 3]  →  [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
nums = [0, 1]     →  [[0, 1], [1, 0]]
"""

SIGNATURE = "def solution(nums: list[int]) -> list[list[int]]:"

HINTS = [
    "n 개 중 첫 자리를 고르는 방법 n 가지, 둘째 자리 n-1 가지 ... → 총 n! 개입니다.",
    "부분집합과 달리 '앞에서 고른 원소보다 뒤만' 이 아니라 '아직 안 쓴 아무 원소나' 고를 수 있어야 합니다. 어떤 원소를 썼는지 used 배열로 기록하세요.",
    "dfs(): len(path) == n 이면 path[:] 저장. 아니면 모든 i 에 대해 used[i] 가 False 일 때만 used[i] = True, path.append → dfs() → path.pop(), used[i] = False.",
]

COMPARE = "unordered"

TESTS = [
    {"input": [[1, 2, 3]], "output": [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]},
    {"input": [[0, 1]], "output": [[0, 1], [1, 0]]},
    {"input": [[1]], "output": [[1]]},
    {"input": [[3, -1]], "output": [[3, -1], [-1, 3]]},
    {"input": [[-10, 0, 10]], "output": [[-10, 0, 10], [-10, 10, 0], [0, -10, 10], [0, 10, -10], [10, -10, 0], [10, 0, -10]]},
    {
        "input": [[1, 2, 3, 4]],
        "output": [
            [1, 2, 3, 4], [1, 2, 4, 3], [1, 3, 2, 4], [1, 3, 4, 2], [1, 4, 2, 3], [1, 4, 3, 2],
            [2, 1, 3, 4], [2, 1, 4, 3], [2, 3, 1, 4], [2, 3, 4, 1], [2, 4, 1, 3], [2, 4, 3, 1],
            [3, 1, 2, 4], [3, 1, 4, 2], [3, 2, 1, 4], [3, 2, 4, 1], [3, 4, 1, 2], [3, 4, 2, 1],
            [4, 1, 2, 3], [4, 1, 3, 2], [4, 2, 1, 3], [4, 2, 3, 1], [4, 3, 1, 2], [4, 3, 2, 1],
        ],
    },
]

EXPLANATION = """
핵심: 각 자리에 "아직 쓰지 않은 원소" 를 하나씩 놓아 보는 백트래킹. used[i] 로 사용 여부를 관리합니다.

nums = [1, 2, 3]
               []
       /        |        \\
     [1]       [2]       [3]
    /   \\     /   \\     /   \\
 [1,2] [1,3] [2,1] [2,3] [3,1] [3,2]
   |     |     |     |     |     |
 [1,2,3] ...                   [3,2,1]   ← 리프(길이 n)만 결과

1. path = [], used = [False] * n
2. len(path) == n 이면 path[:] 저장 후 return
3. 모든 i 에 대해 used[i] 가 False 면: 선택 → 재귀 → 선택 취소 (used 도 되돌리기!)

시간 O(n · n!) — 순열 n! 개, 각각 복사 O(n)
공간 O(n) (재귀 깊이 + used)

면접 포인트
- 부분집합/조합은 "start 인덱스", 순열은 "used 배열" 로 구분해 기억하세요.
- 코딩 테스트(PCCP)에서는 itertools.permutations(nums) 한 줄로 끝낼 수 있습니다 (alternative).
  단, 면접에서는 직접 구현을 요구하는 경우가 많습니다.
- 중복 원소가 있다면(Permutations II) 정렬 후 "같은 값이고 앞 원소를 아직 안 썼으면 건너뛰기" 규칙을 추가합니다.
- 스왑(swap) 방식: 위치 k 에 nums[k..n-1] 을 하나씩 스왑해 넣고 재귀하는 방법도 있습니다 (brute_force).
"""


def reference(nums):
    n = len(nums)
    result = []
    path = []
    used = [False] * n

    def dfs():
        if len(path) == n:
            result.append(path[:])
            return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True          # 선택
            path.append(nums[i])
            dfs()                   # 탐색
            path.pop()              # 선택 취소
            used[i] = False

    dfs()
    return result


def alternative(nums):
    from itertools import permutations
    return [list(p) for p in permutations(nums)]


def brute_force(nums):
    # 스왑 방식: k 번째 자리에 올 원소를 nums[k..] 중에서 골라 스왑
    nums = nums[:]
    result = []

    def dfs(k):
        if k == len(nums):
            result.append(nums[:])
            return
        for i in range(k, len(nums)):
            nums[k], nums[i] = nums[i], nums[k]
            dfs(k + 1)
            nums[k], nums[i] = nums[i], nums[k]

    dfs(0)
    return result
