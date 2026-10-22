# 04. 슬라이딩 윈도우 (Sliding Window)

> 연속된 구간(부분 배열·부분 문자열)을 매번 새로 계산하지 않고, 들어오는 원소와 나가는 원소만 반영해 O(n) 으로 훑는 기법입니다.

## 이런 문제에서 떠올리세요

- 문제에 **"연속된(contiguous)"**, "부분 문자열(substring)", "부분 배열(subarray)", "구간", "연속한 k 일" 이 나온다
- "길이가 k 인 구간의 합/평균/최댓값" → **고정 길이 윈도우**
- "조건을 만족하는 **가장 긴** / **가장 짧은** 구간" → **가변 길이 윈도우**
- "중복 없는", "최대 k 종류", "최대 k 번 바꿔서", "t 의 문자를 모두 포함" → 윈도우 안의 상태를 해시맵/카운터로 관리
- "순열(애너그램)이 들어 있는가" → 길이 len(p) 인 고정 윈도우 + 빈도 비교
- "각 구간의 최댓값/최솟값" → 단조 덱(monotonic deque)
- 입력 크기 힌트: N ≤ 100,000 인데 구간을 다룬다 → 모든 구간 O(N^2) 불가, **O(N)** 윈도우를 의심
- 주의: 값에 **음수가 섞인 "합이 정확히 k 인 구간 개수"** 는 윈도우가 안 됩니다 → 누적합(prefix sum) + 해시맵

## 핵심 개념

### 1) 왜 빨라지는가

길이 3 인 구간 합을 모두 구한다고 해 봅시다.

```
nums = [2, 1, 5, 1, 3, 2]

매번 새로 더하기:  [2 1 5] = 8,  [1 5 1] = 7,  [5 1 3] = 9,  [1 3 2] = 6   → 구간마다 k 번 덧셈 → O(n·k)

슬라이딩 윈도우:
 [2  1  5] 1  3  2      sum = 8
  2 [1  5  1] 3  2      sum = 8 - 2 + 1 = 7     (나가는 2 빼고, 들어오는 1 더하기)
  2  1 [5  1  3] 2      sum = 7 - 1 + 3 = 9
  2  1  5 [1  3  2]     sum = 9 - 5 + 2 = 6     → 구간마다 O(1) → 전체 O(n)
```

### 2) 고정 길이 vs 가변 길이

| 구분 | 언제 | 움직이는 방법 |
|---|---|---|
| 고정 길이 | 구간 길이 k 가 주어짐 | r 이 한 칸 가면 l 도 한 칸 (l = r - k + 1) |
| 가변 길이 (최대) | "조건을 만족하는 가장 긴 구간" | r 을 늘리고, 조건이 깨지면 **깨지지 않을 때까지** l 을 줄임 |
| 가변 길이 (최소) | "조건을 만족하는 가장 짧은 구간" | r 을 늘려 조건을 만족시키고, **만족하는 동안** l 을 줄이며 기록 |

가변 윈도우가 성립하려면 **단조성**이 필요합니다.
"구간 [l, r] 이 조건을 어기면 그보다 긴 [l, r+1] 도 어긴다" (또는 반대) 처럼 늘리면/줄이면 상태가 한 방향으로 변해야 합니다.

### 3) 가변 윈도우 동작 예시 — 중복 없는 가장 긴 부분 문자열

```
s = "abcabcbb"

r=0 'a'  [a]          l=0  길이 1
r=1 'b'  [ab]         l=0  길이 2
r=2 'c'  [abc]        l=0  길이 3  ← best
r=3 'a'  'a' 가 윈도우 안(인덱스 0) → l = 0 + 1 = 1   [bca]  길이 3
r=4 'b'  'b' 가 윈도우 안(인덱스 1) → l = 2           [cab]  길이 3
r=5 'c'  'c' 가 윈도우 안(인덱스 2) → l = 3           [abc]  길이 3
r=6 'b'  'b' 가 윈도우 안(인덱스 4) → l = 5           [cb]   길이 2
r=7 'b'  'b' 가 윈도우 안(인덱스 6) → l = 7           [b]    길이 1
답 = 3
```

l 과 r 은 **둘 다 오른쪽으로만** 움직입니다. 각자 최대 n 번 움직이므로 안쪽에 while 문이 있어도 전체는 O(n) 입니다.

### 4) 최소 윈도우 — "늘려서 만족, 줄여서 최소화"

```
s = "ADOBECODEBANC", t = "ABC"

r 를 늘린다 → [ADOBEC] 에서 A,B,C 모두 포함 (유효)
  l 을 줄여 본다 → [DOBEC] A 가 빠짐 (무효) → 다시 r 늘리기
r 를 늘린다 → ... [DOBECODEBA] 에서 다시 유효
  l 을 줄인다 → [CODEBA] → [ODEBA] 무효 ...
... 마지막에 [BANC] (길이 4) 가 최소
```

