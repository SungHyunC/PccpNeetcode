TITLE = "Rotate Matrix Border (행렬 테두리 회전)"
LEVEL = "Medium"
SOURCE = "PCCP 기출 유형 (프로그래머스 '행렬 테두리 회전하기' 유형)"
PATTERN = "직사각형 테두리 시뮬레이션 — 값 하나를 들고 한 칸씩 밀기"

DESCRIPTION = """
rows × columns 크기의 판에 1 부터 rows × columns 까지의 수가 왼쪽 위부터 행 순서대로 적혀 있습니다.
(r 행 c 열(1부터 시작)에는 (r - 1) × columns + c 가 적혀 있습니다.)

질의 [x1, y1, x2, y2] 는 (x1, y1) 을 왼쪽 위, (x2, y2) 를 오른쪽 아래 꼭짓점으로 하는 직사각형의
'테두리' 칸들을 시계 방향으로 한 칸씩 회전시키라는 뜻입니다. 직사각형 안쪽 칸은 움직이지 않습니다.

  예: 3 × 4 판, 질의 [1, 1, 2, 3]
     1  2  3  4            5  1  2  4
     5  6  7  8     →      6  7  3  8
     9 10 11 12            9 10 11 12
  테두리 1→2→3→7→6→5 가 시계 방향으로 한 칸씩 이동했습니다.

질의를 주어진 순서대로 적용하면서(이전 회전 결과가 유지됨), 각 회전에서 '움직인 수들 중 가장 작은 수' 를
차례대로 담아 return 하세요.

제한사항
- 2 ≤ rows, columns ≤ 100
- 1 ≤ len(queries) ≤ 10,000
- 1 ≤ x1 < x2 ≤ rows, 1 ≤ y1 < y2 ≤ columns (테두리 칸은 항상 4개 이상)
- 좌표는 1부터 시작합니다.

입출력 예
rows = 3, columns = 4, queries = [[1, 1, 2, 3]]                  →  [1]
rows = 3, columns = 3, queries = [[1, 1, 2, 2], [1, 1, 2, 2]]    →  [1, 1]
"""

SIGNATURE = "def solution(rows: int, columns: int, queries: list[list[int]]) -> list[int]:"

HINTS = [
    "판을 실제 2차원 리스트로 만들고 매 질의마다 테두리만 움직이면 됩니다. 질의당 O(테두리 길이) ≤ 400, 전체 400만 번 정도라 충분합니다.",
    "1부터 시작하는 좌표를 0부터로 바꾸세요 (x1 - 1 ...). 판 생성은 [[r * columns + c + 1 for c in range(columns)] for r in range(rows)].",
    "시계 방향 회전 = 왼쪽 위 값 하나를 임시 변수에 들고, '왼쪽 열을 위로 → 아래 행을 왼쪽으로 → 오른쪽 열을 아래로 → 위 행을 오른쪽으로' 당겨 온 뒤, 마지막 빈칸(위 행 두 번째 칸)에 임시 값을 넣습니다.",
    "다른 방법: 테두리 좌표를 시계 방향 순서로 리스트에 모으고, 값 리스트를 한 칸 회전(vals[-1:] + vals[:-1])해서 다시 써 넣기. 최솟값은 min(vals).",
]

