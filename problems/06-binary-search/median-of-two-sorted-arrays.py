TITLE = "Median of Two Sorted Arrays (두 정렬 배열의 중앙값)"
LEVEL = "Hard"
SOURCE = "LeetCode 4"
PATTERN = "짧은 배열의 '자르는 위치' 를 이분 탐색해 왼쪽 절반/오른쪽 절반 나누기"

DESCRIPTION = """
오름차순으로 정렬된 두 정수 배열 nums1, nums2 가 주어집니다.
두 배열을 합친 전체 원소의 중앙값(median)을 실수(float)로 return 하세요.
- 전체 개수가 홀수면 가운데 값, 짝수면 가운데 두 값의 평균입니다.
목표 시간 복잡도는 O(log(min(m, n))) 입니다.

제한사항
- 0 ≤ len(nums1), len(nums2) ≤ 1,000 (단, 둘 중 하나는 비어 있지 않음)
- -10^6 ≤ nums1[i], nums2[i] ≤ 10^6

입출력 예
nums1 = [1, 3],  nums2 = [2]     →  2.0   (합치면 [1, 2, 3])
nums1 = [1, 2],  nums2 = [3, 4]  →  2.5   (합치면 [1, 2, 3, 4] → (2 + 3) / 2)
"""

SIGNATURE = "def solution(nums1: list[int], nums2: list[int]) -> float:"

HINTS = [
    "가장 쉬운 방법은 두 배열을 병합(merge)해서 가운데를 보는 것입니다: O(m + n). 여기서 시작해 더 빠르게 만들어 봅시다.",
    "중앙값은 전체를 '왼쪽 절반' 과 '오른쪽 절반' 으로 나누는 경계입니다. nums1 에서 i 개, nums2 에서 j 개를 왼쪽에 넣는다면 i + j = (m + n + 1) // 2 로 고정됩니다.",
    "i 를 정하면 j 가 정해집니다. 올바른 분할 조건: nums1[i-1] <= nums2[j] 그리고 nums2[j-1] <= nums1[i]. 짧은 배열에서 i 를 이분 탐색하세요.",
    "nums1[i-1] > nums2[j] 이면 i 가 너무 큼 → hi = i - 1. nums2[j-1] > nums1[i] 이면 i 가 너무 작음 → lo = i + 1. 경계 밖은 -inf / +inf 로 취급합니다.",
]

TESTS = [
    {"input": [[1, 3], [2]], "output": 2.0},
    {"input": [[1, 2], [3, 4]], "output": 2.5},
    {"input": [[], [1]], "output": 1.0},
    {"input": [[2], []], "output": 2.0},
    {"input": [[0, 0], [0, 0]], "output": 0.0},
    {"input": [[1, 3, 5, 7], [2, 4, 6]], "output": 4.0},
    {"input": [[-5, -3], [-2, -1, 0]], "output": -2.0},
    {"input": [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]], "output": 6.0},
    {"input": [[100], [1, 2, 3, 4]], "output": 3.0},
    {"input": [[1000000], [-1000000]], "output": 0.0},
]

COMPARE = "float"

EXPLANATION = """
핵심: 합친 배열을 실제로 만들지 않고, "왼쪽 절반에 nums1 에서 몇 개(i), nums2 에서 몇 개(j)" 를 고르는 분할(partition)을 찾습니다.

  nums1:  A[0] ... A[i-1]  |  A[i] ... A[m-1]
  nums2:  B[0] ... B[j-1]  |  B[j] ... B[n-1]
          ---- 왼쪽 절반 ----  ---- 오른쪽 절반 ----
  i + j = (m + n + 1) // 2  (홀수면 왼쪽이 하나 더 많음)

올바른 분할: max(왼쪽) <= min(오른쪽) ⇔ A[i-1] <= B[j] 그리고 B[j-1] <= A[i]

1. nums1 이 더 짧도록 교환 (짧은 쪽에서 이분 탐색해야 j 가 범위를 벗어나지 않음)
2. lo, hi = 0, m 에서 i 를 이분 탐색, j = half - i
3. 경계 밖 값은 -inf / +inf 로 둠
4. A[i-1] > B[j] → i 를 줄임 (hi = i - 1) / B[j-1] > A[i] → i 를 늘림 (lo = i + 1) / 둘 다 아니면 정답
5. 홀수면 max(왼쪽), 짝수면 (max(왼쪽) + min(오른쪽)) / 2

시간 O(log(min(m, n))), 공간 O(1)
면접 포인트: 바로 이 풀이를 떠올리기는 어렵습니다. 병합 O(m + n) → "k 번째 원소 찾기" O(log(m + n)) → 분할 이분 탐색 순서로
설명하면 좋습니다. 빈 배열과 i = 0, i = m 경계를 inf 로 처리하는 부분에서 실수가 많습니다.
"""


def reference(nums1, nums2):
    A, B = nums1, nums2
    if len(A) > len(B):
        A, B = B, A  # 짧은 배열에서 이분 탐색
    m, n = len(A), len(B)
    half = (m + n + 1) // 2  # 왼쪽 절반의 크기
    INF = float("inf")
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2  # A 에서 왼쪽으로 보낼 개수
        j = half - i        # B 에서 왼쪽으로 보낼 개수
        a_left = A[i - 1] if i > 0 else -INF
        a_right = A[i] if i < m else INF
        b_left = B[j - 1] if j > 0 else -INF
        b_right = B[j] if j < n else INF
        if a_left > b_right:
            hi = i - 1      # A 에서 너무 많이 가져옴
        elif b_left > a_right:
            lo = i + 1      # A 에서 너무 적게 가져옴
        else:
            if (m + n) % 2:
                return float(max(a_left, b_left))
            return (max(a_left, b_left) + min(a_right, b_right)) / 2
    return 0.0  # 정렬된 입력이면 도달하지 않음


def brute_force(nums1, nums2):
    # 병합 O(m + n)
    merged = []
    i = j = 0
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1
    merged += nums1[i:] + nums2[j:]
    k = len(merged)
    if k % 2:
        return float(merged[k // 2])
    return (merged[k // 2 - 1] + merged[k // 2]) / 2
