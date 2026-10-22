# 09. 트라이 (Trie)

> 문자열을 한 글자씩 쪼개 트리에 저장해 **공통 접두사(prefix)를 공유**하는 자료구조. "이 접두사로 시작하는 단어가 있나/몇 개인가?" 를 문자열 길이 L 에 비례하는 O(L) 로 답합니다. 단어가 많고 질의도 많을 때, 그리고 격자·와일드카드 탐색을 가지치기할 때 씁니다.

## 이런 문제에서 떠올리세요

- "접두사로 시작하는", "자동 완성", "startsWith" → **트라이**
- 단어 목록이 크고(N ≥ 10⁴) 질의도 많아서, 질의마다 전체 단어를 훑으면 O(N·Q) 로 시간 초과 → **미리 트라이로 가공**
- 와일드카드 `.` / `?` 가 있는 패턴 검색 → **트라이 + DFS 분기**
- 격자에서 여러 단어를 동시에 찾기 (Word Search II, Boggle) → **단어 트라이로 DFS 가지치기**
- "접두사가 같은 단어 수" → **노드마다 count 저장**
- 전화번호 목록에서 "어떤 번호가 다른 번호의 접두사인가" → 트라이 (또는 정렬 후 이웃 비교)
- 정수 XOR 최댓값 (Maximum XOR) → **비트 트라이** (0/1 두 자식)
- 입력 크기 힌트: 전체 문자 수 ΣL ≤ 10⁶ 정도면 트라이 노드 수도 그 이하 → 메모리 OK

> 프로그래머스에는 **가사 검색(2020 카카오), 자동완성(2018 카카오), 전화번호 목록** 같은 트라이 유형이 있습니다. 미국 면접에서는 Implement Trie, Add and Search Word, Word Search II 가 단골입니다.

## 핵심 개념

### 1) 구조

단어 `car`, `card`, `cat`, `do` 를 넣은 트라이:

```
            (root)
           /      \
          c        d
          |        |
          a        o*
        /   \
       r*    t*            * = is_end (여기서 끝나는 단어가 있음)
       |
       d*
```

- 루트는 빈 문자열. 루트에서 어떤 노드까지의 경로가 곧 접두사
- 노드 = `children` (문자 → 자식 노드) + `is_end` (단어의 끝인가)
- `car` 와 `card` 는 `c-a-r` 경로를 **공유** → 메모리 절약 + 접두사 질의가 빠름
- `is_end` 가 필요한 이유: `car` 를 넣지 않고 `card` 만 넣었다면 `search("car")` 는 False 여야 함

### 2) 기본 연산 동작

```
insert("cab")                 search("ca")             startsWith("ca")
root → c (있음)               root → c → a             root → c → a
     → a (있음)               a.is_end == False        노드가 존재함
     → b (없음 → 새로 만듦)    → False                  → True
b.is_end = True
```

### 3) 노드에 정보 붙이기

트라이 노드에 필요한 정보를 더 저장하면 응용 범위가 넓어집니다.

| 붙이는 정보 | 용도 | 예 |
|---|---|---|
| `is_end` | 단어 존재 여부 | Implement Trie |
| `word` (단어 자체) | 찾은 단어를 바로 꺼내기 | Word Search II |
| `count` (지나간 단어 수) | 접두사가 같은 단어 개수 | 가사 검색, 자동완성 |
| `best` / 정렬된 상위 k 개 | 접두사별 추천 | Search Suggestions System |

```
count 를 붙인 트라이 (frodo, front, frost, frame)
  root(4) ─ f(4) ─ r(4) ─┬─ o(3) ─┬─ d(1) ─ o(1)
                         │        ├─ n(1) ─ t(1)
                         │        └─ s(1) ─ t(1)
                         └─ a(1) ─ m(1) ─ e(1)
  "fro" 로 시작하는 단어 수 = o 노드의 count = 3
```

### 4) 와일드카드 DFS

```
pattern = "c.t"
  root ─c→ (c) ─ '.' → 모든 자식 {a, o} 각각 시도 ─t→ is_end?
```

