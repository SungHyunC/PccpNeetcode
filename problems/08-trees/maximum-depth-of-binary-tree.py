from collections import deque

from lib.structures import TreeNode, build_tree

TITLE = "Maximum Depth of Binary Tree (이진 트리 최대 깊이)"
LEVEL = "Easy"
SOURCE = "LeetCode 104"
PATTERN = "자식의 깊이를 받아 1 + max (후위 순회) / BFS 레벨 수 세기"

DESCRIPTION = """
이진 트리의 root 가 주어집니다.
루트에서 가장 먼 리프(leaf)까지 가는 경로에 있는 '노드의 개수'를 return 하세요.
빈 트리의 깊이는 0 입니다.

트리는 레벨 순서 리스트로 표기합니다. 빈 자리는 None 입니다.

제한사항
- 0 ≤ 노드 개수 ≤ 10,000
- -100 ≤ 노드 값 ≤ 100

입출력 예
root = [3, 9, 20, None, None, 15, 7]  →  3
root = [1, None, 2]                   →  2
root = []                             →  0
"""

SIGNATURE = "def solution(root: TreeNode) -> int:"

IMPORTS = "from lib.structures import TreeNode"

HINTS = [
    "어떤 노드의 깊이 = 1 + (왼쪽 서브트리 깊이와 오른쪽 서브트리 깊이 중 큰 값). 빈 트리는 0.",
    "재귀 한 줄: return 0 if root is None else 1 + max(f(root.left), f(root.right))",
    "반복 풀이: BFS 로 레벨 단위로 처리하면서 레벨 수를 세면 그게 깊이입니다. 스택에 (노드, 깊이) 를 넣는 DFS 도 가능합니다.",
]

TESTS = [
    {"input": [[3, 9, 20, None, None, 15, 7]], "output": 3},
    {"input": [[1, None, 2]], "output": 2},
    {"input": [[]], "output": 0},
    {"input": [[0]], "output": 1},
    {"input": [[1, 2, 3, 4, None, None, None, 5]], "output": 4},
    {"input": [[1, None, 2, None, 3, None, 4, None, 5]], "output": 5},
    {"input": [[1, 2, 3, 4, 5, 6, 7]], "output": 3},
]


def prepare(values):
    return [build_tree(values)]


EXPLANATION = """
핵심: "아래에서 위로 정보 올리기" 의 가장 단순한 예. 자식들이 자기 깊이를 알려 주면 부모는 1 + max 만 하면 됩니다.

        3          depth(9) = 1, depth(15) = depth(7) = 1
       / \\         depth(20) = 1 + max(1, 1) = 2
      9  20        depth(3)  = 1 + max(1, 2) = 3
         / \\
        15  7

1. root 가 None 이면 0
2. 왼쪽 깊이 L, 오른쪽 깊이 R 을 재귀로 구함
3. 1 + max(L, R) 반환

시간 O(n), 공간 O(h) (재귀 스택, h 는 높이: 균형 트리면 log n, 치우친 트리면 n)
면접 포인트: 재귀(DFS) / BFS(레벨 수) / 스택 DFS 세 가지를 모두 말할 수 있으면 좋습니다.
'깊이(depth)'를 노드 개수로 세는지 간선 개수로 세는지 문제마다 다르니 꼭 확인하세요 (이 문제는 노드 개수).
치우친 트리에서 노드가 수천 개를 넘으면 파이썬 재귀 한도에 걸립니다 → sys.setrecursionlimit 또는 BFS.
"""


def reference(root):
    if root is None:
        return 0
    return 1 + max(reference(root.left), reference(root.right))


def alternative(root):
    # BFS: 레벨을 하나 처리할 때마다 depth += 1
    if root is None:
        return 0
    q, depth = deque([root]), 0
    while q:
        depth += 1
        for _ in range(len(q)):  # 현재 레벨의 노드 수만큼만 꺼냄
            node = q.popleft()
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
    return depth
