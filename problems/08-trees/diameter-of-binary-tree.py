from lib.structures import TreeNode, build_tree

TITLE = "Diameter of Binary Tree (이진 트리의 지름)"
LEVEL = "Easy"
SOURCE = "LeetCode 543"
PATTERN = "높이는 위로 반환, 지름은 바깥 변수로 갱신 (후위 순회)"

DESCRIPTION = """
이진 트리의 root 가 주어집니다.
트리에서 두 노드를 잇는 경로 중 가장 긴 경로의 길이(간선 개수)를 return 하세요.
이 경로는 루트를 지나지 않을 수도 있습니다. 빈 트리와 노드가 1개인 트리의 지름은 0 입니다.

트리는 레벨 순서 리스트로 표기합니다. 빈 자리는 None 입니다.

제한사항
- 0 ≤ 노드 개수 ≤ 10,000
- -100 ≤ 노드 값 ≤ 100

입출력 예
root = [1, 2, 3, 4, 5]  →  3    (4 - 2 - 1 - 3 또는 5 - 2 - 1 - 3)
root = [1, 2]           →  1
"""

SIGNATURE = "def solution(root: TreeNode) -> int:"

IMPORTS = "from lib.structures import TreeNode"

HINTS = [
    "가장 긴 경로에는 '가장 높은 위치의 노드(꺾이는 지점)'가 하나 있습니다. 그 노드를 기준으로 경로 길이 = 왼쪽 높이 + 오른쪽 높이 입니다.",
    "모든 노드를 꺾이는 지점 후보로 보고 왼쪽 높이 + 오른쪽 높이의 최댓값을 구하면 됩니다. 그런데 노드마다 높이를 새로 계산하면 O(n^2) 입니다.",
    "후위 순회로 높이를 반환하면서, 그 과정에서 left_h + right_h 로 정답 변수를 갱신하세요. 반환값(높이)과 정답(지름)이 다르다는 점이 핵심입니다.",
]

TESTS = [
    {"input": [[1, 2, 3, 4, 5]], "output": 3},
    {"input": [[1, 2]], "output": 1},
    {"input": [[1]], "output": 0},
    {"input": [[]], "output": 0},
    {"input": [[1, 2, None, 3, 4, 5, None, None, 6]], "output": 4},
    {"input": [[1, None, 2, None, 3, None, 4]], "output": 3},
    {"input": [[1, 2, 3, 4, 5, 6, 7, 8, None, None, None, None, None, None, 9]], "output": 6},
]


def prepare(values):
    return [build_tree(values)]


EXPLANATION = """
핵심: 재귀 함수가 "반환하는 값"과 "구하려는 답"이 다른 대표 문제입니다.
- 반환값: 이 노드에서 아래로 내려가는 가장 긴 경로의 높이 (부모가 이어 붙일 수 있는 정보)
- 갱신값: 이 노드에서 꺾이는 경로 길이 = 왼쪽 높이 + 오른쪽 높이 (부모에게는 못 올려 보냄)

          1
         /          노드 2 에서: 왼쪽 높이 2 (3-5), 오른쪽 높이 2 (4-6)
        2           → 이 노드에서 꺾이는 경로 5-3-2-4-6 = 4
       / \\          노드 1 에서: 왼쪽 높이 3, 오른쪽 0 → 3
      3   4         답 = 4 (루트를 지나지 않음)
     /     \\
    5       6

1. best = 0
2. height(node): None 이면 0. L = height(left), R = height(right)
   best = max(best, L + R), return 1 + max(L, R)
3. height(root) 호출 후 best 반환

시간 O(n), 공간 O(h)
면접 포인트: 노드마다 높이를 다시 구하는 brute_force 는 O(n^2) (치우친 트리에서) 입니다.
"자식에게서 정보를 받아 내 답을 갱신하고, 부모에게는 이어 붙일 수 있는 정보만 올린다" 패턴은
Binary Tree Maximum Path Sum, Longest Univalue Path 와 같은 구조입니다.
"""


def reference(root):
    best = 0

    def height(node):
        nonlocal best
        if node is None:
            return 0
        left, right = height(node.left), height(node.right)
        best = max(best, left + right)   # 이 노드에서 꺾이는 경로 (간선 수)
        return 1 + max(left, right)      # 부모에게는 한쪽 가지만 올려 보냄

    height(root)
    return best


def brute_force(root):
    # 모든 노드에서 높이를 새로 계산: O(n^2)
    def height(node):
        return 0 if node is None else 1 + max(height(node.left), height(node.right))

    if root is None:
        return 0
    through_here = height(root.left) + height(root.right)
    return max(through_here, brute_force(root.left), brute_force(root.right))
