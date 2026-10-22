# 10. 힙 / 우선순위 큐 (Heap / Priority Queue)

> "지금 가장 작은(큰) 것"을 반복해서 꺼내야 할 때 쓰는 자료구조. 최솟값 확인 O(1), 넣기·꺼내기 O(log n). 파이썬은 `heapq` 모듈(최소 힙)을 쓰고, 최대 힙은 **부호를 뒤집어** 만듭니다. Top-k, k 개 병합, 두 힙으로 중앙값, 스케줄링 시뮬레이션이 대표 패턴입니다.

## 이런 문제에서 떠올리세요

- "가장 작은/큰 것을 꺼내고, 새 값을 넣고, 다시 가장 작은/큰 것을…" 반복 → **힙**
- "k 번째로 큰/작은", "상위 k 개", "가장 가까운 k 개", "가장 자주 나온 k 개" → **크기 k 힙 (Top-k)**
- "정렬된 k 개의 리스트/배열 병합" → **각 리스트의 head 를 힙에** (→ [07. 연결 리스트](07-linked-list.md))
- "실시간으로 들어오는 데이터의 중앙값" → **두 힙**
- "작업/회의/디스크 요청 스케줄링", "가장 이른 종료 시각" → **시간순 정렬 + 힙 시뮬레이션**
- 다익스트라(최단 경로) → **(거리, 노드) 힙** (→ 그래프 문서)
- 매번 정렬하거나 `min()` 을 반복하는 풀이가 O(n²) 으로 느릴 때 → 힙으로 O(n log n)
- 입력 크기 힌트: n ≤ 10⁶ 에서 "반복적으로 최솟값" → heapify O(n) + pop/push O(log n)

> 프로그래머스 고득점 Kit 의 힙 단원(**더 맵게, 디스크 컨트롤러, 이중우선순위큐**)이 PCCP 의 단골 유형입니다. 효율성 테스트가 있어 힙을 쓰지 않으면 통과하지 못합니다.

## 핵심 개념

### 1) 이진 힙 (binary heap)

완전 이진 트리(complete binary tree)이면서 **부모 ≤ 자식** (최소 힙) 을 만족합니다. 배열 하나로 저장합니다.

```
          1                  인덱스:   0  1  2  3  4  5  6
        /   \                배열:   [ 1, 3, 2, 7, 4, 5, 9 ]
       3     2
      / \   / \              i 의 자식: 2i+1, 2i+2
     7   4 5   9             i 의 부모: (i-1)//2
```

- **루트(heap[0])가 항상 최솟값** → 확인 O(1)
- 형제끼리는 순서가 없습니다. 힙 배열은 **정렬된 상태가 아닙니다** (`heap[1]` 이 두 번째로 작은 값이라는 보장 없음)

### 2) push 와 pop 의 동작

```
push(0): 맨 끝에 넣고, 부모보다 작으면 위로 교환 (sift up)  O(log n)
          1                  1                  0
        /   \              /   \              /   \
       3     2     →      0     2     →      1     2
      / \                / \                / \
     7   0              7   3              7   3
   (끝에 추가)        (부모 3과 교환)     (부모 1과 교환, 루트 도착)

pop(): 루트를 꺼내고, 맨 끝 원소를 루트로 올린 뒤
       더 작은 자식과 교환하며 아래로 내려 보냄 (sift down)  O(log n)
```

`heapify(list)` 는 아래쪽부터 sift down 을 하여 **O(n)** 에 힙을 만듭니다 (n 번 push 하는 O(n log n) 보다 빠름).

### 3) 파이썬 heapq API

| 함수 | 동작 | 시간 |
|---|---|---|
| `heapq.heapify(a)` | 리스트 a 를 제자리에서 최소 힙으로 | O(n) |
| `heapq.heappush(h, x)` | x 추가 | O(log n) |
| `heapq.heappop(h)` | 최솟값 꺼내기 (비었으면 IndexError) | O(log n) |
| `h[0]` | 최솟값 확인 (꺼내지 않음) | O(1) |
| `heapq.heappushpop(h, x)` | push 후 pop (x 가 최소면 바로 x 반환) | O(log n) |
| `heapq.heapreplace(h, x)` | pop 후 push (크기 유지, 비어 있으면 에러) | O(log n) |
| `heapq.nsmallest(k, it, key=)` | 가장 작은 k 개 (정렬된 리스트) | O(n log k) |
| `heapq.nlargest(k, it, key=)` | 가장 큰 k 개 | O(n log k) |

