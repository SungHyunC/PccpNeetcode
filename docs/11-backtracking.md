# 11. 백트래킹 (Backtracking)

> 가능한 선택지를 하나씩 "골라 보고(choose) → 끝까지 가 보고(explore) → 되돌리는(unchoose)" 완전 탐색. 안 되는 길은 일찍 잘라(pruning) 시간을 줄입니다.

## 이런 문제에서 떠올리세요

- "가능한 **모든** 조합 / 순열 / 부분집합 / 배치를 구하라" → 결과 자체가 지수 개이므로 백트래킹
- "~하는 방법의 수" 인데 입력이 아주 작음 (n ≤ 10~20) → 완전 탐색 + 가지치기
- 격자에서 "같은 칸을 두 번 쓰지 않고" 경로/단어 만들기 → 격자 백트래킹 (방문 표시 후 복구)
- 스도쿠, N-Queen, 단어 퍼즐 등 **제약 조건 만족(constraint satisfaction)** 문제
- 입력 크기 힌트
  | n 의 범위 | 가능한 복잡도 | 대표 |
  |---|---|---|
  | n ≤ 8~10 | O(n!) | 순열, N-Queen |
  | n ≤ 20 | O(2^n · n) | 부분집합, 비트마스크 |
  | n ≤ 25~30 | O(2^(n/2)) | 반으로 나눠 탐색(meet in the middle) |
  | n > 30 | 백트래킹만으로는 어려움 | DP·그리디 고려 |
- PCCP / 프로그래머스: "소수 찾기"(숫자 조각 순열), "피로도"(던전 순서 순열), "모음 사전", "N-Queen", "양궁대회" 처럼 n 이 작고 경우의 수를 다 따져야 하는 문제

## 핵심 개념

### 1) 결정 트리(decision tree)

백트래킹은 "선택의 연속" 을 트리로 보고 DFS 로 훑는 것입니다. 트리의 각 노드는 "지금까지의 선택(path)" 입니다.

```
nums = [1, 2, 3] 의 부분집합 결정 트리 (start 인덱스 방식)

                    []                         depth 0
         ┌──────────┼──────────┐
        [1]        [2]        [3]              depth 1
      ┌──┴──┐       │
   [1,2]  [1,3]   [2,3]                        depth 2
     │
  [1,2,3]                                      depth 3

모든 노드 = 부분집합 (8개)
"다음 선택은 지금 고른 원소보다 뒤에서만" → [2,1] 같은 중복이 생기지 않음
```

### 2) choose → explore → unchoose

```
path = [1]          path = [1, 2]        path = [1]           path = [1, 3]
   │  append(2)        │  dfs(...)          │  append(3)
   └────────────▶  탐색 후 돌아와서  ──pop()──▶ ────────────▶ ...
                    "원래 상태로 복구" 가 핵심
```

공유 상태(path, used, 방문 표시, 집합 등)를 **들어갈 때 바꾸고 나올 때 정확히 되돌리면** 하나의 리스트로 트리 전체를 탐색할 수 있습니다.

### 3) 순열 vs 조합 vs 부분집합

| 종류 | 개수 | 구분 포인트 | 다음 재귀 | 결과 저장 시점 | itertools |
|---|---|---|---|---|---|
| 부분집합 (subsets) | 2^n | 순서 무관, 크기 자유 | `dfs(j + 1)` | 모든 노드 | `combinations(nums, k)` 를 k = 0..n |
| 조합 (combinations) | C(n, k) | 순서 무관, 크기 k | `dfs(j + 1)` | `len(path) == k` | `combinations(nums, k)` |
| 중복 조합 | C(n+k-1, k) | 같은 원소 재사용 | `dfs(j)` | 조건 충족 시 | `combinations_with_replacement` |
| 순열 (permutations) | n! / (n-k)! | 순서 중요 | `used[]` 로 아무거나 | `len(path) == k` | `permutations(nums, k)` |
| 데카르트 곱 | ∏ 후보 수 | 자리마다 독립 선택 | `dfs(i + 1)` | `i == 자리 수` | `product(*lists)` / `product(xs, repeat=k)` |

