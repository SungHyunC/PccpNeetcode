TITLE = "Trapping Rain Water (빗물 트래핑)"
LEVEL = "Hard"
SOURCE = "LeetCode 42"
PATTERN = "각 칸의 물 = min(왼쪽 최대, 오른쪽 최대) - 높이, 투 포인터로 O(1) 공간"

DESCRIPTION = """
너비가 1 인 막대들의 높이를 나타내는 배열 height 가 주어집니다.
비가 내린 뒤 막대 사이사이에 고이는 빗물의 총량을 return 하세요.
양 끝 바깥으로는 물이 흘러 나갑니다.

제한사항
- 1 ≤ len(height) ≤ 200,000
- 0 ≤ height[i] ≤ 100,000

입출력 예
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]  →  6
height = [4, 2, 0, 3, 2, 5]                    →  9
"""

SIGNATURE = "def solution(height: list[int]) -> int:"

HINTS = [
    "칸 하나만 생각해 보세요. i 번 칸 위에 고이는 물의 높이는 '왼쪽에서 가장 높은 막대' 와 '오른쪽에서 가장 높은 막대' 중 낮은 쪽에 의해 결정됩니다.",
    "water[i] = min(leftMax[i], rightMax[i]) - height[i]. leftMax, rightMax 배열을 미리 구해 두면 O(n) 시간, O(n) 공간입니다.",
    "공간을 O(1) 로: l, r 투 포인터와 leftMax, rightMax 변수를 둡니다. leftMax < rightMax 라면 l 칸의 물은 leftMax 로 확정됩니다(오른쪽에는 그보다 높은 벽이 이미 있으니까요).",
    "if leftMax < rightMax: l += 1; leftMax = max(leftMax, h[l]); ans += leftMax - h[l]  (반대쪽도 대칭으로)",
]

TESTS = [
    {"input": [[0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]], "output": 6},
    {"input": [[4, 2, 0, 3, 2, 5]], "output": 9},
    {"input": [[5]], "output": 0},
    {"input": [[1, 2, 3, 4]], "output": 0},
    {"input": [[4, 3, 2, 1]], "output": 0},
    {"input": [[3, 0, 3]], "output": 3},
    {"input": [[5, 4, 1, 2]], "output": 1},
    {"input": [[2, 0, 2, 0, 2]], "output": 4},
    {"input": [[0, 0, 0]], "output": 0},
    {"input": [[100000, 0, 0, 100000]], "output": 200000},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    height = [random.randint(0, 100_000) for _ in range(200_000)]
    return {"input": [height], "output": None}


EXPLANATION = """
핵심: i 칸에 고이는 물 = min(왼쪽 최대 높이, 오른쪽 최대 높이) - height[i].
이를 모든 칸에 대해 빠르게 구하는 것이 문제입니다.

방법 1 (prefix/suffix 최대, 공간 O(n)):
  leftMax[i] = max(height[0..i]), rightMax[i] = max(height[i..n-1]) 을 미리 구한 뒤 합산.

방법 2 (투 포인터, 공간 O(1)):
1. l = 0, r = n - 1, leftMax = height[l], rightMax = height[r]
2. leftMax < rightMax 이면:
   l 칸의 오른쪽에는 rightMax(> leftMax) 짜리 벽이 이미 있으므로 l 칸의 수위는 leftMax 로 확정
   → l += 1, leftMax = max(leftMax, height[l]), ans += leftMax - height[l]
3. 아니면 대칭으로 r 쪽을 처리
4. l < r 인 동안 반복

시간 O(n), 공간 O(1)
면접 포인트: 바로 투 포인터를 쓰기보다 "칸 하나의 물 공식" → O(n^2) 브루트포스 → prefix/suffix 배열 O(n) 공간
→ 투 포인터 O(1) 공간 순서로 설명하면 좋습니다. 단조 스택(monotonic stack)으로 '가로 층' 단위로 세는 풀이도 있습니다.
"""


def reference(height):
    l, r = 0, len(height) - 1
    left_max, right_max = height[l], height[r]
    water = 0
    while l < r:
        if left_max < right_max:
            # 오른쪽에 더 높은 벽이 보장됨 → l 쪽 수위는 left_max
            l += 1
            left_max = max(left_max, height[l])
            water += left_max - height[l]
        else:
            r -= 1
            right_max = max(right_max, height[r])
            water += right_max - height[r]
    return water


def alternative(height):
    # prefix / suffix 최대 배열 (공간 O(n))
    n = len(height)
    left = [0] * n
    right = [0] * n
    cur = 0
    for i in range(n):
        cur = max(cur, height[i])
        left[i] = cur
    cur = 0
    for i in range(n - 1, -1, -1):
        cur = max(cur, height[i])
        right[i] = cur
    return sum(min(left[i], right[i]) - height[i] for i in range(n))


def brute_force(height):
    n = len(height)
    water = 0
    for i in range(n):
        water += min(max(height[: i + 1]), max(height[i:])) - height[i]
    return water
