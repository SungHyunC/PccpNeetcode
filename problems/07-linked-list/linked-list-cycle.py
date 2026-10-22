import random

from lib.structures import ListNode, build_linked_list

TITLE = "Linked List Cycle (연결 리스트 사이클 판별)"
LEVEL = "Easy"
SOURCE = "LeetCode 141"
PATTERN = "플로이드 토끼와 거북이 (fast / slow 포인터)"

DESCRIPTION = """
단방향 연결 리스트의 head 가 주어집니다.
next 를 계속 따라갔을 때 이미 지나간 노드로 되돌아오는 경우(사이클)가 있으면 True,
끝(None)에 도달하면 False 를 return 하세요.

채점용 입력은 [values, pos] 입니다.
- values: 노드 값들을 앞에서부터 나열한 리스트
- pos: 마지막 노드의 next 가 가리키는 노드의 인덱스 (0부터). -1 이면 사이클 없음.
solution 에는 이 정보로 실제 사이클을 만든 head 만 전달됩니다. (pos 는 전달되지 않습니다)

제한사항
- 0 ≤ 노드 개수 ≤ 100,000
- -100,000 ≤ 노드 값 ≤ 100,000 (값은 중복될 수 있습니다)
- pos 는 -1 이거나 유효한 인덱스
- 추가 공간 O(1) 로 풀어 보세요.

입출력 예
values = [3, 2, 0, -4], pos = 1   →  True   (-4 다음이 다시 2)
values = [1, 2],        pos = 0   →  True
values = [1],           pos = -1  →  False
"""

SIGNATURE = "def solution(head: ListNode) -> bool:"

IMPORTS = "from lib.structures import ListNode"

HINTS = [
    "사이클이 있으면 next 를 따라가는 루프가 영원히 끝나지 않습니다. '이미 방문한 노드인가?'를 어떻게 알 수 있을까요?",
    "방문한 노드 자체(값이 아니라 객체)를 set 에 넣으면 O(n) 공간으로 풀립니다. 값은 중복될 수 있으니 값으로 판단하면 안 됩니다.",
    "O(1) 공간: slow 는 한 칸, fast 는 두 칸씩 움직입니다. 사이클이 있으면 fast 가 결국 slow 를 따라잡아 같은 노드에서 만납니다.",
    "while fast and fast.next: slow = slow.next; fast = fast.next.next; if slow is fast: return True. 루프를 빠져나오면 False.",
]

TESTS = [
    {"input": [[3, 2, 0, -4], 1], "output": True},
    {"input": [[1, 2], 0], "output": True},
    {"input": [[1], -1], "output": False},
    {"input": [[], -1], "output": False},
    {"input": [[1], 0], "output": True},
    {"input": [[1, 2, 3, 4, 5], -1], "output": False},
    {"input": [[1, 1, 1, 1], -1], "output": False},
    {"input": [[1, 2, 3, 4, 5, 6], 5], "output": True},
]


def prepare(values, pos):
    head = build_linked_list(values)
    if pos >= 0 and head:
        target, tail, i = None, head, 0
        node = head
        while node:
            if i == pos:
                target = node
            tail = node
            node = node.next
            i += 1
        tail.next = target  # 꼬리를 pos 번째 노드에 연결해 사이클 생성
    return [head]


PERF_LIMIT = 1.0


def perf_case():
    n = 100_000
    values = [random.randint(-100_000, 100_000) for _ in range(n)]
    return {"input": [values, n // 3], "output": None}


EXPLANATION = """
핵심: 플로이드의 사이클 탐지(Floyd's cycle detection). 속도가 다른 두 포인터가 원형 트랙 위에 있으면 언젠가 만납니다.

1. slow = fast = head
2. fast 와 fast.next 가 있는 동안: slow 1칸, fast 2칸 이동
3. slow is fast 이면 사이클 → True
4. fast 가 끝(None)에 닿으면 사이클 없음 → False

왜 만나나? 둘 다 사이클에 들어간 뒤에는 매 단계 fast 가 slow 와의 거리를 1씩 줄입니다.
따라서 사이클 길이 이내의 단계 안에 반드시 만납니다 (건너뛰는 일이 없음).

  1 -> 2 -> 3 -> 4
       ^         |
       +---------+      slow: 1,2,3,4,2,...   fast: 1,3,2,4,...  → 만남

시간 O(n), 공간 O(1)
면접 포인트: 먼저 set 풀이(O(n) 공간)를 말하고 → "공간을 줄일 수 있나요?" 에 플로이드로 답하는 흐름이 자연스럽습니다.
노드 비교는 값(==)이 아니라 객체 동일성(is)으로 해야 합니다. 후속 질문: 사이클 시작점 찾기(LeetCode 142),
Find the Duplicate Number(LeetCode 287)도 같은 원리입니다.
"""


def reference(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next          # 1칸
        fast = fast.next.next     # 2칸
        if slow is fast:          # 객체가 같으면 만난 것
            return True
    return False                  # fast 가 끝에 닿음 → 사이클 없음


def alternative(head):
    # 방문한 노드 객체를 set 에 저장 (공간 O(n))
    seen = set()
    while head:
        if id(head) in seen:
            return True
        seen.add(id(head))
        head = head.next
    return False
