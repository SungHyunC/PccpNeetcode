# 05. 스택 (Stack)

> 가장 나중에 넣은 것을 가장 먼저 꺼내는(LIFO) 자료구조입니다. "가장 최근의 짝", "아직 처리되지 않은 것들" 을 기억할 때 쓰고, 단조 스택(monotonic stack)으로 "다음 큰/작은 원소" 를 O(n) 에 찾습니다.

## 이런 문제에서 떠올리세요

- **괄호 짝 맞추기**, 태그 열고 닫기, "올바른 문자열인가" → 스택
- "인접한 같은 문자 제거", "짝지어 제거하기", "뒤로 가기(undo)" → 스택
- **후위 표기식 계산**, 계산기, 중첩 구조(`3[a2[c]]`) 해석 → 스택
- "다음으로 큰(또는 작은) 원소", "며칠 뒤에 더 따뜻해지나", "가격이 떨어지지 않은 기간" → **단조 스택**
- "히스토그램에서 가장 큰 직사각형", "양쪽으로 처음 낮아지는 곳" → 단조 증가 스택
- "앞차를 추월할 수 없다", "앞의 것이 뒤의 것을 막는다" → 정렬 후 스택으로 그룹 세기
- 재귀 DFS 를 반복문으로 바꿀 때 → 명시적 스택
- 입력 크기 힌트: N ≤ 100,000 에서 "각 원소마다 오른쪽에서 처음 ~ 인 원소" → O(N^2) 대신 단조 스택 O(N)

## 핵심 개념

### 1) 파이썬에서 스택 쓰기

파이썬 `list` 가 그대로 스택입니다. 끝에서 넣고 빼는 연산은 모두 O(1) 입니다.

| 연산 | 코드 | 시간 |
|---|---|---|
| push | `stack.append(x)` | O(1) |
| pop | `stack.pop()` | O(1) |
| top 보기 | `stack[-1]` | O(1) |
| 비었는지 | `not stack` | O(1) |

`stack.pop(0)` 이나 `stack.insert(0, x)` 는 O(n) 이니 쓰지 마세요. 앞에서 빼야 한다면 `collections.deque` 를 씁니다.

### 2) 괄호 짝 맞추기

```
s = "{[()]}"

문자  동작           스택
{     push          {
[     push          { [
(     push          { [ (
)     top '(' 와 짝  { [         ← pop
]     top '[' 와 짝  {           ← pop
}     top '{' 와 짝  (비었음)     ← pop
끝    스택이 비었음 → True

s = "([)]" 에서는 ')' 를 만났을 때 top 이 '[' 라서 짝이 안 맞음 → False
```

### 3) 후위 표기식 계산

```
tokens = ["2", "1", "+", "3", "*"]      (= (2 + 1) * 3)

토큰  스택
2     [2]
1     [2, 1]
+     b=1, a=2 → [3]
3     [3, 3]
*     b=3, a=3 → [9]       답 9
```

먼저 꺼낸 값이 **오른쪽** 피연산자입니다. `a - b`, `a / b` 순서에 주의하세요.

### 4) 단조 스택 (monotonic stack) — "다음 큰 원소"

스택에 "아직 답을 못 찾은 원소의 인덱스" 를 쌓습니다. 새 원소가 top 보다 크면, top 의 답이 바로 그 새 원소입니다.
그래서 스택 안의 값은 항상 위로 갈수록 작아지는(단조 감소) 상태가 유지됩니다.

```
temperatures = [73, 74, 75, 71, 69, 72, 76, 73]

i  온도  동작                                   스택(온도)        answer
0  73   push                                    [73]
1  74   74 > 73 → pop 0, ans[0]=1               [74]              [1,0,0,0,0,0,0,0]
2  75   75 > 74 → pop 1, ans[1]=1               [75]              [1,1,0,...]
3  71   push                                    [75, 71]
4  69   push                                    [75, 71, 69]
5  72   72 > 69 → ans[4]=1, 72 > 71 → ans[3]=2  [75, 72]
6  76   76 > 72 → ans[5]=1, 76 > 75 → ans[2]=4  [76]
7  73   push                                    [76, 73]
끝: 남은 6, 7 은 0                                                [1,1,4,2,1,1,0,0]
```

while 문이 안에 있어도 각 인덱스는 **한 번 push, 한 번 pop** 되므로 전체 O(n) 입니다 (분할 상환, amortized).

| 찾고 싶은 것 | 스택 상태 | pop 조건 |
|---|---|---|
| 오른쪽 첫 번째 **더 큰** 원소 | 단조 감소 | `nums[top] < x` |
| 오른쪽 첫 번째 **더 작은** 원소 | 단조 증가 | `nums[top] > x` |
| 왼쪽 첫 번째 더 큰/작은 원소 | 위와 같음 | push 직전 스택 top 이 답 |

### 5) 히스토그램에서 가장 큰 직사각형

