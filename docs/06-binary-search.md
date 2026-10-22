# 06. 이분 탐색 (Binary Search)

> 정렬되어 있거나 "단조로운(monotonic)" 조건이 있을 때, 후보 구간을 매번 절반으로 줄여 O(log n) 에 답을 찾습니다. PCCP 에서는 **답 자체를 이분 탐색하는 파라메트릭 서치(parametric search)** 가 특히 자주 나옵니다.

## 이런 문제에서 떠올리세요

- **정렬된 배열**에서 값 찾기, "x 이상인 첫 위치", "x 보다 큰 첫 위치", "x 의 개수" → 기본 이분 탐색 / `bisect`
- "회전된 정렬 배열", "2차원 정렬 행렬", "봉우리(peak) 찾기" → 변형 이분 탐색 (어느 절반이 정렬되어 있는지 판단)
- **"~ 의 최솟값(최댓값)을 구하라"** 인데, 답을 하나 정하면 "가능한가?" 를 쉽게 판정할 수 있다 → **파라메트릭 서치**
  - "모든 사람이 심사를 받는 데 걸리는 **최소 시간**" (프로그래머스 '입국심사')
  - "h 시간 안에 다 먹는 **최소 속도**" (Koko Eating Bananas)
  - "바위를 n 개 제거한 뒤 거리의 최솟값 중 **최댓값**" (프로그래머스 '징검다리')
  - "**최대** 몇 명이 징검다리를 건널 수 있나" (프로그래머스 '징검다리 건너기')
- 입력 크기 힌트
  - 값의 범위가 **10^9 ~ 10^18** 처럼 거대하다 → 하나씩 시도는 불가능, 답의 범위를 이분 탐색 (약 30 ~ 60 번)
  - N ≤ 100,000 이고 판정 함수가 O(N) → 전체 O(N log(범위)) 로 충분히 통과
  - 질의(query)가 많고 매번 "x 이상인 개수" 를 묻는다 → 정렬 한 번 + 질의마다 `bisect` O(log N)

## 핵심 개념

### 1) 기본 이분 탐색 — 후보 구간을 절반씩 버리기

```
nums = [-1, 0, 3, 5, 9, 12], target = 9

lo=0, hi=5 → mid=2, nums[2]=3  < 9  → 왼쪽 절반 버림, lo = 3
lo=3, hi=5 → mid=4, nums[4]=9 == 9  → 찾음! 인덱스 4

n = 100,000 이면 최대 17 번, n = 10^9 이면 최대 30 번 비교로 끝납니다.  (2^17 ≈ 131,072, 2^30 ≈ 10^9)
```

**구간 정의를 하나로 정하고 끝까지 지키는 것**이 버그를 막는 핵심입니다.

| 스타일 | 구간 의미 | while 조건 | 갱신 | 언제 |
|---|---|---|---|---|
| 닫힌 구간 | `[lo, hi]` 모두 후보 | `lo <= hi` | `lo = mid + 1` / `hi = mid - 1` | 값이 정확히 있는지 찾기 |
| lower bound | 답은 `[lo, hi]` 안에 반드시 있음 | `lo < hi` | 조건 참이면 `hi = mid`, 거짓이면 `lo = mid + 1` | "조건을 만족하는 첫 위치/최솟값" |

### 2) lower bound / upper bound 와 `bisect`

```
nums = [1, 2, 4, 4, 4, 7],  x = 4

인덱스:  0  1  2  3  4  5
값:      1  2  4  4  4  7
               ↑        ↑
     bisect_left(nums, 4) = 2   (4 이상이 처음 나오는 위치)
     bisect_right(nums, 4) = 5  (4 보다 큰 값이 처음 나오는 위치)

4 의 개수 = bisect_right - bisect_left = 3
4 미만인 원소 수 = bisect_left = 2
```

### 3) 파라메트릭 서치 (parametric search) — "최적화 문제" 를 "결정 문제" 로

**가장 중요한 개념입니다.** 다음 세 가지가 보이면 파라메트릭 서치입니다.

1. 구하는 답이 어떤 **수(시간, 속도, 거리, 개수)** 이고, 그 범위가 거대하다.
2. 답 후보 x 를 하나 정하면 **"x 로 가능한가?"** 를 빠르게(보통 O(n)) 판정할 수 있다.
3. 판정 결과가 **단조적**이다. x 가 가능하면 x 보다 큰 값(또는 작은 값)도 모두 가능하다.

