# 08. 트리 (Trees)

> 트리 문제의 90% 는 "각 노드에서 무엇을 하고, 자식에게 무엇을 받아, 부모에게 무엇을 돌려줄까?" 를 정하는 문제입니다. 깊이 우선 탐색(DFS: 전위·중위·후위)과 너비 우선 탐색(BFS: 레벨 순회), 그리고 이진 탐색 트리(BST)의 정렬 성질을 익히면 대부분 풀립니다.

## 이런 문제에서 떠올리세요

- 입력이 `TreeNode root` → 이 문서의 순회 템플릿 중 하나
- "깊이 / 높이 / 지름 / 균형 / 경로 합" → **후위 순회(post-order)로 자식 정보를 받아 올리기**
- "레벨별로", "가장 왼쪽/오른쪽에 보이는 노드", "루트에서 가장 가까운 리프" → **BFS (레벨 순회)**
- "BST 에서 k 번째", "정렬된 순서로", "BST 가 맞는지" → **중위 순회(in-order) = 오름차순**
- "BST 에서 찾기/삽입/공통 조상" → **값 비교로 한쪽만 내려가기 O(h)**
- "순회 결과로 트리를 복원", "직렬화(serialize)" → **전위 순회 + 범위 분할**
- 부모→자식으로 조건(허용 범위, 지금까지의 합, 깊이)을 넘겨야 함 → **전위 순회로 인자 내려보내기**
- 입력 크기: N ≤ 100,000 이면 O(N) / O(N log N). 노드마다 서브트리를 다시 훑는 O(N²) 은 위험
- 치우친 트리(높이 = N)가 가능하면 **파이썬 재귀 한도(기본 1000)** 를 먼저 걱정하세요

> PCCP / 프로그래머스에서는 `TreeNode` 대신 **간선 리스트나 부모 배열**로 트리를 주는 경우가 많습니다 (예: 전력망을 둘로 나누기, 길 찾기 게임). 이때는 인접 리스트를 만든 뒤 같은 DFS/BFS 를 적용합니다 (→ 그래프 문서).

## 핵심 개념

### 1) 용어

```
              1          ← 루트(root), 깊이 0
            /   \
           2     3       ← 1 의 자식(child), 서로 형제(sibling)
          / \     \
         4   5     6     ← 리프(leaf): 자식이 없는 노드
        /
       7                 ← 높이(height) = 루트에서 가장 먼 리프까지 간선 3개 (노드 기준이면 4)
```

- 서브트리(subtree): 어떤 노드와 그 모든 자손
- 이진 트리에서 노드 수 n, 높이 h: 균형이면 h ≈ log₂ n, 한쪽으로 치우치면 h = n - 1
- 재귀 DFS 의 공간 복잡도는 O(h). 그래서 "균형 트리면 O(log n), 최악 O(n)" 이라고 말합니다

### 2) DFS 세 가지 순서

```
        A
       / \          전위(pre-order)  : 나 → 왼 → 오   A B D E C
      B   C         중위(in-order)   : 왼 → 나 → 오   D B E A C
     / \            후위(post-order) : 왼 → 오 → 나   D E B C A
    D   E           레벨(BFS)        : 위에서 아래로   A B C D E
```

| 순서 | 언제 쓰나 |
|---|---|
| 전위 | 부모의 정보를 자식에게 내려보낼 때 (경로 합, 허용 범위, 깊이), 트리 복사·직렬화 |
| 중위 | BST 를 오름차순으로 볼 때 (k 번째, 검증, 범위 합) |
| 후위 | 자식의 결과를 모아 내 답을 만들 때 (높이, 지름, 균형, 최대 경로 합, 삭제) |
| BFS | 레벨 단위 처리, 루트에서 가장 가까운 것 찾기 |

### 3) "자식에게 정보를 받아 위로 올리기" 패턴 (후위 순회)

트리 문제를 푸는 가장 강력한 사고법입니다. 재귀 함수의 **반환값**을 "부모가 필요로 하는 정보"로 정의하고, 문제의 **정답**은 따로 바깥 변수로 갱신합니다.

