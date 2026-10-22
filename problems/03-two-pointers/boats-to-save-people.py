TITLE = "Boats to Save People (구명보트)"
LEVEL = "Medium"
SOURCE = "LeetCode 881 · 프로그래머스 Lv.2 '구명보트' 유형"
PATTERN = "정렬 후 가장 가벼운 사람 + 가장 무거운 사람 짝짓기 (그리디 투 포인터)"

DESCRIPTION = """
사람들의 몸무게 배열 people 과 보트 한 척의 무게 제한 limit 이 주어집니다.
보트 한 척에는 최대 2명까지 탈 수 있고, 탄 사람들의 몸무게 합은 limit 이하여야 합니다.
모든 사람을 구출하는 데 필요한 보트 수의 최솟값을 return 하세요.
모든 사람의 몸무게는 limit 이하이므로 항상 구출할 수 있습니다.

(프로그래머스 '구명보트' 문제와 같은 유형입니다.)

제한사항
- 1 ≤ len(people) ≤ 50,000
- 1 ≤ people[i] ≤ limit ≤ 30,000

입출력 예
people = [1, 2],         limit = 3    →  1   ((1, 2) 한 척)
people = [3, 2, 2, 1],   limit = 3    →  3   ((1, 2), (2), (3))
people = [70, 50, 80, 50], limit = 100 →  3  ((50, 50), (70), (80))
"""

SIGNATURE = "def solution(people: list[int], limit: int) -> int:"

HINTS = [
    "가장 무거운 사람은 반드시 어떤 보트에 타야 합니다. 그 사람과 같이 탈 수 있는 사람이 있다면 누구를 태우는 것이 가장 '손해가 적을까요'?",
    "가장 무거운 사람과 짝지을 후보로는 가장 가벼운 사람이 최선입니다. 가장 가벼운 사람과도 못 타면 누구와도 못 탑니다.",
    "정렬 후 l = 0(가벼운 쪽), r = n - 1(무거운 쪽). people[l] + people[r] ≤ limit 이면 l += 1. 어쨌든 r 은 보트를 하나 쓰므로 r -= 1, boats += 1.",
]

TESTS = [
    {"input": [[1, 2], 3], "output": 1},
    {"input": [[3, 2, 2, 1], 3], "output": 3},
    {"input": [[3, 5, 3, 4], 5], "output": 4},
    {"input": [[70, 50, 80, 50], 100], "output": 3},
    {"input": [[70, 80, 50], 100], "output": 3},
    {"input": [[5], 5], "output": 1},
    {"input": [[1, 1, 1, 1], 2], "output": 2},
    {"input": [[1, 1, 1, 1], 3], "output": 2},
    {"input": [[2, 49, 50, 51, 98], 100], "output": 3},
]

PERF_LIMIT = 1.0


def perf_case():
    import random
    people = [random.randint(1, 30_000) for _ in range(50_000)]
    return {"input": [people, 30_000], "output": None}


EXPLANATION = """
핵심: 가장 무거운 사람부터 보트를 배정하고, 남는 자리에 가장 가벼운 사람을 태울 수 있으면 태웁니다.

1. people 을 오름차순 정렬
2. l = 0, r = n - 1, boats = 0
3. l <= r 인 동안:
   - people[l] + people[r] <= limit 이면 가벼운 사람도 함께 탑승 → l += 1
   - 무거운 사람은 항상 탑승 → r -= 1, boats += 1
4. boats return

왜 최적인가? 가장 무거운 사람 r 은 어차피 보트 하나가 필요합니다. 그와 함께 탈 수 있는 사람이 있다면
가장 가벼운 사람을 태워도 손해가 없습니다(교환 논증: 다른 사람 x 를 태운 최적해에서 x 와 가장 가벼운 사람을 바꿔도 여전히 가능).

시간 O(n log n) (정렬), 공간 O(1) (정렬 제외)
면접 포인트: 보트 정원이 2명이라는 조건 덕분에 투 포인터 그리디가 성립합니다. 3명 이상이면 다른 문제(빈 패킹)가 됩니다.
프로그래머스 '구명보트' 도 같은 코드로 통과합니다.
"""


def reference(people, limit):
    people = sorted(people)
    l, r = 0, len(people) - 1
    boats = 0
    while l <= r:
        if people[l] + people[r] <= limit:
            l += 1  # 가장 가벼운 사람이 함께 탈 수 있다
        r -= 1      # 가장 무거운 사람은 항상 탄다
        boats += 1
    return boats