직사각형의 높이는 반드시 어떤 막대 하나의 높이입니다. 막대 i 를 높이로 쓰면 좌우로 "처음 더 낮은 막대" 직전까지 넓힐 수 있습니다.
단조 증가 스택에서 막대가 pop 되는 순간, 그 막대의 **오른쪽 경계(현재 i)** 와 **왼쪽 경계(pop 후 새 top)** 가 동시에 확정됩니다.

```
heights = [2, 1, 5, 6, 2, 3]

                 █
             █   █
             █   █
             █   █       █
     █       █   █   █   █
     █   █   █   █   █   █
     2   1   5   6   2   3
    i=0 i=1 i=2 i=3 i=4 i=5        (최대 직사각형: i=2..3, 높이 5 × 폭 2 = 10)

i=4 (높이 2) 가 들어올 때: 스택(높이) = [1, 5, 6]
  pop 6: 왼쪽 경계 = 5 의 위치(2), 오른쪽 경계 = 4 → 폭 4-2-1 = 1 → 넓이 6
  pop 5: 왼쪽 경계 = 1 의 위치(1), 오른쪽 경계 = 4 → 폭 4-1-1 = 2 → 넓이 10  ← 최대
```

### 6) 스택으로 "무리(그룹)" 세기 — Car Fleet

목적지에 가까운 차부터 보면서 "혼자 달렸을 때 도착 시간" 을 스택에 쌓습니다.
뒤차의 시간이 top 이하이면 앞차를 따라잡아 합류(push 안 함), 더 크면 새 무리(push)입니다. 답은 스택 길이입니다.

## 코드 템플릿

### 템플릿 1. 짝 맞추기 스택

```python
def is_valid(s):
    pair = {")": "(", "]": "[", "}": "{"}
    stack = []
    for c in s:
        if c in pair:                         # 닫는 괄호
            if not stack or stack[-1] != pair[c]:
                return False
            stack.pop()
        else:                                 # 여는 괄호
            stack.append(c)
    return not stack                          # 남은 여는 괄호가 없어야 함
```

### 템플릿 2. 단조 스택 — 오른쪽의 첫 번째 더 큰 원소까지 거리

```python
def next_greater_distance(nums):
    ans = [0] * len(nums)
    stack = []                                # 인덱스, nums 값은 단조 감소
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:  # x 가 top 의 '다음 큰 원소'
            j = stack.pop()
            ans[j] = i - j                    # 값이 필요하면 ans[j] = x
        stack.append(i)
    return ans                                # 스택에 남은 것은 답 없음(0)
```

### 템플릿 3. 단조 증가 스택 + 끝에 센티널(sentinel) — 히스토그램

```python
def largest_rectangle(heights):
    stack, best = [], 0
    for i, h in enumerate(heights + [0]):     # 끝에 높이 0 을 붙여 스택을 비움
        while stack and heights[stack[-1]] >= h:
            top = stack.pop()
            left = stack[-1] if stack else -1
            best = max(best, heights[top] * (i - left - 1))
        stack.append(i)
    return best
```

### 템플릿 4. 최솟값을 함께 저장하는 스택 (설계 문제)

```python
class MinStack:
    def __init__(self):
        self.stack = []                       # (값, 지금까지의 최솟값)

    def push(self, val):
        m = val if not self.stack else min(val, self.stack[-1][1])
        self.stack.append((val, m))

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def getMin(self):
        return self.stack[-1][1]
```

## 시간 · 공간 복잡도

| 문제 유형 | 브루트포스 | 스택 풀이 | 공간 |
|---|---|---|---|
| 괄호 짝 검사 | O(n^2) (짝 지우기 반복) | O(n) | O(n) |
| Min Stack 의 getMin | O(n) (`min(stack)`) | O(1) | O(n) |
| 후위 표기식 계산 | - | O(n) | O(n) |
| 다음 큰 원소 / 일일 온도 | O(n^2) | O(n) | O(n) |
| Car Fleet | 시뮬레이션 | O(n log n) (정렬) | O(n) |
| 히스토그램 최대 직사각형 | O(n^2) | O(n) | O(n) |

## 자주 하는 실수