윈도우가 유효한지 매번 두 Counter 를 비교하지 말고, "조건을 채운 글자 종류 수(have)" 를 관리하면 O(1) 에 판정할 수 있습니다.

### 5) 단조 덱 (monotonic deque) — 윈도우 최댓값

덱에 인덱스를 넣되 **값이 감소하는 순서**를 유지합니다. 새 값보다 작거나 같은 후보는 뒤에서 버립니다.

```
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3      덱(값으로 표시)    윈도우 최댓값
i=0  1                                        [1]
i=1  3  → 1 은 3 보다 작으니 pop              [3]
i=2 -1                                        [3, -1]            3
i=3 -3                                        [3, -1, -3]        3
i=4  5  → 3 은 윈도우 밖(popleft), -3, -1 pop [5]                5
i=5  3                                        [5, 3]             5
i=6  6  → 3, 5 pop                            [6]                6
i=7  7  → 6 pop                               [7]                7
```

"나보다 오른쪽에 있고 나보다 크거나 같은 값이 있으면, 나는 앞으로 최댓값이 될 수 없다" 가 핵심 논리입니다.

## 코드 템플릿

### 템플릿 1. 고정 길이 윈도우

```python
def fixed_window(nums, k):
    window = sum(nums[:k])            # 첫 윈도우
    best = window
    for r in range(k, len(nums)):
        window += nums[r] - nums[r - k]   # 들어오는 것 +, 나가는 것 -
        best = max(best, window)
    return best
```

### 템플릿 2. 가변 윈도우 — 조건을 만족하는 "가장 긴" 구간

```python
# is_valid 는 문제마다 다릅니다.
#   중복 없음        → count[c] <= 1 (방금 넣은 c 만 확인하면 충분)
#   최대 k 종류      → len(count) <= k
#   k 번 바꿔서 통일 → (r - l + 1) - max(count.values()) <= k
def longest_valid(s):
    count = {}
    l = 0
    best = 0
    for r, c in enumerate(s):
        count[c] = count.get(c, 0) + 1           # 1) r 을 넣는다
        while not is_valid(count, l, r):         # 2) 깨졌으면 l 을 줄여 복구
            count[s[l]] -= 1
            if count[s[l]] == 0:
                del count[s[l]]
            l += 1
        best = max(best, r - l + 1)              # 3) 유효한 윈도우로 답 갱신
    return best
```

### 템플릿 3. 가변 윈도우 — 조건을 만족하는 "가장 짧은" 구간

```python
from collections import Counter

def shortest_covering(s, t):
    need = Counter(t)
    required, have = len(need), 0
    window = {}
    best = (float("inf"), 0)
    l = 0
    for r, c in enumerate(s):
        window[c] = window.get(c, 0) + 1
        if c in need and window[c] == need[c]:
            have += 1
        while have == required:                  # 유효한 동안 줄이며 기록
            best = min(best, (r - l + 1, l))
            window[s[l]] -= 1
            if s[l] in need and window[s[l]] < need[s[l]]:
                have -= 1
            l += 1
    length, start = best
    return "" if length == float("inf") else s[start:start + length]
```

### 템플릿 4. 단조 덱으로 윈도우 최댓값

```python
from collections import deque

def window_max(nums, k):
    dq, res = deque(), []          # dq: 인덱스, 값은 감소 순서
    for i, x in enumerate(nums):
        if dq and dq[0] <= i - k:
            dq.popleft()           # 윈도우 밖
        while dq and nums[dq[-1]] <= x:
            dq.pop()               # 쓸모없는 후보 제거
        dq.append(i)
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res
```

## 시간 · 공간 복잡도

| 문제 유형 | 브루트포스 | 슬라이딩 윈도우 | 공간 |
|---|---|---|---|
| 길이 k 구간 합 최대 | O(n·k) | O(n) | O(1) |
| 최대 이익 (한 번 거래) | O(n^2) | O(n) | O(1) |
| 중복 없는 가장 긴 부분 문자열 | O(n^2) | O(n) | O(문자 종류) |
| k 번 바꿔서 가장 긴 반복 | O(n^2) | O(n) | O(26) |
| 순열 포함 여부 | O(n · m log m) | O(26 · n) 또는 O(n) | O(26) |
| 최소 윈도우 부분 문자열 | O(n^2) 이상 | O(\|s\| + \|t\|) | O(문자 종류) |
| 윈도우 최댓값 | O(n·k) | O(n) (단조 덱) / O(n log n) (힙) | O(k) |

## 자주 하는 실수

