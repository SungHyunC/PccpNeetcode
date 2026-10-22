from lib.structures import ListNode, build_linked_list, linked_list_to_list

TITLE = "Merge Two Sorted Lists (정렬된 두 리스트 합치기)"
LEVEL = "Easy"
SOURCE = "LeetCode 21"
PATTERN = "더미 노드(dummy) + 두 포인터로 작은 쪽 이어 붙이기"

DESCRIPTION = """
오름차순으로 정렬된 단방향 연결 리스트 두 개 list1, list2 의 head 가 주어집니다.
두 리스트의 노드를 이어 붙여 오름차순으로 정렬된 하나의 리스트를 만들고, 그 head 를 return 하세요.
새 노드를 만들기보다 기존 노드를 재사용하는 것이 좋습니다.

리스트는 [1, 2, 4] 처럼 표기합니다 (1 -> 2 -> 4). [] 는 빈 리스트(None)입니다.

제한사항
- 각 리스트의 노드 개수는 0 이상 50 이하
- -100 ≤ 노드 값 ≤ 100
- 두 리스트 모두 오름차순(같은 값 허용)으로 정렬되어 있습니다.

입출력 예
list1 = [1, 2, 4], list2 = [1, 3, 4]  →  [1, 1, 2, 3, 4, 4]
list1 = [],        list2 = []         →  []
list1 = [],        list2 = [0]        →  [0]
"""

SIGNATURE = "def solution(list1: ListNode, list2: ListNode) -> ListNode:"

IMPORTS = "from lib.structures import ListNode"

HINTS = [
    "두 리스트의 맨 앞 노드 중 더 작은 것이 결과의 다음 노드가 됩니다. 병합 정렬(merge sort)의 merge 단계와 같습니다.",
    "결과 리스트의 첫 노드를 따로 처리하기 귀찮다면, 가짜 시작 노드 dummy = ListNode() 를 만들고 tail 포인터로 뒤에 붙여 나가세요.",
    "while list1 and list2: 작은 쪽을 tail.next 에 붙이고 그 리스트를 한 칸 전진. 루프가 끝나면 남은 리스트를 통째로 tail.next 에 붙이고 dummy.next 를 return.",
]

TESTS = [
    {"input": [[1, 2, 4], [1, 3, 4]], "output": [1, 1, 2, 3, 4, 4]},
    {"input": [[], []], "output": []},
    {"input": [[], [0]], "output": [0]},
    {"input": [[5], []], "output": [5]},
    {"input": [[1, 1, 1], [1, 1]], "output": [1, 1, 1, 1, 1]},
    {"input": [[-100, -3, 50], [-50, 0, 100]], "output": [-100, -50, -3, 0, 50, 100]},
    {"input": [[1, 2, 3], [7, 8, 9, 10]], "output": [1, 2, 3, 7, 8, 9, 10]},
]


def prepare(list1, list2):
    return [build_linked_list(list1), build_linked_list(list2)]


def present(head):
    if head is None or (hasattr(head, "val") and hasattr(head, "next")):
        return linked_list_to_list(head)
    return head


EXPLANATION = """
핵심: 병합 정렬의 merge 단계. 두 리스트의 앞쪽 노드끼리 비교해 작은 것을 결과 끝에 붙입니다.

1. dummy = ListNode(), tail = dummy  (결과 리스트의 '앞에 붙은 가짜 노드')
2. 둘 다 남아 있는 동안: 작은 쪽 노드를 tail.next 에 붙이고, 그 리스트와 tail 을 한 칸 전진
3. 한쪽이 끝나면 남은 쪽은 이미 정렬되어 있으므로 tail.next = 남은 리스트
4. dummy.next 를 return

  dummy -> 1(a) -> 1(b) -> 2(a) -> 3(b) -> 4(a) -> [남은 4(b)]

시간 O(n + m), 공간 O(1) (노드를 재사용)
면접 포인트: dummy 노드를 쓰면 "결과가 비어 있을 때"와 "첫 노드 결정" 같은 경계 처리가 사라집니다.
같은 값일 때 list1 을 먼저 붙이면(<=) 안정 정렬(stable)이 됩니다.
이 함수는 Merge K Sorted Lists, Sort List(연결 리스트 병합 정렬)의 부품입니다.
"""


def reference(list1, list2):
    dummy = ListNode()
    tail = dummy
    while list1 and list2:
        if list1.val <= list2.val:   # 같으면 list1 먼저 → 안정적
            tail.next, list1 = list1, list1.next
        else:
            tail.next, list2 = list2, list2.next
        tail = tail.next
    tail.next = list1 if list1 else list2  # 남은 꼬리를 통째로 연결
    return dummy.next


def alternative(list1, list2):
    # 재귀 풀이: 더 작은 head 를 고르고, 그 뒤는 나머지끼리 합친 결과
    if list1 is None:
        return list2
    if list2 is None:
        return list1
    if list1.val <= list2.val:
        list1.next = alternative(list1.next, list2)
        return list1
    list2.next = alternative(list1, list2.next)
    return list2
