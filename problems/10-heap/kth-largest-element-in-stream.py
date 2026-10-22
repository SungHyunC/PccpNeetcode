import heapq
import random

TITLE = "Kth Largest Element in a Stream (스트림에서 k번째로 큰 값)"
LEVEL = "Easy"
SOURCE = "LeetCode 703"
PATTERN = "크기 k 최소 힙: 루트가 곧 k번째로 큰 값"

DESCRIPTION = """
숫자가 하나씩 계속 들어오는 상황(스트림)에서, 지금까지 들어온 숫자 중 k 번째로 큰 값을 알려 주는 클래스를 설계하세요.
(중복된 값도 각각 하나로 셉니다. [5, 5, 4] 에서 2번째로 큰 값은 5)

- KthLargest(k, nums): 정수 k 와 처음 숫자들 nums 로 초기화합니다.
- add(val): val 을 추가한 뒤, 지금까지의 모든 숫자 중 k 번째로 큰 값을 반환합니다.

[채점 방식] 클래스 설계 문제를 solution(commands, values) 로 바꿨습니다.
commands[i] 는 호출할 이름, values[i] 는 그 인자 리스트입니다.
각 호출의 반환값을 순서대로 담은 리스트를 return 하세요 (생성자는 None).

제한사항
- 1 ≤ k ≤ 20,001, 0 ≤ len(nums) ≤ 20,000
- -10^4 ≤ nums[i], val ≤ 10^4
- add 호출 횟수 ≤ 20,000 (효율성 테스트 있음)
- add 를 호출한 시점에는 항상 숫자가 k 개 이상 있습니다.

입출력 예
commands = ["KthLargest", "add", "add", "add", "add", "add"]
values   = [[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]
→ [None, 4, 5, 5, 8, 8]
"""

SIGNATURE = "def solution(commands: list[str], values: list[list]) -> list:"

HINTS = [
    "뼈대: 생성자면 obj = KthLargest(*args) (args = [k, nums]), 아니면 out.append(obj.add(*args)).",
    "매번 정렬하면 add 하나에 O(n log n) 입니다. k 번째로 큰 값을 알려면 '큰 값 k 개'만 기억하면 됩니다.",
    "큰 값 k 개를 최소 힙에 유지하면, 그중 가장 작은 값(heap[0])이 k 번째로 큰 값입니다. 크기가 k 를 넘으면 heappop 으로 가장 작은 것을 버리세요.",
]

TESTS = [
    {
        "input": [
            ["KthLargest", "add", "add", "add", "add", "add"],
            [[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]],
        ],
        "output": [None, 4, 5, 5, 8, 8],
    },
    {
        "input": [["KthLargest", "add", "add", "add"], [[1, []], [-3], [-2], [-4]]],
        "output": [None, -3, -2, -2],
    },
    {
        "input": [
            ["KthLargest", "add", "add", "add", "add", "add"],
            [[2, [0]], [-1], [1], [-2], [-4], [3]],
        ],
        "output": [None, -1, 0, 0, 0, 1],
    },
    {
        "input": [["KthLargest", "add", "add", "add", "add"], [[3, [5, 5, 5]], [5], [6], [7], [8]]],
        "output": [None, 5, 5, 5, 6],
    },
    {
        "input": [["KthLargest", "add", "add"], [[4, [1, 2, 3]], [0], [10]]],
        "output": [None, 0, 1],
    },
    {
        "input": [["KthLargest", "add", "add"], [[1, [10000, -10000]], [-10000], [10000]]],
        "output": [None, 10000, 10000],
    },
]

PERF_LIMIT = 1.0


def perf_case():
    nums = [random.randint(-10**4, 10**4) for _ in range(20_000)]
    commands, values = ["KthLargest"], [[5_000, nums]]
    for _ in range(20_000):
        commands.append("add")
        values.append([random.randint(-10**4, 10**4)])
    return {"input": [commands, values], "output": None}


EXPLANATION = """
핵심: k 번째로 큰 값만 알면 되므로 "상위 k 개"만 최소 힙에 유지합니다. 힙의 루트(가장 작은 값)가 정답입니다.

  k = 3, nums = [4, 5, 8, 2]
  힙(상위 3개) = [4, 5, 8]   ← 2 는 버림          답 = heap[0] = 4
  add(3):  [3, 4, 5, 8] → pop 3 → [4, 5, 8]      답 4
  add(5):  [4, 5, 5, 8] → pop 4 → [5, 5, 8]      답 5
  add(10): [5, 5, 8, 10] → pop 5 → [5, 8, 10]    답 5

1. 생성자: heap = nums, heapify 후 크기가 k 가 될 때까지 heappop
2. add(val): heappush(val), 크기가 k 보다 크면 heappop → heap[0] 반환
   (heappushpop 을 쓰면 push + pop 을 한 번에 더 빠르게 할 수 있습니다)

시간: 생성 O(n + (n - k) log n), add O(log k)
공간: O(k)
면접 포인트: "Top-k 큰 값 → 크기 k 최소 힙" 은 반드시 외워야 할 패턴입니다 (반대로 Top-k 작은 값은 크기 k 최대 힙).
모든 값을 저장하고 정렬하는 brute_force 는 add 마다 O(n log n) 이라 효율성 테스트에서 실패합니다.
"""


def reference(commands, values):
    class KthLargest:
        def __init__(self, k, nums):
            self.k = k
            self.heap = list(nums)
            heapq.heapify(self.heap)
            while len(self.heap) > k:     # 상위 k 개만 남기기
                heapq.heappop(self.heap)

        def add(self, val):
            if len(self.heap) < self.k:
                heapq.heappush(self.heap, val)
            elif val > self.heap[0]:      # 상위 k 개에 들어갈 자격이 있을 때만
                heapq.heapreplace(self.heap, val)  # pop 후 push 를 한 번에
            return self.heap[0]           # 상위 k 개 중 가장 작은 값 = k 번째로 큰 값

    out, obj = [], None
    for cmd, args in zip(commands, values):
        if cmd == "KthLargest":
            obj = KthLargest(*args)
            out.append(None)
        else:
            out.append(obj.add(*args))
    return out


def brute_force(commands, values):
    # 전부 저장하고 매번 정렬: add 마다 O(n log n) → 효율성 실패
    out, k, nums = [], 0, []
    for cmd, args in zip(commands, values):
        if cmd == "KthLargest":
            k, nums = args[0], list(args[1])
            out.append(None)
        else:
            nums.append(args[0])
            out.append(sorted(nums, reverse=True)[k - 1])
    return out