### 4) 최대 힙 = 부호 반전

```python
max_heap = []
heapq.heappush(max_heap, -x)     # 넣을 때 -
largest = -max_heap[0]           # 볼 때 -
largest = -heapq.heappop(max_heap)
```

문자열처럼 부호를 뒤집을 수 없는 값은 `(-우선순위, 값)` 튜플로 넣습니다.

### 5) 튜플로 우선순위 정하기

튜플은 **첫 원소부터 차례로** 비교됩니다.

```
(거리, 노드번호)          → 거리가 같으면 노드번호로 비교
(-빈도, 단어)            → 빈도 큰 순, 같으면 사전순
(값, 리스트번호, 노드)    → 값이 같을 때 ListNode 끼리 비교되는 TypeError 방지 (tie-breaker)
```

비교할 수 없는 객체(ListNode, dict 등)를 넣을 때는 반드시 고유한 tie-breaker(인덱스, `itertools.count()`)를 그 앞에 두세요.

### 6) Top-k 패턴

```
"가장 큰 k 개"  → 크기 k 의 최소 힙   (루트 = 상위 k 개 중 가장 작은 값 = k 번째로 큰 값)
"가장 작은 k 개" → 크기 k 의 최대 힙   (루트 = 하위 k 개 중 가장 큰 값)

k = 3, 들어오는 값: 5 1 9 3 7
  [5] → [1,5] → [1,5,9] → 3 > 1 이므로 교체 [3,5,9] → 7 > 3 교체 [5,7,9]
  상위 3개 = {5, 7, 9}, 3번째로 큰 값 = 루트 5
```

전체 정렬 O(n log n) 대신 O(n log k), 공간 O(k). 데이터가 스트림으로 들어와도 동작합니다.

### 7) 두 힙 (중앙값)

```
   small (최대 힙)        large (최소 힙)
   [1, 2, 3] 루트 3   |   루트 5 [5, 8, 9]
   ────────────────── 중앙선 ──────────────────
   불변식: small 의 모든 값 ≤ large 의 모든 값,  len(small) - len(large) ∈ {0, 1}
   중앙값 = 3 (홀수) 또는 (3 + 5) / 2 (짝수)
```

### 8) 지연 삭제 (lazy deletion)

`heapq` 는 임의 원소 삭제를 지원하지 않습니다 (찾는 데 O(n)). 대신

1. 삭제할 값을 `deleted` 카운터(dict)에 기록만 해 두고
2. 나중에 그 값이 **루트로 올라왔을 때** 꺼내 버립니다.

```python
from collections import defaultdict
deleted = defaultdict(int)

def remove(x):
    deleted[x] += 1                    # 표시만 (O(1))

def clean_top(heap):
    while heap and deleted[heap[0]]:   # 루트가 삭제 표시된 값이면 버림
        deleted[heap[0]] -= 1
        heapq.heappop(heap)
```

이중우선순위큐(최소·최대 힙 두 개를 동기화), 슬라이딩 윈도우 중앙값, 다익스트라에서 "이미 더 짧은 거리로 처리된 노드 건너뛰기"가 모두 이 아이디어입니다.

## 코드 템플릿

### 템플릿 1. 반복 추출 (더 맵게 / Last Stone Weight 형)

```python
import heapq

def repeat_merge(nums, K):
    heap = list(nums)
    heapq.heapify(heap)                 # O(n)
    count = 0
    while heap[0] < K:                  # 최솟값이 조건 미달인 동안
        if len(heap) < 2:
            return -1
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        heapq.heappush(heap, a + 2 * b)
        count += 1
    return count
```

### 템플릿 2. Top-k (k 번째로 큰 값 / 가장 가까운 k 개)

