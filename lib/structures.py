"""연결 리스트 / 이진 트리 문제에서 쓰는 공용 자료구조와 변환 헬퍼.

LeetCode와 같은 표기법을 씁니다.
- 연결 리스트: [1, 2, 3]  ->  1 -> 2 -> 3
- 이진 트리:   [3, 9, 20, None, None, 15, 7]  (레벨 순서, 빈 자리는 None)
"""
from collections import deque
from typing import List, Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({linked_list_to_list(self)})"


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({tree_to_list(self)})"


def build_linked_list(values: List) -> Optional[ListNode]:
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def linked_list_to_list(head: Optional[ListNode], limit: int = 10_000) -> List:
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
        if len(out) > limit:  # 사이클이 생긴 리스트를 출력하다 멈추지 않도록
            out.append("...cycle?")
            break
    return out


def build_tree(values: List) -> Optional[TreeNode]:
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    while q and i < len(values):
        node = q.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            q.append(node.right)
        i += 1
    return root


def tree_to_list(root: Optional[TreeNode]) -> List:
    if root is None:
        return []
    out, q = [], deque([root])
    while q:
        node = q.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        q.append(node.left)
        q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def find_node(root: Optional[TreeNode], val) -> Optional[TreeNode]:
    """트리에서 값이 val인 노드를 찾습니다 (LCA 같은 문제의 입력 변환용)."""
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        if node.val == val:
            return node
        stack.append(node.left)
        stack.append(node.right)
    return None
