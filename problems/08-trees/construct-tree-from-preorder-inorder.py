from lib.structures import TreeNode, tree_to_list

TITLE = "Construct Binary Tree from Preorder and Inorder Traversal (전위·중위 순회로 트리 복원)"
LEVEL = "Medium"
SOURCE = "LeetCode 105"
PATTERN = "전위의 첫 값 = 루트, 중위에서 루트 위치로 왼쪽/오른쪽 분할"

DESCRIPTION = """
어떤 이진 트리를 전위 순회(preorder: 나 → 왼쪽 → 오른쪽)한 결과와
중위 순회(inorder: 왼쪽 → 나 → 오른쪽)한 결과가 주어집니다.
원래 트리를 복원해 root 를 return 하세요. 채점기는 반환한 트리를 레벨 순서 리스트로 바꿔 비교합니다.

제한사항
- 0 ≤ len(preorder) = len(inorder) ≤ 3,000
- -3,000 ≤ 노드 값 ≤ 3,000
- 노드 값은 모두 다릅니다.
- 두 배열은 같은 트리에서 나온 올바른 순회 결과입니다.

입출력 예
preorder = [3, 9, 20, 15, 7], inorder = [9, 3, 15, 20, 7]  →  [3, 9, 20, None, None, 15, 7]
preorder = [-1],              inorder = [-1]               →  [-1]
preorder = [],                inorder = []                 →  []
"""

SIGNATURE = "def solution(preorder: list[int], inorder: list[int]) -> TreeNode:"

IMPORTS = "from lib.structures import TreeNode"

HINTS = [
    "전위 순회의 첫 값은 항상 루트입니다.",
    "중위 순회에서 루트의 위치를 찾으면, 그 왼쪽은 왼쪽 서브트리, 오른쪽은 오른쪽 서브트리의 중위 순회입니다. 왼쪽 서브트리의 크기도 알 수 있습니다.",
    "슬라이싱 + inorder.index() 는 매번 O(n) 이라 최악 O(n^2) 입니다. {값: 중위 인덱스} dict 를 미리 만들고, 인덱스 범위만 넘기는 재귀로 바꾸세요.",
    "전위 순회를 앞에서부터 하나씩 꺼내 쓰는 포인터(pre_idx)를 두고, build(lo, hi) 가 inorder[lo..hi] 범위의 서브트리를 만들게 하면 왼쪽을 먼저 만들기만 하면 순서가 맞습니다.",
]

TESTS = [
    {"input": [[3, 9, 20, 15, 7], [9, 3, 15, 20, 7]], "output": [3, 9, 20, None, None, 15, 7]},
    {"input": [[-1], [-1]], "output": [-1]},
    {"input": [[], []], "output": []},
    {"input": [[1, 2], [2, 1]], "output": [1, 2]},
    {"input": [[1, 2], [1, 2]], "output": [1, None, 2]},
    {"input": [[1, 2, 3], [3, 2, 1]], "output": [1, 2, None, 3]},
    {"input": [[1, 2, 4, 5, 3, 6, 7], [4, 2, 5, 1, 6, 3, 7]], "output": [1, 2, 3, 4, 5, 6, 7]},
]


def present(root):
    if root is None or (hasattr(root, "left") and hasattr(root, "right")):
        return tree_to_list(root)
    return root


EXPLANATION = """
핵심: 전위 순회는 "루트가 누구인지", 중위 순회는 "누가 왼쪽이고 누가 오른쪽인지"를 알려 줍니다.

  preorder = [3 | 9 | 20, 15, 7]     inorder = [9 | 3 | 15, 20, 7]
              루트  왼   오른                    왼  루트  오른

  → 루트 3, 왼쪽 서브트리 {9}, 오른쪽 서브트리 {15, 20, 7} 을 같은 방법으로 재귀 복원

1. pos = {값: inorder 인덱스} 를 미리 만들기 (O(1) 로 루트 위치 찾기)
2. pre_idx = 0 (전위 순회에서 다음에 쓸 루트)
3. build(lo, hi): inorder[lo..hi] 범위로 서브트리를 만듦
   - lo > hi 이면 None
   - val = preorder[pre_idx], pre_idx += 1, mid = pos[val]
   - node.left = build(lo, mid - 1)   ← 전위 순서상 왼쪽을 먼저!
   - node.right = build(mid + 1, hi)
4. build(0, n - 1)

시간 O(n), 공간 O(n) (dict + 재귀 스택 O(h))
면접 포인트: 슬라이싱 풀이(brute_force)도 정답이지만 O(n^2) 입니다. dict + 인덱스 범위로 개선하는 과정을 말해 보세요.
값이 중복되면 루트 위치가 모호해져 복원할 수 없다는 점도 짚을 수 있으면 좋습니다.
치우친 트리면 재귀 깊이가 n 이 되므로 setrecursionlimit 을 늘려 둡니다.
비슷한 문제: 중위 + 후위로 복원(LeetCode 106) — 후위의 마지막 값이 루트, 오른쪽부터 만듭니다.
"""


def reference(preorder, inorder):
    import sys
    sys.setrecursionlimit(10_000)

    pos = {v: i for i, v in enumerate(inorder)}  # 값 → 중위 인덱스
    pre_idx = 0

    def build(lo, hi):
        nonlocal pre_idx
        if lo > hi:
            return None
        val = preorder[pre_idx]   # 전위 순서상 다음 값이 이 서브트리의 루트
        pre_idx += 1
        mid = pos[val]
        node = TreeNode(val)
        node.left = build(lo, mid - 1)    # 왼쪽 먼저 (전위 순서)
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(inorder) - 1)


def brute_force(preorder, inorder):
    # 슬라이싱 + index(): 직관적이지만 O(n^2)
    if not preorder:
        return None
    root = TreeNode(preorder[0])
    mid = inorder.index(preorder[0])  # 왼쪽 서브트리 크기
    root.left = brute_force(preorder[1:mid + 1], inorder[:mid])
    root.right = brute_force(preorder[mid + 1:], inorder[mid + 1:])
    return root
