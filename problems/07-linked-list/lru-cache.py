import random
from collections import OrderedDict

TITLE = "LRU Cache (LRU 캐시 설계)"
LEVEL = "Medium"
SOURCE = "LeetCode 146"
PATTERN = "해시맵 + 이중 연결 리스트 (OrderedDict)"

DESCRIPTION = """
용량이 정해진 LRU(Least Recently Used) 캐시를 설계하세요.

- LRUCache(capacity): 용량 capacity 로 캐시를 만듭니다.
- get(key): key 가 있으면 값을, 없으면 -1 을 반환합니다. 조회한 key 는 '가장 최근에 사용'한 것이 됩니다.
- put(key, value): key 가 있으면 값을 바꾸고, 없으면 새로 넣습니다. 이것도 '가장 최근 사용'으로 칩니다.
  넣은 뒤 개수가 capacity 를 넘으면, 가장 오랫동안 사용하지 않은 key 하나를 지웁니다.
- get 과 put 은 모두 평균 O(1) 이어야 합니다.

[채점 방식] 클래스 설계 문제를 solution(commands, values) 로 바꿨습니다.
commands[i] 는 호출할 이름, values[i] 는 그 인자 리스트입니다.
각 호출의 반환값을 순서대로 담은 리스트를 return 하세요. 생성자와 put 처럼 반환값이 없으면 None 을 담습니다.
solution 안(또는 밖)에 class LRUCache 를 정의하고 commands 를 차례로 실행하면 됩니다.

제한사항
- 1 ≤ capacity ≤ 50,000
- 0 ≤ key, value ≤ 100,000
- 호출 횟수 ≤ 100,000 (효율성 테스트 있음)
- commands[0] 은 항상 "LRUCache"

입출력 예
commands = ["LRUCache", "put", "put", "get", "put", "get", "get"]
values   = [[2], [1, 10], [2, 20], [1], [3, 30], [2], [3]]
→ [None, None, None, 10, None, -1, 30]
(get(1) 로 1 이 최근 사용이 되었으므로, put(3) 때 가장 오래된 2 가 지워집니다.)
"""

SIGNATURE = "def solution(commands: list[str], values: list[list]) -> list:"

HINTS = [
    "뼈대: obj = None; out = [] → for cmd, args in zip(commands, values): 생성자면 obj = LRUCache(*args); out.append(None), 아니면 out.append(getattr(obj, cmd)(*args)).",
    "dict 만으로는 '가장 오래된 key'를 O(1) 에 찾을 수 없고, 리스트로 사용 순서를 관리하면 중간 삭제가 O(n) 입니다.",
    "파이썬이라면 collections.OrderedDict 가 정답에 가깝습니다: move_to_end(key) 로 최근 사용 표시, popitem(last=False) 로 가장 오래된 항목 삭제.",
    "직접 구현: key → 노드 dict + 이중 연결 리스트(head/tail 더미 노드). 사용할 때마다 노드를 떼어 tail 앞에 붙이고, 용량 초과 시 head.next 를 삭제합니다.",
]

TESTS = [
    {
        "input": [
            ["LRUCache", "put", "put", "get", "put", "get", "get"],
            [[2], [1, 10], [2, 20], [1], [3, 30], [2], [3]],
        ],
        "output": [None, None, None, 10, None, -1, 30],
    },
    {
        "input": [
            ["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"],
            [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]],
        ],
        "output": [None, None, None, 1, None, -1, None, -1, 3, 4],
    },
    {
        "input": [["LRUCache", "get", "put", "get"], [[1], [5], [5, 50], [5]]],
        "output": [None, -1, None, 50],
    },
    {
        "input": [
            ["LRUCache", "put", "put", "get", "get"],
            [[1], [1, 1], [2, 2], [1], [2]],
        ],
        "output": [None, None, None, -1, 2],
    },
    {
        # 이미 있는 key 를 put 하면 값이 바뀌고 '최근 사용'이 됩니다
        "input": [
            ["LRUCache", "put", "put", "put", "put", "get", "get", "get"],
            [[2], [1, 1], [2, 2], [1, 100], [3, 3], [1], [2], [3]],
        ],
        "output": [None, None, None, None, None, 100, -1, 3],
    },
    {
        "input": [
            ["LRUCache", "put", "put", "put", "get", "get", "get"],
            [[3], [0, 0], [100000, 7], [0, 9], [0], [100000], [42]],
        ],
        "output": [None, None, None, None, 9, 7, -1],
    },
]


PERF_LIMIT = 1.0


def perf_case():
    commands, values = ["LRUCache"], [[30_000]]
    for _ in range(100_000):
        key = random.randint(0, 60_000)
        if random.random() < 0.5:
            commands.append("put")
            values.append([key, random.randint(0, 100_000)])
        else:
            commands.append("get")
            values.append([key])
    return {"input": [commands, values], "output": None}