```
                 반환: 1 + max(L, R)  (높이)
                 갱신: best = max(best, L + R)  (지름 후보)
                      ┌───┐
                      │ 2 │
                      └───┘
             L=2 ↗          ↖ R=2
             ┌───┐          ┌───┐
             │ 3 │          │ 4 │
             └───┘          └───┘
```

| 문제 | 부모에게 반환하는 값 | 노드에서 하는 일 |
|---|---|---|
| 최대 깊이 | 서브트리 높이 | 1 + max(L, R) |
| 지름 | 높이 | best = max(best, L + R) |
| 균형 판별 | 높이, 불균형이면 -1 | |L - R| > 1 이면 -1 전파 |
| 최대 경로 합 | 한쪽 가지 최대 합 (음수면 0) | best = max(best, val + L + R) |
| 일반 트리 LCA | p/q 를 찾았으면 그 노드, 아니면 None | 양쪽 다 찾았으면 나 자신 |

핵심 질문 세 개: ① 빈 노드(None)는 무엇을 반환? ② 자식 두 개의 반환값으로 내 반환값을 어떻게 만들지? ③ 정답은 반환값과 같은가, 따로 갱신해야 하는가?

### 4) BFS 레벨 순회

```
큐 상태                    이번 레벨
[1]                  →    [1]          자식 2, 3 추가
[2, 3]               →    [2, 3]       자식 4, 5, 6 추가
[4, 5, 6]            →    [4, 5, 6]    자식 7 추가
[7]                  →    [7]
```

레벨 시작 시점의 `len(q)` 가 그 레벨의 노드 수입니다.

### 5) 이진 탐색 트리 (BST)

```
            8
          /   \          왼쪽 서브트리의 모든 값 < 8 < 오른쪽 서브트리의 모든 값
         3     10        (모든 노드에서 성립)
        / \      \
       1   6      14     중위 순회: 1 3 4 6 7 8 10 13 14  ← 정렬됨!
          / \    /
         4   7  13
```

- 탐색/삽입/삭제: 값 비교로 한쪽으로만 내려가므로 O(h). 균형이면 O(log n), 치우치면 O(n)
- 중위 순회 = 오름차순 → k 번째 원소, BST 검증, 두 노드의 최소 차이
- **주의**: "왼쪽 자식 < 나 < 오른쪽 자식" 만 검사하면 틀립니다. 조건은 서브트리 **전체**에 대한 것 → `(low, high)` 범위를 내려보내세요
- LCA: 루트부터 내려가며 p, q 가 갈라지는 첫 노드

## 코드 템플릿

### 템플릿 1. 재귀 DFS (세 가지 순서) + 정보 올리기

```python
import sys
sys.setrecursionlimit(10**6)   # 깊은 트리 대비 (PCCP 에서 특히)

def dfs(node):
    if node is None:
        return 0                # ① 빈 노드의 기본값
    # 전위 위치: 여기서 node 처리하면 pre-order
    left = dfs(node.left)
    # 중위 위치: 여기서 처리하면 in-order
    right = dfs(node.right)
    # 후위 위치: 자식 결과(left, right)로 내 결과 계산
    return 1 + max(left, right) # ② 부모에게 올릴 정보

# 정답이 반환값과 다를 때: 바깥 변수 + nonlocal
def diameter(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
        l, r = height(node.left), height(node.right)
        best = max(best, l + r) # ③ 정답 갱신
        return 1 + max(l, r)
    height(root)
    return best
```

### 템플릿 2. 반복 DFS (전위 / 중위 / 후위)

