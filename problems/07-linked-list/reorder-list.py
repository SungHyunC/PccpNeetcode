import random

from lib.structures import ListNode, build_linked_list, linked_list_to_list

TITLE = "Reorder List (리스트 재배열)"
LEVEL = "Medium"
SOURCE = "LeetCode 143"
PATTERN = "중간 찾기 + 뒤 절반 뒤집기 + 번갈아 합치기"

DESCRIPTION = """
연결 리스트 L0 -> L1 -> ... -> L(n-1) 의 head 가 주어집니다.
노드를 다음 순서로 다시 연결한 뒤 head 를 return 하세요.

  L0 -> L(n-1) -> L1 -> L(n-2) -> L2 -> L(n-3) -> ...

즉 "맨 앞, 맨 뒤, 앞에서 두 번째, 뒤에서 두 번째, ..." 순서입니다.
노드의 값을 바꾸지 말고 연결(next)만 바꿔야 합니다.
(원래 LeetCode 문제는 in-place 로 바꾸고 아무것도 반환하지 않지만, 여기서는 head 를 return 합니다.)

제한사항
- 0 ≤ 노드 개수 ≤ 200,000
- 1 ≤ 노드 값 ≤ 1,000
- 효율성 테스트가 있습니다. O(n) 으로 풀어 보세요.

입출력 예
head = [1, 2, 3, 4]     →  [1, 4, 2, 3]
head = [1, 2, 3, 4, 5]  →  [1, 5, 2, 4, 3]
"""

SIGNATURE = "def solution(head: ListNode) -> ListNode:"

IMPORTS = "from lib.structures import ListNode"

HINTS = [
    "매번 끝 노드를 찾으러 리스트를 끝까지 걸어가면 O(n^2) 입니다. 뒤쪽 노드들을 '거꾸로' 접근할 방법이 필요합니다.",
    "가장 쉬운 방법: 노드들을 파이썬 리스트에 담고, 양쪽 끝에서 투 포인터로 번갈아 연결합니다 (공간 O(n)).",
    "O(1) 공간: (1) slow/fast 로 중간을 찾고 (2) 뒤 절반을 뒤집은 뒤 (3) 앞 절반과 뒤집힌 뒤 절반을 지퍼처럼 번갈아 연결합니다.",
    "앞 절반의 끝(slow).next = None 으로 끊는 것을 잊지 마세요. 끊지 않으면 사이클이 생깁니다.",
]

TESTS = [
    {"input": [[1, 2, 3, 4]], "output": [1, 4, 2, 3]},
    {"input": [[1, 2, 3, 4, 5]], "output": [1, 5, 2, 4, 3]},
    {"input": [[]], "output": []},
    {"input": [[1]], "output": [1]},
    {"input": [[1, 2]], "output": [1, 2]},
    {"input": [[1, 2, 3]], "output": [1, 3, 2]},
    {"input": [[5, 5, 7, 7, 9, 9]], "output": [5, 9, 5, 9, 7, 7]},
]


def prepare(values):
    return [build_linked_list(values)]


def present(head):
    if head is None or (hasattr(head, "val") and hasattr(head, "next")):
        return linked_list_to_list(head, limit=300_000)
    return head


PERF_LIMIT = 1.0


def perf_case():
    n = 200_000
    return {"input": [[random.randint(1, 1000) for _ in range(n)]], "output": None}


EXPLANATION = """
핵심: 결과는 "앞 절반"과 "거꾸로 된 뒤 절반"을 번갈아 끼운 것입니다.

  1 -> 2 -> 3 -> 4 -> 5
  ① 중간 찾기 (slow/fast)        앞: 1 -> 2 -> 3     뒤: 4 -> 5
  ② 뒤 절반 뒤집기               앞: 1 -> 2 -> 3     뒤: 5 -> 4
  ③ 번갈아 합치기                1 -> 5 -> 2 -> 4 -> 3

1. slow = head, fast = head.next 로 시작해 fast 가 끝날 때까지 slow 1칸, fast 2칸
   → slow 는 앞 절반의 마지막 노드 (홀수 길이면 앞 절반이 1개 더 많음)
2. second = slow.next, slow.next = None (반드시 끊기)
3. second 를 뒤집기 (Reverse Linked List)
4. first, second 를 번갈아 연결: first.next = second, second.next = 원래 first.next ...

시간 O(n), 공간 O(1)
면접 포인트: 세 가지 기본기(중간 찾기, 뒤집기, 병합)를 조합하는 문제입니다. 각 단계를 함수로 나눠 말하면 깔끔합니다.
노드 배열 + 투 포인터 풀이(공간 O(n))를 먼저 제시하고 O(1) 공간으로 개선하는 흐름도 좋습니다.
매번 꼬리를 찾는 O(n^2) 풀이는 효율성 테스트에서 실패합니다.
"""


def reference(head):
    if head is None or head.next is None:
        return head

    # 1) 중간 찾기: slow 가 앞 절반의 마지막 노드에서 멈춥니다
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # 2) 앞/뒤 절반 분리 후 뒤 절반 뒤집기
    second, slow.next = slow.next, None
    prev = None
    while second:
        second.next, prev, second = prev, second, second.next

    # 3) 번갈아 합치기: first 쪽이 길이가 같거나 1 더 깁니다
    first, second = head, prev
    while second:
        n1, n2 = first.next, second.next
        first.next = second
        second.next = n1
        first, second = n1, n2
    return head


def alternative(head):
    # 노드를 배열에 담고 양 끝에서 투 포인터 (공간 O(n))
    nodes = []
    while head:
        nodes.append(head)
        head = head.next
    if not nodes:
        return None
    i, j = 0, len(nodes) - 1
    while i < j:
        nodes[i].next = nodes[j]
        i += 1
        if i == j:
            break
        nodes[j].next = nodes[i]
        j -= 1
    nodes[i].next = None  # 마지막 노드에서 끊기
    return nodes[0]


def brute_force(head):
    # 매번 끝 노드를 찾아 떼어 와서 끼워 넣기: O(n^2) → 효율성 실패
    cur = head
    while cur and cur.next and cur.next.next:
        prev_tail = cur
        while prev_tail.next.next:
            prev_tail = prev_tail.next
        tail = prev_tail.next
        prev_tail.next = None
        tail.next = cur.next
        cur.next = tail
        cur = tail.next
    return head
