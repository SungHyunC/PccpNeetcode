import random
import string

TITLE = "Word Search II (단어 찾기 II)"
LEVEL = "Hard"
SOURCE = "LeetCode 212"
PATTERN = "단어들로 트라이를 만들고, 격자 DFS 를 트라이로 가지치기"

DESCRIPTION = """
영어 소문자가 적힌 m x n 격자 board 와 단어 목록 words 가 주어집니다.
격자에서 찾을 수 있는 단어를 모두 return 하세요 (순서는 상관없고, 같은 단어는 한 번만).

단어를 찾는 규칙
- 시작 칸은 아무 곳이나 됩니다.
- 다음 글자는 바로 위/아래/왼쪽/오른쪽 칸에 있어야 합니다 (대각선 불가).
- 한 단어 안에서 같은 칸을 두 번 쓸 수 없습니다.

제한사항
- 1 ≤ m, n ≤ 12
- 1 ≤ len(words) ≤ 20,000, 1 ≤ len(words[i]) ≤ 10
- words 의 단어는 모두 다릅니다.
- 효율성 테스트가 있습니다.

입출력 예
board = [["o","a","a","n"],
         ["e","t","a","e"],
         ["i","h","k","r"],
         ["i","f","l","v"]]
words = ["oath", "pea", "eat", "rain"]  →  ["eat", "oath"]

board = [["a","b"],["c","d"]], words = ["abcb"]  →  []
"""

SIGNATURE = "def solution(board: list[list[str]], words: list[str]) -> list[str]:"

HINTS = [
    "단어마다 따로 Word Search(격자 DFS)를 돌리면 단어 수 x 격자 크기 x 탐색 비용이 됩니다. 단어가 2만 개면 너무 느립니다.",
    "모든 단어를 트라이에 넣고, 격자 DFS 를 한 번만 하면서 '지금까지 만든 문자열이 트라이의 경로에 있는가'를 동시에 확인하세요. 트라이에 없는 경로는 바로 중단(가지치기)합니다.",
    "트라이의 단어 끝 노드에 단어 자체를 저장해 두면(node.word = 'oath') 문자열을 따로 이어 붙일 필요가 없습니다. 찾으면 결과에 넣고 node.word = None 으로 중복을 막습니다.",
    "방문 표시는 board[r][c] 를 '#' 으로 바꿨다가 돌아올 때 되돌리는 방식이 간단합니다. 찾은 뒤 자식이 없어진 트라이 노드를 지우면 더 빨라집니다.",
]

