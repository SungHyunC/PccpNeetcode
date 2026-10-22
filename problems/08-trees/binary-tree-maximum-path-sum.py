from lib.structures import TreeNode, build_tree

TITLE = "Binary Tree Maximum Path Sum (이진 트리 최대 경로 합)"
LEVEL = "Hard"
SOURCE = "LeetCode 124"
PATTERN = "한쪽 가지 이득은 위로 반환, 꺾이는 경로는 전역 최댓값으로 갱신"

DESCRIPTION = """
이진 트리의 root 가 주어집니다. 여기서 '경로'란 부모-자식 간선을 따라 이어진 노드들의 나열로,
같은 노드를 두 번 지나지 않으며 노드를 최소 1개 포함합니다. 루트를 지나지 않아도 됩니다.
경로에 포함된 노드 값의 합을 경로 합이라고 할 때, 가능한 경로 합의 최댓값을 return 하세요.

트리는 레벨 순서 리스트로 표기합니다. 빈 자리는 None 입니다.

제한사항
- 1 ≤ 노드 개수 ≤ 30,000
- -1,000 ≤ 노드 값 ≤ 1,000

입출력 예
root = [1, 2, 3]                          →  6    (2 - 1 - 3)
root = [-10, 9, 20, None, None, 15, 7]    →  42   (15 - 20 - 7)
root = [-3]                               →  -3
"""

SIGNATURE = "def solution(root: TreeNode) -> int:"

IMPORTS = "from lib.structures import TreeNode"

HINTS = [
    "경로에는 가장 높은 노드(꺾이는 지점)가 하나 있고, 그 노드에서 왼쪽 아래로 한 줄, 오른쪽 아래로 한 줄이 뻗어 나갑니다. (Diameter of Binary Tree 와 같은 구조)",
    "gain(node) = node 에서 시작해 아래로 '한쪽으로만' 내려가는 경로의 최대 합. 이 값이 부모에게 올려 보낼 정보입니다.",
    "자식의 gain 이 음수면 붙이지 않는 편이 낫습니다: left = max(gain(left), 0). 꺾이는 경로 후보는 node.val + left + right 로 전역 최댓값을 갱신하고, 부모에게는 node.val + max(left, right) 를 반환합니다.",
    "정답 초깃값을 0 으로 두면 모든 값이 음수인 트리에서 틀립니다. -무한대(또는 root.val)로 시작하세요.",
]

TESTS = [
    {"input": [[1, 2, 3]], "output": 6},
    {"input": [[-10, 9, 20, None, None, 15, 7]], "output": 42},
    {"input": [[-3]], "output": -3},
    {"input": [[2, -1]], "output": 2},
    {"input": [[-1, -2, -3]], "output": -1},
    {"input": [[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]], "output": 48},
    {"input": [[1, -2, 3]], "output": 4},
    {"input": [[-2, 6, None, 0, -6]], "output": 6},
]


def prepare(values):
    return [build_tree(values)]


EXPLANATION = """
핵심: Diameter 와 같은 "반환값 ≠ 정답" 패턴에, 음수 처리가 더해진 문제입니다.
- 반환값 gain(node): node 에서 아래로 한쪽 가지만 타고 내려가는 최대 합 (부모가 이어 붙일 수 있음)
- 정답 후보: node.val + 왼쪽 gain + 오른쪽 gain (node 에서 꺾이는 경로, 부모에게는 못 올림)

        -10
        /  \\             gain(15) = 15, gain(7) = 7
       9    20           노드 20: 후보 = 20 + 15 + 7 = 42 ← 최댓값
           /  \\                  반환 = 20 + max(15, 7) = 35
          15   7         노드 -10: 후보 = -10 + 9 + 35 = 34, 반환 = 25

1. best = -무한대
2. gain(node): None 이면 0
   left = max(gain(node.left), 0), right = max(gain(node.right), 0)   ← 손해 보는 가지는 버림
   best = max(best, node.val + left + right)
   return node.val + max(left, right)
3. gain(root) 호출 후 best

시간 O(n), 공간 O(h)
면접 포인트: (1) 음수 가지를 0 으로 잘라내는 이유, (2) 부모에게 두 가지를 모두 올리면 안 되는 이유
(경로가 Y 자로 갈라지게 되므로), (3) 모든 값이 음수일 때 초깃값 문제를 설명하세요.
alternative 는 재귀 없이 BFS 순서를 거꾸로 처리해 후위 순회를 흉내 내는 방법으로, 깊은 트리에서도 안전합니다.
"""


def reference(root):
    import sys
    sys.setrecursionlimit(100_000)
    best = float("-inf")

    def gain(node):
        nonlocal best
        if node is None:
            return 0
        left = max(gain(node.left), 0)    # 음수 가지는 안 붙이는 게 이득
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)  # node 에서 꺾이는 경로
        return node.val + max(left, right)         # 부모에게는 한쪽 가지만

    gain(root)
    return best


def alternative(root):
    # 반복 풀이: BFS 순서의 역순으로 처리하면 자식이 항상 부모보다 먼저 처리됨 (후위 순회 효과)
    order, stack = [], [root]
    while stack:
        node = stack.pop()
        if node:
            order.append(node)
            stack.append(node.left)
            stack.append(node.right)
    gain = {None: 0}
    best = float("-inf")
    for node in reversed(order):
        left = max(gain[node.left], 0)
        right = max(gain[node.right], 0)
        best = max(best, node.val + left + right)
        gain[node] = node.val + max(left, right)
    return best
