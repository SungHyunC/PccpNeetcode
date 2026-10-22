# 16. 그리디 (Greedy)

> 매 순간 "지금 가장 좋아 보이는 선택" 을 하고 되돌아보지 않는 기법입니다. 빠르고 코드가 짧지만, **그 선택이 최적해를 잃지 않는다는 근거** 가 있어야만 정답입니다.

## 이런 문제에서 떠올리세요

- "최소 개수로", "최대한 많이", "가장 큰/작은 수를 만들어라" + 입력이 커서(n ≤ 10^5 ~ 10^6) **O(n) 또는 O(n log n)** 이 필요한 문제
- **정렬하면 순서가 명확해지는** 문제: 회의실 배정(끝나는 시간 순), 구명보트(가벼운+무거운 짝), 단속카메라(구간 끝 기준)
- 앞에서부터 보면서 **"도달 가능한 범위", "누적합", "필요한 최소/최대 개수"** 하나만 갱신하면 되는 문제
- 숫자 문자열에서 **앞자리를 키우는/줄이는** 문제 → 단조 스택 그리디 (프로그래머스 '큰 수 만들기')
- 반대로 이런 신호가 있으면 **그리디를 의심하고 DP 를 고려**하세요
  - 동전 액면가가 임의로 주어짐 (예: [1, 3, 4]) — 배수 관계가 아니면 그리디 실패
  - "어떤 선택이 나중에 영향을 준다" — 지금 작은 이익이 나중에 큰 이익을 막는 경우 (배낭, 정수 삼각형)
- 입력 크기 힌트
  - n ≤ 20 → 완전 탐색으로 그리디 가설을 검증해 볼 수 있음
  - n ≤ 10^5 이상 → 그리디 O(n) / 정렬 O(n log n) 이 거의 유일한 선택

## 핵심 개념

### 그리디가 정답이 되는 두 조건

1. **탐욕 선택 속성 (greedy choice property)**: 지금 최선의 선택을 포함하는 최적해가 항상 존재한다.
2. **최적 부분 구조 (optimal substructure)**: 그 선택 후 남은 문제의 최적해 + 지금 선택 = 전체 최적해.

DP 도 2번을 요구합니다. 차이는 1번입니다. DP 는 모든 선택지를 비교하고, 그리디는 하나만 골라 확정합니다.

### 그리디 정당화: 교환 논법 (exchange argument)

"내 그리디 해와 다른 최적해 OPT 가 있다고 하자. OPT 의 선택 하나를 그리디의 선택으로 **바꿔도(교환) 손해가 없다**. 이를 반복하면 OPT 를 그리디 해로 바꿀 수 있으므로 그리디 해도 최적이다."

```
예) 회의실 배정: 끝나는 시간이 가장 빠른 회의부터 고른다

  OPT     : [──B──]      [──C──]   [──D──]
  그리디   : [─A─]                             A = 가장 먼저 끝나는 회의 (A.end ≤ B.end)

  OPT 의 첫 회의 B 를 A 로 바꿔도 A.end ≤ B.end 이므로 C, D 와 겹치지 않음
  → 회의 수는 그대로 → A 를 고르는 것은 손해가 아님 → 남은 구간에서 같은 논리를 반복
```

```
예) 큰 수 만들기: 앞자리 숫자가 더 작으면 지운다

  number = 1 9 2 4, k = 2
  1 을 남기고 다른 걸 지운 해 "1x" 와 1 을 지운 해 "9x" 를 비교하면 첫 자리에서 9 > 1
  → 앞에 있는 작은 숫자를 지우는 쪽으로 '교환' 해도 결과가 같거나 커짐
```

### 그리디가 실패하는 대표 예: 동전 교환

```
coins = [1, 3, 4], amount = 6

그리디(큰 동전부터) : 4 → 남은 2 → 1 → 1      = 3개   ✘
최적 (DP)           : 3 → 3                   = 2개   ✔

dp[a] = min(dp[a - c] + 1)
 a  : 0  1  2  3  4  5  6
 dp : 0  1  2  1  1  2  2
```

- 한국 화폐(10, 50, 100, 500)처럼 **큰 액면가가 작은 액면가의 배수** 이면 그리디가 맞습니다.
- 액면가가 임의로 주어지면 반례를 몇 개 손으로 만들어 보고, 하나라도 있으면 DP 로 갑니다.
- 0/1 배낭도 "가치/무게 비율 순" 그리디가 틀립니다 (쪼갤 수 있는 fractional knapsack 에서만 정답).

### 그리디 vs DP 판단 흐름

