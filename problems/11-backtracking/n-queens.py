TITLE = "N-Queens (N-퀸, 해의 개수)"
LEVEL = "Hard"
SOURCE = "LeetCode 51/52 · 프로그래머스 Lv.2 'N-Queen' 유형"
PATTERN = "행마다 퀸 하나 + 열/대각선 집합으로 O(1) 충돌 검사"

DESCRIPTION = """
n × n 체스판에 퀸 n 개를 놓으려고 합니다. 퀸은 같은 행, 같은 열, 같은 대각선에 있는 말을 공격할 수 있습니다.
어떤 두 퀸도 서로 공격하지 못하도록 n 개를 모두 놓는 방법의 수를 return 하세요.

(변형) 면접에서는 가능한 배치를 모두 그려서 return 하라고 하기도 합니다.
예: n = 4 → [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]
이 저장소에서는 출력을 단순하게 하려고 '개수' 만 return 합니다. 해설의 board_variant 를 참고하세요.

제한사항
- 1 ≤ n ≤ 10

입출력 예
n = 4  →  2
n = 1  →  1
n = 3  →  0
"""

SIGNATURE = "def solution(n: int) -> int:"

HINTS = [
    "한 행에는 퀸이 정확히 하나 들어갑니다. 그러니 '각 행의 퀸을 몇 번 열에 둘지' 만 정하면 됩니다 → 행 단위 백트래킹.",
    "(r, c) 에 퀸을 놓을 수 있는지 매번 판 전체를 확인하면 느립니다. 같은 대각선의 칸은 r - c 가 같고, 반대 대각선의 칸은 r + c 가 같습니다.",
    "cols, diag(r - c), anti(r + c) 세 개의 집합을 두고, 셋 중 하나라도 이미 있으면 건너뛰세요. 놓을 때 세 집합에 추가하고 돌아올 때 제거합니다.",
    "모든 열 배치를 itertools.permutations 로 만들고 대각선을 검사하는 방법은 n! 개를 다 보므로 n = 10 에서 너무 느립니다. 충돌하는 순간 바로 가지치기하는 것이 백트래킹의 힘입니다.",
]

TESTS = [
    {"input": [1], "output": 1},
    {"input": [2], "output": 0},
    {"input": [3], "output": 0},
    {"input": [4], "output": 2},
    {"input": [5], "output": 10},
    {"input": [6], "output": 4},
    {"input": [7], "output": 40},
    {"input": [8], "output": 92},
]

PERF_LIMIT = 1.0


def perf_case():
    return {"input": [10], "output": 724}


EXPLANATION = """
핵심: 행 r 마다 퀸 하나를 놓는 백트래킹. 충돌 검사를 집합 3개로 O(1) 에 합니다.

대각선 번호 매기기 (n = 4)
  r - c (↘ 대각선)        r + c (↙ 대각선)
   0 -1 -2 -3              0  1  2  3
   1  0 -1 -2              1  2  3  4
   2  1  0 -1              2  3  4  5
   3  2  1  0              3  4  5  6
→ 같은 숫자 = 같은 대각선

n = 4 의 해 하나:  . Q . .    cols = {1, 3, 0, 2}
                   . . . Q    r-c  = {-1, -2, 2, 1}
                   Q . . .    r+c  = {1, 4, 2, 5}
                   . . Q .

1. dfs(r): r == n 이면 해 하나 완성 → count += 1
2. c = 0..n-1: c in cols or r-c in diag or r+c in anti 이면 건너뜀 (가지치기)
3. 세 집합에 추가 → dfs(r+1) → 세 집합에서 제거

시간 O(n!) 상한 (첫 행 n 가지, 둘째 행 최대 n-1 가지 ...), 실제로는 가지치기로 훨씬 적음
공간 O(n)

면접 포인트
- 판 전체를 2차원 배열로 들고 매번 행/열/대각선을 훑으면 검사가 O(n) → 집합으로 O(1) 로 개선했다고 설명하세요.
- 비트마스크 최적화(alternative): cols, diag, anti 를 정수 비트로 관리하고
  available = ~(cols | diag | anti) & full, 가장 낮은 비트 = available & -available 로 빠르게 순회합니다.
- 배치를 그려서 반환하는 변형(LeetCode 51)은 queens[r] = c 배열을 저장했다가
  ["." * c + "Q" + "." * (n - c - 1) for c in queens] 로 바꾸면 됩니다 (아래 board_variant 참고).
- 프로그래머스 'N-Queen' (Lv.2) 도 n ≤ 12 개수 세기로 같은 풀이입니다.
"""


def reference(n):
    cols, diag, anti = set(), set(), set()
    count = 0

    def dfs(r):
        nonlocal count
        if r == n:
            count += 1
            return
        for c in range(n):
            if c in cols or (r - c) in diag or (r + c) in anti:
                continue                    # 공격받는 칸 → 가지치기
            cols.add(c); diag.add(r - c); anti.add(r + c)
            dfs(r + 1)
            cols.remove(c); diag.remove(r - c); anti.remove(r + c)

    dfs(0)
    return count


def alternative(n):
    # 비트마스크 버전: 비트 i 가 1 이면 i 번 열이 막혀 있음
    full = (1 << n) - 1

    def dfs(cols, diag, anti):
        if cols == full:
            return 1
        total = 0
        available = full & ~(cols | diag | anti)
        while available:
            bit = available & -available    # 가장 낮은 1 비트
            available -= bit
            # 다음 행으로 내려가면 대각선 제약이 한 칸씩 이동
            total += dfs(cols | bit, ((diag | bit) << 1) & full, (anti | bit) >> 1)
        return total

    return dfs(0, 0, 0)


def brute_force(n):
    # 모든 열 순열을 만들고 대각선만 검사: O(n! · n^2) → n = 10 이면 시간 초과
    from itertools import permutations

    count = 0
    for perm in permutations(range(n)):
        if all(abs(perm[i] - perm[j]) != j - i for i in range(n) for j in range(i + 1, n)):
            count += 1
    return count


def board_variant(n):
    """(참고용) LeetCode 51: 가능한 배치를 문자열 판으로 모두 반환."""
    boards, queens = [], []
    cols, diag, anti = set(), set(), set()

    def dfs(r):
        if r == n:
            boards.append(["." * c + "Q" + "." * (n - c - 1) for c in queens])
            return
        for c in range(n):
            if c in cols or (r - c) in diag or (r + c) in anti:
                continue
            queens.append(c); cols.add(c); diag.add(r - c); anti.add(r + c)
            dfs(r + 1)
            queens.pop(); cols.remove(c); diag.remove(r - c); anti.remove(r + c)

    dfs(0)
    return boards