- [ ] **연속이 아닌** 부분 수열(subsequence) 문제에 윈도우를 쓴다. 윈도우는 연속 구간 전용입니다.
- [ ] 음수가 섞인 배열에서 "합이 k 이상인 최단 구간" 을 일반 윈도우로 푼다. 합의 단조성이 깨지므로 누적합 + 다른 기법이 필요합니다.
- [ ] 윈도우 길이를 `r - l` 로 계산한다. 양 끝 포함이면 **`r - l + 1`** 입니다.
- [ ] 고정 윈도우에서 첫 윈도우(인덱스 0..k-1)를 결과에 넣는 것을 빠뜨린다.
- [ ] 마지막 위치 해시맵 풀이에서 `last[c] >= l` 확인 없이 `l = last[c] + 1` 을 해 l 이 뒤로 간다. (예: `"abba"`)
- [ ] 카운터에서 개수가 0 이 된 키를 지우지 않고 `len(count)` 로 종류 수를 센다.
- [ ] 최소 윈도우에서 답을 `while` 문 **밖**에서 기록해 최소 길이를 놓친다. 줄이기 직전, 유효할 때 기록해야 합니다.
- [ ] 윈도우마다 `Counter(s[l:r+1])` 나 `sorted()` 를 새로 만든다. 이러면 O(n·k) 로 돌아갑니다.
- [ ] 단조 덱에 **값**을 넣어 윈도우 밖으로 나갔는지 판단하지 못한다. 덱에는 **인덱스**를 넣으세요.

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Best Time to Buy and Sell Stock | Easy | 지금까지의 최저가 유지 | `python practice.py start best-time-to-buy-sell-stock` |
| 2 | Longest Substring Without Repeating Characters | Medium | 문자 마지막 위치 해시맵 + l 점프 | `python practice.py start longest-substring-without-repeating` |
| 3 | Longest Repeating Character Replacement | Medium | 길이 - 최다 문자 수 ≤ k 유지 | `python practice.py start longest-repeating-character-replacement` |
| 4 | Permutation in String | Medium | 고정 윈도우 + 26 칸 빈도 비교 | `python practice.py start permutation-in-string` |
| 5 | Minimum Window Substring | Hard | 늘려서 만족, 줄여서 최소화 + have/required | `python practice.py start minimum-window-substring` |
| 6 | Sliding Window Maximum | Hard | 단조 감소 덱에 인덱스 저장 | `python practice.py start sliding-window-maximum` |

## 더 풀어 볼 문제

- LeetCode 643. Maximum Average Subarray I (고정 윈도우 기본)
- LeetCode 209. Minimum Size Subarray Sum (양수 배열, 가장 짧은 구간)
- LeetCode 1004. Max Consecutive Ones III (0 을 최대 k 개 포함하는 가장 긴 구간)
- LeetCode 438. Find All Anagrams in a String (Permutation in String 의 모든 위치 버전)
- LeetCode 904. Fruit Into Baskets (최대 2 종류를 포함하는 가장 긴 구간)
- LeetCode 340/159. Longest Substring with At Most K / Two Distinct Characters
- LeetCode 992. Subarrays with K Different Integers (정확히 K = 최대 K - 최대 K-1)
- LeetCode 862. Shortest Subarray with Sum at Least K (음수 포함 → 누적합 + 단조 덱)
- 프로그래머스 Lv.2 연속된 부분 수열의 합 (양수 배열, 가변 윈도우)
- 프로그래머스 Lv.3 보석 쇼핑 (2020 카카오 인턴십, 모든 종류를 포함하는 최단 구간 = Minimum Window 유형)
- 프로그래머스 Lv.2 할인 행사 (길이 10 고정 윈도우 + 카운터)
- 프로그래머스 Lv.2 롤케이크 자르기 (왼쪽/오른쪽 종류 수 카운터 이동)

## 영어로 설명하기 (미국 면접용)

- "Since the problem asks about a contiguous substring, I'll use a sliding window with two pointers that only move forward."
- "I expand the window by moving the right pointer, and whenever the window becomes invalid, I shrink it from the left until it's valid again."
- "Each character is added once and removed at most once, so even with the inner while loop the total time is O(n)."
- "To check validity in O(1), I keep a count of how many characters currently meet their required frequency instead of comparing two hash maps every step."
- "For the sliding window maximum, I maintain a monotonic decreasing deque of indices, so the front is always the maximum of the current window."

## 체크리스트

- [ ] 문제 문장에서 "연속(contiguous)" 이라는 신호를 찾아 윈도우를 떠올릴 수 있다.
- [ ] 고정 길이 / 가변(최장) / 가변(최단) 세 가지 템플릿을 보지 않고 쓸 수 있다.
- [ ] 안쪽 while 문이 있어도 O(n) 인 이유(각 원소는 한 번 들어오고 한 번 나감)를 설명할 수 있다.
- [ ] 윈도우가 성립하지 않는 경우(음수 포함 합, 비연속 부분 수열)를 구분할 수 있다.
- [ ] Longest Repeating Character Replacement 에서 max_count 를 줄이지 않아도 되는 이유를 설명할 수 있다.
- [ ] 단조 덱이 왜 O(n) 인지, 왜 인덱스를 저장하는지 설명할 수 있다.
- [ ] 프로그래머스 '보석 쇼핑' 을 보고 Minimum Window Substring 과 같은 구조임을 알아챌 수 있다.
