TITLE = "Best Time to Buy and Sell Stock with Cooldown (쿨다운이 있는 주식 매매)"
LEVEL = "Medium"
SOURCE = "LeetCode 309"
PATTERN = "상태 기계 DP (보유 / 막 팖 / 쉼)"

DESCRIPTION = """
prices[i] 는 i 일째의 주가입니다. 주식은 한 번에 최대 1주만 가질 수 있으며,
사고팔기를 원하는 만큼 반복할 수 있습니다. 단, 다음 규칙을 지켜야 합니다.
- 주식을 가지고 있을 때는 새로 살 수 없습니다. (먼저 팔아야 함)
- 주식을 판 다음 날은 쿨다운이라 살 수 없습니다.
얻을 수 있는 최대 이익을 return 하세요. 거래하지 않으면 이익은 0 입니다.

제한사항
- 1 ≤ len(prices) ≤ 100,000
- 0 ≤ prices[i] ≤ 1,000

입출력 예
prices = [1, 2, 3, 0, 2]  →  3   (1일 매수, 2일 매도, 3일 쿨다운, 4일 매수, 5일 매도)
prices = [1]              →  0
"""

SIGNATURE = "def solution(prices: list[int]) -> int:"

HINTS = [
    "하루가 끝났을 때 나는 세 가지 상태 중 하나입니다: 주식 보유(hold) / 오늘 막 팔았음(sold) / 주식 없음 + 쿨다운 아님(rest).",
    "상태 사이의 전이를 그려 보세요: rest → hold (매수), hold → sold (매도), sold → rest (쿨다운), 그리고 hold → hold, rest → rest (대기).",
    "new_hold = max(hold, rest - p), new_sold = hold + p, new_rest = max(rest, sold). 모두 '어제' 값으로 동시에 계산하세요. 초기값 hold = -inf, sold = 0, rest = 0. 답은 max(sold, rest).",
]

TESTS = [
    {"input": [[1, 2, 3, 0, 2]], "output": 3},
    {"input": [[1]], "output": 0},
    {"input": [[2, 1]], "output": 0},
    {"input": [[1, 2]], "output": 1},
    {"input": [[1, 2, 4]], "output": 3},
    {"input": [[6, 1, 6, 4, 3, 0, 2]], "output": 7},
    {"input": [[1, 4, 2, 7]], "output": 6},
    {"input": [[3, 3, 3]], "output": 0},
    {"input": [[1, 3, 1, 3, 1, 3]], "output": 4},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    prices = [random.randint(0, 1000) for _ in range(100_000)]
    return {"input": [prices], "output": None}


EXPLANATION = """
아이디어
- "오늘 무엇을 할 수 있는가" 가 어제의 상태(보유 중? 어제 팔았나?)에 따라 달라집니다.
- 이럴 때는 날짜(i) × 상태(s) 의 2차원 DP, 즉 상태 기계(state machine) DP 를 씁니다.

상태 기계

              매수 (-p)            매도 (+p)
   ┌──────┐  ─────────▶  ┌──────┐  ─────────▶  ┌──────┐
   │ rest │              │ hold │              │ sold │
   └──────┘  ◀───────────────────────────────  └──────┘
    ↺ 대기                ↺ 보유 유지      다음 날 rest 로 (쿨다운)

DP 레시피
1. 상태 정의: i 일이 끝났을 때
   hold[i] = 주식을 보유한 상태의 최대 이익
   sold[i] = i 일에 막 판 상태의 최대 이익
   rest[i] = 주식이 없고 i 일에 팔지 않은 상태의 최대 이익
2. 점화식:
   hold[i] = max(hold[i-1], rest[i-1] - p)   ← 쿨다운 때문에 sold 가 아닌 rest 에서만 매수
   sold[i] = hold[i-1] + p
   rest[i] = max(rest[i-1], sold[i-1])
3. 초기값:   hold = -inf (아직 못 가짐), sold = 0, rest = 0
4. 계산 순서: i = 0 → n-1, 세 값을 '어제 값' 으로 동시에 갱신
5. 답:       max(sold, rest)  (마지막에 주식을 들고 있는 건 손해)

  prices :    1     2     3     0     2
  hold   :   -1    -1    -1     1     1     (4일째: 3일째 rest=1 에서 0원에 매수)
  sold   : -inf     1     2    -1     3
  rest   :    0     0     1     2     2
  답 = max(sold, rest) = max(3, 2) = 3

복잡도: 시간 O(n), 공간 O(1)

면접 포인트
- 주식 문제 시리즈(I: 1회, II: 무제한, III: 2회, IV: k회, 쿨다운, 수수료)는 모두 상태 기계로 통일해 풀 수 있습니다.
  상태만 (거래 횟수, 보유 여부, 쿨다운 여부) 로 늘리면 됩니다.
- 갱신 순서 버그 주의: hold 를 먼저 바꾸고 그 값으로 sold 를 계산하면 같은 날 사고파는 셈이 됩니다.
  튜플 동시 대입(a, b, c = ...)으로 어제 값만 쓰세요.
- top-down(best(i, holding) + 메모, alternative)도 같은 점화식이지만 n = 100,000 이면 재귀 깊이 초과입니다.
  이 저장소의 효율성 테스트도 그래서 바텀업 상태 변수 풀이를 기대합니다.
"""


def reference(prices):
    hold, sold, rest = float("-inf"), 0, 0
    for p in prices:
        # 세 상태 모두 '어제' 값으로 동시에 갱신
        hold, sold, rest = (
            max(hold, rest - p),  # 계속 보유 or 쉬던 상태에서 매수
            hold + p,             # 보유 중이던 주식을 오늘 매도
            max(rest, sold),      # 계속 쉼 or 어제 판 뒤 쿨다운 종료
        )
    return max(sold, rest)


def alternative(prices):
    # top-down: best(i, holding) = i 일부터 시작할 때의 최대 이익
    from functools import lru_cache

    n = len(prices)

    @lru_cache(maxsize=None)
    def best(i, holding):
        if i >= n:
            return 0
        skip = best(i + 1, holding)
        if holding:
            return max(skip, prices[i] + best(i + 2, False))  # 팔면 다음 날 쿨다운
        return max(skip, -prices[i] + best(i + 1, True))

    return best(0, False)


def brute_force(prices):
    # 매일 할 수 있는 행동을 모두 시도: O(2^n)
    n = len(prices)

    def go(i, holding):
        if i >= n:
            return 0
        res = go(i + 1, holding)
        if holding:
            res = max(res, prices[i] + go(i + 2, False))
        else:
            res = max(res, -prices[i] + go(i + 1, True))
        return res

    return go(0, False)
