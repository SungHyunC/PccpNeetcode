TITLE = "Integer Triangle (숫자 삼각형 최대 경로 합)"
LEVEL = "Medium"
SOURCE = "프로그래머스 Lv.3 '정수 삼각형' 유형"
PATTERN = "아래에서 위로 올라오는 삼각형 DP: dp[j] = row[j] + max(dp[j], dp[j+1])"

DESCRIPTION = """
숫자가 삼각형 모양으로 쌓여 있습니다. triangle[i] 는 위에서 i 번째 줄이며 i + 1 개의 수가 있습니다.
맨 위 꼭짓점에서 출발해 한 줄씩 내려가 맨 아래 줄까지 이동합니다.
i 번째 줄의 j 번째 수에서는 바로 아래 줄의 j 번째 또는 j + 1 번째 수로만 내려갈 수 있습니다.
지나온 수들의 합이 가장 클 때 그 합을 return 하세요.

제한사항
- 1 ≤ len(triangle) ≤ 500
- len(triangle[i]) == i + 1
- 0 ≤ triangle[i][j] ≤ 9,999

입출력 예
triangle = [[5],
            [9, 6],
            [4, 6, 8],
            [0, 7, 1, 5]]   →  27   (5 → 9 → 6 → 7)
"""

SIGNATURE = "def solution(triangle: list[list[int]]) -> int:"

HINTS = [
    "매 줄에서 더 큰 쪽으로 내려가는 그리디는 틀립니다. 지금 작은 수 아래에 아주 큰 수가 숨어 있을 수 있습니다.",
    "모든 경로를 보면 2^(높이-1) 개 → 높이 500 이면 불가능. 각 칸까지의 '최대 합' 만 기억하면 됩니다.",
    "아래 줄부터 위로 올라오세요: dp[j] = triangle[i][j] + max(dp[j], dp[j+1]). 그러면 꼭대기 dp[0] 이 답이고 경계 처리도 필요 없습니다.",
]

TESTS = [
    {"input": [[[5], [9, 6], [4, 6, 8], [0, 7, 1, 5]]], "output": 27},
    {"input": [[[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]], "output": 30},
    {"input": [[[1]]], "output": 1},
    {"input": [[[1], [2, 3]]], "output": 4},
    {"input": [[[0], [0, 0], [0, 0, 0]]], "output": 0},
    {"input": [[[1], [9, 1], [1, 1, 1], [1, 1, 1, 100]]], "output": 103},
    {"input": [[[9999], [9999, 0], [9999, 0, 0]]], "output": 29997},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    tri = [[random.randint(0, 9999) for _ in range(i + 1)] for i in range(500)]
    return {"input": [tri], "output": None}


EXPLANATION = """
아이디어
- 각 칸에서 '여기서 바닥까지 내려갈 때 얻을 수 있는 최대 합' 은 아래 두 칸의 값만으로 정해집니다.
- 아래에서 위로 올라오면 모든 칸에 자식이 정확히 두 개 있어서 경계 조건이 사라집니다.

DP 레시피 (bottom-up, 아래 → 위)
1. 상태 정의: dp[j] = (현재 줄 i, j 번째 칸) 에서 바닥까지 내려가는 최대 합
2. 점화식:   dp[j] = triangle[i][j] + max(dp[j], dp[j+1])   (dp 는 i+1 번째 줄 값)
3. 초기값:   dp = 맨 아래 줄 복사본
4. 계산 순서: i = 높이-2 → 0, j = 0 → i  (dp[j] 갱신 시 dp[j+1] 은 아직 아래 줄 값)
5. 답:       dp[0]

  [5]                       dp 변화 (아래 → 위)
  [9, 6]                    줄3: [0, 7, 1, 5]
  [4, 6, 8]                 줄2: [4+7, 6+7, 8+5]   = [11, 13, 13]
  [0, 7, 1, 5]              줄1: [9+13, 6+13]      = [22, 19]
                            줄0: [5+22]            = [27]  ← 답

위 → 아래 방향으로 풀어도 됩니다.
- dp[i][j] = triangle[i][j] + max(dp[i-1][j-1], dp[i-1][j]) 이고, j == 0 과 j == i 는 부모가 하나뿐이라 따로 처리.
- 답은 마지막 줄의 max(dp[-1]).

복잡도: 시간 O(칸 수) = O(h^2), 공간 O(h)

면접/시험 포인트
- 그리디 반례: [[1], [9, 1], [1, 1, 1], [1, 1, 1, 100]]
  그리디는 둘째 줄에서 9 를 골라 1 + 9 + 1 + 1 = 12 (9 아래에서는 100 에 닿을 수 없음).
  정답은 오른쪽 끝을 따라 1 + 1 + 1 + 100 = 103. → "지금 큰 것" 이 "전체 최대" 를 보장하지 않습니다.
- 입력 triangle 을 직접 덮어쓰면 추가 공간 없이 풀 수 있지만, 면접에서는 '입력 변경 괜찮은지' 먼저 물어보세요.
- LeetCode 120 Triangle 은 최소 합 버전입니다. max ↔ min 만 바꾸면 됩니다.
"""


def reference(triangle):
    dp = triangle[-1][:]  # 맨 아래 줄에서 시작
    for i in range(len(triangle) - 2, -1, -1):
        row = triangle[i]
        for j in range(i + 1):
            # (i, j) 아래의 두 칸 중 더 큰 쪽을 선택
            dp[j] = row[j] + max(dp[j], dp[j + 1])
    return dp[0]


def brute_force(triangle):
    # 모든 경로를 탐색: O(2^h)
    h = len(triangle)

    def go(i, j):
        if i == h - 1:
            return triangle[i][j]
        return triangle[i][j] + max(go(i + 1, j), go(i + 1, j + 1))

    return go(0, 0)
