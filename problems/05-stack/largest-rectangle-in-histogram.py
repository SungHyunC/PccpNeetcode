TITLE = "Largest Rectangle in Histogram (히스토그램에서 가장 큰 직사각형)"
LEVEL = "Hard"
SOURCE = "LeetCode 84"
PATTERN = "단조 증가 스택: pop 될 때 그 막대를 높이로 하는 최대 폭이 확정"

DESCRIPTION = """
너비가 1 인 막대들의 높이를 담은 배열 heights 가 주어집니다. (막대들은 붙어 있습니다)
히스토그램 안에 그릴 수 있는 직사각형 중 가장 큰 넓이를 return 하세요.
직사각형은 연속된 막대들 위에 놓이며, 높이는 그 막대들 중 가장 낮은 막대 이하여야 합니다.

제한사항
- 1 ≤ len(heights) ≤ 100,000
- 0 ≤ heights[i] ≤ 10,000

입출력 예
heights = [2, 1, 5, 6, 2, 3]  →  10   (높이 5, 6 인 두 막대 위에 높이 5 × 폭 2)
heights = [2, 4]              →  4
"""

SIGNATURE = "def solution(heights: list[int]) -> int:"

HINTS = [
    "직사각형의 높이는 어떤 막대 하나의 높이와 같습니다. 각 막대 i 를 '높이로 쓰는' 가장 넓은 직사각형을 구하면 됩니다.",
    "막대 i 를 높이로 쓰면 왼쪽·오른쪽으로 i 보다 낮은 막대를 만나기 직전까지 넓힐 수 있습니다. 즉 '왼쪽/오른쪽에서 처음 만나는 더 낮은 막대' 를 알면 됩니다.",
    "높이가 증가하는 순서로 인덱스를 스택에 쌓습니다. 현재 막대가 top 보다 낮으면, top 막대의 오른쪽 경계는 현재 i, 왼쪽 경계는 pop 후의 새 top 입니다.",
    "pop 할 때 넓이 = heights[top] × (i - stack[-1] - 1) (스택이 비면 폭은 i). 마지막에 높이 0 짜리 막대를 하나 더 처리하면 남은 막대도 깔끔하게 정리됩니다.",
]

TESTS = [
    {"input": [[2, 1, 5, 6, 2, 3]], "output": 10},
    {"input": [[2, 4]], "output": 4},
    {"input": [[1]], "output": 1},
    {"input": [[0]], "output": 0},
    {"input": [[2, 2, 2]], "output": 6},
    {"input": [[6, 2, 5, 4, 5, 1, 6]], "output": 12},
    {"input": [[1, 2, 3, 4, 5]], "output": 9},
    {"input": [[5, 4, 3, 2, 1]], "output": 9},
    {"input": [[0, 0]], "output": 0},
    {"input": [[2, 1, 2]], "output": 3},
]

PERF_LIMIT = 1.0


def perf_case():
    n = 100_000
    heights = [i // 10 for i in range(n)]  # 증가하는 막대 → 브루트포스는 매번 끝까지 확장
    return {"input": [heights], "output": None}


EXPLANATION = """
핵심: 스택에 높이가 증가하는 막대의 인덱스를 유지합니다. 더 낮은 막대가 오면,
스택에서 꺼내지는 막대는 "오른쪽으로 더 넓힐 수 없다" 가 확정되므로 그 순간 넓이를 계산합니다.

1. stack = [] (인덱스, heights 증가 순)
2. i = 0..n (i == n 일 때 높이 0 인 가상의 막대를 처리해 스택을 비움)
   - h = heights[i] (i == n 이면 0)
   - stack 이 있고 heights[stack[-1]] >= h 인 동안:
       top = stack.pop()
       left = stack[-1] if stack else -1   (top 보다 낮은 왼쪽 막대)
       넓이 = heights[top] × (i - left - 1)   (오른쪽 경계는 i)
   - stack.append(i)
3. 최대 넓이 return

시간 O(n) (각 인덱스 한 번 push, 한 번 pop), 공간 O(n)
면접 포인트: "직사각형의 높이는 반드시 어떤 막대의 높이" → "그 막대의 좌우로 처음 낮아지는 곳" → 단조 스택 순서로
관찰을 쌓아 가세요. 같은 높이를 >= 로 pop 해도 마지막 같은 높이 막대가 올바른 넓이를 계산하므로 답이 맞습니다.
2D 버전인 Maximal Rectangle(LeetCode 85)은 행마다 이 함수를 호출해 풉니다.
"""


def reference(heights):
    stack = []  # 높이가 증가하는 막대들의 인덱스
    best = 0
    n = len(heights)
    for i in range(n + 1):
        h = heights[i] if i < n else 0  # 끝에 높이 0 막대를 둬서 스택을 비운다
        while stack and heights[stack[-1]] >= h:
            top = stack.pop()
            left = stack[-1] if stack else -1  # top 보다 낮은 왼쪽 막대 위치
            best = max(best, heights[top] * (i - left - 1))
        stack.append(i)
    return best


def brute_force(heights):
    n = len(heights)
    best = 0
    for i in range(n):
        low = heights[i]
        for j in range(i, n):
            low = min(low, heights[j])
            best = max(best, low * (j - i + 1))
    return best
