TITLE = "Surveillance Cameras (과속 단속 카메라 최소 설치)"
LEVEL = "Medium"
SOURCE = "PCCP 기출 유형 (프로그래머스 '단속카메라' 유형)"
PATTERN = "끝 기준 정렬 그리디 — 구간 찌르기(interval stabbing)"

DESCRIPTION = """
일직선 국도 위를 여러 대의 차량이 지나갑니다. 차량 i 는 지점 a 와 지점 b 사이를 달린 뒤 국도를 빠져나가며,
routes[i] = [a, b] 로 주어집니다. 차량은 어느 방향으로든 달릴 수 있어서 a > b 일 수도 있습니다.
(예: [9, 2] 는 9 에서 진입해 2 에서 나가는 차량이며, 지나간 구간은 [2, 9] 와 같습니다.)

도로공사는 정수 지점에 단속 카메라를 설치하려고 합니다. 카메라가 차량이 지나간 구간 위
(양 끝 지점 포함)에 하나라도 있으면 그 차량은 단속 카메라를 만난 것입니다.
모든 차량이 적어도 한 번 카메라를 만나도록 할 때, 필요한 카메라의 최소 개수를 return 하세요.

제한사항
- 1 ≤ len(routes) ≤ 100,000
- -30,000 ≤ a, b ≤ 30,000
- a == b 이면 그 한 지점에서만 국도를 이용한 차량입니다.

입출력 예
routes = [[-20, -15], [-14, -5], [-18, -13], [-5, -3]]  →  2   (-15 와 -5 에 설치)
routes = [[9, 2], [3, 5], [8, 12]]                      →  2   (5 와 12 등)
routes = [[1, 1], [1, 1]]                               →  1
"""

SIGNATURE = "def solution(routes: list[list[int]]) -> int:"

HINTS = [
    "먼저 [a, b] 를 [min(a, b), max(a, b)] 로 바꿔 '왼쪽 끝, 오른쪽 끝' 형태로 통일하세요.",
    "아직 카메라를 못 만난 차량 중 '가장 먼저 도로를 떠나는(오른쪽 끝이 가장 작은)' 차량을 생각해 보세요. 그 차량을 위한 카메라는 어디에 두는 게 가장 이득일까요?",
    "그 차량의 오른쪽 끝에 카메라를 두면, 같은 카메라로 최대한 많은 다른 차량도 잡을 수 있습니다.",
    "오른쪽 끝 기준 정렬 → camera = -무한대 → 각 [l, r] 에 대해 l > camera 이면 camera = r, 개수 += 1.",
]

TESTS = [
    {"input": [[[-20, -15], [-14, -5], [-18, -13], [-5, -3]]], "output": 2},
    {"input": [[[9, 2], [3, 5], [8, 12]]], "output": 2},
    {"input": [[[1, 1], [1, 1]]], "output": 1},
    {"input": [[[0, 10]]], "output": 1},
    {"input": [[[1, 2], [3, 4], [5, 6], [7, 8]]], "output": 4},
    {"input": [[[0, 100], [10, 20], [30, 40], [50, 60]]], "output": 3},
    {"input": [[[5, 1], [4, 2], [3, 3], [2, 4]]], "output": 1},
    {"input": [[[-30000, 30000], [30000, 30000], [-30000, -30000]]], "output": 2},
    {"input": [[[1, 5], [5, 9], [9, 13]]], "output": 2},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    routes = []
    for _ in range(100_000):
        a = random.randint(-30_000, 30_000)
        b = max(-30_000, min(30_000, a + random.randint(-200, 200)))
        routes.append([a, b])
    return {"input": [routes], "output": None}


EXPLANATION = """
핵심: 구간 찌르기(interval stabbing) — '모든 구간을 찌르는 최소 점 개수'. 오른쪽 끝 기준 정렬 그리디입니다.

1. 각 경로를 [min, max] 로 정규화 (역방향 차량 처리)
2. 오른쪽 끝(r) 기준 오름차순 정렬
3. camera = -무한대 (마지막으로 설치한 카메라 위치)
4. 각 [l, r]:
   - l ≤ camera 이면 이미 카메라를 지남 (camera ≤ r 은 정렬 덕분에 자동 성립)
   - 아니면 camera = r 에 새로 설치, count += 1

  routes(정렬): [-20,-15] [-18,-13] [-14,-5] [-5,-3]
  [-20,-15] → 설치 @-15
  [-18,-13] → -18 ≤ -15 통과
  [-14,-5]  → -14 > -15 → 설치 @-5
  [-5,-3]   → -5 ≤ -5 통과                  ⇒ 2대

왜 오른쪽 끝에 두는가?
  가장 먼저 떠나는 차량은 r 이전에 반드시 찍혀야 합니다. 그 범위 안에서 카메라를 최대한 오른쪽(r)에 두면
  다른 차량들과 겹칠 가능성이 가장 커집니다(교환 논증).

시간 O(n log n), 공간 O(n)
실전 포인트: Non-overlapping Intervals(최소 제거), 풍선 터뜨리기(LeetCode 452), 프로그래머스 '단속카메라',
'요격 시스템' 이 모두 같은 '끝 기준 정렬 그리디' 입니다. 다만 끝점이 닿을 때 포함인지(≤)/미포함인지(<) 가
문제마다 다르니 반드시 확인하세요.
"""


def reference(routes):
    # 1) 방향 정규화 후 2) 오른쪽 끝 기준 정렬
    segs = sorted(([min(a, b), max(a, b)] for a, b in routes), key=lambda s: s[1])
    count = 0
    camera = float("-inf")
    for left, right in segs:
        if left > camera:  # 마지막 카메라를 지나지 않은 차량
            camera = right  # 가장 오른쪽(나가는 지점)에 설치
            count += 1
    return count


def brute_force(routes):
    # 모든 정수 지점을 오른쪽으로 쓸면서 '지금 찍지 않으면 놓치는 차량' 이 있을 때만 설치 (좌표 범위가 작을 때만 가능)
    segs = [[min(a, b), max(a, b)] for a, b in routes]
    covered = [False] * len(segs)
    count = 0
    for x in range(-30_000, 30_001):
        if any(not covered[i] and segs[i][1] == x for i in range(len(segs))):
            count += 1
            for i, (l, r) in enumerate(segs):
                if l <= x <= r:
                    covered[i] = True
    return count