일반 문자는 한 갈래, `.` 는 존재하는 모든 자식으로 갈라집니다. 트라이에 없는 경로는 시도조차 하지 않으므로, 단어 목록 전체와 비교하는 것보다 훨씬 빠릅니다.

### 5) 트라이 vs 해시셋 vs 정렬 + 이분 탐색

| 질의 | set | 트라이 | 정렬 + bisect |
|---|---|---|---|
| 정확히 일치 | O(L) 평균 | O(L) | O(L log N) |
| 접두사 존재/개수 | O(N·L) | O(L) | O(L log N) |
| 와일드카드 | O(N·L) | 경로 수만큼 | 어려움 |
| 구현 난이도 | 쉬움 | 보통 | 쉬움 |

> 파이썬에서는 "정렬 + bisect" 가 의외로 빠르고 짧습니다. 접두사 개수만 필요하면 `bisect_left(arr, p + '{') - bisect_left(arr, p)` 한 줄로 끝납니다 (`'{'` 는 `'z'` 다음 문자).

## 코드 템플릿

### 템플릿 1. 클래스형 트라이

```python
class TrieNode:
    __slots__ = ("children", "is_end")   # 메모리 절약 (노드가 많을 때)
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def _walk(self, s):                 # s 를 따라간 마지막 노드, 없으면 None
        node = self.root
        for ch in s:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._walk(prefix) is not None
```

### 템플릿 2. 중첩 dict 트라이 (코딩 테스트용 단축형)

```python
END = "$"
root = {}
def insert(word):
    node = root
    for ch in word:
        node = node.setdefault(ch, {})
    node[END] = True

def search(word):
    node = root
    for ch in word:
        if ch not in node:
            return False
        node = node[ch]
    return END in node
```

### 템플릿 3. count 트라이 (접두사 개수)

```python
class Node:
    __slots__ = ("children", "count")
    def __init__(self):
        self.children, self.count = {}, 0

def build(words):
    root = Node()
    for w in words:
        node = root
        node.count += 1
        for ch in w:
            node = node.children.setdefault(ch, Node())
            node.count += 1          # 이 노드를 지나간 단어 수
    return root

def count_prefix(root, prefix):
    node = root
    for ch in prefix:
        node = node.children.get(ch)
        if node is None:
            return 0
    return node.count
```

### 템플릿 4. 트라이 + 격자 DFS (Word Search II)

```python
def find_words(board, words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w                     # 끝 노드에 단어 저장
    m, n, found = len(board), len(board[0]), []

    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent.get(ch)
        if node is None:                  # 방문한 칸('#') 또는 트라이에 없는 경로
            return
        if "$" in node:
            found.append(node.pop("$"))   # 찾으면 제거 → 중복 방지
        board[r][c] = "#"
        for nr, nc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1)):
            if 0 <= nr < m and 0 <= nc < n:
                dfs(nr, nc, node)
        board[r][c] = ch
        if not node:                      # 빈 가지는 잘라내기
            parent.pop(ch)

    for r in range(m):
        for c in range(n):
            dfs(r, c, root)
    return found
```

## 시간 · 공간 복잡도

| 작업 | 시간 | 공간 | 비고 |
|---|---|---|---|
| insert / search / startsWith | O(L) | insert 시 최대 O(L) 노드 추가 | L = 문자열 길이 |
| 트라이 구축 (N 개 단어) | O(ΣL) | O(ΣL) 노드 | 공통 접두사가 많을수록 노드 적음 |
| 접두사 개수 (count 트라이) | O(L) | - | |
| 와일드카드 검색 (`.` d 개) | 최악 O(26^d · L) | O(L) 재귀 | 실제로는 존재하는 경로로만 분기 |
| Word Search II | 최악 O(m·n·4·3^(L-1)) | O(ΣL) | 트라이 가지치기로 실제론 훨씬 빠름 |

## 자주 하는 실수

