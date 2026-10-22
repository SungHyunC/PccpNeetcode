TITLE = "Container With Most Water (물을 가장 많이 담는 통)"
LEVEL = "Medium"
SOURCE = "LeetCode 11"
PATTERN = "양 끝에서 시작해 더 낮은 쪽 포인터를 옮기는 그리디 투 포인터"

DESCRIPTION = """
정수 배열 height 가 주어집니다. i 번 위치에 높이 height[i] 인 세로 막대가 서 있습니다.
두 막대를 골라 x 축과 함께 통을 만들면, 담을 수 있는 물의 양은
(두 막대 사이 거리) × (두 막대 중 낮은 쪽 높이) 입니다.
담을 수 있는 물의 최댓값을 return 하세요. (통을 기울일 수 없습니다)

제한사항
- 2 ≤ len(height) ≤ 100,000
- 0 ≤ height[i] ≤ 10,000

입출력 예
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]  →  49   (1번과 8번 막대: 거리 7 × 높이 7)
height = [1, 1]                       →  1
"""

SIGNATURE = "def solution(height: list[int]) -> int:"

HINTS = [
    "모든 쌍을 보면 O(n^2) 입니다. n = 100,000 이면 시간 초과입니다.",
    "가장 넓은 폭(l = 0, r = n - 1)에서 시작합니다. 포인터를 안쪽으로 옮기면 폭은 반드시 줄어듭니다. 그렇다면 어느 쪽을 옮겨야 더 커질 '가능성' 이 있을까요?",
    "높이는 낮은 쪽이 결정합니다. 높은 쪽을 옮기면 높이는 그대로거나 낮아지고 폭은 줄어 절대 좋아지지 않습니다. 그러니 항상 낮은 쪽 포인터를 옮기세요.",
]

TESTS = [
    {"input": [[1, 8, 6, 2, 5, 4, 8, 3, 7]], "output": 49},
    {"input": [[1, 1]], "output": 1},
    {"input": [[4, 3, 2, 1, 4]], "output": 16},
    {"input": [[1, 2, 1]], "output": 2},
    {"input": [[0, 0]], "output": 0},
    {"input": [[0, 10000]], "output": 0},
    {"input": [[2, 3, 4, 5, 18, 17, 6]], "output": 17},
    {"input": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], "output": 25},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    height = [random.randint(0, 10_000) for _ in range(100_000)]
    return {"input": [height], "output": None}


EXPLANATION = """
핵심: 넓이 = 폭 × min(왼쪽, 오른쪽). 가장 넓은 폭에서 시작해, 낮은 쪽 막대를 버리며 안쪽으로 좁힙니다.

1. l = 0, r = n - 1, best = 0
2. best = max(best, (r - l) * min(height[l], height[r]))
3. height[l] < height[r] 이면 l += 1, 아니면 r -= 1
4. l < r 인 동안 반복

왜 낮은 쪽을 버려도 되나? height[l] 이 더 낮다면, l 과 짝지을 수 있는 어떤 r' (< r) 도
폭은 더 좁고 높이는 height[l] 이하이므로 지금보다 클 수 없습니다. 즉 l 은 이미 최선을 확인했습니다.

시간 O(n), 공간 O(1)
면접 포인트: 그리디 선택(낮은 쪽 이동)의 정당성을 위 논리로 설명하는 것이 핵심입니다.
Trapping Rain Water 와 헷갈리지 마세요: 이 문제는 '두 막대만' 고르고 사이 막대는 무시합니다.
"""


def reference(height):
    l, r = 0, len(height) - 1
    best = 0
    while l < r:
        h = min(height[l], height[r])
        best = max(best, (r - l) * h)
        # 낮은 쪽을 옮겨야만 더 큰 넓이의 가능성이 생긴다
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return best


def brute_force(height):
    n = len(height)
    best = 0
    for i in range(n):
        for j in range(i + 1, n):
            best = max(best, (j - i) * min(height[i], height[j]))
    return best
