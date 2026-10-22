from lib.structures import ListNode, build_linked_list, linked_list_to_list

TITLE = "Remove Nth Node From End of List (뒤에서 n번째 노드 삭제)"
LEVEL = "Medium"
SOURCE = "LeetCode 19"
PATTERN = "n칸 간격을 둔 두 포인터 + 더미 노드"

DESCRIPTION = """
연결 리스트의 head 와 정수 n 이 주어집니다.
리스트의 끝에서부터 세어 n 번째 노드를 삭제한 뒤 head 를 return 하세요.
(마지막 노드가 끝에서 1번째입니다.)

제한사항
- 1 ≤ 노드 개수 sz ≤ 30
- 0 ≤ 노드 값 ≤ 100
- 1 ≤ n ≤ sz
- 리스트를 한 번만 훑어서(one pass) 풀 수 있는지 생각해 보세요.

입출력 예
head = [1, 2, 3, 4, 5], n = 2  →  [1, 2, 3, 5]
head = [1],             n = 1  →  []
head = [1, 2],          n = 1  →  [1]
"""

SIGNATURE = "def solution(head: ListNode, n: int) -> ListNode:"

IMPORTS = "from lib.structures import ListNode"

HINTS = [
    "두 번 훑는 방법: 먼저 길이 L 을 세고, 앞에서 (L - n) 번째 노드(삭제할 노드의 바로 앞)를 찾아 건너뛰게 연결합니다.",
    "첫 노드를 지워야 하는 경우(n == 길이)가 까다롭습니다. head 앞에 dummy 노드를 두면 이 경우도 똑같이 처리됩니다.",
    "한 번에 훑기: fast 를 먼저 n 칸 보낸 뒤 slow 와 fast 를 함께 움직입니다. fast 가 마지막 노드에 닿으면 slow 는 삭제할 노드의 바로 앞입니다.",
]

TESTS = [
    {"input": [[1, 2, 3, 4, 5], 2], "output": [1, 2, 3, 5]},
    {"input": [[1], 1], "output": []},
    {"input": [[1, 2], 1], "output": [1]},
    {"input": [[1, 2], 2], "output": [2]},
    {"input": [[1, 2, 3], 3], "output": [2, 3]},
    {"input": [[10, 20, 30, 40], 1], "output": [10, 20, 30]},
    {"input": [[7, 7, 7, 7, 7], 3], "output": [7, 7, 7, 7]},
]


def prepare(values, n):
    return [build_linked_list(values), n]


def present(head):
    if head is None or (hasattr(head, "val") and hasattr(head, "next")):
        return linked_list_to_list(head)
    return head


EXPLANATION = """
핵심: 두 포인터 사이 간격을 n 으로 유지하면, 앞 포인터가 끝에 닿을 때 뒤 포인터는 끝에서 n 번째 근처에 있습니다.

1. dummy -> head 를 만들고 slow = fast = dummy
2. fast 를 n 칸 먼저 이동
3. fast.next 가 None 이 될 때까지 slow, fast 를 함께 1칸씩 이동
   → slow.next 가 삭제 대상
4. slow.next = slow.next.next, dummy.next 를 return

  n = 2:  dummy  1  2  3  4  5
          s         f                (fast 를 2칸 먼저)
                   s        f        (fast.next 가 None 일 때까지 함께)
          → slow=3, 3.next(=4) 삭제 → 1 2 3 5

시간 O(L), 공간 O(1)
면접 포인트: dummy 노드는 "head 자체가 삭제되는 경우"를 없애 줍니다. 두 번 훑기(길이 세기)도 O(L) 이므로
"one pass 가 꼭 더 빠른가?" 라는 질문에는 "점근적으로는 같고, 순회 횟수만 줄어든다"고 답하면 됩니다.
"""


def reference(head, n):
    dummy = ListNode(0, head)
    slow = fast = dummy
    for _ in range(n):          # fast 를 n 칸 앞서 보냄
        fast = fast.next
    while fast.next:            # fast 가 마지막 노드에 닿을 때까지
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next  # slow 다음 노드(뒤에서 n번째)를 건너뜀
    return dummy.next


def alternative(head, n):
    # 두 번 훑기: 길이를 센 뒤 앞에서 (L - n) 번째 노드 다음을 삭제
    length, cur = 0, head
    while cur:
        length += 1
        cur = cur.next
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(length - n):
        prev = prev.next
    prev.next = prev.next.next
    return dummy.next