### 4) 가지치기 (pruning)

```
Combination Sum: candidates = [2, 3, 6, 7] (정렬), target = 7

dfs(remain=7)
├─ 2 → remain 5
│   ├─ 2 → remain 3
│   │   ├─ 2 → remain 1
│   │   │   └─ 2 > 1  ✂ break  (정렬돼 있으니 3, 6, 7 도 볼 필요 없음)
│   │   └─ 3 → remain 0  ✔
...
```

자주 쓰는 가지치기:
- **정렬 + break**: 남은 합보다 큰 후보가 나오면 그 뒤는 전부 불가능
- **같은 레벨 중복 건너뛰기**: 정렬 후 `j > start and nums[j] == nums[j-1]` → continue (Subsets II, Combination Sum II)
- **유효성 즉시 검사**: N-Queen 에서 공격받는 칸이면 바로 다음 열로
- **상한/하한(bound)**: 현재까지 비용 + 남은 최소 비용 ≥ 지금까지의 최적값이면 중단 (branch and bound)
- **사전 검사**: Word Search 에서 글자 수 Counter 로 불가능한 단어를 탐색 전에 걸러냄

### 5) 중복 원소 처리 (Subsets II / Permutations II)

```
nums = [1, 2, 2]  (정렬 후, 두 2 를 2a, 2b)

같은 레벨(같은 for 루프)에서:      [ ]
                           ┌──────┼──────┐
                          [1]   [2a]   [2b] ✂   ← 2b 는 2a 와 같은 값 → 건너뜀
깊이 방향으로는 허용:            [2a, 2b] ✔
```

## 코드 템플릿

### 템플릿 1: 부분집합 / 조합 (start 인덱스)

```python
def subsets(nums):
    result, path = [], []

    def dfs(start):
        result.append(path[:])              # 모든 노드가 답 (조합이면 len(path)==k 일 때만)
        for j in range(start, len(nums)):
            # if j > start and nums[j] == nums[j-1]: continue   # 중복 원소가 있을 때 (정렬 필수)
            path.append(nums[j])            # choose
            dfs(j + 1)                      # explore  (재사용 허용이면 dfs(j))
            path.pop()                      # unchoose

    dfs(0)
    return result
```

### 템플릿 2: 순열 (used 배열)

```python
def permutations(nums):
    n = len(nums)
    result, path, used = [], [], [False] * n

    def dfs():
        if len(path) == n:
            result.append(path[:])
            return
        for i in range(n):
            if used[i]:
                continue
            # 중복 원소: if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue
            used[i] = True
            path.append(nums[i])
            dfs()
            path.pop()
            used[i] = False

    dfs()
    return result
```

### 템플릿 3: 가지치기가 있는 합 찾기 (정렬 + break)

```python
def combination_sum(candidates, target):
    candidates.sort()
    result, path = [], []

    def dfs(start, remain):
        if remain == 0:
            result.append(path[:])
            return
        for j in range(start, len(candidates)):
            if candidates[j] > remain:      # 정렬돼 있으므로 이후도 모두 불가 → break
                break
            path.append(candidates[j])
            dfs(j, remain - candidates[j])  # 같은 수 재사용 가능
            path.pop()

    dfs(0, target)
    return result
```

### 템플릿 4: 격자 백트래킹 (방문 표시 → 복구)

```python
def exist(board, word):
    R, C = len(board), len(board[0])

    def dfs(r, c, i):
        if not (0 <= r < R and 0 <= c < C) or board[r][c] != word[i]:
            return False
        if i == len(word) - 1:
            return True
        tmp, board[r][c] = board[r][c], "#"         # 방문 표시
        found = any(dfs(r + dr, c + dc, i + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        board[r][c] = tmp                           # 반드시 복구
        return found

    return any(dfs(r, c, 0) for r in range(R) for c in range(C))
```

