TITLE = "Board Damage with 2D Difference Array (2차원 차분 배열로 성벽 피해 계산)"
LEVEL = "Hard"
SOURCE = "PCCP 기출 유형 (프로그래머스 '파괴되지 않은 건물' 유형)"
PATTERN = "2차원 차분 배열(imos): 직사각형 갱신 O(1) + 누적합 두 번"

DESCRIPTION = """
성벽이 N × M 개의 블록으로 이루어져 있고, board[r][c] 는 각 블록의 내구도입니다.
전투 중 다음과 같은 효과가 skill 목록 순서대로 일어납니다.

skill[i] = [type, r1, c1, r2, c2, degree]
- (r1, c1) 을 왼쪽 위, (r2, c2) 를 오른쪽 아래 꼭짓점으로 하는 직사각형 안의 모든 블록에 적용됩니다.
  (0부터 시작하는 좌표, 양 끝 포함)
- type = 1 : 적의 투석 공격. 내구도가 degree 만큼 감소합니다.
- type = 2 : 아군의 보수 작업. 내구도가 degree 만큼 증가합니다.

내구도가 0 이하로 떨어진 블록도 이후 보수 작업으로 다시 1 이상이 될 수 있습니다. (블록은 사라지지 않음)
모든 효과가 끝난 뒤 내구도가 1 이상인 블록의 개수를 return 하세요.

제한사항
- 1 ≤ N, M ≤ 1,000
- 1 ≤ board[r][c] ≤ 1,000
- 1 ≤ len(skill) ≤ 250,000
- 0 ≤ r1 ≤ r2 < N, 0 ≤ c1 ≤ c2 < M, 1 ≤ degree ≤ 500
- 효율성 테스트: 직사각형마다 칸을 하나씩 갱신하면 O(K · N · M) 으로 시간 초과입니다.

입출력 예
board = [[5, 5, 5], [5, 5, 5], [5, 5, 5]]
skill = [[1, 0, 0, 1, 1, 5], [1, 1, 1, 2, 2, 2], [2, 0, 0, 0, 0, 3]]
→ 6

  공격 (0,0)~(1,1) -5     공격 (1,1)~(2,2) -2     보수 (0,0)~(0,0) +3
  0 0 5                  0  0 5                 3  0 5
  0 0 5         →        0 -2 3        →        0 -2 3
  5 5 5                  5  3 3                 5  3 3
  1 이상인 블록: 3, 5, 3, 5, 3, 3 → 6개
"""

SIGNATURE = "def solution(board: list[list[int]], skill: list[list[int]]) -> int:"

HINTS = [
    "skill 25만 개 × 직사각형 최대 100만 칸 → 직접 갱신은 불가능합니다. '마지막 결과만 필요하다' 는 점에 주목하세요.",
    "1차원에서 [l, r] 에 v 를 더하는 것은 diff[l] += v, diff[r+1] -= v 로 표시하고 마지막에 누적합 한 번이면 됩니다. 이것을 2차원으로 확장해 보세요.",
    "2차원: diff[r1][c1] += v, diff[r1][c2+1] -= v, diff[r2+1][c1] -= v, diff[r2+1][c2+1] += v (크기 (N+1) × (M+1)). 공격이면 v = -degree.",
    "모든 skill 을 표시한 뒤 '행 방향 누적합' → '열 방향 누적합' 을 하면 각 칸의 총 변화량이 나옵니다. board 에 더해 1 이상인 칸을 세세요.",
]