EXPLANATION = """
핵심: "key 로 O(1) 조회" + "사용 순서를 O(1) 로 갱신/삭제" 를 동시에 하려면
해시맵(hash map) 과 이중 연결 리스트(doubly linked list)를 함께 씁니다.

  dict: key → 노드
  [head] <-> (1) <-> (3) <-> (2) <-> [tail]
   오래됨 ←                    → 최근

- get(key): dict 로 노드를 찾고, 리스트에서 떼어 tail 앞으로 이동
- put(key, v): 있으면 값 갱신 + 이동, 없으면 새 노드를 tail 앞에 추가. 크기 초과 시 head.next 삭제
- 이중 연결 리스트라서 노드 하나를 prev/next 만 바꿔 O(1) 에 떼어낼 수 있습니다.

파이썬 OrderedDict 는 내부가 바로 이 구조라서
  move_to_end(key)       = 최근 사용으로 이동
  popitem(last=False)    = 가장 오래된 항목 삭제
로 몇 줄 만에 구현됩니다 (reference). alternative 는 직접 만든 이중 연결 리스트 버전입니다.

시간: 모든 연산 O(1), 공간 O(capacity)
면접 포인트: 미국 빅테크 단골 문제입니다. OrderedDict 풀이를 먼저 말해도 되지만,
"라이브러리 없이 구현해 보세요" 라는 요청이 거의 항상 따라오므로 dict + DLL 버전을 손으로 쓸 수 있어야 합니다.
head/tail 더미 노드를 쓰면 빈 리스트·맨 앞·맨 뒤 경계 처리가 사라집니다.
삭제할 때 dict 에서도 지워야 하므로 노드에 key 를 함께 저장하는 것이 포인트입니다.
리스트로 순서를 관리하는 brute_force 는 연산마다 O(n) 이라 효율성 테스트에서 실패합니다.
"""


def reference(commands, values):
    class LRUCache:
        def __init__(self, capacity):
            self.cap = capacity
            self.data = OrderedDict()  # 앞쪽 = 오래됨, 뒤쪽 = 최근

        def get(self, key):
            if key not in self.data:
                return -1
            self.data.move_to_end(key)  # 최근 사용으로 표시
            return self.data[key]

        def put(self, key, value):
            if key in self.data:
                self.data.move_to_end(key)
            self.data[key] = value
            if len(self.data) > self.cap:
                self.data.popitem(last=False)  # 가장 오래된 항목 제거

    out, obj = [], None
    for cmd, args in zip(commands, values):
        if cmd == "LRUCache":
            obj = LRUCache(*args)
            out.append(None)
        else:
            out.append(getattr(obj, cmd)(*args))
    return out


def alternative(commands, values):
    # dict + 직접 만든 이중 연결 리스트
    class Node:
        __slots__ = ("key", "val", "prev", "next")

        def __init__(self, key=0, val=0):
            self.key, self.val = key, val
            self.prev = self.next = None

    class LRUCache:
        def __init__(self, capacity):
            self.cap = capacity
            self.map = {}
            self.head, self.tail = Node(), Node()  # 더미: head.next 가 가장 오래됨
            self.head.next, self.tail.prev = self.tail, self.head

        def _remove(self, node):
            node.prev.next, node.next.prev = node.next, node.prev

        def _append(self, node):  # tail 바로 앞(가장 최근)에 붙이기
            last = self.tail.prev
            last.next = node
            node.prev, node.next = last, self.tail
            self.tail.prev = node

        def get(self, key):
            node = self.map.get(key)
            if node is None:
                return -1
            self._remove(node)
            self._append(node)
            return node.val

        def put(self, key, value):
            node = self.map.get(key)
            if node:
                node.val = value
                self._remove(node)
            else:
                node = Node(key, value)
                self.map[key] = node
            self._append(node)
            if len(self.map) > self.cap:
                oldest = self.head.next
                self._remove(oldest)
                del self.map[oldest.key]  # 노드에 key 를 저장해 둔 이유

    out, obj = [], None
    for cmd, args in zip(commands, values):
        if cmd == "LRUCache":
            obj = LRUCache(*args)
            out.append(None)
        else:
            out.append(getattr(obj, cmd)(*args))
    return out


def brute_force(commands, values):
    # dict + 사용 순서 리스트: list.remove 가 O(n) → 효율성 실패
    out, cap, data, order = [], 0, {}, []
    for cmd, args in zip(commands, values):
        if cmd == "LRUCache":
            cap = args[0]
            out.append(None)
        elif cmd == "get":
            key = args[0]
            if key in data:
                order.remove(key)
                order.append(key)
                out.append(data[key])
            else:
                out.append(-1)
        else:
            key, value = args
            if key in data:
                order.remove(key)
            data[key] = value
            order.append(key)
            if len(order) > cap:
                del data[order.pop(0)]
            out.append(None)
    return out
