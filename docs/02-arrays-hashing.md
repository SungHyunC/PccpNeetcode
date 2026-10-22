# 02. 배열 · 해시 (Arrays & Hashing)

> "이미 본 적 있나?", "몇 번 나왔나?", "같은 그룹인가?" 를 O(1)에 답하는 것이 해시의 힘입니다. 대부분의 O(N²) → O(N) 최적화가 여기서 시작됩니다.

## 이런 문제에서 떠올리세요

- **중복** 확인, **등장 횟수**, **빈도수 상위 K 개** → `set`, `Counter`
- **두 값의 합/차가 target** → 보수(complement)를 해시맵에서 찾기
- **같은 성질끼리 묶기**(애너그램, 같은 패턴) → 정규화한 키 + `defaultdict(list)`
- **연속 부분 배열의 합** (음수 포함) → 누적합(prefix sum) + 해시맵
- 입력 N ≤ 10^5 인데 2중 반복이 떠오른다 → "안쪽 반복을 해시 조회로 바꿀 수 있을까?"

## 핵심 개념

### 해시 테이블은 "값 → 위치" 를 바로 계산한다

```
key ──hash()──▶ 버킷 번호 ──▶ 값
"apple"  → 3     [0] -
"banana" → 0     [1] -
                 [2] -
                 [3] "apple": 5
평균 조회/삽입 O(1), 최악 O(N) (충돌이 몰릴 때)
```

- `set` : 키만 저장 (존재 여부)
- `dict` : 키 → 값
- 키는 **해시 가능(immutable)** 해야 합니다: `int, str, tuple` ✅ / `list, set, dict` ❌

### 브루트포스 → 해시 최적화 패턴

```
Two Sum: target = 9, nums = [2, 7, 11, 15]

i=0  x=2   need=7   seen={}          → 없음, seen={2:0}
i=1  x=7   need=2   seen={2:0}       → 있음! [0, 1]

"안쪽 for 문으로 찾던 것"을 "dict 조회"로 바꾸면 O(N²) → O(N)
```

### 누적합(prefix sum)

```
nums   =    [3,  4,  7,  2, -3]
prefix = [0, 3,  7, 14, 16, 13]

sum(nums[i:j]) = prefix[j] - prefix[i]     ← 구간 합을 O(1) 에
```

누적합 + 해시맵 조합은 "합이 k 인 연속 부분 배열 개수", "0 과 1 의 개수가 같은 가장 긴 구간" 같은 문제를 O(N)에 풉니다.

## 코드 템플릿

### 템플릿 1 — 이미 본 값 / 짝 찾기

```python
def two_sum(nums, target):
    seen = {}                       # 값 -> 인덱스
    for i, x in enumerate(nums):
        if target - x in seen:      # 짝을 먼저 확인
            return [seen[target - x], i]
        seen[x] = i                 # 그다음 자신을 저장
```

### 템플릿 2 — 빈도수 세기 & 그룹핑

```python
from collections import Counter, defaultdict

cnt = Counter(nums)                         # 값 -> 횟수
top_k = [v for v, _ in cnt.most_common(k)]

groups = defaultdict(list)
for s in strs:
    groups[''.join(sorted(s))].append(s)    # 정규화한 키로 묶기
```

### 템플릿 3 — 누적합 + 해시맵

```python
from collections import defaultdict

def count_subarrays_with_sum(nums, k):
    count = defaultdict(int)
    count[0] = 1          # 빈 접두사
    prefix = answer = 0
    for x in nums:
        prefix += x
        answer += count[prefix - k]
        count[prefix] += 1
    return answer
```

### 템플릿 4 — 버킷 정렬 (값의 범위가 작을 때 O(N))

```python
buckets = [[] for _ in range(len(nums) + 1)]   # 인덱스 = 빈도수
for v, f in Counter(nums).items():
    buckets[f].append(v)
```

## 시간 · 공간 복잡도

| 연산 | 시간 | 비고 |
|---|---|---|
| set/dict 삽입·조회·삭제 | 평균 O(1) | 최악 O(N) |
| Counter(list) | O(N) | |
| most_common(k) | O(N log k) | 인자가 없으면 전체 정렬 O(N log N) |
| 정렬된 키로 그룹핑 | O(N · K log K) | K = 문자열 길이 |
| 누적합 배열 만들기 | O(N) | 이후 구간 합 O(1) |

## 자주 하는 실수

- Two Sum 에서 자신을 먼저 저장한 뒤 짝을 찾아 **같은 원소를 두 번** 사용
- 누적합 + 해시에서 `count[0] = 1` 초기화를 빼먹어 처음부터 시작하는 구간을 놓침
- `list` 를 dict 키로 사용 → `TypeError: unhashable type` → `tuple(...)` 로 변환
- `Counter` 끼리 비교할 때 값이 0 인 키 처리 (3.10+ 은 0 을 무시하고 비교)
- 음수가 있는 "합이 k" 문제를 슬라이딩 윈도우로 풀기 (투 포인터는 모든 값이 양수일 때만)

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Contains Duplicate | Easy | set 에 이미 본 값 기록 | `python practice.py start contains-duplicate` |
| 2 | Valid Anagram | Easy | 문자 빈도수 비교 | `python practice.py start valid-anagram` |
| 3 | Two Sum | Easy | 해시맵에 보수 저장 | `python practice.py start two-sum` |
| 4 | Group Anagrams | Medium | 정렬된 문자열을 키로 그룹핑 | `python practice.py start group-anagrams` |
| 5 | Top K Frequent Elements | Medium | Counter + 버킷 정렬 | `python practice.py start top-k-frequent-elements` |
| 6 | Product of Array Except Self | Medium | prefix 곱 × suffix 곱 | `python practice.py start product-of-array-except-self` |
| 7 | Longest Consecutive Sequence | Medium | 시작점에서만 확장 | `python practice.py start longest-consecutive-sequence` |
| 8 | Subarray Sum Equals K | Medium | 누적합 + 해시맵 | `python practice.py start subarray-sum-equals-k` |

## 더 풀어 볼 문제

- LeetCode 36 Valid Sudoku, 271 Encode and Decode Strings, 49 Group Anagrams, 525 Contiguous Array
- 프로그래머스 Lv.1 완주하지 못한 선수, Lv.1 폰켓몬, Lv.2 전화번호 목록, Lv.2 의상, Lv.2 할인 행사, Lv.2 연속 부분 수열 합의 개수

## 영어로 설명하기 (미국 면접용)

- "A brute-force approach would compare every pair, which is O(n²). I can trade space for time by storing what I've seen in a hash map."
- "For each number, I check whether its complement, target minus the number, is already in the map."
- "I'll normalize each string by sorting its characters and use that as the key to group anagrams."
- "Since there can be negative numbers, a sliding window won't work, so I'll use prefix sums with a hash map of counts."
- "Hash map operations are O(1) on average, so the total time is O(n) with O(n) extra space."

## 체크리스트

- [ ] Two Sum 을 2분 안에 해시맵으로 쓸 수 있다
- [ ] `Counter`, `defaultdict(list)` 로 세기/묶기를 할 수 있다
- [ ] 누적합으로 구간 합을 O(1) 에 구할 수 있고, `count[0] = 1` 의 의미를 설명할 수 있다
- [ ] 해시 가능한 키와 불가능한 키를 구분할 수 있다
- [ ] 정렬 O(N log N) / 힙 O(N log K) / 버킷 O(N) 의 차이를 설명할 수 있다