TESTS = [
    {"input": [3, 4, [[1, 1, 2, 3]]], "output": [1]},
    {"input": [3, 3, [[1, 1, 2, 2], [1, 1, 2, 2]]], "output": [1, 1]},
    {"input": [2, 2, [[1, 1, 2, 2], [1, 1, 2, 2], [1, 1, 2, 2], [1, 1, 2, 2]]], "output": [1, 1, 1, 1]},
    {"input": [5, 5, [[2, 2, 4, 4], [1, 1, 3, 3], [3, 3, 5, 5]]], "output": [7, 1, 7]},
    {"input": [4, 6, [[1, 2, 3, 5], [2, 1, 4, 3], [1, 1, 4, 6]]], "output": [2, 7, 1]},
    {"input": [100, 100, [[1, 1, 100, 100]]], "output": [1]},
    {"input": [6, 5, [[2, 2, 5, 4], [3, 3, 6, 5], [5, 1, 6, 3], [1, 4, 2, 5]]], "output": [7, 9, 21, 4]},
    {"input": [3, 3, [[2, 2, 3, 3], [1, 2, 3, 3], [1, 1, 3, 3]]], "output": [5, 2, 1]},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    rows = columns = 100
    queries = []
    for _ in range(10_000):
        x1, x2 = sorted(random.sample(range(1, rows + 1), 2))
        y1, y2 = sorted(random.sample(range(1, columns + 1), 2))
        queries.append([x1, y1, x2, y2])
    return {"input": [rows, columns, queries], "output": None}


EXPLANATION = """
핵심: 시뮬레이션. 테두리 회전은 '값 하나를 들고 나머지를 한 칸씩 당겨 오기' 로 구현합니다.

  (0-index) top=x1, left=y1, bottom=x2, right=y2,  temp = board[top][left]

   ┌→→→→┐       당기는 순서 (덮어쓰기 순서가 중요!)
   ↑    ↓       1) 왼쪽 열: 아래 값을 위로      board[r][left]  = board[r+1][left]
   ↑    ↓       2) 아래 행: 오른쪽 값을 왼쪽으로  board[bottom][c] = board[bottom][c+1]
   └←←←←┘       3) 오른쪽 열: 위 값을 아래로    board[r][right] = board[r-1][right]
                4) 위 행: 왼쪽 값을 오른쪽으로   board[top][c]   = board[top][c-1]
                5) board[top][left+1] = temp

  이렇게 '이동 방향과 반대 순서로 당겨 오면' 아직 읽지 않은 값을 덮어쓰지 않습니다.
  각 단계에서 옮기는 값으로 최솟값을 갱신합니다.

시간 O(Q · (rows + columns)), 공간 O(rows · columns)
실전 포인트:
- 1-index ↔ 0-index 변환을 맨 처음 한 번만 하세요. 중간에 섞으면 디버깅이 매우 어렵습니다.
- 반복문의 range 방향(증가/감소)과 끝값을 손으로 2×2, 2×3 예제에 대입해 확인하세요.
- 좌표 리스트 방식(alternative)은 코드가 조금 길지만 덮어쓰기 순서를 고민할 필요가 없어 실수가 적습니다.
"""


def reference(rows, columns, queries):
    board = [[r * columns + c + 1 for c in range(columns)] for r in range(rows)]
    answer = []
    for x1, y1, x2, y2 in queries:
        top, left, bottom, right = x1 - 1, y1 - 1, x2 - 1, y2 - 1  # 0-index 로 변환
        temp = board[top][left]
        smallest = temp
        for r in range(top, bottom):  # 1) 왼쪽 열: 아래 → 위로 당김
            board[r][left] = board[r + 1][left]
            smallest = min(smallest, board[r][left])
        for c in range(left, right):  # 2) 아래 행: 오른쪽 → 왼쪽으로 당김
            board[bottom][c] = board[bottom][c + 1]
            smallest = min(smallest, board[bottom][c])
        for r in range(bottom, top, -1):  # 3) 오른쪽 열: 위 → 아래로 당김
            board[r][right] = board[r - 1][right]
            smallest = min(smallest, board[r][right])
        for c in range(right, left + 1, -1):  # 4) 위 행: 왼쪽 → 오른쪽으로 당김
            board[top][c] = board[top][c - 1]
            smallest = min(smallest, board[top][c])
        board[top][left + 1] = temp  # 5) 들고 있던 값 내려놓기
        answer.append(smallest)
    return answer


def alternative(rows, columns, queries):
    # 테두리 좌표를 시계 방향으로 모은 뒤 값 리스트를 한 칸 회전
    board = [[r * columns + c + 1 for c in range(columns)] for r in range(rows)]
    answer = []
    for x1, y1, x2, y2 in queries:
        t, l, b, r = x1 - 1, y1 - 1, x2 - 1, y2 - 1
        coords = [(t, c) for c in range(l, r)]          # 위 행 (왼 → 오)
        coords += [(row, r) for row in range(t, b)]     # 오른쪽 열 (위 → 아래)
        coords += [(b, c) for c in range(r, l, -1)]     # 아래 행 (오 → 왼)
        coords += [(row, l) for row in range(b, t, -1)]  # 왼쪽 열 (아래 → 위)
        vals = [board[i][j] for i, j in coords]
        answer.append(min(vals))
        vals = vals[-1:] + vals[:-1]  # 시계 방향 = 다음 좌표로 한 칸씩 이동
        for (i, j), v in zip(coords, vals):
            board[i][j] = v
    return answer
