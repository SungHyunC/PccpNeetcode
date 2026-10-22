# 17. 구간 (Intervals)

> 구간 문제의 8할은 "무엇을 기준으로 정렬할까?" 입니다. 시작 기준 정렬은 **병합**, 끝 기준 정렬은 **선택/찌르기**, 동시에 몇 개인지는 **스위프 라인**.

## 이런 문제에서 떠올리세요

- 입력이 `[start, end]` 쌍의 리스트 → 구간 문제
- "겹치는 구간을 합쳐라", "빈 시간을 구하라" → 시작 기준 정렬 + 병합 (Merge Intervals)
- "최대 몇 개를 겹치지 않게 고를까", "최소 몇 개를 지울까", "최소 몇 개의 점(카메라/화살)으로 모두 찌를까" → **끝 기준 정렬 그리디**
- "동시에 최대 몇 개", "회의실/객실/서버가 최소 몇 개 필요" → 최소 힙 또는 스위프 라인 (sweep line)
- "각 질의 지점을 포함하는 구간 중 ~" → 구간·질의를 함께 정렬하는 오프라인 처리 + 힙
- "구간 [l, r] 에 x 를 더하는 작업이 많다" → 차분 배열 (difference array)
- 입력 크기: N ≤ 100,000 이면 정렬 O(N log N) 한 번 + 선형 스캔이 정답인 경우가 대부분입니다. O(N²) 로 모든 쌍을 비교하면 시간 초과.

## 핵심 개념

### 1) 두 구간이 겹치는 조건

구간 A = [a1, a2], B = [b1, b2] 가 겹친다 ⇔ **a1 < b2 그리고 b1 < a2** (닫힌 구간이면 ≤)

```
겹치지 않는 경우는 딱 두 가지뿐입니다.
  A 가 완전히 왼쪽:   [a1──a2]          a2 ≤ b1
                               [b1──b2]
  A 가 완전히 오른쪽:          [a1──a2]   b2 ≤ a1
                     [b1──b2]
그 외는 전부 겹침 → not (a2 ≤ b1 or b2 ≤ a1) = (a1 < b2 and b1 < a2)
```

겹친 부분(교집합)은 `[max(a1, b1), min(a2, b2)]` 이고, `max(a1,b1) < min(a2,b2)` 일 때만 존재합니다.

**끝점이 닿는 경우**(`[1,5]` 와 `[5,8]`)를 겹침으로 볼지는 문제마다 다릅니다. 회의실 문제는 보통 "안 겹침", 단속카메라·Merge Intervals 는 "겹침(포함)". `<` 와 `≤` 하나 차이로 오답이 나므로 문제를 읽자마자 표시해 두세요.

### 2) 시작 기준 정렬 vs 끝 기준 정렬

| 정렬 기준 | 언제 | 대표 문제 | 이유 |
|---|---|---|---|
| 시작(start) | 구간을 **합치거나**, 겹침 **존재 여부**만 볼 때 | Merge / Insert Interval, Meeting Rooms | 정렬 후 새 구간은 "직전 결과" 하고만 겹칠 수 있음 |
| 끝(end) | 겹치지 않게 **최대한 많이 고르거나**, 최소 개수 점으로 **찌를 때** | Non-overlapping Intervals, 단속카메라, 풍선 터뜨리기 | 가장 먼저 끝나는 것을 고르면 뒤에 남는 공간이 최대 (교환 논증) |
| 시작 + 끝 시각 힙 | **동시에 몇 개**가 진행 중인지 | Meeting Rooms II | 지금 쓰는 자원 중 "가장 빨리 비는 것" 만 알면 됨 |

```
시작 기준 병합 (Merge Intervals)
  정렬:  [1,3] [2,6] [8,10] [15,18]
           └──┬──┘
  결과:  [1,6]      [8,10] [15,18]

끝 기준 선택 (활동 선택, activity selection)
  끝 정렬:  [1,11] [2,12] [11,22] [1,100]
  선택:      ✔       ✘      ✔       ✘      → 2개 남김 = 2개 제거
  시작 기준으로 [1,100] 을 먼저 고르면 나머지를 다 못 고르는 함정에 빠집니다.
```

### 3) 스위프 라인 (sweep line) — 이벤트로 바꾸기

구간 `[s, e)` 를 두 개의 이벤트 `(s, +1)`, `(e, -1)` 로 쪼개고 시간 순으로 훑으면, 누적합이 "그 순간 진행 중인 구간 수" 입니다.

```
회의: [0,30] [5,10] [15,20]

시간    0    5    10   15   20   30
이벤트  +1   +1   -1   +1   -1   -1
진행중   1    2    1    2    1    0      → 최댓값 2 = 필요한 회의실 수

같은 시각에 -1 과 +1 이 있으면?
  [1,5] [5,8]: (5,-1) 을 (5,+1) 보다 먼저 처리해야 동시 진행 1개.
  파이썬 튜플 정렬은 (5,-1) < (5,+1) 이라 자동으로 맞습니다.
```

