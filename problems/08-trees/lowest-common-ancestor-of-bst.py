from lib.structures import TreeNode, build_tree, find_node

TITLE = "Lowest Common Ancestor of a BST (BST 의 최소 공통 조상)"
LEVEL = "Medium"
SOURCE = "LeetCode 235"
PATTERN = "BST 성질로 p, q 가 갈라지는 지점 찾기"

DESCRIPTION = """
이진 탐색 트리(BST)의 root 와 트리 안의 서로 다른 두 노드 p, q 가 주어집니다.
p 와 q 를 모두 자손으로 갖는 노드 중 가장 깊은(가장 아래에 있는) 노드, 즉 최소 공통 조상(LCA)을 return 하세요.
노드는 자기 자신의 자손으로 칩니다. (p 가 q 의 조상이면 답은 p)

채점용 입력은 [트리 리스트, p 의 값, q 의 값] 이고,
solution 에는 build 된 root 와 그 값을 가진 실제 노드 p, q 가 전달됩니다.
노드(TreeNode)를 return 하면 채점기가 그 값으로 비교합니다.

제한사항
- 2 ≤ 노드 개수 ≤ 100,000
- 노드 값은 모두 다르며 -10^9 ≤ 노드 값 ≤ 10^9
- p != q 이고 둘 다 트리에 있습니다.

입출력 예
root = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], p = 2, q = 8  →  6
root = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], p = 2, q = 4  →  2
root = [2, 1],                                  p = 2, q = 1  →  2
"""

SIGNATURE = "def solution(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:"

IMPORTS = "from lib.structures import TreeNode"

HINTS = [
    "BST 에서는 값만 보고 p, q 가 현재 노드의 왼쪽에 있는지 오른쪽에 있는지 알 수 있습니다.",
    "p, q 가 둘 다 현재 노드보다 작으면 LCA 는 왼쪽 서브트리에, 둘 다 크면 오른쪽 서브트리에 있습니다.",
    "그 외의 경우(한쪽은 작고 한쪽은 크거나, 둘 중 하나가 현재 노드와 같음)에는 현재 노드에서 두 경로가 갈라지므로 현재 노드가 정답입니다. 반복문으로 루트에서 내려가면 공간 O(1).",
]

TESTS = [
    {"input": [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 8], "output": 6},
    {"input": [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 4], "output": 2},
    {"input": [[2, 1], 2, 1], "output": 2},
    {"input": [[2, 1, 3], 1, 3], "output": 2},
    {"input": [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 3, 5], "output": 4},
    {"input": [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 5, 0], "output": 2},
    {"input": [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 7, 9], "output": 8},
    {"input": [[-10, -20, 30, None, None, 10, 40], 10, 40], "output": 30},
]


def prepare(values, p_val, q_val):
    root = build_tree(values)
    return [root, find_node(root, p_val), find_node(root, q_val)]


def present(node):
    # 노드를 반환하면 값으로 바꿔 비교합니다 (정수를 직접 반환해도 그대로 비교)
    return node.val if hasattr(node, "val") else node


EXPLANATION = """
핵심: BST 에서 루트부터 내려가다 보면 p 와 q 로 가는 길이 처음으로 갈라지는 노드가 있습니다. 그곳이 LCA 입니다.

            6
          /   \\
         2     8          p=2, q=8: 6 에서 왼쪽/오른쪽으로 갈라짐 → 6
        / \\   / \\        p=3, q=5: 6(둘 다 작음) → 2(둘 다 큼) → 4(갈라짐) → 4
       0   4 7   9        p=2, q=4: 6(둘 다 작음) → 2(p 자신) → 2
          / \\
         3   5

1. node = root
2. p, q 가 둘 다 node 보다 작으면 node = node.left
3. 둘 다 크면 node = node.right
4. 아니면 node 가 정답

시간 O(h), 공간 O(1) (반복문)
면접 포인트: "BST 가 아닌 일반 이진 트리라면?" (LeetCode 236) 이 단골 후속 질문입니다.
그때는 값으로 방향을 정할 수 없으므로 후위 순회로 "이 서브트리에 p 나 q 가 있는가"를 위로 올려 보내고,
왼쪽과 오른쪽 모두에서 찾았다고 보고된 첫 노드가 LCA 가 됩니다 (alternative). 시간 O(n).
"""


def reference(root, p, q):
    node = root
    while node:
        if p.val < node.val and q.val < node.val:
            node = node.left        # 둘 다 왼쪽에 있음
        elif p.val > node.val and q.val > node.val:
            node = node.right       # 둘 다 오른쪽에 있음
        else:
            return node             # 여기서 갈라짐 (또는 p/q 자신)
    return None


def alternative(root, p, q):
    # 일반 이진 트리용 LCA (LeetCode 236): BST 성질을 쓰지 않음
    def dfs(node):
        if node is None or node is p or node is q:
            return node
        left, right = dfs(node.left), dfs(node.right)
        if left and right:          # 양쪽에서 하나씩 발견 → 내가 LCA
            return node
        return left or right        # 발견한 쪽을 위로 전달

    return dfs(root)