```python
def kth_largest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)                 # 크기 k 최소 힙
    for x in nums[k:]:
        if x > heap[0]:
            heapq.heapreplace(heap, x)  # 루트를 버리고 x 넣기
    return heap[0]

def k_closest(points, k):               # 가장 작은 k 개 → 최대 힙 (부호 반전)
    heap = []
    for x, y in points:
        d = x * x + y * y
        if len(heap) < k:
            heapq.heappush(heap, (-d, x, y))
        elif d < -heap[0][0]:
            heapq.heapreplace(heap, (-d, x, y))
    return [[x, y] for _, x, y in heap]
```

### 템플릿 3. 두 힙 (실시간 중앙값)

```python
small, large = [], []                   # small: 최대 힙(음수), large: 최소 힙

def add(num):
    heapq.heappush(small, -num)
    heapq.heappush(large, -heapq.heappop(small))       # 순서 불변식
    if len(large) > len(small):                        # 크기 불변식
        heapq.heappush(small, -heapq.heappop(large))

def median():
    if len(small) > len(large):
        return float(-small[0])
    return (-small[0] + large[0]) / 2
```

### 템플릿 4. 시간 순 시뮬레이션 (디스크 컨트롤러 / 작업 스케줄링)

```python
def schedule(jobs):                     # jobs: [요청 시각, 소요 시간]
    jobs = sorted(jobs)                 # 요청 시각 순
    heap, i, time, total = [], 0, 0, 0
    while i < len(jobs) or heap:
        while i < len(jobs) and jobs[i][0] <= time:     # 지금까지 도착한 작업을 힙에
            heapq.heappush(heap, (jobs[i][1], jobs[i][0]))  # (소요 시간, 요청 시각)
            i += 1
        if heap:
            dur, req = heapq.heappop(heap)              # 가장 짧은 작업부터 (SJF)
            time += dur
            total += time - req
        else:
            time = jobs[i][0]                           # 할 일 없으면 다음 요청 시각으로 점프
    return total // len(jobs)
```

## 시간 · 공간 복잡도

| 작업 | 시간 | 공간 | 비고 |
|---|---|---|---|
| heapify | O(n) | O(1) (제자리) | n 번 push 는 O(n log n) |
| push / pop / pushpop / replace | O(log n) | - | |
| 최솟값 확인 `h[0]` | O(1) | - | |
| 임의 원소 삭제 | O(n) | - | 지연 삭제로 우회 |
| Top-k (크기 k 힙) | O(n log k) | O(k) | 정렬은 O(n log n) |
| k 개 정렬 리스트 병합 | O(N log k) | O(k) | |
| 두 힙 중앙값 | add O(log n), median O(1) | O(n) | |
| 힙 정렬 (n 번 pop) | O(n log n) | O(n) | |

## 자주 하는 실수

- [ ] 파이썬 `heapq` 가 **최소 힙**이라는 것을 잊고 최댓값을 꺼내려 함 → 부호 반전
- [ ] 부호를 뒤집어 넣고 꺼낼 때 다시 뒤집지 않음 (`-heappop(h)`)
- [ ] `heap[1]` 을 두 번째로 작은 값이라고 착각 (형제 사이에는 순서가 없음)
- [ ] 힙 리스트를 `sorted()` 하거나 `append` 로 원소를 넣어 힙 성질이 깨짐 → 항상 `heappush`
- [ ] 빈 힙에서 `heap[0]` / `heappop` → `IndexError`. `while heap and ...` 로 확인
- [ ] `(우선순위, 객체)` 에서 우선순위가 같을 때 객체 비교로 `TypeError` → tie-breaker 추가
- [ ] Top-k 에서 힙의 방향을 반대로 고름 (큰 k 개는 **최소** 힙, 작은 k 개는 **최대** 힙)
- [ ] 거리 비교에 `sqrt` 사용 → 불필요하고 부동소수점 오차 위험
- [ ] 더 맵게 유형에서 원소가 1개 남았을 때(-1) 처리 누락
- [ ] 임의 원소를 `heap.remove(x)` 로 지운 뒤 `heapify` 를 안 함 → 힙 성질 붕괴 (그리고 O(n))

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Last Stone Weight | Easy | 최대 힙(부호 반전)에서 두 개씩 | `python practice.py start last-stone-weight` |
| 2 | Kth Largest Element in a Stream | Easy | 크기 k 최소 힙, 루트가 답 | `python practice.py start kth-largest-element-in-stream` |
| 3 | K Closest Points to Origin | Medium | 크기 k 최대 힙 / nsmallest | `python practice.py start k-closest-points-to-origin` |
| 4 | Kth Largest Element in an Array | Medium | 크기 k 힙 / 퀵셀렉트 | `python practice.py start kth-largest-element-in-array` |
| 5 | Mix Spicy Food (PCCP 유형) | Medium | 최소 힙에서 가장 작은 두 개 합치기 | `python practice.py start mix-spicy-food` |
| 6 | Task Scheduler | Medium | 최대 힙 + 쿨다운 큐 / 공식 | `python practice.py start task-scheduler` |
| 7 | Find Median from Data Stream | Hard | 두 힙 + 크기 균형 | `python practice.py start find-median-from-data-stream` |

