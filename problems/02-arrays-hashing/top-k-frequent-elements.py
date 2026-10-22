TITLE = "Top K Frequent Elements (가장 많이 나온 K개)"
LEVEL = "Medium"
SOURCE = "LeetCode 347"
PATTERN = "빈도수 세기 + 버킷 정렬 (또는 힙)"

DESCRIPTION = """
정수 배열 nums 와 정수 k 가 주어집니다. 가장 자주 등장하는 값 k 개를 return 하세요 (순서 무관).
답이 유일하도록 입력이 주어집니다.

제한사항
- 1 ≤ len(nums) ≤ 100,000
- 1 ≤ k ≤ (서로 다른 값의 개수)
- O(n log n) 보다 빠른 풀이를 목표로 해 보세요.

입출력 예
nums = [1,1,1,2,2,3], k = 2  →  [1, 2]
nums = [1],           k = 1  →  [1]
"""

SIGNATURE = "def solution(nums: list[int], k: int) -> list[int]:"

HINTS = [
    "먼저 각 값의 등장 횟수를 셉니다 (Counter).",
    "횟수 기준으로 정렬하면 O(n log n). Counter.most_common(k) 도 가능합니다.",
    "등장 횟수는 최대 n 입니다. buckets[횟수] = [값들] 로 만든 뒤 큰 횟수부터 훑으면 O(n).",
]

COMPARE = "unordered"

TESTS = [
    {"input": [[1, 1, 1, 2, 2, 3], 2], "output": [1, 2]},
    {"input": [[1], 1], "output": [1]},
    {"input": [[4, 4, 4, 4], 1], "output": [4]},
    {"input": [[-1, -1, 2, 2, 2, 3], 2], "output": [2, -1]},
    {"input": [[5, 3, 1, 1, 1, 3, 73, 1], 2], "output": [1, 3]},
    {"input": [[1, 2], 2], "output": [1, 2]},
]

EXPLANATION = """
1. Counter 로 값별 빈도를 셉니다.
2. 버킷 정렬: buckets[f] 에 빈도가 f 인 값들을 넣습니다 (f ≤ n).
3. 빈도가 큰 버킷부터 k 개가 찰 때까지 꺼냅니다.

시간 O(n), 공간 O(n)
대안: heapq.nlargest(k, cnt.keys(), key=cnt.get) → O(n log k)
면접 포인트: 정렬 O(n log n) → 힙 O(n log k) → 버킷 O(n) 로 개선 과정을 설명할 수 있어야 합니다.
"""


def reference(nums, k):
    from collections import Counter
    cnt = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for value, freq in cnt.items():
        buckets[freq].append(value)
    answer = []
    for freq in range(len(buckets) - 1, 0, -1):
        for value in buckets[freq]:
            answer.append(value)
            if len(answer) == k:
                return answer
    return answer


def alternative(nums, k):
    import heapq
    from collections import Counter
    cnt = Counter(nums)
    return heapq.nlargest(k, cnt.keys(), key=cnt.get)