### PCCP 지름길: itertools

```python
from itertools import permutations, combinations, product, combinations_with_replacement

list(permutations([1, 2, 3], 2))      # [(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)]   순열 nPr
list(combinations([1, 2, 3], 2))      # [(1,2),(1,3),(2,3)]                     조합 nCr
list(product("ab", repeat=2))         # [('a','a'),('a','b'),('b','a'),('b','b')] 중복 순열
list(product("ab", "xy"))             # [('a','x'),('a','y'),('b','x'),('b','y')] 데카르트 곱

# 예: 프로그래머스 '소수 찾기' — 숫자 조각으로 만들 수 있는 모든 수
nums = {int("".join(p)) for k in range(1, len(s) + 1) for p in permutations(s, k)}
```

- 결과가 **튜플**로 나옵니다. 리스트가 필요하면 `list(p)` 로 바꾸세요.
- 가지치기를 할 수 없으므로 경우의 수가 크면(예: 10! = 360만 × 검사 비용) 직접 백트래킹이 더 빠를 수 있습니다.
- 면접(미국)에서는 "itertools 없이 구현해 보라" 는 요청이 흔합니다. 둘 다 할 줄 알아야 합니다.

## 시간 · 공간 복잡도

| 문제 유형 | 시간 | 공간(재귀) | n 한계(파이썬 감) |
|---|---|---|---|
| 부분집합 | O(n · 2^n) | O(n) | n ≤ 20 |
| 조합 nCk | O(k · C(n, k)) | O(k) | C(n,k) ≤ 수백만 |
| 순열 | O(n · n!) | O(n) | n ≤ 9~10 |
| 데카르트 곱 (자리 n, 후보 b) | O(n · b^n) | O(n) | b^n ≤ 수백만 |
| 격자 단어 찾기 | O(R · C · 3^L) | O(L) | L ≤ 15 정도 |
| N-Queen | O(n!) 상한 (가지치기로 훨씬 적음) | O(n) | n ≤ 12~13 |

- 결과를 **모두 출력**하는 문제는 결과 개수 × 결과 길이가 하한입니다. 더 줄일 수 없습니다.
- 파이썬은 1초에 대략 천만 번 안팎의 단순 연산이 가능하다고 보고 경우의 수를 계산하세요.

## 자주 하는 실수

- [ ] `result.append(path)` — 같은 리스트 객체를 넣어서 나중에 전부 빈 리스트가 됨 → `path[:]` 또는 `list(path)` 로 **복사**
- [ ] choose 와 unchoose 가 짝이 맞지 않음 (append 했는데 return 경로에서 pop 을 빠뜨림, used 를 되돌리지 않음)
- [ ] 조합인데 `dfs(j + 1)` 대신 `dfs(start + 1)` 을 호출 → 중복 조합 생성
- [ ] 재사용 가능 여부 혼동: 재사용 가능 `dfs(j)`, 불가능 `dfs(j + 1)`
- [ ] 중복 skip 조건을 `j > 0` 으로 씀 → 깊이 방향의 정상적인 선택까지 막힘. **`j > start`** 가 맞음 (그리고 정렬 필수)
- [ ] 격자 탐색에서 방문 표시를 복구하지 않음 → 다른 시작점 탐색 결과가 틀어짐
- [ ] 빈 입력 처리: 전화번호 조합에서 `""` 은 `[]` 를 반환해야 하는데 `[""]` 반환
- [ ] 가지치기 `break` 를 쓰면서 정렬을 안 함 → 답을 놓침
- [ ] 문자열 `path + ch` 로 넘기기 vs 리스트 append/pop: 둘 다 되지만 문자열 방식은 매번 새 문자열을 만들어 O(n) 이 곱해짐 (작은 n 에서는 괜찮음)
- [ ] 재귀 깊이: 백트래킹은 보통 깊이가 n 이하라 괜찮지만, 깊이가 1000 을 넘을 수 있으면 `sys.setrecursionlimit` 필요

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Subsets | Medium | start 인덱스로 모든 노드 수집, 비트마스크 대안 | `python practice.py start subsets` |
| 2 | Combination Sum | Medium | 재사용이면 `dfs(j)`, 정렬 + break 가지치기 | `python practice.py start combination-sum` |
| 3 | Permutations | Medium | used 배열, itertools.permutations | `python practice.py start permutations` |
| 4 | Subsets II | Medium | 정렬 + `j > start` 같은 레벨 중복 skip | `python practice.py start subsets-ii` |
| 5 | Word Search | Medium | 격자 백트래킹, 방문 표시 복구, Counter 가지치기 | `python practice.py start word-search` |
| 6 | Palindrome Partitioning | Medium | 자를 위치 선택 + 팰린드롬 DP 표 | `python practice.py start palindrome-partitioning` |
| 7 | Letter Combinations of a Phone Number | Medium | 데카르트 곱, itertools.product | `python practice.py start letter-combinations-of-phone-number` |
| 8 | N-Queens | Hard | 열/대각선(r-c, r+c) 집합으로 O(1) 충돌 검사 | `python practice.py start n-queens` |

