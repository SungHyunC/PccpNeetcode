import heapq
import random

from lib.structures import ListNode, build_linked_list, linked_list_to_list

TITLE = "Merge K Sorted Lists (정렬된 K개 리스트 합치기)"
LEVEL = "Hard"
SOURCE = "LeetCode 23"
PATTERN = "최소 힙에 각 리스트의 head 를 넣고 하나씩 꺼내기"

DESCRIPTION = """
오름차순으로 정렬된 연결 리스트 k 개가 담긴 배열 lists 가 주어집니다.
모든 리스트를 합쳐 오름차순으로 정렬된 하나의 연결 리스트를 만들고 head 를 return 하세요.

입력은 [[1, 4, 5], [1, 3, 4], [2, 6]] 처럼 리스트들의 리스트로 표기하며,
solution 에는 각 원소가 ListNode(head) 로 변환된 파이썬 리스트가 전달됩니다. 빈 리스트는 None 입니다.

제한사항
- 0 ≤ k ≤ 10,000
- 모든 노드 개수의 합 N ≤ 100,000
- -10,000 ≤ 노드 값 ≤ 10,000
- 각 리스트는 오름차순으로 정렬되어 있습니다.
- 효율성 테스트가 있습니다 (리스트를 하나씩 차례로 합치면 O(kN) 으로 느립니다).

입출력 예
lists = [[1, 4, 5], [1, 3, 4], [2, 6]]  →  [1, 1, 2, 3, 4, 4, 5, 6]
lists = []                              →  []
lists = [[]]                            →  []
"""

SIGNATURE = "def solution(lists: list[ListNode]) -> ListNode:"

IMPORTS = "from lib.structures import ListNode"

HINTS = [
    "Merge Two Sorted Lists 를 k-1 번 반복하면 앞쪽 결과가 계속 길어져서 O(kN) 입니다. k = 1,000, N = 100,000 이면 너무 느립니다.",
    "매 순간 결과의 다음 노드는 'k 개 리스트의 현재 맨 앞 노드들 중 최솟값' 입니다. 최솟값을 빠르게 반복해서 꺼내는 자료구조는?",
    "heapq 에 (값, 리스트 번호, 노드) 를 넣으세요. ListNode 끼리는 < 비교가 안 되므로, 값이 같을 때를 대비해 고유한 번호를 두 번째 원소로 둡니다.",
    "꺼낸 노드를 결과 끝에 붙이고, 그 노드의 next 가 있으면 다시 힙에 넣습니다. 힙 크기는 항상 k 이하 → O(N log k).",
]

TESTS = [
    {"input": [[[1, 4, 5], [1, 3, 4], [2, 6]]], "output": [1, 1, 2, 3, 4, 4, 5, 6]},
    {"input": [[]], "output": []},
    {"input": [[[]]], "output": []},
    {"input": [[[], [1]]], "output": [1]},
    {"input": [[[-10, -5, 0], [], [-7, 3], [10000]]], "output": [-10, -7, -5, 0, 3, 10000]},
    {"input": [[[2, 2], [2], [1, 2]]], "output": [1, 2, 2, 2, 2]},
    {"input": [[[1, 2, 3, 4, 5]]], "output": [1, 2, 3, 4, 5]},
]


def prepare(lists):
    return [[build_linked_list(v) for v in lists]]


def present(head):
    if head is None or (hasattr(head, "val") and hasattr(head, "next")):
        return linked_list_to_list(head, limit=200_000)
    return head


PERF_LIMIT = 1.0


def perf_case():
    k, size = 1_000, 100
    lists = [sorted(random.randint(-10_000, 10_000) for _ in range(size)) for _ in range(k)]
    return {"input": [lists], "output": None}


EXPLANATION = """
핵심: k 개 리스트의 "현재 맨 앞" 중 최솟값을 반복해서 뽑는 문제 → 크기 k 의 최소 힙(min-heap).

  힙: (1, a) (1, b) (2, c)        a: 1→4→5   b: 1→3→4   c: 2→6
  pop (1, a) → 결과 1, push (4, a)
  pop (1, b) → 결과 1, push (3, b)
  pop (2, c) → 결과 2, push (6, c) ...

1. 비어 있지 않은 각 리스트의 head 를 (val, i, node) 로 힙에 넣기 (i 는 동점 처리용 고유 번호)
2. 힙이 빌 때까지: 최솟값 노드를 꺼내 결과 끝에 붙이고, node.next 가 있으면 (next.val, i, next) push
3. dummy.next 를 return

시간 O(N log k), 공간 O(k) (힙)
면접 포인트:
- (val, node) 만 넣으면 val 이 같을 때 ListNode 끼리 비교하다 TypeError 가 납니다. 고유 번호(또는 카운터)를 중간에 넣으세요.
- 분할 정복(divide and conquer): 리스트를 둘씩 짝지어 병합하는 것을 log k 라운드 반복해도 O(N log k) 입니다 (alternative).
- 순차 병합(brute_force)은 O(kN) 이라 효율성 테스트에서 실패합니다.
- 값을 전부 모아 정렬하는 O(N log N) 풀이도 통과하지만, "정렬되어 있다"는 성질을 쓰지 않으므로 면접에선 힙/분할 정복을 기대합니다.
"""


def reference(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            heap.append((node.val, i, node))  # i: 값이 같을 때 노드 비교를 피하는 tie-breaker
    heapq.heapify(heap)

    dummy = tail = ListNode()
    while heap:
        _, i, node = heapq.heappop(heap)  # 현재 맨 앞 노드들 중 최솟값
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    tail.next = None
    return dummy.next


def _merge_two(a, b):
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


def alternative(lists):
    # 분할 정복: 둘씩 짝지어 병합하는 라운드를 log k 번 반복 → O(N log k)
    lists = [node for node in lists if node]
    if not lists:
        return None
    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            b = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(_merge_two(lists[i], b))
        lists = merged
    return lists[0]


def brute_force(lists):
    # 순차 병합: 결과가 점점 길어져 O(kN) → 효율성 실패
    result = None
    for node in lists:
        result = _merge_two(result, node)
    return result