- [ ] 빈 스택에서 `pop()` 이나 `stack[-1]` 을 호출해 `IndexError`. 항상 `if stack` / `while stack and ...` 으로 먼저 확인하세요.
- [ ] 괄호 문제에서 순회가 끝난 뒤 **스택이 비었는지** 확인하지 않는다. (`"(("` 는 False)
- [ ] 후위 표기식에서 `a = pop(); b = pop()` 으로 순서를 거꾸로 꺼낸다. 먼저 꺼낸 것이 오른쪽 피연산자 b 입니다.
- [ ] 파이썬 `//` 가 0 쪽이 아니라 **내림**이라는 것을 잊는다. `-7 // 2 == -4`, `int(-7 / 2) == -3`.
- [ ] `"-11"` 같은 음수 토큰을 연산자로 착각한다. 토큰 전체가 연산자인지(`t in "+-*/"` 가 아니라 `t in ("+", "-", "*", "/")`)로 판단하세요.
- [ ] 단조 스택에 **값**만 넣어서 거리(인덱스 차이)나 폭을 계산하지 못한다. 보통 **인덱스**를 넣습니다.
- [ ] `<` 와 `<=` 를 헷갈린다. "더 큰" 이면 같은 값은 답이 아니므로 `nums[top] < x` 일 때만 pop.
- [ ] 히스토그램에서 순회가 끝난 뒤 스택에 남은 막대를 처리하지 않는다. 끝에 높이 0 센티널을 붙이면 해결됩니다.
- [ ] Min Stack 에서 보조 스택 방식을 쓸 때 `val < 현재 최솟값` 일 때만 push 해서 같은 최솟값이 여러 개일 때 pop 후 최솟값을 잃는다. `<=` 로 넣어야 합니다.

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Valid Parentheses | Easy | 여는 괄호 push, 닫는 괄호는 top 과 짝 확인 | `python practice.py start valid-parentheses` |
| 2 | Min Stack | Medium | (값, 그 시점 최솟값) 을 함께 저장 | `python practice.py start min-stack` |
| 3 | Evaluate Reverse Polish Notation | Medium | 숫자 push, 연산자면 두 개 pop 후 계산 | `python practice.py start evaluate-reverse-polish-notation` |
| 4 | Daily Temperatures | Medium | 단조 감소 스택, pop 할 때 답 확정 | `python practice.py start daily-temperatures` |
| 5 | Car Fleet | Medium | 위치 내림차순 + 도착 시간 스택 | `python practice.py start car-fleet` |
| 6 | Largest Rectangle in Histogram | Hard | 단조 증가 스택 + 끝에 높이 0 센티널 | `python practice.py start largest-rectangle-in-histogram` |

## 더 풀어 볼 문제

- LeetCode 1047. Remove All Adjacent Duplicates In String (짝지어 제거하기와 같은 유형)
- LeetCode 22. Generate Parentheses (스택 + 백트래킹)
- LeetCode 496 / 503. Next Greater Element I / II (단조 스택, 원형 배열)
- LeetCode 901. Online Stock Span (왼쪽으로 연속된 작거나 같은 날 수)
- LeetCode 394. Decode String (`3[a2[c]]` 중첩 구조)
- LeetCode 224 / 227. Basic Calculator I / II
- LeetCode 85. Maximal Rectangle (행마다 히스토그램)
- LeetCode 42. Trapping Rain Water (단조 스택 풀이로 다시 풀기)
- 프로그래머스 Lv.1 같은 숫자는 싫어
- 프로그래머스 Lv.2 올바른 괄호 (한 종류 괄호 → 카운터로도 가능)
- 프로그래머스 Lv.2 괄호 회전하기 (회전마다 Valid Parentheses)
- 프로그래머스 Lv.2 짝지어 제거하기
- 프로그래머스 Lv.2 주식가격 (단조 스택, Daily Temperatures 와 같은 틀)
- 프로그래머스 Lv.2 뒤에 있는 큰 수 찾기 (다음 큰 원소 그대로)
- 프로그래머스 Lv.2 택배상자 (보조 컨테이너 = 스택 시뮬레이션)
- 프로그래머스 Lv.3 표 편집 (2021 카카오 인턴십, 삭제 기록을 스택으로 되돌리기)

## 영어로 설명하기 (미국 면접용)

- "I'll use a stack because each closing bracket has to match the most recently opened one, which is exactly last-in, first-out."
- "To support getMin in constant time, I store each value together with the minimum at the time it was pushed, so popping automatically restores the previous minimum."
- "This is a next-greater-element problem, so I'll keep a monotonic decreasing stack of indices. When a warmer day comes, I pop every colder day and fill in its answer."
- "Even though there's a nested while loop, each index is pushed and popped at most once, so the total time is O(n)."
- "For the histogram, when a bar is popped from the increasing stack, the current index is its right boundary and the new top is its left boundary, so I can compute the widest rectangle using that bar's height."

## 체크리스트

- [ ] 파이썬 리스트로 push / pop / top / empty 를 O(1) 에 쓸 수 있다.
- [ ] 괄호 문제를 보지 않고 1분 안에 쓸 수 있고, 한 종류 괄호는 카운터로 충분하다는 것을 안다.
- [ ] 후위 표기식에서 피연산자 순서와 0 쪽 나눗셈(`int(a / b)`)을 정확히 처리할 수 있다.
- [ ] "다음 큰 원소" 를 보면 단조 스택을 떠올리고, 감소/증가 중 무엇을 유지할지 고를 수 있다.
- [ ] 단조 스택이 O(n) 인 이유를 분할 상환 분석으로 설명할 수 있다.
- [ ] 히스토그램 문제에서 pop 시점에 폭이 `i - stack[-1] - 1` 인 이유를 그림으로 설명할 수 있다.
- [ ] 프로그래머스 '주식가격', '뒤에 있는 큰 수 찾기' 를 단조 스택으로 풀 수 있다.