함께 보기: Merge K Sorted Lists (`python practice.py start merge-k-sorted-lists`) — 힙으로 k 개 리스트 병합

## 더 풀어 볼 문제

- LeetCode 347 Top K Frequent Elements — Counter + nlargest (또는 버킷 정렬)
- LeetCode 692 Top K Frequent Words — `(-빈도, 단어)` 튜플 우선순위
- LeetCode 767 Reorganize String — 최대 힙 + 직전 문자 보류
- LeetCode 1834 Single-Threaded CPU — 시간순 시뮬레이션 + 힙
- LeetCode 355 Design Twitter — 사용자별 트윗을 힙으로 병합
- LeetCode 1642 Furthest Building You Can Reach — 크기 제한 힙 그리디
- LeetCode 480 Sliding Window Median (Hard) — 두 힙 + 지연 삭제
- LeetCode 502 IPO (Hard) — 정렬 + 최대 힙 그리디
- 프로그래머스 Lv.2 더 맵게 — 최소 힙 반복 합치기
- 프로그래머스 Lv.3 디스크 컨트롤러 — 요청 시각 정렬 + 소요 시간 최소 힙
- 프로그래머스 Lv.3 이중우선순위큐 — 최소/최대 힙 + 지연 삭제
- 프로그래머스 Lv.2 야근 지수 — 최대 힙에서 하나씩 줄이기

## 영어로 설명하기 (미국 면접용)

- "Since I repeatedly need the smallest element and then insert a new one, a min-heap fits perfectly: peeking is O(1) and each push or pop is O(log n)."
- "Python's heapq only provides a min-heap, so to simulate a max-heap I'll push the negated values and negate them again when I pop."
- "For the top k largest elements, I keep a min-heap of size k; whenever a new element is larger than the root, I replace the root. That's O(n log k) time and O(k) space, and it also works on a stream."
- "To track the median, I maintain two heaps — a max-heap for the smaller half and a min-heap for the larger half — and rebalance so their sizes differ by at most one. Then the median is just one or both of the roots."
- "Heaps don't support efficient arbitrary deletion, so I'd use lazy deletion: mark the element as removed and discard it only when it reaches the top."

## 체크리스트

- [ ] `heapify / heappush / heappop / heapreplace / nlargest / nsmallest` 의 동작과 복잡도를 말할 수 있다
- [ ] 최대 힙을 부호 반전으로, 복합 우선순위를 튜플로 표현할 수 있다
- [ ] heapify 가 O(n) 이라는 것과 heap 배열이 정렬된 상태가 아니라는 것을 안다
- [ ] Top-k 문제에서 힙의 방향(최소/최대)을 바로 고를 수 있다
- [ ] 두 힙으로 실시간 중앙값을 구하고 두 가지 불변식을 설명할 수 있다
- [ ] 비교 불가능한 객체를 넣을 때 tie-breaker 를 추가할 수 있다
- [ ] 지연 삭제가 필요한 상황(임의 삭제, 이중우선순위큐)을 알아본다
- [ ] 더 맵게 / 디스크 컨트롤러 유형을 효율성 테스트까지 통과하도록 풀 수 있다
