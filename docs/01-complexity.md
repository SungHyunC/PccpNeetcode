# 01. 시간 복잡도와 입력 크기 읽기 (Big-O & Constraints)

> 문제의 **제한사항**을 보고 허용되는 시간 복잡도를 먼저 정하면, 쓸 수 있는 알고리즘이 거의 정해집니다.

## 이런 문제에서 떠올리세요

모든 문제에서 첫 번째로 할 일입니다. 제한사항의 N 을 보고 아래 표에서 목표 복잡도를 고르세요.
파이썬은 대략 **1초에 1,000만~2,000만 번의 단순 연산**을 한다고 보면 안전합니다.

| N 의 크기 | 목표 복잡도 | 떠올릴 알고리즘 |
|---|---|---|
| N ≤ 10 | O(N!) | 순열 완전탐색, 백트래킹 |
| N ≤ 20 | O(2^N), O(2^N · N) | 부분집합, 비트마스크, 백트래킹 |
| N ≤ 100 | O(N³) | 플로이드-워셜, 3중 반복 DP |
| N ≤ 1,000 ~ 5,000 | O(N²) | 2중 반복, 2차원 DP |
| N ≤ 100,000 ~ 1,000,000 | O(N log N) / O(N) | 정렬, 이분 탐색, 힙, 투 포인터, 해시, 누적합 |
| N ≤ 10^9 이상 | O(log N) / O(1) | 이분 탐색(파라메트릭 서치), 수학 공식 |

## 핵심 개념

### Big-O 는 "입력이 커질 때 연산 횟수가 늘어나는 모양"

```
연산 횟수 (N = 100,000 일 때)
O(1)        1
O(log N)    17
O(N)        100,000
O(N log N)  1,700,000         ← 파이썬 1초 안 ✅
O(N²)       10,000,000,000    ← 파이썬 수백 초 ❌
```

### 규칙

1. **상수와 작은 항은 버린다**: O(3N + 5) → O(N), O(N² + N) → O(N²)
2. **연속은 더하고, 중첩은 곱한다**: for 다음 for → O(N + M), for 안에 for → O(N · M)
3. **반으로 줄이면 log**: 이분 탐색, 힙, 균형 트리
4. **상각(amortized) 분석**: 투 포인터나 단조 스택처럼 while 이 for 안에 있어도 각 원소가 한 번씩만 들어가고 나오면 전체 O(N)

### 숨은 비용 찾기

```python
for x in arr:          # O(N)
    if x in other:     # other 가 list 면 O(M) → 전체 O(N·M) ⚠
        ...
for i in range(n):
    s = s + str(i)     # 문자열 복사 O(len) → 전체 O(N²) ⚠
arr.sort()             # O(N log N)
sorted(arr)[0]         # 최솟값 하나 찾는 데 O(N log N) → min(arr) 은 O(N)
```

### 재귀의 복잡도 = 호출 수 × 호출당 작업

```
fib(n) 재귀 (메모 없음)               fib(n) 메모이제이션
           f(5)                        각 n 을 한 번씩만 계산
        /        \                     → 호출 수 O(N), 전체 O(N)
     f(4)        f(3)
    /    \       /   \
  f(3)  f(2)  f(2)  f(1)    → 호출 수 약 2^N → O(2^N)
```

### 공간 복잡도

- 추가로 만든 배열/해시/재귀 스택 깊이를 셉니다.
- 재귀 DFS 의 깊이 N → 스택 공간 O(N). 파이썬 기본 한도(1000)도 함께 고려.
- 면접에서는 "입력/출력 배열은 제외하고 추가 공간 O(1)" 처럼 기준을 명확히 말합니다.

## 코드 템플릿

### 실행 시간 직접 재 보기

```python
import time, random
arr = [random.randint(1, 10**9) for _ in range(100_000)]
start = time.perf_counter()
solution(arr)
print(f"{time.perf_counter() - start:.3f}s")
```