```python
def preorder(root):
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right: stack.append(node.right)  # 오른쪽을 먼저 넣어야
        if node.left:  stack.append(node.left)   # 왼쪽이 먼저 나옴
    return out

def inorder(root):
    out, stack, cur = [], [], root
    while stack or cur:
        while cur:                 # 왼쪽 끝까지 내려가며 쌓기
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()          # 방문
        out.append(cur.val)
        cur = cur.right            # 오른쪽 서브트리로
    return out

def postorder(root):
    # 나 → 오 → 왼 순서(변형 전위)를 뒤집으면 왼 → 오 → 나
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.left:  stack.append(node.left)
        if node.right: stack.append(node.right)
    return out[::-1]
```

### 템플릿 3. BFS 레벨 순회

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    result, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):    # 이번 레벨 노드 수만큼만
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        result.append(level)
    return result
```

### 템플릿 4. BST: 범위 내려보내기 / 한쪽으로 내려가기

```python
def is_valid_bst(root):
    stack = [(root, float("-inf"), float("inf"))]
    while stack:
        node, lo, hi = stack.pop()
        if not node:
            continue
        if not (lo < node.val < hi):
            return False
        stack.append((node.left, lo, node.val))
        stack.append((node.right, node.val, hi))
    return True

def bst_search(root, target):
    node = root
    while node and node.val != target:
        node = node.left if target < node.val else node.right
    return node