### 4) 차분 배열 (difference array)

"구간 `[l, r]` 에 v 를 더하라" 가 많고 마지막에 한 번만 결과를 볼 때, 매번 r-l+1 칸을 갱신하지 않고 양 끝에만 표시합니다.

```
길이 8, 작업: [1,3] += 2, [2,6] += 1

diff:     idx 0  1  2  3  4  5  6  7  8
[1,3]+=2:     0  2  0  0 -2  0  0  0  0
[2,6]+=1:     0  2  1  0 -2  0  0 -1  0
누적합:       0  2  3  3  1  1  1  0  0   ← 각 칸의 최종 값
```

작업 K 개를 O(1) 씩, 마지막 누적합 O(N) → 전체 O(K + N). 좌표가 크면(10^9) 좌표 압축(coordinate compression) 후 적용하거나, 스위프 라인(이벤트 정렬)으로 바꿉니다. 2차원 버전은 [19. 구현 · 시뮬레이션](19-implementation.md) 에서 다룹니다.

### 5) 오프라인 질의 (offline queries)

"질의마다 조건을 만족하는 구간 중 최소/최대" 는 질의를 정렬해 한꺼번에 처리하면 각 구간을 힙에 한 번만 넣고 한 번만 빼면 됩니다. 답은 원래 인덱스에 써 넣습니다 (`sorted(range(len(q)), key=q.__getitem__)`).

## 코드 템플릿

```python
# 1) 병합 (Merge Intervals) — 시작 기준 정렬
def merge(intervals):
    intervals.sort()                       # (start, end) 순
    merged = []
    for s, e in intervals:
        if not merged or s > merged[-1][1]:    # 닿기만 해도 합치려면 >, 안 합치려면 >=
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)  # max 필수: [1,10],[2,3]
    return merged
```

```python
# 2) 끝 기준 그리디 — 최대 선택 / 최소 제거 / 최소 찌르기
def max_non_overlapping(intervals):
    intervals.sort(key=lambda x: x[1])     # 끝 기준
    count, last_end = 0, float("-inf")
    for s, e in intervals:
        if s >= last_end:                  # 찌르기(점 포함)라면 s > last_end
            count += 1
            last_end = e
    return count                           # 최소 제거 = len(intervals) - count
```

```python
# 3) 동시에 진행 중인 최대 개수 — 힙 / 스위프 라인
import heapq

def min_rooms_heap(intervals):
    intervals.sort()
    ends = []                              # 사용 중인 방들의 끝 시각
    for s, e in intervals:
        if ends and ends[0] <= s:          # 가장 빨리 비는 방 재사용
            heapq.heappop(ends)
        heapq.heappush(ends, e)
    return len(ends)

def min_rooms_sweep(intervals):
    events = [(s, 1) for s, _ in intervals] + [(e, -1) for _, e in intervals]
    events.sort()                          # 같은 시각이면 -1(끝) 먼저
    cur = best = 0
    for _, d in events:
        cur += d
        best = max(best, cur)
    return best
```

```python
# 4) 1차원 차분 배열 — 구간 덧셈 여러 번, 마지막에 한 번 조회
def range_add(n, updates):                 # updates: [l, r, v] (닫힌 구간)
    diff = [0] * (n + 1)
    for l, r, v in updates:
        diff[l] += v
        diff[r + 1] -= v                   # r+1 칸이 필요하므로 길이 n+1
    result, run = [], 0
    for i in range(n):
        run += diff[i]
        result.append(run)
    return result
```

## 시간 · 공간 복잡도

| 기법 | 시간 | 공간 | 비고 |
|---|---|---|---|
| 시작 기준 정렬 + 병합 | O(N log N) | O(N) | 정렬이 지배 |
| 정렬된 입력에 구간 삽입 | O(N) | O(N) | 왼쪽/겹침/오른쪽 3구역 |
| 끝 기준 그리디 | O(N log N) | O(1) | 정렬 제외 |
| 최소 힙 회의실 | O(N log N) | O(N) | |
| 스위프 라인 | O(N log N) | O(N) | 이벤트 2N 개 정렬 |
| 차분 배열 | O(K + L) | O(L) | L = 좌표 범위 |
| 오프라인 질의 + 힙 | O(N log N + Q log Q) | O(N + Q) | |
| 모든 쌍 비교 (브루트포스) | O(N²) | O(1) | N = 10^5 이면 시간 초과 |

## 자주 하는 실수

