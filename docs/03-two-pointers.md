# 03. 투 포인터 (Two Pointers)

> 인덱스 두 개를 규칙에 따라 한 방향으로만 움직여, O(n^2) 의 "모든 쌍 확인" 을 O(n) 으로 줄이는 기법입니다.

## 이런 문제에서 떠올리세요

- **정렬된 배열**에서 "합이 target 인 두 수", "차이가 k 인 쌍" 을 찾는다 → 양 끝 투 포인터
- "팰린드롬인가?", "뒤집어라", "양쪽에서 비교" → 양 끝에서 안쪽으로
- "두 개를 골라 최대/최소" 인데 이중 for 문이 아니면 안 될 것 같다 → 한쪽을 버려도 되는 근거가 있는지 확인
- "정렬된 배열 두 개를 합쳐라 / 공통 원소" → 두 배열에 포인터를 하나씩
- "중복 제거를 in-place 로", "0 을 뒤로 보내라" → 같은 방향 투 포인터(slow / fast)
- "최대 2명씩 태운다", "짝을 지어 최소 개수" → 정렬 후 가벼운 것 + 무거운 것 그리디 (프로그래머스 '구명보트')
- 입력 크기 힌트: N ≤ 100,000 인데 "쌍" 을 다룬다 → O(N^2) 불가, **정렬 O(N log N) + 투 포인터 O(N)** 를 의심

## 핵심 개념

### 1) 양 끝에서 좁혀 오기 (opposite direction)

정렬된 배열에서 `l` 은 가장 작은 값, `r` 은 가장 큰 값을 가리킵니다.
합이 작으면 `l` 을, 크면 `r` 을 움직입니다. 한 번 지나간 원소는 **다시 볼 필요가 없다는 것이 증명되기 때문에** 버립니다.

```
numbers = [2, 3, 5, 8, 11, 15],  target = 13

 l                  r
[2, 3, 5, 8, 11, 15]   2 + 15 = 17 > 13  → r 이 너무 큼. 15 는 누구와 더해도 13 보다 큼 → r -= 1
 l              r
[2, 3, 5, 8, 11, 15]   2 + 11 = 13 == 13 → 정답 (0-based 인덱스 0, 4)

만약 합이 작다면?  numbers[l] 은 가장 큰 값과 더해도 부족 → l 은 버려도 안전 → l += 1
```

왜 O(n) 일까요? 매 반복마다 `l` 이 오른쪽으로 가거나 `r` 이 왼쪽으로 가서 둘 사이 간격이 1 씩 줄어듭니다.
간격은 처음에 n-1 이므로 반복은 최대 n-1 번입니다.

### 2) 같은 방향으로 이동하기 (slow / fast)

`fast` 는 모든 원소를 훑고, `slow` 는 "결과를 쓸 위치" 를 가리킵니다. 정렬된 배열의 중복 제거가 대표 예입니다.

```
nums = [1, 1, 2, 2, 2, 3]

slow=0 fast=1 : nums[1]=1 == nums[0]  → 건너뜀
slow=0 fast=2 : nums[2]=2 != nums[0]  → slow=1, nums[1]=2   → [1, 2, 2, 2, 2, 3]
slow=1 fast=3,4 : 2 == 2              → 건너뜀
slow=1 fast=5 : 3 != 2                → slow=2, nums[2]=3   → [1, 2, 3, ...]
결과 길이 = slow + 1 = 3
```

### 3) "왜 한쪽을 버려도 되는가" 가 핵심

투 포인터 풀이의 정당성은 언제나 이 질문에 답하는 것입니다.

| 문제 | 버리는 쪽 | 근거 |
|---|---|---|
| Two Sum II | 합 < target 이면 `l` | `numbers[l]` + (남은 최댓값) 도 부족하다 |
| Container With Most Water | 더 낮은 막대 | 폭은 줄고 높이는 낮은 쪽이 상한 → 더 좋아질 수 없다 |
| 구명보트 | 가장 무거운 사람 `r` | 어차피 보트 1 척 필요, 같이 탈 사람은 가장 가벼운 사람이 최선 |
| Trapping Rain Water | `leftMax < rightMax` 이면 `l` | 오른쪽에 더 높은 벽이 이미 있어 `l` 칸 수위가 확정된다 |

### 4) Trapping Rain Water 시각화

