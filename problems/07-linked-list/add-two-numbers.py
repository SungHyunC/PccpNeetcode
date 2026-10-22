from lib.structures import ListNode, build_linked_list, linked_list_to_list

TITLE = "Add Two Numbers (두 수 더하기)"
LEVEL = "Medium"
SOURCE = "LeetCode 2"
PATTERN = "자릿수 덧셈 시뮬레이션 + 올림(carry) + 더미 노드"

DESCRIPTION = """
음이 아닌 정수 두 개가 연결 리스트 l1, l2 로 주어집니다.
각 노드에는 한 자리 숫자가 들어 있고, 일의 자리가 맨 앞에 오도록 '거꾸로' 저장되어 있습니다.
예) 342 는 [2, 4, 3] (2 -> 4 -> 3)

두 수의 합을 같은 방식(일의 자리부터)의 연결 리스트로 만들어 head 를 return 하세요.

제한사항
- 각 리스트의 노드 개수는 1 이상 100 이하
- 0 ≤ 노드 값 ≤ 9
- 수 0 자체를 제외하면 앞자리(리스트의 마지막 노드)가 0 인 경우는 없습니다.

입출력 예
l1 = [2, 4, 3], l2 = [5, 6, 4]  →  [7, 0, 8]     (342 + 465 = 807)
l1 = [0],       l2 = [0]        →  [0]
l1 = [9, 9, 9], l2 = [1]        →  [0, 0, 0, 1]  (999 + 1 = 1000)
"""

SIGNATURE = "def solution(l1: ListNode, l2: ListNode) -> ListNode:"

IMPORTS = "from lib.structures import ListNode"

HINTS = [
    "초등학교 세로셈과 같습니다. 일의 자리부터 더하면서 10 이상이면 올림(carry)을 다음 자리로 넘깁니다. 리스트가 이미 일의 자리부터 시작하니 순서가 딱 맞습니다.",
    "두 리스트의 길이가 다를 수 있습니다. 끝난 쪽은 0 으로 취급하세요.",
    "while l1 or l2 or carry: 로 돌면 마지막 올림(999 + 1 의 맨 앞 1)까지 자연스럽게 처리됩니다. total = a + b + carry, 새 노드 값은 total % 10, carry = total // 10.",
]

TESTS = [
    {"input": [[2, 4, 3], [5, 6, 4]], "output": [7, 0, 8]},
    {"input": [[0], [0]], "output": [0]},
    {"input": [[9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9]], "output": [8, 9, 9, 9, 0, 0, 0, 1]},
    {"input": [[9, 9, 9], [1]], "output": [0, 0, 0, 1]},
    {"input": [[5], [5]], "output": [0, 1]},
    {"input": [[1, 8], [0]], "output": [1, 8]},
    {"input": [[0], [3, 2, 1]], "output": [3, 2, 1]},
]


def prepare(l1, l2):
    return [build_linked_list(l1), build_linked_list(l2)]


def present(head):
    if head is None or (hasattr(head, "val") and hasattr(head, "next")):
        return linked_list_to_list(head)
    return head


EXPLANATION = """
핵심: 세로셈 시뮬레이션. 일의 자리부터 더하며 carry 를 넘깁니다.

    2 -> 4 -> 3      (342)
  + 5 -> 6 -> 4      (465)
  ---------------
    7 -> 0 -> 8      (807)   4+6 = 10 → 0 쓰고 carry 1 → 3+4+1 = 8

1. dummy = ListNode(), tail = dummy, carry = 0
2. while l1 or l2 or carry:
   - a = l1.val (없으면 0), b = l2.val (없으면 0)
   - carry, digit = divmod(a + b + carry, 10)
   - tail.next = ListNode(digit), tail 전진, l1 / l2 전진
3. dummy.next 를 return

시간 O(max(m, n)), 공간 O(max(m, n)) (결과 리스트)
면접 포인트: 루프 조건에 carry 를 넣는 것이 핵심입니다 (빠뜨리면 999 + 1 이 000 이 됩니다).
"정수로 바꿔 더한 뒤 다시 리스트로" 풀이는 파이썬에선 동작하지만, 자릿수가 100 이면 다른 언어에서는
64비트 정수를 넘으므로 면접에서는 시뮬레이션 풀이를 기대합니다.
후속 질문: 자릿수가 앞에서부터 저장되어 있다면? (LeetCode 445, 스택 또는 뒤집기 사용)
"""


def reference(l1, l2):
    dummy = ListNode()
    tail = dummy
    carry = 0
    while l1 or l2 or carry:
        a = l1.val if l1 else 0
        b = l2.val if l2 else 0
        carry, digit = divmod(a + b + carry, 10)
        tail.next = ListNode(digit)
        tail = tail.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next


def alternative(l1, l2):
    # 파이썬 큰 정수로 변환해서 더하기 (파이썬에서만 편한 방법)
    def to_int(node):
        num, place = 0, 1
        while node:
            num += node.val * place
            place *= 10
            node = node.next
        return num

    total = to_int(l1) + to_int(l2)
    dummy = tail = ListNode()
    for ch in reversed(str(total)):
        tail.next = ListNode(int(ch))
        tail = tail.next
    return dummy.next
