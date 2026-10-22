TITLE = "Two Sum II - Sorted Array (정렬된 배열의 두 수의 합)"
LEVEL = "Medium"
SOURCE = "LeetCode 167"
PATTERN = "정렬된 배열 + 양 끝 투 포인터로 합 조절"

DESCRIPTION = """
오름차순(같은 값 허용)으로 정렬된 정수 배열 numbers 와 정수 target 이 주어집니다.
더해서 target 이 되는 두 원소의 위치를 1부터 세는 번호로 [i, j] (i < j) 형태로 return 하세요.
답은 항상 정확히 하나 존재하며, 같은 원소를 두 번 쓸 수 없습니다.
추가 메모리는 O(1) 만 사용하도록 노력해 보세요.

제한사항
- 2 ≤ len(numbers) ≤ 100,000
- -1,000 ≤ numbers[i] ≤ 1,000, numbers 는 오름차순 정렬
- -2,000 ≤ target ≤ 2,000

입출력 예
numbers = [2, 7, 11, 15], target = 9   →  [1, 2]
numbers = [2, 3, 4],      target = 6   →  [1, 3]
numbers = [-1, 0],        target = -1  →  [1, 2]
"""

SIGNATURE = "def solution(numbers: list[int], target: int) -> list[int]:"

HINTS = [
    "해시맵(Two Sum 1번 풀이)도 통과하지만 공간이 O(n) 입니다. '정렬되어 있다' 는 조건을 어떻게 활용할까요?",
    "가장 작은 값(맨 왼쪽)과 가장 큰 값(맨 오른쪽)의 합을 봅니다. 합이 target 보다 작으면 어느 쪽을 움직여야 합이 커질까요?",
    "l = 0, r = n - 1. 합 < target 이면 l += 1, 합 > target 이면 r -= 1, 같으면 [l + 1, r + 1] 을 return 합니다.",
]

TESTS = [
    {"input": [[2, 7, 11, 15], 9], "output": [1, 2]},
    {"input": [[2, 3, 4], 6], "output": [1, 3]},
    {"input": [[-1, 0], -1], "output": [1, 2]},
    {"input": [[1, 2], 3], "output": [1, 2]},
    {"input": [[0, 0, 3, 4], 0], "output": [1, 2]},
    {"input": [[-5, -3, -1, 0, 2, 9], 4], "output": [1, 6]},
    {"input": [[1, 3, 5, 5, 8], 10], "output": [3, 4]},
    {"input": [[-1000, -1, 0, 1000], 0], "output": [1, 4]},
]

PERF_LIMIT = 1.0


def perf_case():
    n = 100_000
    numbers = [-1000] * (n - 2) + [999, 1000]
    return {"input": [numbers, 1999], "output": [n - 1, n]}


EXPLANATION = """
핵심: 정렬된 배열에서 양 끝 합을 보면 "합을 키울지/줄일지" 를 한 번에 결정할 수 있습니다.

1. l = 0, r = n - 1
2. cur = numbers[l] + numbers[r]
   - cur == target → [l + 1, r + 1]
   - cur <  target → 더 큰 값이 필요 → l += 1
   - cur >  target → 더 작은 값이 필요 → r -= 1
3. 매 단계 포인터 하나가 안쪽으로 움직이므로 최대 n 번 반복

왜 답을 놓치지 않나? cur < target 일 때 numbers[l] 은 남은 어떤 값(≤ numbers[r])과 더해도 target 보다 작으므로
numbers[l] 은 답이 될 수 없어 버려도 안전합니다. 반대 경우도 같습니다.

시간 O(n), 공간 O(1)
면접 포인트: "왜 l 을 버려도 되는가" 를 위처럼 한 문장으로 증명할 수 있어야 합니다. 3Sum, 4Sum 의 기본 부품입니다.
"""


def reference(numbers, target):
    l, r = 0, len(numbers) - 1
    while l < r:
        cur = numbers[l] + numbers[r]
        if cur == target:
            return [l + 1, r + 1]  # 1부터 세는 번호
        if cur < target:
            l += 1  # 합을 키운다
        else:
            r -= 1  # 합을 줄인다
    return []


def brute_force(numbers, target):
    n = len(numbers)
    for i in range(n):
        for j in range(i + 1, n):
            if numbers[i] + numbers[j] == target:
                return [i + 1, j + 1]
    return []