- [ ] `is_end` 를 빼먹어 "접두사로만 존재하는 문자열"도 search 에서 True 가 됨
- [ ] 노드마다 `[None] * 26` 배열을 만들어 메모리 초과 → 파이썬에서는 dict 가 유리
- [ ] 클래스 노드를 수십만 개 만들면서 `__slots__` 를 안 써 메모리/시간 낭비
- [ ] Word Search II 에서 찾은 단어를 결과에 중복으로 넣음 → 찾으면 끝 표시를 지우세요
- [ ] 격자 DFS 에서 방문 표시를 되돌리지 않아(백트래킹 누락) 다른 경로 탐색이 막힘
- [ ] 와일드카드 검색에서 패턴 끝에 도달했을 때 `is_end` 가 아니라 `True` 를 반환
- [ ] 가사 검색류에서 길이 조건을 잊음 → "fro??" 는 **5글자** 단어만. 길이별로 트라이를 나누세요
- [ ] count 를 단어 끝 노드에만 더함 → 접두사 개수를 세려면 **지나가는 모든 노드**에 더해야 함
- [ ] 재귀 DFS 중 dict 를 순회하면서 삭제 → `RuntimeError: dictionary changed size during iteration`

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Implement Trie | Medium | children dict + is_end | `python practice.py start implement-trie` |
| 2 | Design Add and Search Words | Medium | 트라이 + '.' 에서 모든 자식으로 DFS | `python practice.py start design-add-and-search-words` |
| 3 | Prefix Query Count (PCCP 유형) | Medium | 길이별 트라이 + 노드 count | `python practice.py start prefix-query-count` |
| 4 | Word Search II | Hard | 단어 트라이로 격자 DFS 가지치기 | `python practice.py start word-search-ii` |

## 더 풀어 볼 문제

- LeetCode 14 Longest Common Prefix — 트라이 또는 정렬 후 첫/끝 비교
- LeetCode 1268 Search Suggestions System — 접두사별 사전순 상위 3개
- LeetCode 648 Replace Words — 가장 짧은 접두사(root) 찾기
- LeetCode 720 Longest Word in Dictionary — 모든 접두사가 단어인 가장 긴 단어
- LeetCode 421 Maximum XOR of Two Numbers in an Array — 비트 트라이
- LeetCode 745 Prefix and Suffix Search (Hard)
- 프로그래머스 Lv.4 가사 검색 (2020 카카오 블라인드) — 길이별 트라이 + 뒤집은 트라이
- 프로그래머스 Lv.4 자동완성 (2018 카카오 블라인드 3차) — 노드 count 가 1 이 되는 깊이
- 프로그래머스 Lv.2 전화번호 목록 — 트라이 또는 정렬/해시

## 영어로 설명하기 (미국 면접용)

- "Since we have many prefix queries, I'll build a trie so each query costs O(L), where L is the length of the query, instead of scanning every word."
- "Each trie node stores a map from character to child and a flag that marks the end of a word, so that a prefix of a stored word isn't mistaken for a word itself."
- "For the wildcard search, I do a DFS on the trie: a regular character follows a single edge, while a dot tries every existing child, so we only explore paths that actually exist in the dictionary."
- "For Word Search II, instead of running a separate search for every word, I put all words in a trie and run one backtracking DFS over the grid, pruning as soon as the current path isn't a prefix in the trie."
- "I'll also store a count at every node — the number of words passing through it — so the number of words with a given prefix is just the count at the node where the prefix ends."

## 체크리스트

- [ ] Trie 클래스(insert / search / startsWith)를 5분 안에 보지 않고 쓸 수 있다
- [ ] `is_end` 가 왜 필요한지 예시로 설명할 수 있다
- [ ] 노드에 `count`, `word` 같은 정보를 붙여 문제에 맞게 변형할 수 있다
- [ ] 와일드카드 패턴을 트라이 DFS 로 검색할 수 있다
- [ ] Word Search II 에서 트라이 가지치기와 찾은 단어 제거를 구현할 수 있다
- [ ] 트라이 대신 정렬 + bisect 나 해시맵으로 풀 수 있는 경우를 구별할 수 있다
- [ ] 트라이의 시간·공간 복잡도를 단어 수 N, 길이 L 로 표현할 수 있다
