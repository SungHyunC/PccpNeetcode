TITLE = "Hand of Straights (연속 카드 묶음 만들기)"
LEVEL = "Medium"
SOURCE = "LeetCode 846"
PATTERN = "가장 작은 카드부터 묶음 시작 (정렬 + Counter 그리디)"

DESCRIPTION = """
정수가 적힌 카드 목록 hand 와 정수 group_size 가 주어집니다.
카드를 빠짐없이 모두 사용해서, 각 묶음이 group_size 장이고
묶음 안의 숫자가 1씩 연속으로 증가하는(예: 3, 4, 5) 묶음들로 나눌 수 있는지 확인하세요.
나눌 수 있으면 True, 없으면 False 를 return 하세요.

제한사항
- 1 ≤ len(hand) ≤ 100,000
- 0 ≤ hand[i] ≤ 10^9
- 1 ≤ group_size ≤ len(hand)

입출력 예
hand = [1, 2, 3, 6, 2, 3, 4, 7, 8], group_size = 3  →  True   ([1,2,3], [2,3,4], [6,7,8])
hand = [1, 2, 3, 4, 5],             group_size = 4  →  False  (5장은 4장씩 나눌 수 없음)
"""

SIGNATURE = "def solution(hand: list[int], group_size: int) -> bool:"

HINTS = [
    "len(hand) 가 group_size 로 나누어떨어지지 않으면 바로 False.",
    "현재 남은 카드 중 가장 작은 카드 x 를 생각해 보세요. x 는 어떤 묶음의 '맨 앞' 이 될 수밖에 없습니다(x-1 이 없으니까).",
    "Counter 로 개수를 세고, 작은 값부터 보며 count[x] > 0 이면 x, x+1, ..., x+group_size-1 의 개수를 count[x] 만큼 한꺼번에 줄이세요. 어느 값이 부족하면 False.",
]

TESTS = [
    {"input": [[1, 2, 3, 6, 2, 3, 4, 7, 8], 3], "output": True},
    {"input": [[1, 2, 3, 4, 5], 4], "output": False},
    {"input": [[1], 1], "output": True},
    {"input": [[1, 1, 2, 2, 3, 3], 3], "output": True},
    {"input": [[1, 2, 3, 4, 5, 6], 2], "output": True},
    {"input": [[1, 1, 2, 3], 2], "output": False},
    {"input": [[8, 10, 12], 3], "output": False},
    {"input": [[5, 3, 4, 1000000000, 999999999, 999999998], 3], "output": True},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    hand = []
    for _ in range(25_000):
        x = random.randint(0, 10**9 - 4)
        hand.extend([x, x + 1, x + 2, x + 3])
    random.shuffle(hand)
    return {"input": [hand, 4], "output": True}


EXPLANATION = """
아이디어
- 남은 카드 중 가장 작은 값 x 는 반드시 어떤 묶음의 시작이어야 합니다. (x-1 이 없으므로 x 앞에 올 카드가 없음)
- 따라서 "가장 작은 카드로 묶음을 시작한다" 는 선택은 강제이고, 그리디가 곧 정답입니다.

단계
1. len(hand) % group_size != 0 → False
2. count = Counter(hand)
3. 정렬된 고유값 x 마다 c = count[x] 가 0 보다 크면:
   - x, x+1, ..., x+group_size-1 각각에서 c 장씩 빼기 (x 로 시작하는 묶음 c 개를 한꺼번에)
   - 어떤 값의 개수가 c 보다 적으면 False
4. 끝까지 오면 True

  hand = [1,2,3,6,2,3,4,7,8], size = 3
  count: {1:1, 2:2, 3:2, 4:1, 6:1, 7:1, 8:1}
  x=1 (c=1): 1,2,3 에서 1씩 → {2:1, 3:1, 4:1, 6:1, 7:1, 8:1}
  x=2 (c=1): 2,3,4 에서 1씩 → {6:1, 7:1, 8:1}
  x=6 (c=1): 6,7,8 에서 1씩 → {}  → True

복잡도: 시간 O(n log n) (정렬), 공간 O(n)
- 묶음 차감 연산의 총합은 (묶음 수 × group_size) = n 이하입니다.

면접 포인트
- "왜 가장 작은 카드부터?" 를 한 문장으로 정당화하세요: 가장 작은 카드는 다른 선택지가 없다.
- 묶음을 하나씩 만들면(c 번 반복) 같은 결과지만 느려질 수 있습니다. 개수 c 만큼 한 번에 빼는 게 깔끔합니다.
- 같은 문제: LeetCode 1296 Divide Array in Sets of K Consecutive Numbers.
"""


def reference(hand, group_size):
    from collections import Counter

    if len(hand) % group_size:
        return False
    count = Counter(hand)
    for x in sorted(count):
        c = count[x]
        if c == 0:
            continue
        # x 로 시작하는 묶음을 c 개 만든다
        for v in range(x, x + group_size):
            if count[v] < c:
                return False
            count[v] -= c
    return True


def brute_force(hand, group_size):
    # 정렬 후 가장 작은 카드부터 리스트에서 직접 제거: O(n^2)
    if len(hand) % group_size:
        return False
    cards = sorted(hand)
    while cards:
        x = cards[0]
        for v in range(x, x + group_size):
            if v not in cards:
                return False
            cards.remove(v)
    return True