```
height = [0,1,0,2,1,0,1,3,2,1,2,1]

                █
        █ ~ ~ ~ █ █ ~ █
    █ ~ █ █ ~ █ █ █ █ █ █
  0 1 0 2 1 0 1 3 2 1 2 1   (~ = 고인 물, 총 6)

칸 i 의 물 = min(왼쪽 최대, 오른쪽 최대) - height[i]
i=5: 왼쪽 최대 2, 오른쪽 최대 3 → min = 2 → 2 - 0 = 2
```

투 포인터 버전에서는 `leftMax < rightMax` 일 때 왼쪽 칸을 확정합니다.
오른쪽 어딘가에 `rightMax` 높이 벽이 있으므로, 왼쪽 칸의 수위는 `leftMax` 를 넘지 않고 정확히 `leftMax` 가 됩니다.

### 5) 3Sum = 정렬 + 고정 + Two Sum II

```
정렬: [-4, -1, -1, 0, 1, 2]
 i=0 (-4): l..r 에서 합 4 찾기 → 없음
 i=1 (-1): l..r 에서 합 1 찾기 → (-1, 2), (0, 1)
 i=2 (-1): nums[2] == nums[1] → 건너뜀 (중복 조합 방지)
 i=3 ( 0): 0 > 0 아님, l..r 에서 합 0 → 없음
 (i 는 n-3 까지만 돈다. 정렬 후 nums[i] > 0 이 되면 그 즉시 break 해도 된다)
```

## 코드 템플릿

### 템플릿 1. 양 끝 투 포인터 (정렬된 배열의 쌍 찾기)

```python
def two_sum_sorted(nums, target):
    l, r = 0, len(nums) - 1
    while l < r:                 # 같은 원소를 두 번 쓰지 않도록 l < r
        s = nums[l] + nums[r]
        if s == target:
            return [l, r]
        if s < target:
            l += 1               # 합을 키운다
        else:
            r -= 1               # 합을 줄인다
    return []
```

### 템플릿 2. 정렬 + 하나 고정 + 투 포인터 (k-Sum, 중복 건너뛰기)

```python
def three_sum(nums):
    nums.sort()
    res = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue                         # 같은 첫 수 건너뛰기
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1                   # 같은 두 번째 수 건너뛰기
    return res
```

### 템플릿 3. 같은 방향 (slow / fast) — in-place 압축

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    slow = 0                       # 마지막으로 '확정된' 위치
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1                # 남은 길이
```

### 템플릿 4. 정렬된 배열 두 개 병합 (포인터 두 개, 배열 두 개)

```python
def merge(a, b):
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:])              # 남은 쪽을 그대로 붙인다
    out.extend(b[j:])
    return out