```

## 시간 · 공간 복잡도

| 작업 | 시간 | 공간 | 비고 |
|---|---|---|---|
| DFS 순회 (재귀/스택) | O(n) | O(h) | h: 균형 log n, 최악 n |
| BFS 레벨 순회 | O(n) | O(w) | w: 최대 너비 (최대 약 n/2) |
| 후위 순회로 높이·지름·경로 합 | O(n) | O(h) | 노드마다 높이를 다시 구하면 O(n²) |
| BST 탐색/삽입/LCA | O(h) | O(1) 반복 | 균형 BST 면 O(log n) |
| BST k 번째 (중위 순회 중단) | O(h + k) | O(h) | |
| 전위+중위로 복원 | O(n) | O(n) | 슬라이싱 + index() 는 O(n²) |

## 자주 하는 실수

- [ ] `root is None` 기저 사례를 빼먹어 `AttributeError: 'NoneType' object has no attribute 'left'`
- [ ] 깊이를 노드 수로 세는지 간선 수로 세는지 혼동 (Maximum Depth 는 노드 수, Diameter 는 간선 수)
- [ ] BST 검증에서 직속 자식만 비교 → 반례 `[5, 4, 6, None, None, 3, 7]`
- [ ] BST 에서 같은 값 처리 규칙(허용/불허, 왼쪽/오른쪽)을 확인하지 않음
- [ ] "반환값 = 정답" 이라고 착각 → 지름, 최대 경로 합은 반환값(한쪽 가지)과 정답(꺾이는 경로)이 다름
- [ ] 최대 경로 합의 초깃값을 0 으로 둠 → 모든 값이 음수면 오답. `float('-inf')`
- [ ] 반복 전위 순회에서 왼쪽을 먼저 push → 오른쪽이 먼저 나옴 (스택은 LIFO)
- [ ] BFS 에서 `list.pop(0)` 사용 → O(n). `collections.deque` 의 `popleft()` 사용
- [ ] 치우친 트리에서 재귀 → `RecursionError`. `sys.setrecursionlimit` 또는 반복문으로
- [ ] 중첩 함수에서 바깥 변수를 갱신하면서 `nonlocal` 을 빠뜨림 (정수는 재할당이므로 필요)

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Invert Binary Tree | Easy | 모든 노드에서 left/right 교환 | `python practice.py start invert-binary-tree` |
| 2 | Maximum Depth of Binary Tree | Easy | 1 + max(L, R) / BFS 레벨 수 | `python practice.py start maximum-depth-of-binary-tree` |
| 3 | Diameter of Binary Tree | Easy | 높이 반환 + L+R 로 정답 갱신 | `python practice.py start diameter-of-binary-tree` |
| 4 | Balanced Binary Tree | Easy | 높이 반환, 불균형이면 -1 전파 | `python practice.py start balanced-binary-tree` |
| 5 | Binary Tree Level Order Traversal | Medium | BFS + len(q) 만큼 꺼내기 | `python practice.py start binary-tree-level-order-traversal` |
| 6 | Validate Binary Search Tree | Medium | (low, high) 범위 내려보내기 | `python practice.py start validate-binary-search-tree` |
| 7 | Kth Smallest Element in a BST | Medium | 반복 중위 순회, k 번째에서 중단 | `python practice.py start kth-smallest-element-in-bst` |
| 8 | Lowest Common Ancestor of a BST | Medium | p, q 가 갈라지는 첫 노드 | `python practice.py start lowest-common-ancestor-of-bst` |
| 9 | Construct Tree from Preorder & Inorder | Medium | 전위 첫 값 = 루트, 중위 dict 로 분할 | `python practice.py start construct-tree-from-preorder-inorder` |
| 10 | Binary Tree Maximum Path Sum | Hard | 음수 가지 버리기 + 꺾이는 경로 갱신 | `python practice.py start binary-tree-maximum-path-sum` |

## 더 풀어 볼 문제

- LeetCode 100 Same Tree / 572 Subtree of Another Tree — 두 트리 동시 재귀
- LeetCode 199 Binary Tree Right Side View — 레벨 순회의 마지막 노드
- LeetCode 1448 Count Good Nodes in Binary Tree — 경로상 최댓값을 내려보내기 (전위)
- LeetCode 236 Lowest Common Ancestor of a Binary Tree — 일반 트리 LCA (후위)
- LeetCode 112 / 113 Path Sum I, II — 남은 합을 내려보내기 + 백트래킹
- LeetCode 297 Serialize and Deserialize Binary Tree (Hard) — 전위 순회 + None 표기
- LeetCode 103 Binary Tree Zigzag Level Order Traversal
- LeetCode 450 Delete Node in a BST — BST 삭제의 세 가지 경우
- 프로그래머스 Lv.3 길 찾기 게임 (2019 카카오 블라인드) — 좌표로 이진 트리 만들고 전위/후위 순회
- 프로그래머스 Lv.2 전력망을 둘로 나누기 — 간선 리스트 트리에서 서브트리 크기
- 프로그래머스 Lv.3 다단계 칫솔 판매 (2021 Dev-Matching) — 부모 포인터 따라 올라가기

## 영어로 설명하기 (미국 면접용)

- "I'll solve this recursively with a post-order traversal: each call returns the height of its subtree, and at every node I update a global answer using the heights from both children."
- "The key observation is that the value I return to the parent is different from the answer I'm tracking — the parent can only extend one branch, but the best path at this node can use both."
- "For BST validation, checking only the immediate children isn't enough, so I pass down a valid range — a lower and an upper bound — and tighten it as I go left or right."
- "An in-order traversal of a BST visits the values in sorted order, so I can do it iteratively with a stack and stop as soon as I've visited k nodes, which is O(h + k)."
- "The recursion uses O(h) stack space; in the worst case of a skewed tree that's O(n), so for very deep trees I'd switch to an iterative version to avoid hitting the recursion limit."

## 체크리스트

- [ ] 전위·중위·후위 순회를 재귀와 반복(스택) 두 가지로 쓸 수 있다
- [ ] 레벨 단위 BFS 를 `len(q)` 를 이용해 1분 안에 쓸 수 있다
- [ ] 문제를 보고 "반환할 정보"와 "갱신할 정답"을 분리해서 말할 수 있다
- [ ] 재귀 DFS 의 공간 복잡도가 O(h) 인 이유와, 균형/치우친 경우의 차이를 설명할 수 있다
- [ ] BST 의 정의(서브트리 전체 조건)와 중위 순회 = 정렬 성질을 활용할 수 있다
- [ ] BST 검증의 흔한 오답과 반례를 알고 있다
- [ ] 전위+중위 배열로 트리를 O(n) 에 복원할 수 있다
- [ ] 파이썬에서 `sys.setrecursionlimit` 이 필요한 상황을 판단할 수 있다
