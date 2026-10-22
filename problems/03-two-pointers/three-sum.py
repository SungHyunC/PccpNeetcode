TITLE = "3Sum (세 수의 합)"
LEVEL = "Medium"
SOURCE = "LeetCode 15"
PATTERN = "정렬 + 하나 고정 + 나머지 둘은 투 포인터, 중복 건너뛰기"

DESCRIPTION = """
정수 배열 nums 가 주어집니다.
서로 다른 위치의 세 원소를 골라 합이 0 이 되는 조합 [a, b, c] 를 모두 찾아 return 하세요.
값이 같은 조합은 한 번만 포함해야 합니다. (예: [-1, 0, 1] 과 [0, 1, -1] 은 같은 조합)
바깥 리스트의 순서와 각 조합 안의 순서는 자유입니다.

제한사항
- 3 ≤ len(nums) ≤ 3,000
- -100,000 ≤ nums[i] ≤ 100,000

입출력 예
nums = [-1, 0, 1, 2, -1, -4]  →  [[-1, -1, 2], [-1, 0, 1]]
nums = [0, 1, 1]              →  []
nums = [0, 0, 0]              →  [[0, 0, 0]]
"""

SIGNATURE = "def solution(nums: list[int]) -> list[list[int]]:"

HINTS = [
    "삼중 for 문은 O(n^3) 입니다. n = 3,000 이면 약 45억 번이라 시간 초과입니다.",
    "먼저 정렬하세요. 첫 번째 수 nums[i] 를 고정하면 나머지는 '정렬된 구간에서 합이 -nums[i] 인 두 수 찾기' = Two Sum II 입니다.",
    "중복 제거: (1) nums[i] == nums[i-1] 이면 i 를 건너뜁니다. (2) 답을 찾은 뒤 l 을 오른쪽으로 옮길 때 같은 값이 계속되면 더 옮깁니다.",
    "가지치기: 정렬 후 nums[i] > 0 이면 뒤는 모두 양수라 합이 0 이 될 수 없으므로 break 합니다.",
]

TESTS = [
    {"input": [[-1, 0, 1, 2, -1, -4]], "output": [[-1, -1, 2], [-1, 0, 1]]},
    {"input": [[0, 1, 1]], "output": []},
    {"input": [[0, 0, 0]], "output": [[0, 0, 0]]},
    {"input": [[0, 0, 0, 0]], "output": [[0, 0, 0]]},
    {"input": [[-2, 0, 1, 1, 2]], "output": [[-2, 0, 2], [-2, 1, 1]]},
    {"input": [[1, 2, -2, -1]], "output": []},
    {"input": [[3, -2, 1, 0]], "output": []},
    {"input": [[-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6]],
     "output": [[-4, -2, 6], [-4, 0, 4], [-4, 1, 3], [-4, 2, 2], [-2, -2, 4], [-2, 0, 2]]},
    {"input": [[-100000, 50000, 50000, 0]], "output": [[-100000, 50000, 50000]]},
]

COMPARE = "unordered_nested"

PERF_LIMIT = 1.0


def perf_case():
    import random
    nums = [random.randint(-3000, 3000) for _ in range(1500)]
    return {"input": [nums], "output": None}


EXPLANATION = """
핵심: 정렬 → 첫 수를 고정 → 나머지 두 수는 Two Sum II 투 포인터. 정렬했기 때문에 중복도 "옆 칸과 같은지" 로 쉽게 거를 수 있습니다.

1. nums.sort()
2. i 를 0 부터 n-3 까지:
   - nums[i] > 0 이면 break (이후 셋 다 양수)
   - i > 0 이고 nums[i] == nums[i-1] 이면 continue (같은 첫 수 중복 방지)
   - l = i + 1, r = n - 1 로 합 s = nums[i] + nums[l] + nums[r] 을 확인
     s < 0 → l += 1 / s > 0 → r -= 1 / s == 0 → 정답 추가 후 l += 1, 그리고 nums[l] == nums[l-1] 인 동안 l += 1
3. 결과 return

시간 O(n^2) (정렬 O(n log n) + 고정 n 번 × 투 포인터 n), 공간 O(1) (출력·정렬 제외)
면접 포인트: set 으로 중복을 거르는 방법도 정답이지만, "정렬 + 인접 중복 건너뛰기" 로 set 없이 처리하는 것을 기대합니다.
k-Sum 으로 일반화하면 O(n^(k-1)) 이라는 것도 같이 말해 보세요.
"""


def reference(nums):
    nums = sorted(nums)
    n = len(nums)
    res = []
    for i in range(n - 2):
        if nums[i] > 0:
            break  # 가장 작은 수가 양수면 합이 0 이 될 수 없음
        if i > 0 and nums[i] == nums[i - 1]:
            continue  # 같은 첫 수는 한 번만
        l, r = i + 1, n - 1
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
                    l += 1  # 같은 두 번째 수 건너뛰기
    return res


def brute_force(nums):
    n = len(nums)
    found = set()
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    found.add(tuple(sorted((nums[i], nums[j], nums[k]))))
    return [list(t) for t in found]