```
문제 읽기
   │
   ├─ 작은 예제로 "가장 좋아 보이는 선택" 규칙을 세운다
   │
   ├─ 손으로 반례를 3~5개 찾아본다 (작은 n 완전 탐색 코드로 대조하면 확실)
   │      ├─ 반례 있음 → DP / 완전 탐색 / 다른 접근
   │      └─ 반례 없음 → 교환 논법으로 한 문장 정당화
   │
   └─ 구현 (대부분 정렬 + 한 번의 순회, 또는 상태 변수 몇 개)
```

### 앞에서부터 상태 하나만 갱신하는 그리디

```
Jump Game: farthest = 지금까지 도달 가능한 가장 먼 칸
  nums     :  2  3  1  1  4
  i+nums[i]:  2  4  3  4  8
  farthest :  2  4  4  4  8   → 마지막 칸(4) ≤ farthest → True

Jump Game II: BFS 층을 구간으로 압축
  층 0 = [0]   → 다음 층 끝 2   (jumps 1)
  층 1 = [1,2] → 다음 층 끝 4   (jumps 2) → 도착

Kadane (Maximum Subarray): 누적합이 음수면 버리고 새로 시작
  nums : -2  1 -3  4 -1  2  1 -5  4
  cur  : -2  1 -2  4  3  5  6  1  5      best = 6
```

## 코드 템플릿

### 1) 정렬 기반 그리디 — 구간 스케줄링 (끝나는 시간 순)

```python
def max_non_overlapping(intervals):
    intervals.sort(key=lambda x: x[1])      # 끝나는 시간 오름차순
    count, end = 0, float("-inf")
    for s, e in intervals:
        if s >= end:                         # 겹치지 않으면 선택
            count += 1
            end = e
    return count
```

### 2) 정렬 + 투 포인터 그리디 — 짝 맞추기 (구명보트 유형)

```python
def min_boats(people, limit):
    people.sort()
    lo, hi, boats = 0, len(people) - 1, 0
    while lo <= hi:
        if people[lo] + people[hi] <= limit:  # 가장 가벼운 사람과 함께 태울 수 있으면
            lo += 1
        hi -= 1                               # 가장 무거운 사람은 항상 이번 보트에
        boats += 1
    return boats
```

### 3) 도달 범위 갱신 그리디

```python
def can_jump(nums):
    farthest = 0
    for i, step in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + step)
    return True
```

### 4) 단조 스택 그리디 — k 개 지워서 가장 큰 수

```python
def largest_after_removal(number, k):
    stack = []
    for d in number:
        while k and stack and stack[-1] < d:   # 가장 작은 수를 원하면 부등호를 > 로
            stack.pop()
            k -= 1
        stack.append(d)
    return "".join(stack[:len(stack) - k])     # 남은 k 는 뒤에서 제거
```

### 5) 범위 [lo, hi] 추적 그리디 — 와일드카드 괄호

```python
def check_valid_string(s):
    lo = hi = 0
    for ch in s:
        lo += 1 if ch == "(" else -1
        hi += 1 if ch != ")" else -1
        if hi < 0:
            return False
        lo = max(lo, 0)
    return lo == 0
```

## 시간 · 공간 복잡도

| 문제 | 시간 | 공간 | 그리디 규칙 |
|---|---|---|---|
| Maximum Subarray | O(n) | O(1) | 누적합 < 0 이면 새로 시작 |
| Jump Game | O(n) | O(1) | farthest 갱신 |
| Jump Game II | O(n) | O(1) | 층(구간) 끝에서 점프 +1 |
| Gas Station | O(n) | O(1) | 연료가 음수면 다음 칸부터 다시 |
| Hand of Straights | O(n log n) | O(n) | 가장 작은 카드로 묶음 시작 |
| Partition Labels | O(n) | O(1) | 마지막 등장 위치까지 확장 후 끊기 |
| Valid Parenthesis String | O(n) | O(1) | 열린 괄호 수 범위 [lo, hi] |
| 큰 수 만들기 | O(n) | O(n) | 단조 감소 스택 |
| 정렬 기반 그리디 일반 | O(n log n) | O(1)~O(n) | 정렬 기준이 핵심 |

## 자주 하는 실수

