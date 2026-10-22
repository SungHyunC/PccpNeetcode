# 00. 코딩 테스트용 파이썬 (Python for Coding Tests)

> 알고리즘보다 먼저, "빠르고 실수 없이" 쓰는 파이썬 문법과 표준 라이브러리를 손에 익힙니다.

PCCP는 프로그래머스 웹 에디터에서 `def solution(...)` 함수를 완성하는 방식이고, 미국 기업 면접은 CoderPad·HackerRank 같은 공유 에디터에서 함수를 작성합니다. 두 환경 모두 **표준 라이브러리만** 쓸 수 있고 자동완성이 거의 없습니다. 아래 내용은 손이 기억할 때까지 반복하세요.

## 이런 상황에서 떠올리세요

| 하고 싶은 일 | 파이썬 도구 |
|---|---|
| 개수 세기 | `collections.Counter` |
| 키가 없을 때 기본값 | `collections.defaultdict(list / int / set)` |
| 양쪽에서 넣고 빼기 (BFS 큐) | `collections.deque` |
| 최솟값을 계속 꺼내기 | `heapq` |
| 정렬된 배열에서 위치 찾기 | `bisect.bisect_left / bisect_right` |
| 순열 · 조합 · 데카르트 곱 | `itertools.permutations / combinations / product` |
| 메모이제이션 | `functools.lru_cache` / `functools.cache` |
| 최대공약수 · 제곱근 · 무한대 | `math.gcd`, `math.isqrt`, `math.inf` |

## 핵심 개념

### 1) 자료형별 연산 비용

```
list   : 인덱싱 O(1) · append/pop() O(1) · pop(0)/insert(0,x) O(n) ⚠ · x in list O(n) ⚠
deque  : appendleft/popleft O(1) · 인덱싱 중간 O(n)
dict   : 조회/삽입/삭제 평균 O(1) · 파이썬 3.7+ 삽입 순서 유지
set    : x in set 평균 O(1) · 합/교/차집합 O(len)
str    : 불변(immutable) → s += c 를 반복하면 O(n²) 위험 → 리스트에 모아 ''.join()
heapq  : push/pop O(log n) · heapify O(n) · 최소 힙만 제공
```

> **가장 흔한 시간 초과 원인**: 큐를 `list.pop(0)` 으로 구현, 반복문 안에서 `x in list`, 문자열을 `+=` 로 이어 붙이기.

### 2) 입력이 함수 인자로 들어온다

PCCP·LeetCode·면접 모두 입력은 함수 인자로 들어오므로 `input()` 파싱이 필요 없습니다.
다만 백준 등에서 연습할 때는 아래 템플릿을 씁니다.

```python
import sys
input = sys.stdin.readline          # input() 보다 훨씬 빠름

n = int(input())
arr = list(map(int, input().split()))
grid = [input().rstrip() for _ in range(n)]   # 개행 문자 제거 주의
```

### 3) 얕은 복사 함정

```
grid = [[0] * 3] * 3      # ❌ 세 행이 '같은 리스트' 를 가리킴
grid[0][0] = 1
→ [[1,0,0],[1,0,0],[1,0,0]]

grid = [[0] * 3 for _ in range(3)]   # ✅ 행마다 새 리스트
```

## 코드 템플릿

### 템플릿 1 — 컬렉션 3종 세트

```python
from collections import Counter, defaultdict, deque

cnt = Counter("banana")             # Counter({'a': 3, 'n': 2, 'b': 1})
cnt.most_common(2)                  # [('a', 3), ('n', 2)]
Counter(a) == Counter(b)            # 애너그램 판별

graph = defaultdict(list)           # 인접 리스트
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)

q = deque([start])                  # BFS 큐
while q:
    node = q.popleft()
```

### 템플릿 2 — 정렬과 key

```python
arr.sort()                                   # 제자리 정렬, None 반환
new = sorted(arr, reverse=True)              # 새 리스트 반환
people.sort(key=lambda p: (-p[1], p[0]))     # 나이 내림차순, 이름 오름차순
words.sort(key=len)                          # 길이순 (안정 정렬이라 같은 길이는 원래 순서 유지)

# 비교 함수가 꼭 필요할 때 (예: 이어 붙여 가장 큰 수 만들기)
from functools import cmp_to_key
nums = list(map(str, nums))
nums.sort(key=cmp_to_key(lambda a, b: -1 if a + b > b + a else 1))
```

### 템플릿 3 — heapq, bisect

```python
import heapq
h = []
heapq.heappush(h, (dist, node))   # 튜플은 첫 원소부터 비교
d, node = heapq.heappop(h)        # 가장 작은 것
heapq.heappush(h, -x)             # 최대 힙: 부호를 뒤집어 넣고 꺼낼 때 다시 뒤집기
heapq.nlargest(k, arr)            # 상위 k 개

import bisect
a = [1, 3, 3, 5]
bisect.bisect_left(a, 3)    # 1 : 3 이 처음 들어갈 수 있는 위치
bisect.bisect_right(a, 3)   # 3 : 3 다음 위치
bisect.bisect_right(a, 3) - bisect.bisect_left(a, 3)  # 3 의 개수 = 2
```