TESTS = [
    {"input": [[[5, 5, 5], [5, 5, 5], [5, 5, 5]], [[1, 0, 0, 1, 1, 5], [1, 1, 1, 2, 2, 2], [2, 0, 0, 0, 0, 3]]],
     "output": 6},
    {"input": [[[1]], [[1, 0, 0, 0, 0, 1]]], "output": 0},
    {"input": [[[1]], [[1, 0, 0, 0, 0, 1], [2, 0, 0, 0, 0, 1]]], "output": 1},
    {"input": [[[3, 3, 3, 3]], [[1, 0, 1, 0, 2, 3]]], "output": 2},
    {"input": [[[2], [2], [2]], [[2, 0, 0, 2, 0, 1], [1, 1, 0, 2, 0, 3]]], "output": 1},
    {"input": [[[10, 10], [10, 10]], [[1, 0, 0, 1, 1, 9]]], "output": 4},
    {"input": [[[10, 10], [10, 10]], [[1, 0, 0, 1, 1, 9], [1, 0, 0, 1, 1, 1], [2, 1, 1, 1, 1, 1]]], "output": 1},
    {"input": [[[4, 7, 2, 9], [6, 1, 8, 3], [5, 5, 5, 5]],
               [[1, 0, 0, 2, 3, 2], [2, 1, 1, 2, 2, 4], [1, 0, 2, 1, 3, 6], [2, 0, 0, 0, 0, 1]]],
     "output": 10},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    n = m = 300
    board = [[random.randint(1, 1000) for _ in range(m)] for _ in range(n)]
    skill = []
    for _ in range(100_000):
        r1, c1 = random.randint(0, 99), random.randint(0, 99)
        r2, c2 = random.randint(200, n - 1), random.randint(200, m - 1)
        skill.append([random.randint(1, 2), r1, c1, r2, c2, random.randint(1, 500)])
    return {"input": [board, skill], "output": None}


EXPLANATION = """
핵심: 2차원 차분 배열(difference array, 일본식 이름 'imos 법'). 직사각형 갱신을 꼭짓점 4곳 표시로 바꾸고, 마지막에 누적합 두 번으로 복원합니다.

[1차원 복습]  [1, 3] 에 +v:   diff:  0 +v  0  0 -v      → 누적합:  0 v v v 0

[2차원] (r1,c1)~(r2,c2) 에 +v 를 더하려면 네 꼭짓점만 표시:
          c1        c2+1
   r1    +v   ...   -v
   r2+1  -v   ...   +v

  예: 4×4 에서 (1,1)~(2,2) 에 +3
   표시(diff)           행 방향 누적합        열 방향 누적합(최종)
   0  0  0  0  0        0  0  0  0  0        0  0  0  0  0
   0 +3  0 -3  0   →    0  3  3  0  0   →    0  3  3  0  0
   0  0  0  0  0        0  0  0  0  0        0  3  3  0  0
   0 -3  0 +3  0        0 -3 -3  0  0        0  0  0  0  0

1. diff = (N+1) × (M+1) 0 행렬
2. skill 마다 v = -degree(공격) 또는 +degree(보수), 꼭짓점 4곳에 표시  → O(K)
3. 각 행에서 왼쪽→오른쪽 누적합, 이어서 각 열에서 위→아래 누적합       → O(N·M)
4. board[r][c] + diff[r][c] ≥ 1 인 칸 개수

시간 O(K + N·M), 공간 O(N·M)    (직접 갱신은 O(K·N·M) ≈ 2.5 × 10^11)
실전 포인트:
- 차분 배열 크기를 (N+1) × (M+1) 로 잡아야 r2+1, c2+1 인덱스가 안전합니다.
- 2차원 리스트는 반드시 [[0] * (M + 1) for _ in range(N + 1)] 로 만드세요. [[0] * (M+1)] * (N+1) 은 모든 행이 같은 리스트입니다.
- 누적합을 '행 방향 → 열 방향' 두 번 해야 합니다. 한 방향만 하면 오답.
- 이 문제처럼 '갱신은 많고 조회는 마지막에 한 번' 이면 차분 배열, '갱신은 없고 구간 합 조회가 많으면' 누적합(prefix sum)입니다.
"""


def reference(board, skill):
    n, m = len(board), len(board[0])
    diff = [[0] * (m + 1) for _ in range(n + 1)]  # 한 칸씩 여유
    for kind, r1, c1, r2, c2, degree in skill:
        v = -degree if kind == 1 else degree
        diff[r1][c1] += v  # 직사각형 시작
        diff[r1][c2 + 1] -= v  # 오른쪽 경계 밖에서 상쇄
        diff[r2 + 1][c1] -= v  # 아래쪽 경계 밖에서 상쇄
        diff[r2 + 1][c2 + 1] += v  # 두 번 빼진 부분 복구
    # 1) 행 방향 누적합
    for row in diff:
        for c in range(1, m + 1):
            row[c] += row[c - 1]
    # 2) 열 방향 누적합
    for r in range(1, n + 1):
        prev, cur = diff[r - 1], diff[r]
        for c in range(m + 1):
            cur[c] += prev[c]
    # 3) 1 이상인 칸 세기
    count = 0
    for r in range(n):
        b, d = board[r], diff[r]
        for c in range(m):
            if b[c] + d[c] >= 1:
                count += 1
    return count


def brute_force(board, skill):
    # 직사각형의 모든 칸을 직접 갱신: O(K · N · M)
    board = [row[:] for row in board]
    for kind, r1, c1, r2, c2, degree in skill:
        v = -degree if kind == 1 else degree
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                board[r][c] += v
    return sum(1 for row in board for x in row if x >= 1)
