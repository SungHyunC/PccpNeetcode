TITLE = "Robot Commands (격자 로봇 명령 실행)"
LEVEL = "Easy"
SOURCE = "PCCP 기출 유형 (프로그래머스 '공원 산책' 유형)"
PATTERN = "방향 벡터 dr/dc + 방향 회전 (d + 1) % 4 + 경계 검사"

DESCRIPTION = """
물류 창고 바닥이 rows × cols 격자로 나뉘어 있고, 왼쪽 위 칸이 (0, 0), 오른쪽 아래 칸이 (rows-1, cols-1) 입니다.
운반 로봇은 처음에 (0, 0) 칸에서 '동쪽(열 번호가 커지는 방향)' 을 바라보고 서 있습니다.

로봇은 명령 문자열 commands 를 앞에서부터 한 글자씩 실행합니다.
- 'F' : 바라보는 방향으로 한 칸 전진합니다. 단, 전진하면 격자 밖으로 나가는 경우 이 명령은 무시합니다.
- 'L' : 제자리에서 왼쪽으로 90도 회전합니다.
- 'R' : 제자리에서 오른쪽으로 90도 회전합니다.

모든 명령을 실행한 뒤 로봇의 위치를 [행, 열] 로 return 하세요.

제한사항
- 1 ≤ rows, cols ≤ 100
- 0 ≤ len(commands) ≤ 10,000
- commands 는 'F', 'L', 'R' 로만 이루어져 있습니다.

입출력 예
rows = 3, cols = 3, commands = "FFF"   →  [0, 2]   (세 번째 F 는 벽 때문에 무시)
rows = 3, cols = 3, commands = "RFF"   →  [2, 0]   (오른쪽으로 돌면 남쪽)
rows = 3, cols = 4, commands = "LFRFF" →  [0, 2]   (북쪽 전진은 무시됨)
"""

SIGNATURE = "def solution(rows: int, cols: int, commands: str) -> list[int]:"

HINTS = [
    "방향을 문자열('N','E' ...)로 if 문 분기하지 말고, 방향 번호 d 와 이동량 배열로 표현해 보세요.",
    "북·동·남·서 순서로 dr = [-1, 0, 1, 0], dc = [0, 1, 0, -1] 을 두면 오른쪽 회전은 d = (d + 1) % 4, 왼쪽 회전은 d = (d + 3) % 4 (또는 (d - 1) % 4) 입니다.",
    "'F' 는 nr, nc = r + dr[d], c + dc[d] 를 먼저 계산하고 0 ≤ nr < rows and 0 ≤ nc < cols 일 때만 이동하세요.",
]

TESTS = [
    {"input": [3, 3, "FFF"], "output": [0, 2]},
    {"input": [3, 3, "RFF"], "output": [2, 0]},
    {"input": [3, 4, "LFRFF"], "output": [0, 2]},
    {"input": [5, 5, ""], "output": [0, 0]},
    {"input": [1, 1, "FRFLFFRRF"], "output": [0, 0]},
    {"input": [4, 4, "FFFRFFFRFFFRFF"], "output": [1, 0]},
    {"input": [2, 5, "RRRRFFFFFFFFFF"], "output": [0, 4]},
    {"input": [3, 3, "RFLFLLLFFRRFRF"], "output": [1, 2]},
    {"input": [100, 100, "F" * 99 + "R" + "F" * 99 + "R" + "F" * 49], "output": [99, 50]},
]

EXPLANATION = """
핵심: 시뮬레이션의 3요소 — 방향 벡터, 방향 회전, 경계 검사.

  방향 번호 d:   0=북   1=동   2=남   3=서      (시계 방향 순서)
  dr          :  -1     0     1     0
  dc          :   0     1     0    -1
  오른쪽 회전: d = (d + 1) % 4,  왼쪽 회전: d = (d - 1) % 4  (파이썬은 음수 % 도 0~3)

1. r = c = 0, d = 1 (동쪽)
2. 명령마다:
   - 'L' / 'R' → d 갱신
   - 'F' → (nr, nc) 계산, 격자 안이면 이동
3. return [r, c]

  rows = 3, cols = 4, "LFRFF"
  L: 동→북   F: (-1,0) 밖 → 무시   R: 북→동   F: (0,1)   F: (0,2)  ⇒ [0, 2]

시간 O(len(commands)), 공간 O(1)
실전 포인트:
- 시계 방향 순서로 방향을 나열해 두면 회전이 % 4 한 줄로 끝납니다. 'UDLR' 처럼 절대 방향 명령이면
  move = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)} 딕셔너리를 쓰세요.
- '나가면 무시' 인지, '벽에 막힐 때까지 이동' 인지, '반대편으로 나옴(순환)' 인지 문제마다 다릅니다. 조건을 먼저 정리하세요.
- (행, 열) 과 (x, y) 를 섞으면 좌표가 뒤집힙니다. 문제의 좌표계를 메모해 두세요.
"""


def reference(rows, cols, commands):
    dr = [-1, 0, 1, 0]  # 북, 동, 남, 서 (시계 방향 순서)
    dc = [0, 1, 0, -1]
    r, c, d = 0, 0, 1  # (0, 0) 에서 동쪽을 바라봄
    for cmd in commands:
        if cmd == "R":
            d = (d + 1) % 4
        elif cmd == "L":
            d = (d - 1) % 4
        else:  # 'F'
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < rows and 0 <= nc < cols:  # 격자 안일 때만 이동
                r, c = nr, nc
    return [r, c]


def alternative(rows, cols, commands):
    # 복소수 트릭: 위치 = 행 + 열j, 방향에 1j 를 곱하면 회전
    # (행이 아래로 증가하는 좌표계에서는 동쪽 1j 에 -1j 를 곱하면 남쪽(1), 즉 오른쪽 회전)
    pos, heading = 0 + 0j, 1j
    for cmd in commands:
        if cmd == "R":
            heading *= -1j
        elif cmd == "L":
            heading *= 1j
        else:
            nxt = pos + heading
            if 0 <= nxt.real < rows and 0 <= nxt.imag < cols:
                pos = nxt
    return [int(pos.real), int(pos.imag)]
