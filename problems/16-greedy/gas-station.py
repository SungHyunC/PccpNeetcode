TITLE = "Gas Station (주유소 순회)"
LEVEL = "Medium"
SOURCE = "LeetCode 134"
PATTERN = "전체 합 ≥ 0 이면 답 존재, 연료가 음수가 되는 순간 다음 칸을 시작점으로"

DESCRIPTION = """
원형 도로 위에 주유소 n 개가 있습니다. i 번 주유소에서는 연료 gas[i] 를 넣을 수 있고,
i 번에서 다음 주유소((i + 1) % n 번)까지 가는 데 연료 cost[i] 가 듭니다.
연료통은 빈 상태로 어떤 주유소에서 출발하며, 연료통 용량은 무제한입니다.
시계 방향으로 한 바퀴를 돌아 출발한 주유소로 돌아올 수 있는 출발 주유소의 번호를 return 하세요.
불가능하면 -1 을 return 합니다. (가능한 출발점이 있다면 유일합니다.)

제한사항
- 1 ≤ n ≤ 100,000, len(gas) == len(cost) == n
- 0 ≤ gas[i], cost[i] ≤ 10,000

입출력 예
gas = [1, 2, 3, 4, 5], cost = [3, 4, 5, 1, 2]  →  3
gas = [2, 3, 4],       cost = [3, 4, 3]        →  -1   (전체 연료 9 < 전체 비용 10)
"""

SIGNATURE = "def solution(gas: list[int], cost: list[int]) -> int:"

HINTS = [
    "모든 출발점에서 한 바퀴를 시뮬레이션하면 O(n^2) 입니다.",
    "sum(gas) < sum(cost) 이면 어디서 출발해도 불가능합니다. 반대로 sum(gas) ≥ sum(cost) 이면 답이 반드시 존재합니다.",
    "start 에서 출발해 i 에서 처음으로 연료가 음수가 됐다면, start..i 사이의 어떤 칸에서 출발해도 i 를 못 넘습니다. 그러니 start = i + 1, tank = 0 으로 다시 시작하세요. 한 번 훑으면 O(n).",
]

TESTS = [
    {"input": [[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]], "output": 3},
    {"input": [[2, 3, 4], [3, 4, 3]], "output": -1},
    {"input": [[5], [4]], "output": 0},
    {"input": [[1], [2]], "output": -1},
    {"input": [[3, 1, 1], [1, 2, 2]], "output": 0},
    {"input": [[5, 1, 2, 3, 4], [4, 4, 1, 5, 1]], "output": 4},
    {"input": [[0, 0, 10], [3, 3, 3]], "output": 2},
]


def check(result, expected, gas, cost):
    # 기댓값이 -1 이면 -1 이어야 하고, 아니면 result 가 실제로 한 바퀴를 돌 수 있는 출발점인지 확인
    if expected == -1:
        return result == -1
    n = len(gas)
    if not isinstance(result, int) or not 0 <= result < n:
        return False
    tank = 0
    for k in range(n):
        i = (result + k) % n
        tank += gas[i] - cost[i]
        if tank < 0:
            return False
    return True


PERF_LIMIT = 1.0


def perf_case():
    import random

    # [연료가 조금씩 남는 구간 99,960칸] + [큰 적자 20칸] + [큰 흑자 20칸]
    # → 앞 구간의 어느 칸에서 출발해도 한참 달린 뒤 적자 구간에서 실패하므로
    #   모든 출발점을 시뮬레이션하는 O(n^2) 풀이는 시간 초과
    gas, cost = [], []
    for _ in range(99_960):
        r = random.randint(0, 9_999)
        gas.append(r + 1)
        cost.append(r)
    gas += [0] * 20 + [10_000] * 20
    cost += [10_000] * 20 + [0] * 20
    return {"input": [gas, cost], "output": None}


EXPLANATION = """
아이디어
- 사실 1: 전체 연료 합 < 전체 비용 합 → 불가능(-1). 전체 합 ≥ 0 이면 답이 존재합니다.
- 사실 2: start 에서 출발해 i 에서 처음 연료가 음수가 되면, start..i 의 어느 칸에서 출발해도 i 에서 실패합니다.
  (start..k 구간은 지금까지 연료를 '보태 주던' 구간이라, 그걸 빼고 k+1 에서 출발하면 연료가 더 적거나 같음)
  → start 를 i + 1 로 건너뛰어도 답을 놓치지 않습니다.

단계
1. total = 0, tank = 0, start = 0
2. i = 0 → n-1: d = gas[i] - cost[i]; total += d; tank += d
   - tank < 0 이면 start = i + 1, tank = 0
3. total < 0 이면 -1, 아니면 start

  gas  : 1   2   3   4   5
  cost : 3   4   5   1   2
  d    : -2  -2  -2  3   3     total = 0 ≥ 0
  tank : -2→리셋(start=1)  -2→리셋(start=2)  -2→리셋(start=3)  3  6   → start = 3

복잡도: 시간 O(n), 공간 O(1)

면접 포인트
- 그리디의 정당성을 "start..i 사이에서 출발하면 왜 안 되는가" 로 설명할 수 있어야 합니다.
- 왜 한 바퀴 다시 확인하지 않아도 되는가? total ≥ 0 이면, start 이전 구간의 부족분(음수)을
  start 이후 구간의 누적 잉여가 정확히 메워 주기 때문입니다.
- 누적합 관점: 누적합 prefix 가 최소가 되는 지점 다음 칸이 출발점입니다.
"""


def reference(gas, cost):
    total = 0  # 전체 연료 - 전체 비용
    tank = 0  # 현재 start 에서 출발했을 때 남은 연료
    start = 0
    for i in range(len(gas)):
        d = gas[i] - cost[i]
        total += d
        tank += d
        if tank < 0:  # start..i 어디서 출발해도 i 를 못 넘음
            start = i + 1
            tank = 0
    return start if total >= 0 else -1


def brute_force(gas, cost):
    # 모든 출발점 시뮬레이션: O(n^2)
    n = len(gas)
    for s in range(n):
        tank = 0
        for k in range(n):
            i = (s + k) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                break
        else:
            return s
    return -1
