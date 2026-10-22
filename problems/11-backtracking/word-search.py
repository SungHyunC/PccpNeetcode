TITLE = "Word Search (단어 찾기)"
LEVEL = "Medium"
SOURCE = "LeetCode 79"
PATTERN = "격자 백트래킹 + 방문 표시 되돌리기 + 가지치기"

DESCRIPTION = """
알파벳 대문자가 적힌 R × C 격자 board 와 문자열 word 가 주어집니다.
격자에서 상하좌우로 인접한 칸을 차례로 이어 word 를 만들 수 있으면 True, 아니면 False 를 return 하세요.
한 단어를 만들 때 같은 칸을 두 번 이상 사용할 수 없습니다.

제한사항
- 1 ≤ R, C ≤ 6
- 1 ≤ len(word) ≤ 15
- board 와 word 는 영어 대문자로만 이루어져 있습니다.

입출력 예
board = [["C","A","T","S"],
         ["O","R","E","A"],
         ["D","E","N","T"]]
word = "CARE"  →  True    (C → A → R → E)
word = "CODE"  →  True    (왼쪽 열을 따라 C → O → D, 오른쪽 E)
word = "CORD"  →  False
"""

SIGNATURE = "def solution(board: list[list[str]], word: str) -> bool:"

HINTS = [
    "모든 칸을 시작점으로 시도하고, 시작점에서 상하좌우로 한 글자씩 맞춰 나가는 DFS 를 하세요.",
    "dfs(r, c, i): board[r][c] 가 word[i] 와 같은지 확인 → 같으면 이웃으로 i + 1 을 찾으러 갑니다. i == len(word) 면 성공.",
    "같은 칸 재사용을 막으려면 들어갈 때 board[r][c] = '#' 으로 표시하고, 돌아올 때 원래 글자로 되돌려 놓으세요 (백트래킹).",
    "효율성: 탐색 전에 word 의 글자 수가 board 에 충분히 있는지 Counter 로 먼저 확인하세요. 또 word 의 첫 글자가 마지막 글자보다 board 에 더 많으면 word 를 뒤집어서 찾으면 시작점이 줄어듭니다.",
]

_BOARD = [
    ["C", "A", "T", "S"],
    ["O", "R", "E", "A"],
    ["D", "E", "N", "T"],
]

TESTS = [
    {"input": [_BOARD, "CARE"], "output": True},
    {"input": [_BOARD, "CODE"], "output": True},
    {"input": [_BOARD, "CORD"], "output": False},
    {"input": [_BOARD, "SAT"], "output": True},
    {"input": [_BOARD, "TEN"], "output": True},
    {"input": [_BOARD, "CAC"], "output": False},
    {"input": [[["A"]], "A"], "output": True},
    {"input": [[["A"]], "AA"], "output": False},
    {"input": [[["A", "B"]], "ABA"], "output": False},
    {"input": [[["A", "B"], ["D", "C"]], "ABCDA"], "output": False},
    {"input": [[["A", "B"], ["D", "C"]], "BCDA"], "output": True},
]

PERF_LIMIT = 1.0


def perf_case():
    # 모든 칸이 'A' 인데 'B' 가 없는 최악의 경우: 가지치기 없이 탐색하면 경로 수가 폭발합니다.
    board = [["A"] * 6 for _ in range(6)]
    return {"input": [board, "A" * 14 + "B"], "output": False}


EXPLANATION = """
핵심: 격자에서의 백트래킹. "방문 표시 → 탐색 → 표시 해제" 가 순열의 used[i] 와 같은 역할입니다.

board            word = "CARE"
C A T S          (0,0)C → (0,1)A → (1,1)R → (1,2)E ✔
O R E A
D E N T          탐색 중 지나간 칸은 '#' 로 바꿔 두고, 돌아올 때 복구

1. (가지치기) Counter(word) 의 각 글자가 board 에 충분히 있는지 확인 → 부족하면 바로 False
2. (가지치기) word[0] 이 word[-1] 보다 흔하면 word 를 뒤집기 → 시작 후보가 줄어듦
3. 모든 (r, c) 에서 dfs(r, c, 0)
4. dfs: 범위 밖 / 글자 불일치 → False. 마지막 글자까지 맞으면 True.
   board[r][c] = '#' → 4방향 재귀 → board[r][c] 복구

시간 O(R · C · 3^L) — 첫 칸 이후로는 왔던 방향을 제외한 3방향만 가능 (L = len(word))
공간 O(L) 재귀 깊이

면접 포인트
- 방문 표시를 별도 visited 집합 대신 board 를 직접 바꾸는 이유: 추가 메모리 없이 O(1) 확인.
  단, 반드시 복구해야 다른 시작점 탐색이 망가지지 않습니다.
- 효율성 테스트는 board 가 전부 'A' 이고 word 끝에 board 에 없는 'B' 가 붙은 경우입니다.
  가지치기가 없으면 길이 14 의 모든 경로를 다 시도하므로 매우 느립니다.
- 여러 단어를 한꺼번에 찾으면 Word Search II → 트라이(Trie) + 백트래킹으로 이어집니다.
"""


def reference(board, word):
    from collections import Counter

    R, C = len(board), len(board[0])

    # 가지치기 1: 글자 수가 부족하면 탐색할 필요가 없음
    have = Counter(ch for row in board for ch in row)
    need = Counter(word)
    if any(have[ch] < cnt for ch, cnt in need.items()):
        return False
    # 가지치기 2: 더 드문 글자 쪽에서 시작하도록 뒤집기
    if have[word[0]] > have[word[-1]]:
        word = word[::-1]

    def dfs(r, c, i):
        if board[r][c] != word[i]:
            return False
        if i == len(word) - 1:
            return True
        tmp = board[r][c]
        board[r][c] = "#"                       # 방문 표시 (choose)
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < R and 0 <= nc < C and dfs(nr, nc, i + 1):
                board[r][c] = tmp
                return True
        board[r][c] = tmp                       # 복구 (unchoose)
        return False

    return any(dfs(r, c, 0) for r in range(R) for c in range(C))


def brute_force(board, word):
    # 가지치기 없는 기본 백트래킹 (정답은 맞지만 최악의 경우 매우 느림)
    R, C = len(board), len(board[0])

    def dfs(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < R and 0 <= c < C) or board[r][c] != word[i]:
            return False
        tmp = board[r][c]
        board[r][c] = "#"
        found = dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1)
        board[r][c] = tmp
        return found

    return any(dfs(r, c, 0) for r in range(R) for c in range(C))
