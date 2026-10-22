import random
import string

TITLE = "Implement Trie (트라이 구현)"
LEVEL = "Medium"
SOURCE = "LeetCode 208"
PATTERN = "문자 → 자식 노드 dict + 단어 끝 표시"

DESCRIPTION = """
문자열을 저장하고 빠르게 검색하는 트라이(Trie, 접두사 트리)를 구현하세요.

- Trie(): 빈 트라이를 만듭니다.
- insert(word): word 를 저장합니다. 반환값 없음.
- search(word): word 가 '단어로서' 저장되어 있으면 True, 아니면 False.
- startsWith(prefix): prefix 로 시작하는 단어가 하나라도 저장되어 있으면 True, 아니면 False.

[채점 방식] 클래스 설계 문제를 solution(commands, values) 로 바꿨습니다.
commands[i] 는 호출할 이름, values[i] 는 그 인자 리스트입니다.
각 호출의 반환값을 순서대로 담은 리스트를 return 하세요 (생성자와 insert 는 None).

제한사항
- 1 ≤ len(word), len(prefix) ≤ 20, 영어 소문자만
- 호출 횟수 ≤ 60,000 (효율성 테스트 있음)
- commands[0] 은 항상 "Trie"

입출력 예
commands = ["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
values   = [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
→ [None, None, True, False, True, None, True]
"""

SIGNATURE = "def solution(commands: list[str], values: list[list]) -> list:"

HINTS = [
    "뼈대: for cmd, args in zip(commands, values): 생성자면 obj = Trie(), 아니면 out.append(getattr(obj, cmd)(*args)).",
    "set 에 단어를 넣으면 search 는 O(1) 이지만 startsWith 는 모든 단어를 확인해야 합니다. 접두사를 공유하는 구조가 필요합니다.",
    "노드마다 children = {문자: 자식 노드} 와 is_end(여기서 끝나는 단어가 있는가) 를 둡니다. insert 는 없는 자식을 만들며 내려가고, 마지막 노드에 is_end = True.",
    "search 와 startsWith 는 같은 '접두사 따라 내려가기' 함수를 공유합니다. 끝까지 내려갔을 때 search 는 is_end 를, startsWith 는 노드 존재 여부만 봅니다.",
]

TESTS = [
    {
        "input": [
            ["Trie", "insert", "search", "search", "startsWith", "insert", "search"],
            [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]],
        ],
        "output": [None, None, True, False, True, None, True],
    },
    {
        "input": [["Trie", "search", "startsWith"], [[], ["a"], ["a"]]],
        "output": [None, False, False],
    },
    {
        "input": [
            ["Trie", "insert", "startsWith", "startsWith", "search"],
            [[], ["abc"], ["abc"], ["abcd"], ["ab"]],
        ],
        "output": [None, None, True, False, False],
    },
    {
        "input": [
            ["Trie", "insert", "insert", "search", "search"],
            [[], ["a"], ["a"], ["a"], ["b"]],
        ],
        "output": [None, None, None, True, False],
    },
    {
        "input": [
            ["Trie", "insert", "insert", "search", "search", "search", "startsWith", "startsWith"],
            [[], ["car"], ["card"], ["car"], ["card"], ["ca"], ["ca"], ["cards"]],
        ],
        "output": [None, None, None, True, True, False, True, False],
    },
    {
        "input": [
            ["Trie", "insert", "insert", "startsWith", "search", "search"],
            [[], ["zebra"], ["zoo"], ["z"], ["zo"], ["zoo"]],
        ],
        "output": [None, None, None, True, False, True],
    },
]


def _rand_word(lo, hi):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(lo, hi)))


PERF_LIMIT = 1.0


