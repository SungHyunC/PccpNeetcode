# 19. 구현 · 시뮬레이션 (PCCP 특화)

> PCCP 는 "알고리즘을 아느냐" 만큼 "긴 지문을 정확히 코드로 옮기느냐" 를 봅니다. **조건 정리 → 예제 손으로 따라가기 → 자료구조 결정 → 함수로 쪼개 구현 → 경계값 테스트** 순서를 몸에 익히세요.

## 이런 문제에서 떠올리세요

- 지문이 길고 규칙이 여러 개("~이면 ~하고, 단 ~인 경우는 ~") → 구현/시뮬레이션. 특별한 알고리즘보다 **정확성**이 핵심
- 격자(board, 지도, 공원)에서 로봇·캐릭터가 명령대로 움직임 → 방향 벡터 `dr/dc` + 경계 검사
- "HH:MM", "YYYY.MM.DD", "차량번호 IN/OUT" 같은 문자열 기록 → 파싱 후 **정수 하나로 변환** (분, 일)
- "~ 순으로 정렬하되, 같으면 ~, 그것도 같으면 입력 순서" → 튜플 정렬 키 + 안정 정렬
- "구간 합을 여러 번 묻는다" → 누적합(prefix sum)
- "직사각형/구간에 값을 더하는 작업이 아주 많고 결과는 마지막에 한 번" → 차분 배열(difference array)
- "각 ~ 가 몇 번 나왔는지", "~ 별로 합계" → `Counter`, `defaultdict`
- 입력 크기 감각 (파이썬은 1초에 대략 1,000만 ~ 2,000만 번 단순 연산):

| 입력 크기 | 허용 복잡도 | 전형적 접근 |
|---|---|---|
| N ≤ 10 | O(N!) | 순열 완전 탐색 |
| N ≤ 20 | O(2^N) | 부분집합 / 비트마스크 |
| N ≤ 500 | O(N³) | 3중 반복 |
| N ≤ 5,000 | O(N²) | 2중 반복, 문자열 압축류 완전 탐색 |
| N ≤ 1,000,000 | O(N log N) / O(N) | 정렬, 누적합, 해시, 투 포인터 |
| 질의/갱신 K 가 수십만 + 격자 | O(K + N·M) | 차분 배열 / 누적합 |

## 핵심 개념

### 1) 긴 지문 읽는 법: 조건 정리 → 예제 따라가기

PCCP 2~3번 문제는 지문만 한 화면이 넘습니다. 읽으면서 바로 코딩하지 말고, **주석으로 조건부터 정리**합니다.

```python
def solution(fees, records):
    # [입력]  fees = [기본시간, 기본요금, 단위시간, 단위요금], records = "HH:MM 번호 IN/OUT"
    # [규칙]  1) 하루 누적 시간으로 계산  2) OUT 없으면 23:59  3) 초과분은 올림
    # [출력]  차량번호 오름차순 요금 리스트
    # [함정]  같은 차 여러 번 입출차 / 23:59 IN → 0분 / 나누어떨어질 때 올림
    # [크기]  records ≤ 1,000 → 아무렇게나 해도 시간 OK, 정확성만 신경
    ...
```

1. **입력 형식**: 1-index 인가 0-index 인가? (행, 열) 인가 (x, y) 인가? 문자열인가 숫자인가?
2. **규칙을 번호 매겨 나열**: 지문의 "단," "다만," "~인 경우" 에 밑줄. 함정은 대부분 여기 있습니다.
3. **출력 형식**: 정렬 순서, 없을 때 반환값(`[-1]`, `[]`, `0`), 1-index 번호인지
4. **입출력 예를 손으로 따라가기**: 예제 하나를 종이(또는 주석)에 직접 계산해 본 뒤 코드와 비교합니다. 예제 해설과 내 계산이 다르면 규칙을 잘못 읽은 것입니다.
5. **제한사항으로 복잡도 결정**: 위 표 참고. 작으면 "그냥 시키는 대로" 구현하는 것이 가장 빠르고 안전합니다.

### 2) 격자 시뮬레이션: 방향 벡터, 회전, 경계

```
방향 번호를 '시계 방향' 순서로 정해 두면 회전이 % 4 한 줄입니다.

            0 = 북(위)  (-1,  0)
                 ↑
  3 = 서 (0,-1) ←  ●  → 1 = 동 (0, +1)
                 ↓
            2 = 남(아래) (+1,  0)

  dr = [-1, 0, 1, 0]
  dc = [ 0, 1, 0,-1]
  오른쪽(시계) 90° : d = (d + 1) % 4
  왼쪽(반시계) 90° : d = (d + 3) % 4   (파이썬은 (d - 1) % 4 도 OK)
  뒤로 돌기        : d = (d + 2) % 4
```