```

## 시간 · 공간 복잡도

| 문제 유형 | 브루트포스 | 투 포인터 | 공간 |
|---|---|---|---|
| 정렬된 배열의 두 수 합 | O(n^2) | O(n) | O(1) |
| 정렬 안 된 배열의 두 수 합 | O(n^2) | O(n log n) (정렬 포함, 인덱스 잃음) | O(1)~O(n) |
| 3Sum | O(n^3) | O(n^2) | O(1) (출력 제외) |
| 팰린드롬 검사 | O(n) (뒤집은 사본) | O(n) | O(1) |
| Container With Most Water | O(n^2) | O(n) | O(1) |
| 구명보트 | O(n^2) (매번 짝 탐색) | O(n log n) (정렬) | O(1) |
| Trapping Rain Water | O(n^2) | O(n) | O(1) (prefix 배열이면 O(n)) |

## 자주 하는 실수

- [ ] **정렬을 안 하고** 양 끝 투 포인터를 쓴다. 양 끝 비교 논리는 정렬이 전제입니다.
- [ ] 원래 인덱스가 필요한 문제(Two Sum 1번)에서 정렬해 버려 인덱스를 잃는다. → 해시맵을 쓰거나 `(값, 인덱스)` 로 정렬.
- [ ] `while l <= r` 와 `while l < r` 를 헷갈린다. 같은 원소를 두 번 쓰면 안 되면 `l < r`, 한 원소가 혼자 처리될 수 있으면(구명보트) `l <= r`.
- [ ] 안쪽 `while` 로 건너뛸 때 `l < r` 조건을 빼먹어 인덱스가 범위를 벗어난다.
- [ ] 3Sum 에서 중복 처리 위치를 틀린다. 첫 수는 `i > 0 and nums[i] == nums[i-1]`, 두 번째 수는 **정답을 찾은 뒤** 건너뛴다.
- [ ] 3Sum 결과를 `set` 에 리스트로 넣으려다 오류(`list` 는 해시 불가). → `tuple` 로 넣어야 합니다.
- [ ] Container 문제에서 높은 쪽을 옮긴다. 항상 **낮은 쪽**을 옮겨야 합니다. 높이가 같으면 어느 쪽이든 괜찮습니다.
- [ ] Trapping Rain Water 에서 `leftMax`, `rightMax` 를 갱신하기 **전에** 물을 더해 음수가 생긴다. 갱신 → 더하기 순서를 지키세요.
- [ ] 팰린드롬에서 `isalnum()` 처리를 빼먹거나 대소문자를 통일하지 않는다.

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Valid Palindrome | Easy | 양 끝 포인터, 영문자·숫자 아닌 문자 건너뛰기 | `python practice.py start valid-palindrome` |
| 2 | Two Sum II - Sorted Array | Medium | 합이 작으면 l++, 크면 r-- | `python practice.py start two-sum-sorted` |
| 3 | 3Sum | Medium | 정렬 + 하나 고정 + Two Sum II, 인접 중복 건너뛰기 | `python practice.py start three-sum` |
| 4 | Container With Most Water | Medium | 낮은 쪽 막대를 버리며 좁히기 | `python practice.py start container-with-most-water` |
| 5 | Boats to Save People (구명보트) | Medium | 정렬 후 가장 무거운 + 가장 가벼운 짝짓기 | `python practice.py start boats-to-save-people` |
| 6 | Trapping Rain Water | Hard | min(왼쪽 최대, 오른쪽 최대) - 높이, 투 포인터로 O(1) 공간 | `python practice.py start trapping-rain-water` |

## 더 풀어 볼 문제

- LeetCode 26. Remove Duplicates from Sorted Array (slow / fast)
- LeetCode 283. Move Zeroes (slow / fast)
- LeetCode 344. Reverse String (양 끝 교환)
- LeetCode 680. Valid Palindrome II (한 글자 삭제 허용 → 어긋난 지점에서 두 갈래 확인)
- LeetCode 88. Merge Sorted Array (뒤에서부터 채우는 투 포인터)
- LeetCode 18. 4Sum (3Sum 에 고정 하나 추가)
- LeetCode 16. 3Sum Closest
- LeetCode 977. Squares of a Sorted Array (양 끝에서 큰 값부터)
- 프로그래머스 Lv.2 구명보트 (이 저장소의 boats-to-save-people 과 같은 유형)
- 프로그래머스 Lv.3 숫자 게임 (정렬 + 투 포인터 그리디)
- 프로그래머스 Lv.2 두 큐 합 같게 만들기 (2022 KAKAO TECH INTERNSHIP, 투 포인터로 이동 횟수 세기)
- 프로그래머스 Lv.2 연속된 부분 수열의 합 (투 포인터 / 슬라이딩 윈도우 경계 문제)

## 영어로 설명하기 (미국 면접용)

- "Since the array is sorted, I'll use two pointers starting at both ends. If the sum is too small I move the left pointer right, and if it's too large I move the right pointer left."
- "Each step discards one element that can't be part of any answer, so the pointers cross after at most n steps, which gives O(n) time and O(1) extra space."
- "For 3Sum, I sort the array, fix the first number, and run the two-pointer Two Sum on the rest. I skip equal neighbors to avoid duplicate triplets, so it's O(n^2) overall."
- "In Container With Most Water, the shorter line limits the area, so moving the taller line can never help. That's why it's safe to always move the pointer at the shorter line."
- "For Trapping Rain Water, the water above each bar is the minimum of the max height to its left and to its right, minus its own height. With two pointers I can settle the side with the smaller max in constant space."

## 체크리스트

- [ ] 투 포인터를 쓰기 전에 배열이 정렬되어 있는지(또는 정렬해도 되는지) 확인했다.
- [ ] "왜 이 포인터를 움직여도 답을 놓치지 않는가" 를 한 문장으로 말할 수 있다.
- [ ] 반복 조건 `l < r` 와 `l <= r` 중 무엇이 맞는지 이유를 설명할 수 있다.
- [ ] 3Sum 의 두 가지 중복 건너뛰기를 보지 않고 쓸 수 있다.
- [ ] Trapping Rain Water 를 prefix 배열 풀이와 투 포인터 풀이 두 가지로 설명할 수 있다.
- [ ] 프로그래머스 '구명보트' 를 보고 바로 정렬 + 투 포인터 그리디를 떠올릴 수 있다.
- [ ] 브루트포스 → 정렬 → 투 포인터 순서로 개선 과정을 영어로 말할 수 있다.
