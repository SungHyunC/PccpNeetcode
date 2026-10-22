from lib.structures import TreeNode, build_tree

TITLE = "Balanced Binary Tree (균형 이진 트리 판별)"
LEVEL = "Easy"
SOURCE = "LeetCode 110"
PATTERN = "높이를 반환하되 불균형이면 -1 로 신호 보내기 (후위 순회)"

DESCRIPTION = """
이진 트리의 root 가 주어집니다.
모든 노드에서 '왼쪽 서브트리 높이'와 '오른쪽 서브트리 높이'의 차이가 1 이하이면 균형 트리입니다.
균형 트리이면 True, 아니면 False 를 return 하세요. 빈 트리는 균형 트리입니다.

트리는 레벨 순서 리스트로 표기합니다. 빈 자리는 None 입니다.

제한사항
- 0 ≤ 노드 개수 ≤ 5,000
- -10,000 ≤ 노드 값 ≤ 10,000

입출력 예
root = [3, 9, 20, None, None, 15, 7]     →  True
root = [1, 2, 2, 3, 3, None, None, 4, 4] →  False
root = []                                →  True
"""

SIGNATURE = "def solution(root: TreeNode) -> bool:"

IMPORTS = "from lib.structures import TreeNode"

HINTS = [
    "루트에서만 확인하면 안 됩니다. '모든' 노드에서 양쪽 높이 차이가 1 이하여야 합니다.",
    "위에서부터 각 노드의 양쪽 높이를 매번 새로 계산하면 같은 서브트리 높이를 반복 계산합니다 (최악 O(n^2)).",
    "아래에서 위로: 높이를 반환하는 함수를 만들되, 어느 서브트리라도 불균형이면 -1 을 반환해 위로 전파하세요. 최종 결과가 -1 이 아니면 균형.",
]

TESTS = [
    {"input": [[3, 9, 20, None, None, 15, 7]], "output": True},
    {"input": [[1, 2, 2, 3, 3, None, None, 4, 4]], "output": False},
    {"input": [[]], "output": True},
    {"input": [[1]], "output": True},
    {"input": [[1, 2, 2, 3, None, None, 3, 4, None, None, 4]], "output": False},
    {"input": [[1, None, 2, None, 3]], "output": False},
    {"input": [[1, 2, 3, 4]], "output": True},
    {"input": [[1, 2, 3, 4, 5, 6, None, 8]], "output": True},
]


def prepare(values):
    return [build_tree(values)]


EXPLANATION = """
핵심: 자식에게서 "높이"를 받아 차이를 확인합니다. 불균형을 발견하면 높이 대신 -1 이라는 특별한 값을 올려 보내
위쪽에서는 더 계산하지 않고 곧바로 -1 을 전달합니다 (조기 종료).

        1                 노드 2(왼쪽): 왼쪽 높이 2, 오른쪽 높이 0 → 차이 2 → -1 반환
       / \\                루트: 왼쪽이 -1 이므로 바로 -1 → False
      2   2
     /     \\              (루트 기준 양쪽 높이는 3 으로 같지만 균형이 아님!)
    3       3
   /         \\
  4           4

1. check(node): None 이면 0
2. L = check(left); L == -1 이면 -1
3. R = check(right); R == -1 이면 -1
4. |L - R| > 1 이면 -1, 아니면 1 + max(L, R)
5. check(root) != -1

시간 O(n), 공간 O(h)
면접 포인트: 위에서 아래로(top-down) 매번 높이를 구하는 brute_force 는 O(n log n)~O(n^2) 입니다.
"높이와 균형 여부를 한 번에 올려 보낸다"는 아이디어를 (balanced, height) 튜플로 구현해도 됩니다.
"""


def reference(root):
    def check(node):
        if node is None:
            return 0
        left = check(node.left)
        if left == -1:
            return -1           # 아래에서 이미 불균형 → 그대로 전파
        right = check(node.right)
        if right == -1:
            return -1
        if abs(left - right) > 1:
            return -1           # 이 노드에서 불균형
        return 1 + max(left, right)

    return check(root) != -1


def brute_force(root):
    # 위에서 아래로: 노드마다 높이를 새로 계산 (중복 계산)
    def height(node):
        return 0 if node is None else 1 + max(height(node.left), height(node.right))

    if root is None:
        return True
    if abs(height(root.left) - height(root.right)) > 1:
        return False
    return brute_force(root.left) and brute_force(root.right)