- (행, 열) 좌표에서 "위" 는 행 번호가 **줄어드는** 방향입니다. 수학 좌표 (x, y) 와 헷갈리지 마세요.
- 경계 검사는 이동 **전에** `0 <= nr < R and 0 <= nc < C` 로. 벽/장애물 검사도 같은 자리에서.
- "범위를 벗어나면 무시 / 벽 앞에서 멈춤 / 반대편으로 순환(`nr % R`)" 중 무엇인지 지문에서 확인합니다.
- 8방향이 필요하면 `dr = [-1,-1,-1,0,0,1,1,1]`, `dc = [-1,0,1,-1,1,-1,0,1]`.
- 격자 바깥을 신경 쓰기 싫으면 **패딩**: 한 칸씩 테두리를 덧댄 `(R+2) × (C+2)` 격자를 만들고 벽으로 채웁니다.

### 3) 문자열 파싱 도구

| 하고 싶은 것 | 코드 |
|---|---|
| 공백으로 나누기 | `t, car, kind = "05:34 5961 IN".split()` |
| 구분자로 나눠 정수로 | `h, m = map(int, "05:34".split(":"))` |
| 시각 → 분 | `h * 60 + m` (23:59 = 1439) |
| 분 → "HH:MM" | `f"{t // 60:02d}:{t % 60:02d}"` |
| 날짜 → 일수 (한 달 28일 같은 단순 달력) | `y * 12 * 28 + (m - 1) * 28 + (d - 1)` |
| 0 채우기 | `str(7).zfill(3) == "007"`, `f"{7:03d}"` |
| 숫자/문자 판별 | `ch.isdigit()`, `ch.isalpha()`, `ch.isalnum()` |
| 대소문자 | `s.lower()`, `s.upper()`, `ch.islower()` |
| 문자 ↔ 코드 | `ord("a") == 97`, `chr(97) == "a"`, 알파벳 순번 `ord(ch) - ord("a")` |
| 마지막 글자 떼기 | `"15D"[:-1] == "15"`, `"15D"[-1] == "D"` |
| 여러 구분자 | `s.replace("-", " ").split()` 또는 `re.split(r"[-.]", s)` |
| 연속 같은 문자 묶기 | `itertools.groupby("aaabcc")` → `a×3, b×1, c×2` |

> 시각·날짜는 **정수로 바꿔서 계산하고, 출력할 때만 문자열로** 되돌립니다. 자릿수가 고정된 `"HH:MM"`, `"YYYY.MM.DD"` 는 문자열 비교만으로도 순서가 맞습니다.

### 4) 커스텀 정렬

```python
# 튜플 키: 앞 원소부터 차례로 비교
people.sort(key=lambda p: (p.age, p.name))          # 나이 오름차순, 같으면 이름 오름차순
people.sort(key=lambda p: (-p.score, p.name))       # 점수 내림차순(숫자는 - 붙이기), 이름 오름차순

# 문자열을 내림차순으로 섞어야 할 때: 두 번 정렬 (안정 정렬 이용, 덜 중요한 키부터)
people.sort(key=lambda p: p.name, reverse=True)
people.sort(key=lambda p: p.age)

# 비교 함수가 꼭 필요할 때: 가장 큰 수 만들기 ("3" + "30" vs "30" + "3")
from functools import cmp_to_key
nums.sort(key=cmp_to_key(lambda a, b: -1 if a + b > b + a else (1 if a + b < b + a else 0)))
```

- 파이썬 `sort` / `sorted` 는 **안정 정렬(stable)**: 키가 같으면 원래 순서 유지. "같으면 입력 순서대로" 규칙은 공짜입니다.
- `list.sort()` 는 제자리 정렬 후 `None` 반환, `sorted()` 는 새 리스트 반환. `a = a.sort()` 는 버그.
- 딕셔너리를 값 기준 정렬: `sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))`

### 5) 누적합과 차분 배열 (1D / 2D)

```
누적합 (prefix sum): 조회가 많을 때            차분 배열 (difference array): 갱신이 많을 때
  a      =    3 -1  4  1  5                     [1,3] 에 +2 를 표시:
  prefix = 0  3  2  6  7 12                       diff = 0 +2  0  0 -2  0
  sum(a[1..3]) = prefix[4] - prefix[1] = 4        누적합 → 0  2  2  2  0     ← 실제 변화량

2차원 누적합 P (P[r+1][c+1] = 왼쪽 위 직사각형 합)
  합(r1,c1 ~ r2,c2) = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]

     ┌─────────┬───┐
     │    A    │ B │        구하는 영역 D = 전체 - (A+B) - (A+C) + A
     ├─────────┼───┤
     │    C    │ D │
     └─────────┴───┘

2차원 차분 배열: (r1,c1)~(r2,c2) 에 +v
         c1      c2+1
   r1    +v      -v          → 행 방향 누적합 → 열 방향 누적합 = 각 칸 변화량
   r2+1  -v      +v
```