그러면 판정 결과는 아래처럼 한 번만 바뀌고, 우리는 **바뀌는 경계**를 이분 탐색으로 찾습니다.

```
"최소 x" 를 구하는 경우 (예: 최소 시간, 최소 속도)
x       :  1   2   3   4   5   6   7   8 ...
가능?    :  F   F   F   F   T   T   T   T ...
                            ↑
                     처음으로 T 가 되는 x  = 답

"최대 x" 를 구하는 경우 (예: 최대 인원, 최소 거리의 최댓값)
x       :  1   2   3   4   5   6   7   8 ...
가능?    :  T   T   T   T   T   F   F   F ...
                        ↑
                 마지막으로 T 인 x  = 답
```

### 4) 예시: 프로그래머스 '입국심사' (= Minimum Time to Complete Trips)

심사관 2 명이 각각 7 분, 10 분씩 걸리고 6 명이 심사를 받아야 합니다. 모든 사람이 심사를 마치는 최소 시간은?

- "최소 시간 T" 를 직접 구하기는 어렵습니다.
- 하지만 **T 를 정하면** "T 분 동안 몇 명을 심사할 수 있나?" 는 쉽습니다: `T // 7 + T // 10`
- T 가 커질수록 심사 인원은 줄지 않습니다 → 단조 → 이분 탐색

```
lo = 1, hi = 7 * 6 = 42   (가장 빠른 심사관 혼자 다 해도 42 분이면 충분)

lo   hi   mid   mid//7 + mid//10   6명 이상?   동작
 1   42    21     3 + 2 = 5          F        lo = 22
22   42    32     4 + 3 = 7          T        hi = 32
22   32    27     3 + 2 = 5          F        lo = 28
28   32    30     4 + 3 = 7          T        hi = 30
28   30    29     4 + 2 = 6          T        hi = 29
28   29    28     4 + 2 = 6          T        hi = 28
28   28   → 종료, 답 28
```

사람 수가 10^9, 심사 시간이 10^9 이어도 범위는 최대 10^18 이고, 이분 탐색은 약 60 번이면 끝납니다.
매번 판정이 O(심사관 수) 이므로 전체 O(심사관 수 × 60) 입니다. **하나씩 시뮬레이션하면 절대 통과할 수 없는 크기**입니다.

### 5) 파라메트릭 서치를 설계하는 4 단계

| 단계 | 질문 | Koko Eating Bananas 예 |
|---|---|---|
| 1. 답의 의미 | 무엇을 이분 탐색하나? | 먹는 속도 k |
| 2. 판정 함수 | x 로 가능한가? | `sum(ceil(p / k)) <= h` |
| 3. 단조성 | x 가 커지면 가능성이 어떻게 변하나? | k 가 커지면 시간 감소 → 가능해지기만 함 |
| 4. 범위 | lo, hi 는? (hi 는 반드시 가능한 값) | `lo = 1`, `hi = max(piles)` |

### 6) 회전된 정렬 배열

```
[4, 5, 6, 7, 0, 1, 2]       mid = 3 (값 7)
 └─ 정렬 ──┘ └ 정렬 ┘
 lo        mid      hi

mid 로 나누면 적어도 한쪽은 정렬되어 있습니다.
- 최솟값 찾기: nums[mid] > nums[hi] 이면 최솟값은 오른쪽 (lo = mid + 1), 아니면 hi = mid
- 값 찾기: 정렬된 쪽의 범위 [시작값, 끝값] 안에 target 이 있으면 그쪽으로, 아니면 반대쪽으로
```

### 7) 중앙값 — 분할(partition) 이분 탐색

두 정렬 배열을 합치지 않고, 짧은 배열에서 "왼쪽 절반에 몇 개를 보낼지(i)" 를 이분 탐색합니다.
`A[i-1] <= B[j]` 이고 `B[j-1] <= A[i]` 이면 올바른 분할입니다 (j = 전체 절반 - i).

## 코드 템플릿

### 템플릿 1. 정확한 값 찾기 (닫힌 구간)

```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1          # [lo, hi] 모두 후보
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

### 템플릿 2. lower bound — "조건을 만족하는 첫 위치" (bisect 직접 구현)

```python
def lower_bound(nums, x):
    lo, hi = 0, len(nums)              # 답은 [0, n] 중 하나 (n 이면 '없음')
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] >= x:             # 조건을 만족 → mid 도 답 후보
            hi = mid
        else:
            lo = mid + 1
    return lo

