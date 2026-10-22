TITLE = "Subsets (부분집합)"
LEVEL = "Medium"
SOURCE = "LeetCode 78"
PATTERN = "백트래킹: 각 원소를 넣는다/안 넣는다"

DESCRIPTION = """
서로 다른 정수가 담긴 배열 nums 가 주어집니다.
nums 로 만들 수 있는 모든 부분집합(멱집합, power set)을 return 하세요.
빈 집합과 nums 전체도 부분집합에 포함됩니다.
부분집합끼리의 순서, 부분집합 안의 원소 순서는 상관없습니다. 같은 부분집합이 두 번 나오면 안 됩니다.

제한사항
- 0 ≤ len(nums) ≤ 12
- -10 ≤ nums[i] ≤ 10
- nums 의 원소는 모두 다릅니다.

입출력 예
nums = [1, 2, 3]  →  [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
nums = [7]        →  [[], [7]]
"""

SIGNATURE = "def solution(nums: list[int]) -> list[list[int]]:"

HINTS = [
    "원소가 n 개이면 부분집합은 2^n 개입니다. 각 원소마다 '넣는다 / 안 넣는다' 두 갈래가 있기 때문입니다.",
    "재귀 함수 dfs(i) 가 'i 번째 원소부터 결정한다' 를 뜻하게 하고, 지금까지 고른 원소를 리스트 path 에 담아 보세요.",
    "dfs(i) 진입 시 path 의 복사본(path[:])을 결과에 넣고, j = i..n-1 에 대해 path.append(nums[j]) → dfs(j + 1) → path.pop() 하면 됩니다.",
]

COMPARE = "unordered_nested"

TESTS = [
    {"input": [[1, 2, 3]], "output": [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]},
    {"input": [[7]], "output": [[], [7]]},
    {"input": [[]], "output": [[]]},
    {"input": [[-1, 5]], "output": [[], [-1], [5], [-1, 5]]},
    {"input": [[0, -10, 10]], "output": [[], [0], [-10], [10], [0, -10], [0, 10], [-10, 10], [0, -10, 10]]},
    {
        "input": [[4, 1, 3, 2]],
        "output": [
            [], [4], [1], [3], [2],
            [4, 1], [4, 3], [4, 2], [1, 3], [1, 2], [3, 2],
            [4, 1, 3], [4, 1, 2], [4, 3, 2], [1, 3, 2],
            [4, 1, 3, 2],
        ],
    },
]

EXPLANATION = """
핵심: 결정 트리(decision tree)를 깊이 우선으로 훑습니다. 트리의 모든 노드가 하나의 부분집합입니다.

        []
      /  |  \\
    [1] [2] [3]          ← 시작 인덱스 이후 원소만 고르므로 [2,1] 같은 중복이 생기지 않음
    / \\    \\
 [1,2] [1,3] [2,3]
   |
[1,2,3]

1. path = [] (지금까지 고른 원소), result = []
2. dfs(start): result 에 path[:] 저장 (복사! 그냥 path 를 넣으면 나중에 다 비어 버림)
3. j = start..n-1: 선택(append) → dfs(j + 1) 탐색 → 선택 취소(pop)

시간 O(n · 2^n) — 부분집합 2^n 개, 각각 복사에 O(n)
공간 O(n) 재귀 깊이 (결과 저장 공간 제외)

면접 포인트
- 백트래킹 템플릿 choose → explore → unchoose 를 그대로 말로 설명하세요.
- 비트마스크 풀이(brute_force)도 알아 두세요: mask 0..2^n-1 의 i 번째 비트가 1 이면 nums[i] 포함.
- 반복문 풀이: result = [[]] 에서 시작해 원소 x 마다 기존 부분집합 각각에 x 를 붙인 것을 추가 (alternative).
- 중복 원소가 있으면 Subsets II (정렬 + 같은 레벨 중복 건너뛰기) 로 이어집니다.
"""


def reference(nums):
    result = []
    path = []

    def dfs(start):
        result.append(path[:])          # 현재 노드 = 하나의 부분집합 (복사해서 저장)
        for j in range(start, len(nums)):
            path.append(nums[j])        # 선택 (choose)
            dfs(j + 1)                  # 탐색 (explore): j 이후 원소만 고려
            path.pop()                  # 선택 취소 (unchoose)

    dfs(0)
    return result


def alternative(nums):
    # 반복문: 원소 하나를 볼 때마다 기존 부분집합에 그 원소를 붙인 것을 추가
    result = [[]]
    for x in nums:
        result += [subset + [x] for subset in result]
    return result


def brute_force(nums):
    # 비트마스크: mask 의 i 번째 비트가 1 이면 nums[i] 를 포함
    n = len(nums)
    return [[nums[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]