| 상황 | 도구 | 갱신 | 조회 |
|---|---|---|---|
| 배열 고정, 구간 합 질의 多 | 누적합 | - | O(1) |
| 구간 갱신 多, 조회는 마지막 1번 | 차분 배열 | O(1) | 마지막 O(N) |
| 갱신과 조회가 섞임 | 펜윅 트리 / 세그먼트 트리 | O(log N) | O(log N) |

### 6) 세기: Counter / defaultdict

```python
from collections import Counter, defaultdict
cnt = Counter(["a", "b", "a"])        # Counter({'a': 2, 'b': 1})
cnt.most_common(1)                    # [('a', 2)]
Counter("aab") == Counter("aba")      # 애너그램 판정
total = defaultdict(int)              # 없는 키는 0 으로 시작 → total[car] += minutes
groups = defaultdict(list)            # 없는 키는 [] 로 시작 → groups[key].append(x)
```

### 7) PCCP 시간 절약 팁

- **쉬운 문제부터**: 4문제를 모두 읽고(5분) 자신 있는 순서로. 한 문제에 40분 이상 막히면 다음으로 넘어갑니다.
- **부분 점수**: 테스트 케이스 단위로 채점되므로, 효율성이 안 나와도 정확한 완전 탐색을 먼저 제출해 점수를 확보합니다.
- **함수로 쪼개기**: `to_minutes`, `parse`, `in_range`, `rotate` 처럼 작은 함수로 나누면 디버깅이 쉽습니다.
- **예제부터 통과**: 지문 예제를 그대로 넣어 보고 `print` 로 중간 상태(격자, dict)를 찍어 봅니다. 제출 전 `print` 는 지워도 되고 남겨도 채점에는 보통 영향이 없지만 출력이 많으면 느려집니다.
- **직접 만든 경계값**: 원소 1개, 전부 같은 값, 최댓값, 빈 결과, 0/음수.
- **재귀 깊이**: DFS 가 깊어지면 `import sys; sys.setrecursionlimit(10**6)` 또는 스택으로.
- **빠른 표준 도구**: `sorted`, `sum`, `min/max(key=)`, `zip(*m)`, `itertools.permutations/combinations/product`, `bisect`, `heapq`, `collections.deque`.
- **입력은 함수 인자**로 들어옵니다 (`input()` 불필요). 반환 타입(리스트/정수/문자열)을 지문과 정확히 맞춥니다.

## 코드 템플릿

```python
# 1) 격자 시뮬레이션 기본형
DR = [-1, 0, 1, 0]                  # 북 동 남 서 (시계 방향)
DC = [0, 1, 0, -1]
MOVE = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}  # 절대 방향 명령용

def simulate(rows, cols, commands, start=(0, 0), d=1):
    r, c = start
    for cmd in commands:
        if cmd == "R":
            d = (d + 1) % 4
        elif cmd == "L":
            d = (d - 1) % 4
        else:
            nr, nc = r + DR[d], c + DC[d]
            if 0 <= nr < rows and 0 <= nc < cols:   # 이동 '전에' 경계 검사
                r, c = nr, nc
    return r, c
```

```python
# 2) 기록 파싱 + 시간 계산 + 집계
from collections import defaultdict

def to_minutes(hhmm):
    h, m = map(int, hhmm.split(":"))
    return h * 60 + m

def ceil_div(a, b):
    return -(-a // b)                 # 정수만으로 올림 (math.ceil(a / b) 도 가능)

def parse_records(records):
    inside, total = {}, defaultdict(int)
    for rec in records:
        t, key, kind = rec.split()
        if kind == "IN":
            inside[key] = to_minutes(t)
        else:
            total[key] += to_minutes(t) - inside.pop(key)
    for key, t in inside.items():     # 끝까지 나가지 않은 것 처리
        total[key] += to_minutes("23:59") - t
    return dict(sorted(total.items()))
```