# 표준 라이브러리
from bisect import bisect_left, bisect_right
# bisect_left(nums, x)  : x 이상이 처음 나오는 위치
# bisect_right(nums, x) : x 보다 큰 값이 처음 나오는 위치
```

### 템플릿 3. 파라메트릭 서치 — 가능한 "최솟값" 찾기

```python
def min_feasible(lo, hi, ok):
    """ok(x) 가 F F F T T T 형태일 때 처음 T 인 x. hi 는 반드시 ok(hi) == True 여야 함."""
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid                   # mid 가능 → 더 작은 쪽도 확인 (mid 포함)
        else:
            lo = mid + 1               # mid 불가능 → mid 보다 커야 함
    return lo

# 예: 입국심사
def immigration(n, times):
    return min_feasible(1, min(times) * n, lambda t: sum(t // x for x in times) >= n)
```

### 템플릿 4. 파라메트릭 서치 — 가능한 "최댓값" 찾기

```python
def max_feasible(lo, hi, ok):
    """ok(x) 가 T T T F F F 형태일 때 마지막 T 인 x. lo 는 반드시 ok(lo) == True 여야 함."""
    while lo < hi:
        mid = (lo + hi + 1) // 2       # 올림! (lo = mid 일 때 무한 루프 방지)
        if ok(mid):
            lo = mid                   # mid 가능 → 더 큰 쪽도 확인 (mid 포함)
        else:
            hi = mid - 1
    return lo
```

`max_feasible` 에서 `mid = (lo + hi) // 2` 를 쓰면 `lo = 3, hi = 4` 일 때 `mid = 3` 이 되고 `lo = mid` 로 영원히 멈춥니다.
**`lo = mid` 로 갱신하는 쪽이 있으면 mid 는 올림**으로 계산하세요.

## 시간 · 공간 복잡도

| 문제 유형 | 선형/브루트포스 | 이분 탐색 | 공간 |
|---|---|---|---|
| 정렬된 배열에서 값 찾기 | O(n) | O(log n) | O(1) |
| 2차원 정렬 행렬 탐색 | O(m·n) | O(log(m·n)) | O(1) |
| 회전 배열 최솟값 / 값 찾기 | O(n) | O(log n) | O(1) |
| Koko Eating Bananas | O(n · max(piles)) | O(n log max(piles)) | O(1) |
| 입국심사 / Minimum Time to Complete Trips | O(인원 · log n) (힙 시뮬레이션) | O(n log(범위)) | O(1) |
| 두 정렬 배열의 중앙값 | O(m + n) (병합) | O(log min(m, n)) | O(1) |

## 자주 하는 실수

- [ ] `while lo <= hi` 와 `while lo < hi` 를 섞어 쓰다가 무한 루프나 원소 누락이 생긴다. 템플릿 하나를 정해 그대로 쓰세요.
- [ ] `lo = mid` 로 갱신하면서 `mid = (lo + hi) // 2` (내림)을 써서 무한 루프. 이때는 **올림** `(lo + hi + 1) // 2`.
- [ ] 파라메트릭 서치에서 `hi` 를 너무 작게 잡아 답이 범위 밖에 있다. **hi 는 반드시 가능한 값**이어야 합니다 (예: `min(times) * n`).
- [ ] `lo = 0` 으로 시작했다가 판정 함수에서 0 으로 나눈다 (Koko 의 속도 k = 0). 범위의 의미를 확인하세요.
- [ ] 올림 나눗셈을 `math.ceil(p / k)` 로 해서 큰 수에서 부동소수점 오차. 정수로 `(p + k - 1) // k` 또는 `-(-p // k)`.
- [ ] 판정 함수의 **단조성**을 확인하지 않고 이분 탐색한다. 단조가 아니면 이분 탐색 결과는 의미가 없습니다.
- [ ] 판정 함수 안에서 합이 목표를 넘었는데도 끝까지 더한다. 범위가 크면 `if total >= n: return True` 로 일찍 끝내면 빨라집니다.
- [ ] 회전 배열에서 `nums[lo] <= nums[mid]` 의 `=` 를 빼먹어 원소 2 개일 때 틀린다.
- [ ] 정렬되지 않은 배열에 `bisect` 를 쓴다. 이분 탐색 전에 **정렬 여부**를 꼭 확인하세요.

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Binary Search | Easy | 닫힌 구간 [lo, hi] 기본형 | `python practice.py start binary-search` |
| 2 | Search a 2D Matrix | Medium | 2차원 → 1차원 인덱스 변환 (k // n, k % n) | `python practice.py start search-a-2d-matrix` |
| 3 | Koko Eating Bananas | Medium | 파라메트릭 서치: 속도 k 로 h 시간 안에 가능? | `python practice.py start koko-eating-bananas` |
| 4 | Minimum Time to Complete Trips | Medium | 파라메트릭 서치 = 프로그래머스 '입국심사' | `python practice.py start minimum-time-to-complete-trips` |
| 5 | Find Minimum in Rotated Sorted Array | Medium | nums[mid] 와 nums[hi] 비교 | `python practice.py start find-minimum-in-rotated-sorted-array` |
| 6 | Search in Rotated Sorted Array | Medium | 정렬된 절반을 찾아 범위 확인 | `python practice.py start search-in-rotated-sorted-array` |
| 7 | Median of Two Sorted Arrays | Hard | 짧은 배열의 분할 위치 이분 탐색 | `python practice.py start median-of-two-sorted-arrays` |

## 더 풀어 볼 문제

- LeetCode 35. Search Insert Position (lower bound 기본)
- LeetCode 34. Find First and Last Position of Element in Sorted Array (bisect_left / bisect_right)
- LeetCode 278. First Bad Version (F F T T 경계 찾기)
- LeetCode 162. Find Peak Element (정렬되지 않아도 이분 탐색)
- LeetCode 981. Time Based Key-Value Store (값 목록에서 bisect)
- LeetCode 1011. Capacity To Ship Packages Within D Days (파라메트릭 서치, 최소 용량)
- LeetCode 410. Split Array Largest Sum (파라메트릭 서치, Hard)
- LeetCode 1482. Minimum Number of Days to Make m Bouquets (파라메트릭 서치)
- 프로그래머스 Lv.3 입국심사 (이 저장소의 minimum-time-to-complete-trips 와 같은 유형)
- 프로그래머스 Lv.3 예산 (상한액을 파라메트릭 서치)
- 프로그래머스 Lv.3 징검다리 건너기 (2019 카카오 겨울 인턴십, 건널 수 있는 최대 인원)
- 프로그래머스 Lv.4 징검다리 (바위 사이 최소 거리의 최댓값)
- 프로그래머스 Lv.3 금과 은 운반하기 (시간을 파라메트릭 서치)
- 프로그래머스 Lv.2 순위 검색 (2021 KAKAO BLIND, 정렬 + bisect 로 "점수 x 이상 인원" 세기)
- 프로그래머스 PCCP 기출 2번 퍼즐 게임 챌린지 (숙련도를 파라메트릭 서치)

## 영어로 설명하기 (미국 면접용)

- "The array is sorted, so I can binary search and discard half of the remaining range at each step, which gives O(log n)."
- "Instead of searching for the answer directly, I'll binary search on the answer. Given a speed k, I can check in O(n) whether Koko finishes within h hours."
- "The check is monotonic: if speed k works, any faster speed also works. So the feasible values form a contiguous range, and I'm looking for the first feasible one."
- "The search space is from 1 to max(piles), so the total time is O(n log M), where M is the largest pile."
- "In a rotated sorted array, at least one half around mid is always sorted, so I check whether the target lies within that sorted half to decide which side to keep."

## 체크리스트

- [ ] 닫힌 구간 템플릿과 lower bound 템플릿의 차이(while 조건, 갱신식)를 설명할 수 있다.
- [ ] `bisect_left`, `bisect_right` 의 반환값 의미와 "x 의 개수" 를 구하는 법을 안다.
- [ ] 문제를 보고 "답을 정하면 판정이 쉽고, 판정이 단조적이다" 를 확인해 파라메트릭 서치를 떠올릴 수 있다.
- [ ] 판정 함수 · 단조성 · lo/hi 범위를 먼저 적고 코드를 쓴다.
- [ ] "최솟값 찾기" 와 "최댓값 찾기" 템플릿을 구분하고, 최댓값 쪽에서 mid 를 올림하는 이유를 안다.
- [ ] 프로그래머스 '입국심사' 를 보지 않고 10 분 안에 풀 수 있다.
- [ ] 회전 배열에서 어느 절반이 정렬되어 있는지 판단하는 조건을 말할 수 있다.
- [ ] 두 정렬 배열의 중앙값을 병합 O(m + n) → 분할 이분 탐색 O(log min(m, n)) 순서로 설명할 수 있다.