- 끝점이 닿는 경우(`[1,5]`, `[5,8]`)의 처리: 문제에서 겹침인지 아닌지 확인하지 않고 `<` / `≤` 를 대충 씀
- 병합할 때 `merged[-1][1] = e` 로 덮어씀 → `[1,10], [2,3]` 에서 `[1,3]` 이 되는 버그. 반드시 `max`
- 최대 선택/찌르기 문제를 **시작 기준**으로 정렬함 → 긴 구간 하나가 앞에 오면 망함. 끝 기준!
- 스위프 라인에서 같은 시각의 시작/끝 처리 순서를 생각하지 않음
- 입력이 정렬되어 있다는 보장이 없는데 정렬을 빼먹음 (반대로 이미 정렬된 입력을 O(N log N) 으로 다시 정렬하는 것은 괜찮지만 면접에서는 언급)
- 방향이 섞인 구간(`[9, 2]`)을 `[min, max]` 로 정규화하지 않음
- `intervals.sort()` 는 원본을 바꿉니다. 원본을 보존해야 하면 `sorted(intervals)`
- 차분 배열 길이를 n 으로 잡아 `diff[r+1]` 에서 IndexError
- 질의를 정렬해 처리한 뒤 **원래 순서**로 답을 돌려주는 것을 잊음

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Meeting Rooms | Easy | 시작 정렬 후 인접 쌍만 비교 | `python practice.py start meeting-rooms` |
| 2 | Merge Intervals | Medium | 시작 정렬 + 마지막 구간과 병합 (`max`) | `python practice.py start merge-intervals` |
| 3 | Insert Interval | Medium | 왼쪽 / 겹침 / 오른쪽 3구역 O(N) | `python practice.py start insert-interval` |
| 4 | Non-overlapping Intervals | Medium | 끝 정렬 그리디, 답 = N - 최대 선택 | `python practice.py start non-overlapping-intervals` |
| 5 | Meeting Rooms II | Medium | 끝 시각 최소 힙 / 스위프 라인 | `python practice.py start meeting-rooms-ii` |
| 6 | Surveillance Cameras | Medium | 구간 찌르기: 끝 정렬, 끝에 카메라 | `python practice.py start surveillance-cameras` |
| 7 | Minimum Interval to Include Each Query | Hard | 질의 오프라인 정렬 + (크기, 끝) 힙 | `python practice.py start minimum-interval-to-include-each-query` |

## 더 풀어 볼 문제

- LeetCode 452 Minimum Number of Arrows to Burst Balloons (단속카메라와 같은 구간 찌르기)
- LeetCode 986 Interval List Intersections (투 포인터로 교집합)
- LeetCode 1288 Remove Covered Intervals (시작 오름차순·끝 내림차순 정렬)
- LeetCode 759 Employee Free Time (병합 후 빈 구간)
- LeetCode 1094 Car Pooling (차분 배열 / 스위프 라인)
- LeetCode 715 Range Module (고급: 정렬된 구간 유지)
- 프로그래머스 Lv.3 단속카메라
- 프로그래머스 Lv.2 호텔 대실 (Meeting Rooms II 와 같은 구조, 청소 시간 10분 추가)
- 프로그래머스 Lv.2 요격 시스템 (열린 구간 찌르기)
- 프로그래머스 Lv.3 광고 삽입 (누적합 + 슬라이딩 윈도우, 시간 문자열 파싱)

## 영어로 설명하기 (미국 면접용)

- "Since the intervals aren't sorted, I'll first sort them by start time, so any interval can only overlap with the last one I've merged."
- "Two intervals overlap exactly when each one starts before the other ends — `a.start < b.end and b.start < a.end`. Can I assume that touching endpoints don't count as an overlap?"
- "For the minimum number of removals, I'll flip the question: keep as many non-overlapping intervals as possible. Greedily picking the one that ends earliest is optimal by an exchange argument."
- "The number of rooms equals the maximum number of meetings happening at the same time. I'll keep a min-heap of end times, so the top of the heap tells me the room that frees up first."
- "Sorting dominates, so the overall complexity is O(n log n) time and O(n) extra space for the heap."

## 체크리스트

- [ ] 두 구간의 겹침 조건 `a1 < b2 and b1 < a2` 를 그림 없이 바로 쓸 수 있다
- [ ] 끝점이 닿는 경우를 문제에서 확인하고 `<` / `≤` 를 의식적으로 선택한다
- [ ] "병합 → 시작 정렬", "최대 선택·최소 찌르기 → 끝 정렬" 을 구분하고 이유(교환 논증)를 말할 수 있다
- [ ] 회의실 문제를 힙과 스위프 라인 두 가지로 풀 수 있다
- [ ] 스위프 라인에서 같은 시각의 이벤트 순서를 설명할 수 있다
- [ ] 차분 배열로 구간 덧셈을 O(1) 에 처리하고 마지막에 누적합을 낼 수 있다
- [ ] 질의를 정렬해 오프라인으로 처리한 뒤 원래 순서로 답을 돌려줄 수 있다