```python
# 3) 1D / 2D 누적합
from itertools import accumulate

prefix = list(accumulate(nums, initial=0))          # 구간 [l, r] 합 = prefix[r+1] - prefix[l]

def prefix_2d(a):
    n, m = len(a), len(a[0])
    P = [[0] * (m + 1) for _ in range(n + 1)]
    for r in range(n):
        for c in range(m):
            P[r + 1][c + 1] = P[r][c + 1] + P[r + 1][c] - P[r][c] + a[r][c]
    return P

def rect_sum(P, r1, c1, r2, c2):                     # 양 끝 포함
    return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]
```

```python
# 4) 2D 차분 배열: 직사각형 갱신 K 번 → 마지막에 복원
def apply_rect_updates(n, m, updates):              # updates: (r1, c1, r2, c2, v)
    diff = [[0] * (m + 1) for _ in range(n + 1)]
    for r1, c1, r2, c2, v in updates:
        diff[r1][c1] += v
        diff[r1][c2 + 1] -= v
        diff[r2 + 1][c1] -= v
        diff[r2 + 1][c2 + 1] += v
    for row in diff:                                 # 행 방향 누적
        for c in range(1, m + 1):
            row[c] += row[c - 1]
    for r in range(1, n + 1):                        # 열 방향 누적
        for c in range(m + 1):
            diff[r][c] += diff[r - 1][c]
    return [row[:m] for row in diff[:n]]             # 각 칸의 총 변화량
```

## 시간 · 공간 복잡도

| 기법 | 시간 | 공간 | 비고 |
|---|---|---|---|
| 명령 시뮬레이션 | O(명령 수) | O(1) | 격자 저장 시 O(R·C) |
| 기록 파싱 + dict 집계 | O(N + K log K) | O(K) | K = 키(차량 등) 개수, 정렬 포함 |
| 튜플 키 정렬 | O(N log N · 키 생성 비용) | O(N) | |
| 테두리 회전 (질의 Q 개) | O(Q · (R + C)) | O(R·C) | |
| 1D 누적합 | 전처리 O(N), 질의 O(1) | O(N) | |
| 2D 누적합 | 전처리 O(N·M), 질의 O(1) | O(N·M) | |
| 2D 차분 배열 | O(K + N·M) | O(N·M) | 직접 갱신은 O(K·N·M) |
| 문자열 압축 완전 탐색 | O(N²) | O(N) | N ≤ 1,000 |

## 자주 하는 실수

**디버깅 체크리스트** — 예제는 맞는데 제출하면 틀릴 때 위에서부터 확인하세요.

- [ ] **off-by-one**: `range(a, b)` 는 b 를 포함하지 않음. "양 끝 포함" 구간은 `range(l, r + 1)`. "~까지 가능" vs "~부터 불가" 의 하루 차이
- [ ] **0/1 인덱스**: 지문이 1부터 세면 입력 직후 한 번만 `-1` 하고, 출력할 때만 `+1`. 중간에 섞지 않기
- [ ] **(행, 열) vs (x, y)**: 위쪽 이동이 `r - 1` 인지 확인. `board[x][y]` 와 `board[y][x]` 를 섞지 않기
- [ ] **리스트 복사 vs 참조**: `[[0] * m] * n` 은 n 개의 행이 **같은 리스트** → 한 칸 바꾸면 한 열 전체가 바뀜. 반드시 `[[0] * m for _ in range(n)]`
- [ ] **얕은 복사**: `b = board` 는 같은 객체. 2차원 복사는 `[row[:] for row in board]` 또는 `copy.deepcopy`
- [ ] **반복 중 수정**: 리스트를 순회하며 `remove`, 딕셔너리를 순회하며 `del` → 복사본을 순회하거나 새로 만들기
- [ ] **동시 갱신**: 시뮬레이션 한 턴의 결과를 같은 격자에 바로 쓰면 아직 처리 안 한 칸이 영향을 받음 → 새 격자에 쓰거나 덮어쓰기 순서 조정(테두리 회전)
- [ ] **올림 나눗셈**: `a // b + 1` 은 나누어떨어질 때 틀림 → `-(-a // b)`
- [ ] **두 자리 숫자**: 반복 횟수 10 이상, 시각 "09" 의 앞자리 0. `len(str(cnt))`, `zfill`
- [ ] **대소문자/공백**: 비교 전에 `lower()`, 파싱 전에 `strip()`
- [ ] **빈 결과 형식**: 답이 없을 때 `[]` 인지 `[-1]` 인지 `0` 인지
- [ ] **정렬 반환값**: `a = a.sort()` → `None`
- [ ] **마지막 묶음 처리**: 연속 구간을 세는 루프는 반복문이 끝난 뒤 마지막 그룹을 반영했는지
- [ ] **누적합 크기**: prefix/diff 배열을 n+1 로 잡았는지, 2D 는 두 방향 모두 누적했는지

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Robot Commands | Easy | `dr/dc` + `(d ± 1) % 4` + 경계 검사 | `python practice.py start robot-commands` |
| 2 | Date and Time Parsing | Easy | 날짜 → 총 일수 정수로 변환 후 비교 | `python practice.py start date-and-time-parsing` |
| 3 | Prefix Sum Range Queries | Easy | `prefix[r+1] - prefix[l]` | `python practice.py start prefix-sum-range-queries` |
| 4 | String Compression | Medium | 모든 단위 길이 완전 탐색 + 연속 묶기 | `python practice.py start string-compression` |
| 5 | Parking Fee | Medium | 분 단위 변환 + dict 누적 + 올림 | `python practice.py start parking-fee` |
| 6 | Rotate Matrix Border | Medium | 값 하나 들고 반대 순서로 당기기 | `python practice.py start rotate-matrix-border` |
| 7 | File Name Sort | Medium | (HEAD.lower(), int(NUMBER)) 키 + 안정 정렬 | `python practice.py start file-name-sort` |
| 8 | Board Damage (2D Difference Array) | Hard | 꼭짓점 4곳 표시 + 누적합 두 번 | `python practice.py start board-damage-difference-array` |