이 저장소의 `python practice.py test <문제>` 는 정확성 테스트와 함께 **효율성 테스트**(큰 입력 + 시간 제한)를 자동으로 돌립니다. PCCP 의 효율성 채점과 같은 감각을 연습할 수 있습니다.

### 자주 나오는 복잡도별 코드 모양

```python
# O(log N): 범위를 반씩 줄임
while lo < hi:
    mid = (lo + hi) // 2
    ...

# O(N): 한 번 훑기 (+ 해시)
seen = set()
for x in arr: ...

# O(N log N): 정렬 후 훑기
arr.sort()
for x in arr: ...

# O(N²): 모든 쌍
for i in range(n):
    for j in range(i + 1, n): ...

# O(2^N): 각 원소를 넣거나 빼거나
def dfs(i, picked):
    if i == n: return
    dfs(i + 1, picked + [arr[i]])
    dfs(i + 1, picked)
```

## 시간 · 공간 복잡도

| 알고리즘 | 시간 | 공간 |
|---|---|---|
| 정렬 (Timsort) | O(N log N) | O(N) |
| 이분 탐색 | O(log N) | O(1) |
| BFS / DFS | O(V + E) | O(V) |
| 다익스트라 (힙) | O(E log V) | O(V + E) |
| 힙 push/pop | O(log N) | – |
| 부분집합 전부 | O(2^N · N) | O(N) |
| 순열 전부 | O(N! · N) | O(N) |

## 자주 하는 실수

- N 이 10^5 인데 2중 반복문부터 짜기 → 제한사항을 먼저 보세요
- `in list` 를 반복문 안에서 사용 (숨은 O(N))
- 메모이제이션 없이 재귀로 DP 를 풀기
- "평균 O(1)" 인 해시를 "항상 O(1)" 이라고 말하기 (면접에서 정확한 표현 사용)
- 공간 복잡도에서 재귀 호출 스택을 빼먹기

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 복잡도 포인트 | 명령어 |
|---|---|---|---|---|
| 1 | Two Sum | Easy | O(N²) → O(N) 해시 | `python practice.py start two-sum` |
| 2 | Longest Consecutive Sequence | Medium | while 이 있어도 O(N) (상각) | `python practice.py start longest-consecutive-sequence` |
| 3 | Product of Array Except Self | Medium | O(N²) → O(N) prefix/suffix | `python practice.py start product-of-array-except-self` |
| 4 | Subarray Sum Equals K | Medium | O(N²) → O(N) 누적합 + 해시 | `python practice.py start subarray-sum-equals-k` |

각 문제에서 `brute_force` 풀이를 먼저 짜서 효율성 테스트가 **실패하는 것**을 직접 확인해 보세요.

## 더 풀어 볼 문제

- 웹 학습 허브(`web/index.html`)의 **복잡도 퀴즈**: N 범위를 보고 목표 복잡도 맞히기
- LeetCode 1 Two Sum, 217 Contains Duplicate, 53 Maximum Subarray (O(N³) → O(N²) → O(N) 개선 연습)

## 영어로 설명하기 (미국 면접용)

- "The brute-force approach checks every pair, which is O(n squared). Given n can be up to 10 to the 5th, that's too slow."
- "Sorting dominates the runtime, so the overall complexity is O(n log n)."
- "Even though there's a nested while loop, each element is pushed and popped at most once, so it's amortized O(n)."
- "The space complexity is O(n) for the hash map, plus O(h) for the recursion stack where h is the tree height."
- "Can I assume the input fits in memory?" / "What's the expected range of n?"

## 체크리스트

- [ ] 제한사항의 N 을 보고 목표 복잡도를 5초 안에 말할 수 있다
- [ ] 내 코드의 숨은 O(N) 연산(`in list`, 슬라이싱, 문자열 +=)을 찾을 수 있다
- [ ] 재귀 함수의 복잡도를 "호출 수 × 호출당 작업"으로 계산할 수 있다
- [ ] 상각 분석으로 O(N) 인 이유를 설명할 수 있다
- [ ] 시간·공간 복잡도를 영어로 말할 수 있다