- [ ] **정당화 없이 그리디 제출**: 예제는 맞는데 숨은 테스트에서 틀림. 반례를 최소 3개는 찾아보세요.
- [ ] **동전 문제를 무조건 그리디로**: 액면가가 배수 관계가 아니면 DP.
- [ ] **정렬 기준을 잘못 고름**: 회의실 배정은 '시작 시간' 이 아니라 '끝나는 시간' 순. 기준을 바꿔 가며 반례를 찾아보세요.
- [ ] **Kadane 의 best 초기값을 0 으로**: 모든 원소가 음수면 틀립니다. `nums[0]` 으로 시작.
- [ ] **Jump Game II 를 마지막 칸까지 순회**: `range(n - 1)` 이어야 점프 수가 1 늘지 않습니다.
- [ ] **큰 수 만들기에서 남은 k 처리 누락**: "54321" 처럼 내림차순이면 pop 이 한 번도 안 일어납니다.
- [ ] **큰 수 만들기를 O(n × k) 로**: 각 자리마다 구간 최댓값을 찾으면 n = 10^6 에서 시간 초과.
- [ ] **Valid Parenthesis String 에서 `lo = max(lo, 0)` 누락**.
- [ ] **Gas Station 에서 전체 합 확인 누락**: 한 바퀴 합이 음수면 -1.

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Maximum Subarray | Medium | Kadane: 음수 누적합 버리기 | `python practice.py start maximum-subarray` |
| 2 | Jump Game | Medium | 도달 가능한 최대 위치 갱신 | `python practice.py start jump-game` |
| 3 | Jump Game II | Medium | BFS 층을 구간으로 압축 | `python practice.py start jump-game-ii` |
| 4 | Gas Station | Medium | 전체 합 ≥ 0, 실패 지점 다음에서 재시작 | `python practice.py start gas-station` |
| 5 | Hand of Straights | Medium | 가장 작은 카드부터 묶음, Counter | `python practice.py start hand-of-straights` |
| 6 | Partition Labels | Medium | 마지막 등장 위치로 구간 확장 | `python practice.py start partition-labels` |
| 7 | Valid Parenthesis String | Medium | 열린 괄호 수 범위 [lo, hi] | `python practice.py start valid-parenthesis-string` |
| 8 | Make Largest Number by Removing K Digits | Medium | 큰 수 만들기 유형: 단조 스택 | `python practice.py start make-largest-number-by-removing-k-digits` |

## 더 풀어 볼 문제

- LeetCode 435 Non-overlapping Intervals / 452 Minimum Number of Arrows to Burst Balloons (끝나는 시간 정렬)
- LeetCode 402 Remove K Digits (가장 작은 수 버전 단조 스택)
- LeetCode 1899 Merge Triplets to Form Target Triplet (조건에 맞는 것만 합치기)
- LeetCode 621 Task Scheduler (가장 많은 작업 기준 배치)
- LeetCode 135 Candy (양방향 두 번 훑기, Hard)
- LeetCode 406 Queue Reconstruction by Height (정렬 + 삽입)
- 프로그래머스 Lv.2 "큰 수 만들기" (단조 스택, n ≤ 1,000,000)
- 프로그래머스 Lv.2 "구명보트" (정렬 + 투 포인터)
- 프로그래머스 Lv.3 "단속카메라" (구간 끝 기준 정렬)
- 프로그래머스 Lv.1 "체육복" (빌려주기 순서 그리디)
- 프로그래머스 Lv.2 "조이스틱" (그리디 + 방향 전환 최소화)
- 프로그래머스 Lv.3 "섬 연결하기" (크루스칼 = 간선 정렬 그리디)

## 영어로 설명하기 (미국 면접용)

- "My greedy choice is to always pick the meeting that ends earliest, because it leaves the most room for the remaining meetings."
- "To justify it, I'll use an exchange argument: take any optimal solution and swap its first choice with mine — the result is still valid and no worse, so my choice is safe."
- "Before committing to greedy, let me check for a counterexample. With coins 1, 3 and 4 and an amount of 6, greedy gives three coins but the optimum is two, so this problem needs DP instead."
- "I only need to track the farthest index I can reach so far; everything before it is reachable, so this runs in O(n) time and O(1) space."
- "I'll keep a monotonic decreasing stack: whenever the current digit is larger than the top, removing the top makes the number bigger, as long as I still have deletions left."

## 체크리스트

- [ ] 그리디가 정답이 되는 두 조건(탐욕 선택 속성, 최적 부분 구조)을 말할 수 있다
- [ ] 교환 논법으로 내 그리디 규칙을 한두 문장으로 정당화할 수 있다
- [ ] 동전 교환 [1, 3, 4] / 6 반례로 그리디가 실패하는 경우를 설명하고 DP 로 전환할 수 있다
- [ ] 정렬 기준(시작 vs 끝, 오름 vs 내림)을 바꿔 가며 반례를 찾아볼 수 있다
- [ ] 작은 입력용 완전 탐색 코드로 그리디 결과를 대조해 본 적이 있다
- [ ] Kadane, 도달 범위, BFS 층 압축 같은 "상태 하나만 갱신" 그리디를 구현할 수 있다
- [ ] 단조 스택으로 "k 개 지워서 가장 큰/작은 수" 를 O(n) 에 풀 수 있다