## 더 풀어 볼 문제

- 프로그래머스 PCCP 기출문제 (프로그래머스 > 코딩테스트 연습 > PCCP 기출문제) — 실제 출제 스타일 확인용으로 꼭 풀어 보세요
- 프로그래머스 Lv.1 공원 산책, Lv.1 바탕화면 정리, Lv.1 키패드 누르기, Lv.1 신고 결과 받기
- 프로그래머스 Lv.1 개인정보 수집 유효기간, Lv.2 주차 요금 계산, Lv.2 [1차] 파일명 정렬
- 프로그래머스 Lv.2 문자열 압축, Lv.2 행렬 테두리 회전하기, Lv.2 삼각 달팽이, Lv.2 [1차] 뉴스 클러스터링
- 프로그래머스 Lv.2 방문 길이 (방향 + 간선 집합), Lv.2 거리두기 확인하기, Lv.2 광물 캐기
- 프로그래머스 Lv.3 파괴되지 않은 건물 (2D 차분 배열), Lv.3 광고 삽입 (시간 파싱 + 누적합)
- 프로그래머스 Lv.3 표 편집, Lv.3 자물쇠와 열쇠 (회전 + 패딩)
- LeetCode 289 Game of Life (동시 갱신), LeetCode 1094 Car Pooling (차분 배열)
- LeetCode 303 / 304 Range Sum Query - Immutable / 2D (누적합)
- LeetCode 874 Walking Robot Simulation, LeetCode 1041 Robot Bounded In Circle (방향 회전)
- LeetCode 937 Reorder Data in Log Files (커스텀 정렬), LeetCode 443 String Compression

## 영어로 설명하기 (미국 면접용)

- "Before writing code, let me restate the rules and walk through the example by hand to make sure I understand the edge cases."
- "I'll encode the four directions as `dr` and `dc` arrays in clockwise order, so turning right is just `(d + 1) % 4`, and I'll check the bounds before every move."
- "I'll convert every `HH:MM` timestamp into minutes since midnight, which turns time arithmetic into plain integer subtraction."
- "Python's sort is stable, so if I sort by the tuple `(head.lower(), int(number))`, ties automatically keep their original order."
- "Applying each rectangle update cell by cell would be O(K·N·M). With a 2D difference array, each update is O(1), and two prefix-sum passes at the end recover the final values in O(N·M)."

## 체크리스트

- [ ] 지문을 읽고 입력/규칙/출력/함정/크기 다섯 가지를 주석으로 정리한 뒤 코딩한다
- [ ] 예제 하나를 손으로 따라가 지문의 해설과 같은 결과를 얻는다
- [ ] `dr/dc` 시계 방향 배열과 `(d + 1) % 4`, `(d + 3) % 4` 회전을 바로 쓸 수 있다
- [ ] "HH:MM" → 분, "YYYY.MM.DD" → 일수 변환과 되돌리기(`f"{x:02d}"`)를 할 수 있다
- [ ] 튜플 키 정렬, 내림차순(`-`), 안정 정렬, `cmp_to_key` 를 상황에 맞게 고른다
- [ ] 1D/2D 누적합과 1D/2D 차분 배열을 템플릿 없이 작성할 수 있다
- [ ] `[[0] * m] * n` 버그와 얕은 복사 문제를 설명할 수 있다
- [ ] 제출 전 디버깅 체크리스트(off-by-one, 0/1 인덱스, 빈 결과 형식)를 확인한다