## 더 풀어 볼 문제

- LeetCode 77. Combinations
- LeetCode 40. Combination Sum II (중복 원소 + 1회 사용)
- LeetCode 216. Combination Sum III
- LeetCode 47. Permutations II
- LeetCode 22. Generate Parentheses (열린/닫힌 괄호 개수로 가지치기)
- LeetCode 51. N-Queens (판 출력 버전)
- LeetCode 37. Sudoku Solver
- LeetCode 212. Word Search II (트라이 + 백트래킹)
- LeetCode 93. Restore IP Addresses
- 프로그래머스 Lv.2 소수 찾기 (완전탐색, 순열)
- 프로그래머스 Lv.2 피로도 (완전탐색, 순열)
- 프로그래머스 Lv.2 모음 사전 (중복 순열 / 사전 순 DFS)
- 프로그래머스 Lv.2 타겟 넘버 (DFS 로 +/- 선택)
- 프로그래머스 Lv.2 N-Queen
- 프로그래머스 Lv.2 양궁대회 (2022 KAKAO BLIND, 중복 조합 + 비교)

## 영어로 설명하기 (미국 면접용)

- "Since we need to return every valid combination, the output itself is exponential, so a backtracking search over the decision tree is the natural approach."
- "At each step I choose a candidate, recurse to explore the rest, and then undo the choice so the shared path is restored for the next branch."
- "To avoid duplicate combinations, I only consider candidates at or after the current start index; for permutations I track a `used` array instead."
- "I sort the input first so I can prune: once a candidate exceeds the remaining target, every later candidate will too, so I break out of the loop."
- "The time complexity is O(n · 2^n) because there are 2^n subsets and copying each one costs O(n); the recursion depth is O(n)."

## 체크리스트

- [ ] 문제를 보고 부분집합 / 조합 / 순열 / 데카르트 곱 중 무엇인지 바로 구분할 수 있다
- [ ] choose → explore → unchoose 템플릿을 보지 않고 쓸 수 있다
- [ ] `result.append(path[:])` 처럼 복사해서 저장하는 이유를 설명할 수 있다
- [ ] 재사용 가능(`dfs(j)`) / 불가능(`dfs(j+1)`) 차이를 설명할 수 있다
- [ ] 정렬 + `j > start` 중복 skip 규칙이 왜 맞는지 그림으로 설명할 수 있다
- [ ] N-Queen 의 대각선을 `r - c`, `r + c` 로 식별할 수 있다
- [ ] itertools 의 permutations / combinations / product 사용법과 반환형(튜플)을 안다
- [ ] 입력 크기를 보고 백트래킹이 시간 안에 끝나는지 경우의 수로 계산할 수 있다
