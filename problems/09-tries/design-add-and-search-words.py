import random
import string

TITLE = "Design Add and Search Words Data Structure (와일드카드 단어 검색)"
LEVEL = "Medium"
SOURCE = "LeetCode 211"
PATTERN = "트라이 + '.' 에서만 모든 자식으로 분기하는 DFS"

DESCRIPTION = """
단어를 추가하고, 와일드카드가 포함된 패턴으로 검색하는 자료구조를 설계하세요.

- WordDictionary(): 빈 자료구조를 만듭니다.
- addWord(word): word 를 추가합니다. 반환값 없음.
- search(pattern): 저장된 단어 중 pattern 과 '길이가 같고' 모든 위치가 일치하는 단어가 있으면 True.
  pattern 의 '.' 은 아무 문자 하나와 일치합니다.

[채점 방식] 클래스 설계 문제를 solution(commands, values) 로 바꿨습니다.
commands[i] 는 호출할 이름, values[i] 는 그 인자 리스트입니다.
각 호출의 반환값을 순서대로 담은 리스트를 return 하세요 (생성자와 addWord 는 None).

제한사항
- 1 ≤ len(word), len(pattern) ≤ 25
- word 는 영어 소문자, pattern 은 영어 소문자와 '.'
- 하나의 pattern 에 '.' 은 최대 2개
- 호출 횟수 ≤ 20,000 (효율성 테스트 있음)

입출력 예
commands = ["WordDictionary", "addWord", "addWord", "addWord", "search", "search", "search", "search"]
values   = [[], ["cat"], ["cot"], ["cart"], ["c.t"], ["ca"], ["c..t"], ["...."]]
→ [None, None, None, None, True, False, True, True]
"""

SIGNATURE = "def solution(commands: list[str], values: list[list]) -> list:"

HINTS = [
    "단어 목록 전체를 매번 비교하면 search 하나에 O(N·L) 입니다. 트라이로 공통 접두사를 묶으세요.",
    "'.' 이 없으면 Implement Trie 의 search 와 같습니다. '.' 을 만나면 어느 자식으로 가야 할지 모르니, 모든 자식을 시도해야 합니다.",
    "dfs(node, i): i == len(pattern) 이면 node.is_end 반환. pattern[i] 가 '.' 이면 node 의 모든 자식 c 에 대해 dfs(c, i+1) 중 하나라도 True 면 True. 아니면 해당 문자 자식으로만 내려갑니다.",
]

TESTS = [
    {
        "input": [
            ["WordDictionary", "addWord", "addWord", "addWord", "search", "search", "search", "search"],
            [[], ["cat"], ["cot"], ["cart"], ["c.t"], ["ca"], ["c..t"], ["...."]],
        ],
        "output": [None, None, None, None, True, False, True, True],
    },
    {
        "input": [["WordDictionary", "search", "search"], [[], ["a"], ["."]]],
        "output": [None, False, False],
    },
    {
        "input": [
            ["WordDictionary", "addWord", "search", "search", "search"],
            [[], ["a"], ["."], [".."], ["a"]],
        ],
        "output": [None, None, True, False, True],
    },
    {
        "input": [
            ["WordDictionary", "addWord", "search", "search", "search", "search"],
            [[], ["abc"], ["ab"], ["ab."], ["abc."], [".bc"]],
        ],
        "output": [None, None, False, True, False, True],
    },
    {
        "input": [
            ["WordDictionary", "addWord", "addWord", "search", "search", "addWord", "search"],
            [[], ["bad"], ["dad"], ["b.d"], ["m.d"], ["mad"], ["m.d"]],
        ],
        "output": [None, None, None, True, False, None, True],
    },
    {
        "input": [
            ["WordDictionary", "addWord", "addWord", "search", "search", "search"],
            [[], ["xyz"], ["xya"], ["x.a"], ["..z"], ["x.b"]],
        ],
        "output": [None, None, None, True, True, False],
    },
]


def _rand_word(lo, hi):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(lo, hi)))


PERF_LIMIT = 1.0


def perf_case():
    commands, values, words = ["WordDictionary"], [[]], []
    for _ in range(10_000):
        w = _rand_word(3, 8)
        words.append(w)
        commands.append("addWord")
        values.append([w])
    for _ in range(10_000):
        w = list(random.choice(words) if random.random() < 0.6 else _rand_word(3, 8))
        for i in random.sample(range(len(w)), random.randint(0, 2)):
            w[i] = "."
        commands.append("search")
        values.append(["".join(w)])
    return {"input": [commands, values], "output": None}


EXPLANATION = """
핵심: 트라이 위에서 DFS. 일반 문자는 한 갈래로만, '.' 은 모든 자식으로 갈라집니다.

  addWord: cat, cot, cart
       (root)
         c
       /   \\
      a     o
     / \\     \\
    t*  r     t*
        t*
  search("c.t"): c → ('.': a, o 둘 다 시도) → a 의 t* (끝) → True
  search("ca") : c → a, 하지만 a 는 is_end 가 아님 → False

1. addWord: Implement Trie 의 insert 와 같음
2. search(pattern): dfs(root, 0)
   - i == len(pattern) → node.is_end
   - ch == '.' → any(dfs(child, i + 1) for child in node.children.values())
   - 그 외 → 자식 ch 가 있으면 dfs(child, i + 1), 없으면 False

시간: addWord O(L). search 는 '.' 이 없으면 O(L), '.' 이 d 개면 최악 O(26^d · L) (여기선 d ≤ 2)
공간: O(총 문자 수)
면접 포인트: "'.' 이 많으면 느려지지 않나요?" → 최악은 지수적이지만, 실제로는 트라이에 존재하는 경로로만 분기하므로
분기 수가 저장된 단어 수로 제한됩니다. 길이별로 단어를 나눠 두면 길이가 다른 단어를 아예 보지 않아 더 빨라집니다.
전수 비교(brute_force)는 search 마다 O(N·L) 이라 효율성 테스트에서 실패합니다.
"""


def reference(commands, values):
    class Node:
        __slots__ = ("children", "is_end")

        def __init__(self):
            self.children = {}
            self.is_end = False

    class WordDictionary:
        def __init__(self):
            self.root = Node()

        def addWord(self, word):
            node = self.root
            for ch in word:
                node = node.children.setdefault(ch, Node())
            node.is_end = True

        def search(self, pattern):
            def dfs(node, i):
                if i == len(pattern):
                    return node.is_end
                ch = pattern[i]
                if ch == ".":   # 와일드카드: 존재하는 모든 자식으로 분기
                    return any(dfs(child, i + 1) for child in node.children.values())
                child = node.children.get(ch)
                return child is not None and dfs(child, i + 1)

            return dfs(self.root, 0)

    out, obj = [], None
    for cmd, args in zip(commands, values):
        if cmd == "WordDictionary":
            obj = WordDictionary()
            out.append(None)
        else:
            out.append(getattr(obj, cmd)(*args))
    return out


def brute_force(commands, values):
    # 모든 단어와 직접 비교: search 하나에 O(N·L) → 효율성 실패
    words, out = [], []
    for cmd, args in zip(commands, values):
        if cmd == "WordDictionary":
            words = []
            out.append(None)
        elif cmd == "addWord":
            words.append(args[0])
            out.append(None)
        else:
            p = args[0]
            found = False
            for w in words:
                if len(w) == len(p) and all(pc == "." or pc == wc for pc, wc in zip(p, w)):
                    found = True
                    break
            out.append(found)
    return out