def perf_case():
    commands, values, words = ["Trie"], [[]], []
    for _ in range(20_000):
        w = _rand_word(4, 10)
        words.append(w)
        commands.append("insert")
        values.append([w])
    for _ in range(20_000):
        if random.random() < 0.5:
            w = random.choice(words)
            commands.append("startsWith")
            values.append([w[: random.randint(1, len(w))]])
        else:
            commands.append(random.choice(["search", "startsWith"]))
            values.append([_rand_word(3, 8)])
    return {"input": [commands, values], "output": None}


EXPLANATION = """
핵심: 단어들을 문자 단위로 쪼개 트리에 저장하고, 공통 접두사는 같은 경로를 공유합니다.

  insert: car, card, cat
        (root)
          c
          a
        /   \\
       r*    t*         * = is_end (여기서 끝나는 단어가 있음)
       d*

  search("ca")     → c → a 까지 갔지만 a 는 is_end 가 아님 → False
  startsWith("ca") → c → a 노드가 존재 → True

1. TrieNode: children(dict), is_end(bool)
2. insert: 루트에서 문자마다 자식이 없으면 만들고 내려감 → 마지막 노드 is_end = True
3. _walk(s): 문자마다 자식을 따라가다 없으면 None, 끝까지 가면 그 노드
4. search(w) = 노드가 있고 is_end, startsWith(p) = 노드가 있음

시간: 각 연산 O(L) (L = 문자열 길이), 공간: 저장된 전체 문자 수 O(총 길이)
면접 포인트: 해시셋과 비교해 "접두사 질의가 O(L)" 이라는 장점을 말하세요. set 으로 startsWith 를 하면 O(N·L) 입니다.
자식을 dict 대신 길이 26 배열로 두는 방법도 있습니다 (빠르지만 메모리 낭비).
파이썬에서는 중첩 dict 와 끝 표시 키("$")만으로도 짧게 구현할 수 있습니다 (alternative).
"""


def reference(commands, values):
    class TrieNode:
        __slots__ = ("children", "is_end")

        def __init__(self):
            self.children = {}   # 문자 → TrieNode
            self.is_end = False  # 여기서 끝나는 단어가 있는가

    class Trie:
        def __init__(self):
            self.root = TrieNode()

        def insert(self, word):
            node = self.root
            for ch in word:
                if ch not in node.children:
                    node.children[ch] = TrieNode()
                node = node.children[ch]
            node.is_end = True

        def _walk(self, s):
            # s 를 따라 내려간 마지막 노드 (중간에 끊기면 None)
            node = self.root
            for ch in s:
                node = node.children.get(ch)
                if node is None:
                    return None
            return node

        def search(self, word):
            node = self._walk(word)
            return node is not None and node.is_end

        def startsWith(self, prefix):
            return self._walk(prefix) is not None

    out, obj = [], None
    for cmd, args in zip(commands, values):
        if cmd == "Trie":
            obj = Trie()
            out.append(None)
        else:
            out.append(getattr(obj, cmd)(*args))
    return out


def alternative(commands, values):
    # 중첩 dict 트라이: 노드 = dict, 단어 끝은 "$" 키로 표시
    root, out = {}, []
    for cmd, args in zip(commands, values):
        if cmd == "Trie":
            root = {}
            out.append(None)
            continue
        s = args[0]
        if cmd == "insert":
            node = root
            for ch in s:
                node = node.setdefault(ch, {})
            node["$"] = True
            out.append(None)
            continue
        node = root
        for ch in s:
            node = node.get(ch)
            if node is None:
                break
        if node is None:
            out.append(False)
        else:
            out.append("$" in node if cmd == "search" else True)
    return out


def brute_force(commands, values):
    # set + startswith 전수 검사: startsWith 가 O(N·L) → 효율성 실패
    words, out = set(), []
    for cmd, args in zip(commands, values):
        if cmd == "Trie":
            words = set()
            out.append(None)
        elif cmd == "insert":
            words.add(args[0])
            out.append(None)
        elif cmd == "search":
            out.append(args[0] in words)
        else:
            out.append(any(w.startswith(args[0]) for w in words))
    return out