TESTS = [
    {
        "input": [
            [["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]],
            ["oath", "pea", "eat", "rain"],
        ],
        "output": ["eat", "oath"],
    },
    {"input": [[["a", "b"], ["c", "d"]], ["abcb"]], "output": []},
    {"input": [[["a"]], ["a", "b"]], "output": ["a"]},
    {"input": [[["a", "a"]], ["aaa"]], "output": []},
    {
        "input": [
            [["a", "b"], ["c", "d"]],
            ["ab", "cb", "ad", "bd", "ac", "ca", "da", "bc", "db", "abdc", "cdba", "acb", "abb"],
        ],
        "output": ["ab", "bd", "ac", "ca", "db", "abdc", "cdba"],
    },
    {"input": [[["a", "a"], ["a", "a"]], ["aa", "aaaa", "aaaaa"]], "output": ["aa", "aaaa"]},
    {
        "input": [[["s", "e", "e"], ["n", "d", "t"]], ["see", "seed", "send", "ten", "need", "eet", "tde", "dee"]],
        "output": ["see", "eet", "tde", "dee"],
    },
]

COMPARE = "unordered"

PERF_LIMIT = 1.5


def perf_case():
    m = n = 12
    board = [[random.choice("abcdefghijklmnoprstu") for _ in range(n)] for _ in range(m)]
    words = set()
    # 격자에서 실제로 만들 수 있는 단어 일부 + 무작위 단어 다수
    while len(words) < 300:
        r, c = random.randrange(m), random.randrange(n)
        path, seen = [board[r][c]], {(r, c)}
        for _ in range(random.randint(2, 9)):
            nxt = [(r + dr, c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                   if 0 <= r + dr < m and 0 <= c + dc < n and (r + dr, c + dc) not in seen]
            if not nxt:
                break
            r, c = random.choice(nxt)
            seen.add((r, c))
            path.append(board[r][c])
        words.add("".join(path))
    while len(words) < 20_000:
        words.add("".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(3, 10))))
    return {"input": [board, sorted(words)], "output": None}


EXPLANATION = """
핵심: 단어마다 격자를 탐색하지 말고, "격자 탐색 한 번 + 트라이로 모든 단어를 동시에 확인" 합니다.
트라이에 없는 접두사가 되는 순간 그 방향의 탐색을 멈추므로 가지치기가 강력합니다.

  words = [oath, eat]          board 에서 'o' → 'a' → 't' → 'h' 로 이동하며
       (root)                  트라이도 o → a → t → h 로 함께 내려감
       /    \\                  h 노드에 word = "oath" → 결과에 추가
      o      e                 'o' → 'e' 는 트라이에 o-e 경로가 없으므로 즉시 중단
      a      a
      t      t(eat)
      h(oath)

1. 모든 단어로 트라이 생성. 단어 끝 노드에 word 저장
2. 모든 칸 (r, c) 에서 dfs(r, c, root)
3. dfs: ch = board[r][c], 자식 ch 가 없으면 return
   - node = node.children[ch]
   - node.word 가 있으면 결과에 추가하고 None 으로 (중복 방지)
   - board[r][c] = '#' 로 방문 표시 → 4방향 dfs → 원래 문자로 복구
   - (최적화) 자식이 없어진 노드는 부모에서 삭제해 다시 들어오지 않게 함
4. 결과 반환

시간: 최악 O(m·n·4·3^(L-1)) (L = 최대 단어 길이) 이지만 트라이 가지치기로 실제로는 훨씬 적음
공간: O(총 단어 문자 수) + 재귀 깊이 O(L)
면접 포인트: Word Search I 을 단어마다 반복하는 풀이(brute_force)에서 출발해 "공통 접두사를 한 번에 탐색"하는
트라이 아이디어로 개선하는 과정을 설명하세요. 찾은 단어 제거(pruning)는 같은 단어를 여러 번 찾는 낭비도 막아 줍니다.
"""


def reference(board, words):
    class Node:
        __slots__ = ("children", "word")

        def __init__(self):
            self.children = {}
            self.word = None   # 이 노드에서 끝나는 단어

    root = Node()
    for w in words:
        node = root
        for ch in w:
            node = node.children.setdefault(ch, Node())
        node.word = w

    m, n = len(board), len(board[0])
    found = []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent.children.get(ch)
        if node is None:            # '#'(방문함) 이거나 트라이에 없는 경로 → 가지치기
            return
        if node.word is not None:
            found.append(node.word)
            node.word = None        # 같은 단어 중복 방지
        board[r][c] = "#"           # 방문 표시
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n:
                dfs(nr, nc, node)
        board[r][c] = ch            # 복구 (백트래킹)
        if not node.children and node.word is None:
            del parent.children[ch]  # 더 찾을 게 없는 가지는 잘라냄

    for r in range(m):
        for c in range(n):
            dfs(r, c, root)
    return found


def brute_force(board, words):
    # 단어마다 Word Search I 을 수행: 단어 수에 비례해 느려짐 → 효율성 실패
    m, n = len(board), len(board[0])

    def exist(word):
        def dfs(r, c, i):
            if i == len(word):
                return True
            if not (0 <= r < m and 0 <= c < n) or board[r][c] != word[i]:
                return False
            board[r][c] = "#"
            ok = dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1) or dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1)
            board[r][c] = word[i]
            return ok

        return any(dfs(r, c, 0) for r in range(m) for c in range(n))

    return [w for w in words if exist(w)]
