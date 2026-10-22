from lib.structures import ListNode, build_linked_list, linked_list_to_list

TITLE = "Reverse Linked List (연결 리스트 뒤집기)"
LEVEL = "Easy"
SOURCE = "LeetCode 206"
PATTERN = "prev / cur / nxt 세 포인터로 링크 방향 바꾸기"

DESCRIPTION = """
단방향 연결 리스트의 첫 노드 head 가 주어집니다.
노드들의 연결 방향을 모두 반대로 바꾼 뒤, 새 첫 노드를 return 하세요.
(새 노드를 만들지 말고 기존 노드의 next 만 바꾸는 것이 목표입니다.)

입력/출력은 채점 편의를 위해 리스트로 표기합니다. [1, 2, 3] 은 1 -> 2 -> 3 을 뜻합니다.
빈 리스트([])는 head 가 None 인 경우입니다.

제한사항
- 0 ≤ 노드 개수 ≤ 5,000
- -5,000 ≤ 노드 값 ≤ 5,000

입출력 예
head = [1, 2, 3, 4, 5]  →  [5, 4, 3, 2, 1]
head = [1, 2]           →  [2, 1]
head = []               →  []
"""

SIGNATURE = "def solution(head: ListNode) -> ListNode:"

IMPORTS = "from lib.structures import ListNode"

HINTS = [
    "값을 리스트에 모아 뒤집은 뒤 새 리스트를 만들 수도 있지만, O(1) 추가 공간으로 노드의 next 만 바꿀 수 있습니다.",
    "cur.next 를 이전 노드로 바꾸는 순간 원래 다음 노드를 잃어버립니다. 바꾸기 전에 nxt = cur.next 로 저장해 두세요.",
    "prev = None, cur = head 에서 시작해 반복: nxt = cur.next → cur.next = prev → prev = cur → cur = nxt. 끝나면 prev 가 새 head 입니다.",
]

TESTS = [
    {"input": [[1, 2, 3, 4, 5]], "output": [5, 4, 3, 2, 1]},
    {"input": [[1, 2]], "output": [2, 1]},
    {"input": [[]], "output": []},
    {"input": [[7]], "output": [7]},
    {"input": [[3, 3, -1, 3]], "output": [3, -1, 3, 3]},
    {"input": [[-5000, 0, 5000]], "output": [5000, 0, -5000]},
]


def prepare(values):
    return [build_linked_list(values)]


def present(head):
    # ListNode → 리스트 (None 이면 []). 다른 타입은 그대로 둬서 오답으로 보이게 합니다.
    if head is None or (hasattr(head, "val") and hasattr(head, "next")):
        return linked_list_to_list(head)
    return head


EXPLANATION = """
핵심: 각 노드의 화살표(next)를 하나씩 반대로 돌립니다. 돌리기 전에 다음 노드를 저장해 두는 것이 전부입니다.

1. prev = None, cur = head
2. cur 가 None 이 될 때까지
   - nxt = cur.next      (다음 노드 기억)
   - cur.next = prev     (화살표 뒤집기)
   - prev, cur = cur, nxt (한 칸 전진)
3. prev 가 새 head

  None   1 -> 2 -> 3        prev=None, cur=1
  None <- 1    2 -> 3       prev=1,    cur=2
  None <- 1 <- 2    3       prev=2,    cur=3
  None <- 1 <- 2 <- 3       prev=3,    cur=None → return 3

시간 O(n), 공간 O(1)
면접 포인트: 반복(iterative)과 재귀(recursive) 두 가지를 모두 설명할 수 있어야 합니다.
재귀는 공간 O(n)(호출 스택)이고, 파이썬 기본 재귀 한도(약 1000) 때문에 긴 리스트에서는 RecursionError 가 납니다.
이 연산은 Reorder List, Palindrome Linked List, Reverse Nodes in k-Group 의 부품으로 자주 쓰입니다.
"""


def reference(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next      # 1) 다음 노드를 잃어버리지 않게 저장
        cur.next = prev     # 2) 화살표 방향 뒤집기
        prev, cur = cur, nxt  # 3) 한 칸 전진
    return prev             # cur 가 None 일 때 prev 가 마지막(=새 첫) 노드


def alternative(head):
    # 재귀 풀이: "head.next 이후를 뒤집은 결과"의 끝에 head 를 붙입니다.
    if head is None or head.next is None:
        return head
    new_head = alternative(head.next)
    head.next.next = head   # 내 다음 노드가 나를 가리키게
    head.next = None        # 사이클 방지
    return new_head
