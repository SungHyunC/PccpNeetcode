TITLE = "Minimum Time to Complete Trips (여행을 완료하는 최소 시간)"
LEVEL = "Medium"
SOURCE = "LeetCode 2187 · 프로그래머스 Lv.3 '입국심사' 유형"
PATTERN = "파라메트릭 서치: '시간 T 동안 몇 번 가능한가?' 로 바꿔 최소 T 이분 탐색"

DESCRIPTION = """
버스 n 대가 있고, i 번 버스는 한 번 운행하는 데 time[i] 만큼의 시간이 걸립니다.
모든 버스는 시각 0 에 동시에 출발하며, 운행을 마치면 쉬지 않고 바로 다음 운행을 시작합니다.
버스들은 서로 독립적으로 움직입니다.
모든 버스의 운행 횟수를 합쳐 totalTrips 번 이상이 되는 가장 이른 시각을 return 하세요.

(프로그래머스 '입국심사' 와 같은 구조입니다: 심사관 = 버스, 심사 시간 = time[i], 입국자 수 = totalTrips)

제한사항
- 1 ≤ len(time) ≤ 100,000
- 1 ≤ time[i] ≤ 10,000,000
- 1 ≤ totalTrips ≤ 10,000,000
- 답은 10^14 를 넘을 수 있으므로 정수(int)로 정확히 계산해야 합니다.

입출력 예
time = [1, 2, 3], totalTrips = 5  →  3
  시각 1: 운행 횟수 [1, 0, 0] → 합 1
  시각 2: [2, 1, 0] → 합 3
  시각 3: [3, 1, 1] → 합 5  ✔
time = [2], totalTrips = 1  →  2
time = [7, 10], totalTrips = 6 → 28   (프로그래머스 '입국심사' 예시와 같은 상황)
"""

SIGNATURE = "def solution(time: list[int], totalTrips: int) -> int:"

HINTS = [
    "시각 T 가 주어지면, i 번 버스는 T // time[i] 번 운행을 마칩니다. 그러면 'T 까지 총 몇 번?' 은 O(n) 에 계산됩니다.",
    "T 가 커지면 총 운행 횟수는 줄어들지 않습니다(단조 증가). '총 운행 ≥ totalTrips' 를 만족하는 가장 작은 T 를 이분 탐색하세요.",
    "범위: lo = 1, hi = min(time) * totalTrips (가장 빠른 버스 혼자서도 이 시각이면 충분). 이 값은 최대 10^14 이지만 이분 탐색은 약 47 번이면 끝납니다.",
    "while lo < hi: mid = (lo + hi) // 2; sum(mid // t for t in time) >= totalTrips 이면 hi = mid, 아니면 lo = mid + 1.",
]

TESTS = [
    {"input": [[1, 2, 3], 5], "output": 3},
    {"input": [[2], 1], "output": 2},
    {"input": [[7, 10], 6], "output": 28},
    {"input": [[5, 10, 10], 9], "output": 25},
    {"input": [[1], 1], "output": 1},
    {"input": [[3, 3, 3], 3], "output": 3},
    {"input": [[10000000], 1000], "output": 10000000000},
    {"input": [[10000000, 10000000], 10000], "output": 50000000000},
    {"input": [[9, 3, 10, 5], 2], "output": 5},
    {"input": [[1, 1, 1, 1], 10], "output": 3},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    time = [random.randint(1_000_000, 10_000_000) for _ in range(30_000)]
    return {"input": [time, 10_000_000], "output": None}


EXPLANATION = """
핵심(파라메트릭 서치): "최소 시각 T 는?" → "시각 T 까지 totalTrips 번 이상 운행할 수 있는가?" 로 바꿉니다.
T 가 커질수록 운행 횟수는 늘기만 하므로 [불가능 … 불가능, 가능 … 가능] 형태 → 처음으로 가능한 T 를 이분 탐색합니다.

1. trips(T) = sum(T // t for t in time)
2. lo, hi = 1, min(time) * totalTrips
3. while lo < hi:
     mid = (lo + hi) // 2
     trips(mid) >= totalTrips 이면 hi = mid, 아니면 lo = mid + 1
4. lo return

시간 O(n log(min(time) · totalTrips)) ≈ 47 · n, 공간 O(1)
프로그래머스 '입국심사'(심사관 times, 입국자 n)도 같은 코드입니다. 그 문제는 범위가 10^9 × 10^9 = 10^18 까지 커지지만
파이썬 int 는 오버플로가 없고 이분 탐색은 약 60 번이면 끝납니다.
면접 포인트: 시뮬레이션(힙으로 다음에 끝나는 버스 꺼내기)은 O(totalTrips · log n) 이라 totalTrips = 10^7 이면 느립니다.
"답의 범위는 거대하지만 답을 정하면 판정이 쉽다" → 파라메트릭 서치라는 판단 근거를 말하세요.
hi 를 max(time) * totalTrips 로 잡아도 맞지만, min(time) 을 쓰면 범위가 더 좁습니다.
"""


def reference(time, totalTrips):
    def enough(t):
        # 시각 t 까지 완료한 총 운행 횟수가 totalTrips 이상인가?
        return sum(t // x for x in time) >= totalTrips

    lo, hi = 1, min(time) * totalTrips  # 가장 빠른 버스 혼자서도 hi 면 충분
    while lo < hi:
        mid = (lo + hi) // 2
        if enough(mid):
            hi = mid      # mid 도 가능 → 더 이른 시각을 찾는다
        else:
            lo = mid + 1
    return lo


def brute_force(time, totalTrips):
    # 힙으로 '다음에 운행을 마치는 버스' 를 하나씩 꺼내는 시뮬레이션: O(totalTrips · log n)
    import heapq

    heap = [(t, t) for t in time]  # (다음 완료 시각, 1회 운행 시간)
    heapq.heapify(heap)
    done = 0
    while True:
        finish, t = heapq.heappop(heap)
        done += 1
        if done == totalTrips:
            return finish
        heapq.heappush(heap, (finish + t, t))
