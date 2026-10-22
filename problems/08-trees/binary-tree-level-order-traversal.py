from collections import deque

from lib.structures import TreeNode, build_tree

TITLE = "Binary Tree Level Order Traversal (이진 트리 레벨 순회)"
LEVEL = "Medium"
SOURCE = "LeetCode 102"
PATTERN = "BFS + 레벨 크기만큼 꺼내기"

DESCRIPTION = """
이진 트리의 root 가 주어집니다.
같은 깊이(레벨)에 있는 노드의 값들을 왼쪽에서 오른쪽 순서로 리스트에 담고,
루트 레벨부터 차례대로 그 리스트들을 모아 return 하세요. 빈 트리는 [] 입니다.

트리는 레벨 순서 리스트로 표기합니다. 빈 자리는 None 입니다.

제한사항
- 0 ≤ 노드 개수 ≤ 2,000
- -1,000 ≤ 노드 값 ≤ 1,000

입출력 예
root = [3, 9, 20, None, None, 15, 7]  →  [[3], [9, 20], [15, 7]]
root = [1]                            →  [[1]]
root = []                             →  []
"""

SIGNATURE = "def solution(root: TreeNode) -> list[list[int]]:"

IMPORTS = "from lib.structures import TreeNode"

HINTS = [
    "가까운 노드부터 차례로 방문하는 탐색은 BFS 입니다. collections.deque 를 큐로 쓰세요.",
    "큐에는 여러 레벨의 노드가 섞일 수 있습니다. 레벨을 구분하려면 '지금 큐에 들어 있는 노드 수'를 먼저 저장하세요.",
    "while q: size = len(q) → size 번만 popleft 하며 값을 level 리스트에 담고 자식을 append → level 을 결과에 추가.",
]

TESTS = [
    {"input": [[3, 9, 20, None, None, 15, 7]], "output": [[3], [9, 20], [15, 7]]},
    {"input": [[1]], "output": [[1]]},
    {"input": [[]], "output": []},
    {"input": [[1, 2, 3, 4, None, None, 5]], "output": [[1], [2, 3], [4, 5]]},
    {"input": [[1, None, 2, None, 3]], "output": [[1], [2], [3]]},
    {"input": [[0, -1, -2, -3]], "output": [[0], [-1, -2], [-3]]},
    {"input": [[1, 2, 3, 4, 5, 6, 7]], "output": [[1], [2, 3], [4, 5, 6, 7]]},
]


def prepare(values):
    return [build_tree(values)]


EXPLANATION = """
핵심: BFS 에서 "한 번에 한 레벨씩" 처리하는 방법. 레벨을 시작할 때 큐 길이가 곧 그 레벨의 노드 수입니다.

  큐: [3]          size=1 → [3]        자식 9, 20 추가
  큐: [9, 20]      size=2 → [9, 20]    자식 15, 7 추가
  큐: [15, 7]      size=2 → [15, 7]
  큐: []           종료

1. root 가 None 이면 []
2. q = deque([root])
3. while q: size = len(q), level = []
   size 번: node = q.popleft(), level.append(node.val), 자식이 있으면 q.append
   result.append(level)

시간 O(n), 공간 O(w) (w = 가장 넓은 레벨의 노드 수, 최대 약 n/2)
면접 포인트: 레벨 단위 BFS 는 Right Side View, Zigzag Level Order, 레벨별 평균/최댓값,
Minimum Depth, 최단 거리 문제(→ 그래프 BFS)의 기본 틀입니다.
DFS 로 (노드, 깊이) 를 넘기며 result[depth] 에 append 해도 같은 결과가 나옵니다 (alternative).
list.pop(0) 은 O(n) 이므로 반드시 deque.popleft() 를 쓰세요.
"""


def reference(root):
    if root is None:
        return []
    result, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):  # 이번 레벨의 노드 수만큼만
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        result.append(level)
    return result


def alternative(root):
    # DFS(전위 순회) + 깊이: 왼쪽을 먼저 방문하므로 각 레벨 안의 순서가 유지됩니다
    result = []
    stack = [(root, 0)] if root else []
    while stack:
        node, depth = stack.pop()
        if depth == len(result):
            result.append([])
        result[depth].append(node.val)
        # 스택은 LIFO 이므로 오른쪽을 먼저 넣어야 왼쪽이 먼저 나옵니다
        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))
    return result
