from collections import deque

from lib.structures import TreeNode, build_tree, tree_to_list

TITLE = "Invert Binary Tree (이진 트리 좌우 반전)"
LEVEL = "Easy"
SOURCE = "LeetCode 226"
PATTERN = "모든 노드에서 left / right 교환 (DFS 또는 BFS)"

DESCRIPTION = """
이진 트리의 root 가 주어집니다.
모든 노드의 왼쪽 자식과 오른쪽 자식을 서로 바꿔 거울에 비친 모양의 트리를 만들고, root 를 return 하세요.

트리는 레벨 순서 리스트로 표기합니다. 빈 자리는 None 입니다.
예) [4, 2, 7, 1, 3, 6, 9]

        4                  4
     ┌──┴──┐            ┌──┴──┐
     2     7     →      7     2
    ┌┴┐   ┌┴┐          ┌┴┐   ┌┴┐
    1 3   6 9          9 6   3 1

제한사항
- 0 ≤ 노드 개수 ≤ 100
- -100 ≤ 노드 값 ≤ 100

입출력 예
root = [4, 2, 7, 1, 3, 6, 9]  →  [4, 7, 2, 9, 6, 3, 1]
root = [2, 1, 3]              →  [2, 3, 1]
root = []                     →  []
"""

SIGNATURE = "def solution(root: TreeNode) -> TreeNode:"

IMPORTS = "from lib.structures import TreeNode"

HINTS = [
    "트리 전체를 뒤집는 것은 '루트의 두 자식을 바꾸고, 각 서브트리도 똑같이 뒤집는 것'과 같습니다. 재귀로 표현해 보세요.",
    "기저 사례: root 가 None 이면 None 을 return.",
    "root.left, root.right = solution(root.right), solution(root.left) 한 줄이면 됩니다. 재귀가 싫다면 큐(BFS)나 스택으로 모든 노드를 방문하며 자식을 바꿔도 됩니다.",
]

TESTS = [
    {"input": [[4, 2, 7, 1, 3, 6, 9]], "output": [4, 7, 2, 9, 6, 3, 1]},
    {"input": [[2, 1, 3]], "output": [2, 3, 1]},
    {"input": [[]], "output": []},
    {"input": [[1]], "output": [1]},
    {"input": [[1, 2]], "output": [1, None, 2]},
    {"input": [[1, 2, 3, 4, None, None, 5]], "output": [1, 3, 2, 5, None, None, 4]},
    {"input": [[-1, -2, None, -3]], "output": [-1, None, -2, None, -3]},
]


def prepare(values):
    return [build_tree(values)]


def present(root):
    if root is None or (hasattr(root, "left") and hasattr(root, "right")):
        return tree_to_list(root)
    return root


EXPLANATION = """
핵심: "트리를 뒤집는다" = "자식 둘을 바꾸고, 두 서브트리를 각각 뒤집는다". 트리 재귀의 가장 기본 형태입니다.

1. root 가 None 이면 None
2. 왼쪽 서브트리와 오른쪽 서브트리를 각각 뒤집은 결과를 서로 반대편에 연결
3. root 를 return

순회 순서는 상관없습니다. 전위(pre-order: 먼저 바꾸고 내려감)든 후위(post-order: 내려갔다 와서 바꿈)든,
BFS 든 "모든 노드에서 한 번씩 교환"만 하면 됩니다.

시간 O(n), 공간 O(h) (h = 트리 높이, 재귀 스택). BFS 는 공간 O(w) (w = 최대 너비)
면접 포인트: 재귀 풀이를 쓰고 나서 "트리가 한쪽으로 치우쳐 높이가 10만이면?" 이라는 질문에
반복(스택/큐) 풀이로 답할 수 있으면 좋습니다. 파이썬 기본 재귀 한도는 약 1000 입니다.
"""


def reference(root):
    if root is None:
        return None
    # 오른쪽을 뒤집은 결과를 왼쪽에, 왼쪽을 뒤집은 결과를 오른쪽에
    root.left, root.right = reference(root.right), reference(root.left)
    return root


def alternative(root):
    # BFS 반복 풀이: 큐에서 꺼낸 노드마다 자식 교환
    q = deque([root] if root else [])
    while q:
        node = q.popleft()
        node.left, node.right = node.right, node.left
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return root