### 템플릿 4 — itertools, functools, 재귀 제한

```python
from itertools import permutations, combinations, product, accumulate
list(permutations([1, 2, 3], 2))   # 순서 O: (1,2) (1,3) (2,1) ...  nPr
list(combinations([1, 2, 3], 2))   # 순서 X: (1,2) (1,3) (2,3)       nCr
list(product("01", repeat=3))      # 000 ~ 111 모든 경우
list(accumulate([1, 2, 3]))        # 누적합 [1, 3, 6]

from functools import lru_cache
import sys
sys.setrecursionlimit(10**6)       # 파이썬 기본 재귀 한도는 1000

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

### 자주 쓰는 한 줄 표현

```python
dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]           # 상하좌우
0 <= nr < R and 0 <= nc < C                           # 범위 체크
list(zip(*matrix))                                    # 전치(transpose)
[list(r) for r in zip(*matrix[::-1])]                 # 시계 방향 90도 회전
float('inf'), -float('inf')                           # 무한대 (math.inf 도 가능)
divmod(17, 5)                                         # (3, 2)
-(-a // b)                                            # 올림 나눗셈 (= math.ceil(a / b), 실수 오차 없음)
ord('a'), chr(97)                                     # 문자 ↔ 숫자
s[::-1]                                               # 뒤집기
''.join(sorted(s))                                    # 문자열 정렬
f"{n:05d}", bin(10)[2:], int("1010", 2), format(255, 'x')  # 포맷 · 진법 변환
any(x > 0 for x in arr), all(...)                      # 조건 검사
max(arr, key=lambda x: x[1])                           # 기준이 있는 최댓값
for i, x in enumerate(arr, start=1): ...               # 인덱스와 함께
```

## 시간 · 공간 복잡도

| 연산 | list | deque | set / dict |
|---|---|---|---|
| 끝에 추가/삭제 | O(1) | O(1) | – |
| 앞에 추가/삭제 | **O(n)** | O(1) | – |
| 원소 존재 확인 | **O(n)** | O(n) | O(1) 평균 |
| 인덱스 접근 | O(1) | O(n) (양 끝은 O(1)) | – |
| 정렬 | O(n log n) | – | – |

## 자주 하는 실수

- `arr.sort()` 의 반환값(None)을 변수에 담기 → `arr = arr.sort()` ❌
- 리스트를 순회하면서 그 리스트에서 원소를 삭제하기
- `[[0]*m]*n` 으로 2차원 배열 만들기
- 기본 인자에 가변 객체 사용: `def f(a=[])` ❌
- 재귀 DFS 에서 `RecursionError` → `sys.setrecursionlimit` 또는 반복문 + 스택
- 나눗셈 `/` 은 항상 float. 정수 몫은 `//`, 음수의 `//` 는 내림(-7 // 2 == -4)
- `round(2.5) == 2` (은행가 반올림). 사사오입이 필요하면 `int(x + 0.5)` (양수일 때)
- 문자열 비교 `"10" < "9"` 는 True (사전순)

## 연습 문제 (이 저장소)

이 문서는 모든 문제의 기초입니다. 아래 문제들로 문법을 손에 익히세요.

| # | 문제 | 난이도 | 연습할 문법 | 명령어 |
|---|---|---|---|---|
| 1 | Contains Duplicate | Easy | `set` | `python practice.py start contains-duplicate` |
| 2 | Valid Anagram | Easy | `Counter`, `ord` | `python practice.py start valid-anagram` |
| 3 | Group Anagrams | Medium | `defaultdict(list)`, `sorted` | `python practice.py start group-anagrams` |
| 4 | Top K Frequent Elements | Medium | `Counter.most_common`, `heapq` | `python practice.py start top-k-frequent-elements` |

## 더 풀어 볼 문제

- 프로그래머스 코딩테스트 입문 / Lv.0 문제 (문법 익히기용으로 좋음)
- 프로그래머스 Lv.1: 완주하지 못한 선수(해시), K번째수(정렬), 같은 숫자는 싫어(스택)
- LeetCode 1929 Concatenation of Array, 1480 Running Sum of 1d Array

## 영어로 설명하기 (미국 면접용)

- "I'll use a hash set here so membership checks are O(1) on average instead of O(n) with a list."
- "I'm using a deque because popping from the front of a Python list is O(n)."
- "Python's heapq is a min-heap, so I'll push negative values to simulate a max-heap."
- "Strings are immutable in Python, so I'll collect the pieces in a list and join them at the end."
- "Python integers don't overflow, but I'll mention how I'd handle it in Java or C++."

## 체크리스트

- [ ] `Counter`, `defaultdict`, `deque`, `heapq`, `bisect` 를 문서 없이 쓸 수 있다
- [ ] `sorted(..., key=lambda x: (...))` 로 다중 조건 정렬을 할 수 있다
- [ ] 2차원 배열을 안전하게 만들고, 90도 회전/전치를 한 줄로 쓸 수 있다
- [ ] `permutations` 와 `combinations` 의 차이를 설명할 수 있다
- [ ] 재귀 한도 문제를 만났을 때 대처법을 안다
