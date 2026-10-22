from lib.structures import TreeNode, build_tree

TITLE = "Kth Smallest Element in a BST (BST 에서 k번째로 작은 값)"
LEVEL = "Medium"
SOURCE = "LeetCode 230"
PATTERN = "BST 중위 순회 = 오름차순, k 번째에서 멈추기"

DESCRIPTION = """
이진 탐색 트리(BST)의 root 와 정수 k 가 주어집니다.
트리의 모든 값 중 k 번째로 작은 값을 return 하세요. (k 는 1부터 셉니다)

트리는 레벨 순서 리스트로 표기합니다. 빈 자리는 None 입니다.

제한사항
- 1 ≤ k ≤ 노드 개수 ≤ 10,000
- 0 ≤ 노드 값 ≤ 10,000
- 트리는 올바른 BST 입니다 (값 중복 없음).

입출력 예
root = [3, 1, 4, None, 2],             k = 1  →  1
root = [5, 3, 6, 2, 4, None, None, 1], k = 3  →  3
"""

SIGNATURE = "def solution(root: TreeNode, k: int) -> int:"

IMPORTS = "from lib.structures import TreeNode"

HINTS = [
    "모든 값을 리스트에 모아 정렬하면 O(n log n) 입니다. BST 의 성질을 쓰면 정렬이 필요 없습니다.",
    "BST 를 중위 순회(왼쪽 → 나 → 오른쪽)하면 값이 오름차순으로 나옵니다.",
    "스택으로 반복 중위 순회를 하면서 노드를 '방문'할 때마다 k 를 1 줄이고, 0 이 되는 순간 그 값을 return 하세요. 전체를 돌 필요가 없습니다.",
]

TESTS = [
    {"input": [[3, 1, 4, None, 2], 1], "output": 1},
    {"input": [[5, 3, 6, 2, 4, None, None, 1], 3], "output": 3},
    {"input": [[1], 1], "output": 1},
    {"input": [[2, 1, 3], 3], "output": 3},
    {"input": [[5, 3, 6, 2, 4, None, None, 1], 6], "output": 6},
    {"input": [[4, 2, 6, 1, 3, 5, 7], 4], "output": 4},
    {"input": [[10, None, 20, None, 30, None, 40], 2], "output": 20},
]


def prepare(values, k):
    return [build_tree(values), k]


EXPLANATION = """
핵심: BST 의 중위 순회(in-order)는 정렬된 순서입니다. k 번째로 방문하는 노드가 정답입니다.

          5
         / \\          중위 순회: 1, 2, 3, 4, 5, 6
        3   6          k = 3 → 세 번째로 방문하는 3
       / \\
      2   4
     /
    1

반복 중위 순회 템플릿
1. cur = root, stack = []
2. cur 가 있는 동안 왼쪽으로 내려가며 stack 에 push
3. stack.pop() 으로 노드 방문 → k -= 1, k == 0 이면 return
4. cur = node.right 로 이동 후 2 반복

시간 O(h + k) (k 번째에서 멈추므로), 공간 O(h)
면접 포인트: 재귀로 전부 모은 뒤 [k-1] 을 고르는 풀이(alternative)는 O(n) 입니다.
후속 질문 "삽입/삭제가 잦고 k 번째 조회도 잦다면?" → 각 노드에 서브트리 크기를 저장하면
크기를 보고 왼쪽/오른쪽으로 내려가 O(h) 에 찾을 수 있습니다 (order-statistic tree).
"""


def reference(root, k):
    stack, cur = [], root
    while stack or cur:
        while cur:              # 가장 왼쪽(가장 작은 값)까지 내려가기
            stack.append(cur)
            cur = cur.left
        node = stack.pop()      # 다음으로 작은 값 방문
        k -= 1
        if k == 0:
            return node.val
        cur = node.right        # 오른쪽 서브트리에서 계속
    return -1


def alternative(root, k):
    # 재귀 중위 순회로 전부 모은 뒤 k-1 번째 선택
    values = []

    def inorder(node):
        if node:
            inorder(node.left)
            values.append(node.val)
            inorder(node.right)

    inorder(root)
    return values[k - 1]
