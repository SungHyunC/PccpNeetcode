from lib.structures import TreeNode, build_tree

TITLE = "Validate Binary Search Tree (이진 탐색 트리 검증)"
LEVEL = "Medium"
SOURCE = "LeetCode 98"
PATTERN = "허용 범위 (low, high) 를 내려보내는 DFS / 중위 순회가 증가하는지"

DESCRIPTION = """
이진 트리의 root 가 주어집니다. 이 트리가 올바른 이진 탐색 트리(BST)이면 True, 아니면 False 를 return 하세요.

올바른 BST 의 조건
- 어떤 노드의 왼쪽 서브트리에 있는 '모든' 값은 그 노드 값보다 작습니다.
- 어떤 노드의 오른쪽 서브트리에 있는 '모든' 값은 그 노드 값보다 큽니다.
- 왼쪽, 오른쪽 서브트리도 각각 BST 입니다.
- 같은 값은 허용하지 않습니다. 빈 트리는 BST 입니다.

트리는 레벨 순서 리스트로 표기합니다. 빈 자리는 None 입니다.

제한사항
- 0 ≤ 노드 개수 ≤ 10,000
- -2^31 ≤ 노드 값 ≤ 2^31 - 1

입출력 예
root = [2, 1, 3]                         →  True
root = [5, 1, 4, None, None, 3, 6]       →  False   (오른쪽 자식 4 가 5 보다 작음)
root = [5, 4, 6, None, None, 3, 7]       →  False   (3 은 6 의 왼쪽이지만 5 의 오른쪽 서브트리에 있음)
"""

SIGNATURE = "def solution(root: TreeNode) -> bool:"

IMPORTS = "from lib.structures import TreeNode"

HINTS = [
    "각 노드에서 '왼쪽 자식 < 나 < 오른쪽 자식' 만 확인하면 틀립니다. 세 번째 입출력 예처럼 손자 노드가 조상과의 조건을 깨뜨릴 수 있습니다.",
    "각 노드는 조상들이 정한 허용 범위 (low, high) 안에 있어야 합니다. 루트의 범위는 (-무한대, +무한대).",
    "왼쪽으로 내려갈 때는 high 를 현재 값으로, 오른쪽으로 내려갈 때는 low 를 현재 값으로 좁히세요. low < node.val < high 가 깨지면 False.",
    "다른 방법: BST 를 중위 순회(왼쪽 → 나 → 오른쪽)하면 값이 엄격하게 증가해야 합니다. 직전 값과 비교하세요.",
]

TESTS = [
    {"input": [[2, 1, 3]], "output": True},
    {"input": [[5, 1, 4, None, None, 3, 6]], "output": False},
    {"input": [[5, 4, 6, None, None, 3, 7]], "output": False},
    {"input": [[]], "output": True},
    {"input": [[1]], "output": True},
    {"input": [[1, 1]], "output": False},
    {"input": [[2, 2, 2]], "output": False},
    {"input": [[3, 1, 5, 0, 2, 4, 6]], "output": True},
    {"input": [[-2147483648, None, 2147483647]], "output": True},
    {"input": [[10, 5, 15, None, None, 6, 20]], "output": False},
]


def prepare(values):
    return [build_tree(values)]


EXPLANATION = """
핵심: BST 조건은 "부모와 자식"이 아니라 "조상 전체와 자손 전체" 사이의 조건입니다.
그래서 위에서 아래로 허용 범위 (low, high) 를 좁혀 가며 내려보냅니다.

            5   (-inf, inf)
           / \\
          4   6   (5, inf)
             / \\
            3   7
           (5, 6)  ← 3 은 이 범위 밖 → False

1. 스택(또는 재귀)에 (root, -inf, inf) 를 넣고 시작
2. 노드를 꺼내 low < val < high 인지 확인 (같으면 실패: 중복 불허)
3. 왼쪽 자식은 (low, val), 오른쪽 자식은 (val, high) 범위로 넣기
4. 끝까지 문제가 없으면 True

다른 풀이 (alternative): 중위 순회 결과가 엄격히 증가하는지 확인. 반복문 중위 순회 템플릿을 연습하기 좋습니다.

시간 O(n), 공간 O(h)
면접 포인트: 가장 흔한 오답은 "직속 자식만 비교"입니다. 반례 [5, 4, 6, None, None, 3, 7] 을 직접 그려 보세요.
경계값으로 float('-inf'), float('inf') 를 쓰면 정수 범위 끝 값(-2^31, 2^31-1) 도 안전하게 처리됩니다.
"""


def reference(root):
    # 반복 DFS: (노드, 허용 하한, 허용 상한)
    stack = [(root, float("-inf"), float("inf"))]
    while stack:
        node, low, high = stack.pop()
        if node is None:
            continue
        if not (low < node.val < high):
            return False
        stack.append((node.left, low, node.val))    # 왼쪽은 나보다 작아야 함
        stack.append((node.right, node.val, high))  # 오른쪽은 나보다 커야 함
    return True


def alternative(root):
    # 반복 중위 순회: 값이 엄격하게 증가해야 BST
    stack, cur, prev = [], root, None
    while stack or cur:
        while cur:              # 왼쪽 끝까지 내려가며 쌓기
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()       # 방문 (중위)
        if prev is not None and cur.val <= prev:
            return False
        prev = cur.val
        cur = cur.right
    return True
