TITLE = "Combination Sum (조합의 합)"
LEVEL = "Medium"
SOURCE = "LeetCode 39"
PATTERN = "백트래킹: 같은 원소 재사용 + 합 초과 시 가지치기"

DESCRIPTION = """
서로 다른 양의 정수 배열 candidates 와 목표값 target 이 주어집니다.
candidates 의 수를 골라 합이 정확히 target 이 되는 모든 조합을 return 하세요.
같은 수를 여러 번 골라도 됩니다. 단, 고른 수의 구성(개수)이 같으면 같은 조합으로 봅니다.
예: [2, 2, 3] 과 [3, 2, 2] 는 같은 조합이므로 한 번만 포함해야 합니다.
조합끼리의 순서, 조합 안의 순서는 상관없습니다. 가능한 조합이 없으면 빈 리스트를 return 합니다.

제한사항
- 1 ≤ len(candidates) ≤ 30
- 1 ≤ candidates[i] ≤ 200, 모든 값은 서로 다름
- 1 ≤ target ≤ 500
- 답이 되는 조합의 개수는 150 개 이하가 되도록 주어집니다.

입출력 예
candidates = [2, 3, 6, 7], target = 7  →  [[2, 2, 3], [7]]
candidates = [2, 3, 5],    target = 8  →  [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
candidates = [2],          target = 1  →  []
"""

SIGNATURE = "def solution(candidates: list[int], target: int) -> list[list[int]]:"

HINTS = [
    "[2, 3] 과 [3, 2] 를 둘 다 만들지 않으려면, 조합 안의 원소를 '인덱스가 줄어들지 않는 순서' 로만 고르게 강제하면 됩니다.",
    "dfs(start, remain): candidates[start:] 중에서만 골라 remain 을 0 으로 만드는 함수로 정의해 보세요.",
    "같은 수를 다시 쓸 수 있으므로 candidates[j] 를 고른 뒤에는 dfs(j, remain - candidates[j]) 로 j 를 그대로 넘깁니다 (j + 1 이 아님).",
    "candidates 를 정렬해 두면 remain - candidates[j] < 0 인 순간 그 뒤는 더 볼 필요가 없으므로 break 할 수 있습니다 (가지치기).",
]

COMPARE = "unordered_nested"

TESTS = [
    {"input": [[2, 3, 6, 7], 7], "output": [[2, 2, 3], [7]]},
    {"input": [[2, 3, 5], 8], "output": [[2, 2, 2, 2], [2, 3, 3], [3, 5]]},
    {"input": [[2], 1], "output": []},
    {"input": [[1], 1], "output": [[1]]},
    {"input": [[1], 4], "output": [[1, 1, 1, 1]]},
    {"input": [[7, 3, 2], 10], "output": [[2, 2, 2, 2, 2], [2, 2, 3, 3], [3, 7]]},
    {"input": [[5, 10], 3], "output": []},
    {"input": [[8, 4, 6], 12], "output": [[4, 4, 4], [4, 8], [6, 6]]},
]

EXPLANATION = """
핵심: 부분집합 템플릿에서 "다음 탐색 시작 인덱스" 만 바꾸면 됩니다.
- 재사용 불가(Subsets, Combination Sum II): dfs(j + 1)
- 재사용 가능(이 문제)              : dfs(j)   ← 같은 원소를 또 고를 수 있음

candidates = [2, 3, 6, 7], target = 7 (정렬됨)
dfs(0, 7)
├─ 2 → dfs(0, 5)
│   ├─ 2 → dfs(0, 3)
│   │   ├─ 2 → dfs(0, 1) → 2 > 1 이라 break (가지치기)
│   │   └─ 3 → dfs(1, 0) ✔ [2, 2, 3]
│   └─ 3 → dfs(1, 2) → 3 > 2 break
├─ 3 → dfs(1, 4) → 3 → dfs(1, 1) → break ...
└─ 7 → dfs(3, 0) ✔ [7]

1. candidates 정렬
2. dfs(start, remain): remain == 0 이면 path 복사본 저장
3. j = start..: candidates[j] > remain 이면 break, 아니면 append → dfs(j, remain - c) → pop

시간: 최악 O(n^(T/m)) 정도 (T = target, m = 최솟값). 트리 깊이가 최대 T/m.
공간: O(T/m) 재귀 깊이

면접 포인트
- "왜 [2,3,2] 같은 중복이 안 생기나요?" → 시작 인덱스가 줄어들지 않아 조합이 항상 비내림차순으로 만들어지기 때문.
- 정렬 + break 가지치기(pruning)의 효과를 설명하세요.
- 개수만 세면 되는 문제라면 DP(동전 교환 Coin Change II)로 바꿀 수 있다는 점도 언급하면 좋습니다.
- alternative 는 DP 로 '합 t 를 만드는 조합 목록' 을 쌓아 가는 방식입니다 (동전 순서대로 바깥 루프 → 중복 없음).
"""


def reference(candidates, target):
    candidates = sorted(candidates)
    result = []
    path = []

    def dfs(start, remain):
        if remain == 0:
            result.append(path[:])
            return
        for j in range(start, len(candidates)):
            c = candidates[j]
            if c > remain:          # 정렬되어 있으므로 뒤쪽은 전부 더 큼 → 가지치기
                break
            path.append(c)
            dfs(j, remain - c)      # j 그대로: 같은 수 재사용 허용
            path.pop()

    dfs(0, target)
    return result


def alternative(candidates, target):
    # DP: combos[t] = 합이 t 인 조합 목록. 동전(후보)을 바깥 루프로 돌려야 순서만 다른 중복이 생기지 않음
    combos = [[] for _ in range(target + 1)]
    combos[0] = [[]]
    for c in candidates:
        for t in range(c, target + 1):
            for prev in combos[t - c]:
                combos[t].append(prev + [c])
    return combos[target]
