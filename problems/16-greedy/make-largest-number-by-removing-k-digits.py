TITLE = "Make Largest Number by Removing K Digits (k 개 지워서 가장 큰 수 만들기)"
LEVEL = "Medium"
SOURCE = "PCCP 기출 유형 (프로그래머스 Lv.2 '큰 수 만들기' 유형)"
PATTERN = "단조 감소 스택 그리디: 앞자리가 클수록 좋다"

DESCRIPTION = """
숫자로 이루어진 문자열 number 와 정수 k 가 주어집니다.
number 에서 숫자 k 개를 지우고, 남은 숫자들을 원래 순서 그대로 이어 붙여 만들 수 있는
가장 큰 수를 문자열로 return 하세요.
결과 문자열의 길이는 len(number) - k 이며, 맨 앞이 0 이더라도 그대로 둡니다.

제한사항
- 2 ≤ len(number) ≤ 300,000
- 1 ≤ k < len(number)
- number 는 '0'~'9' 로만 이루어져 있음

입출력 예
number = "3819",    k = 1  →  "819"
number = "2938471", k = 3  →  "9871"
number = "54321",   k = 2  →  "543"
"""

SIGNATURE = "def solution(number: str, k: int) -> str:"

HINTS = [
    "남길 자릿수가 같다면 앞자리가 큰 수가 무조건 큽니다. 앞자리를 최대한 크게 만드는 데 '지우기' 를 쓰세요.",
    "왼쪽부터 숫자를 하나씩 쌓다가, 새 숫자가 바로 앞에 쌓인 숫자보다 크다면 앞 숫자를 지우는 게 이득입니다(아직 지울 기회 k 가 남아 있다면).",
    "스택: 새 숫자 d 가 오면 k > 0 이고 stack[-1] < d 인 동안 pop (k -= 1), 그다음 d 를 push. 끝까지 봤는데 k 가 남았다면(예: \"54321\") 뒤에서 k 개를 잘라내세요. O(n).",
]

TESTS = [
    {"input": ["3819", 1], "output": "819"},
    {"input": ["2938471", 3], "output": "9871"},
    {"input": ["54321", 2], "output": "543"},
    {"input": ["12345", 2], "output": "345"},
    {"input": ["1111", 2], "output": "11"},
    {"input": ["10", 1], "output": "1"},
    {"input": ["100", 1], "output": "10"},
    {"input": ["0091", 2], "output": "91"},
    {"input": ["9999999998", 9], "output": "9"},
    {"input": ["7712843", 4], "output": "843"},
]

PERF_LIMIT = 1.0


def perf_case():
    import random

    n = 300_000
    number = "".join(random.choice("0123456789") for _ in range(n))
    return {"input": [number, n // 2], "output": None}


EXPLANATION = """
아이디어
- 길이가 같은 두 수는 앞자리부터 비교합니다. 앞자리를 1 키우는 것이 뒤의 모든 자리를 합친 것보다 중요합니다.
- 왼쪽부터 보면서, 지금 숫자 d 가 바로 앞에 남겨 둔 숫자보다 크다면 앞 숫자를 지우면 그 자리에 d 가 당겨져 와서 이득입니다.
- 이 "앞의 작은 값을 밀어내는" 동작이 단조 감소 스택(monotonic stack)입니다.

단계
1. stack = []
2. 각 숫자 d 에 대해: while k > 0 and stack and stack[-1] < d: pop, k -= 1
   그다음 stack.append(d)
3. 끝났는데 k > 0 이면 (내림차순 구간이 남은 경우) 뒤에서 k 개 제거
4. "".join(stack)

  number = "2938471", k = 3
  d=2 → [2]
  d=9 → 2 < 9 pop (k=2) → [9]
  d=3 → [9, 3]
  d=8 → 3 < 8 pop (k=1) → [9, 8]
  d=4 → [9, 8, 4]
  d=7 → 4 < 7 pop (k=0) → [9, 8, 7]
  d=1 → [9, 8, 7, 1]       → "9871"

왜 그리디가 맞는가 (교환 논법)
- stack[-1] < d 인데 stack[-1] 을 남기고 다른 숫자를 지운 해가 있다고 합시다.
  stack[-1] 대신 그 숫자를 남기도록 바꾸면 그 자리 숫자가 d 쪽으로 당겨져 커지거나 같아집니다 → 손해가 없음.

복잡도: 시간 O(n) (각 숫자는 최대 한 번 push, 한 번 pop), 공간 O(n)

시험 포인트
- 프로그래머스 '큰 수 만들기' 는 number 길이가 최대 1,000,000 입니다.
  "각 자리마다 남은 구간에서 최댓값 찾기" 방식은 O(n × k) 로 큰 테스트에서 시간 초과 → 스택 풀이가 필요합니다.
- k 가 남는 경우(예: "54321")를 처리하지 않으면 길이가 틀려 오답이 됩니다.
- 반대 문제(LeetCode 402 Remove K Digits, 가장 작은 수)는 부등호만 뒤집고 앞의 0 제거 규칙이 추가됩니다.
"""


def reference(number, k):
    stack = []
    for d in number:
        # 앞에 남긴 숫자가 더 작으면 지우는 게 이득 (지울 기회가 남은 동안)
        while k > 0 and stack and stack[-1] < d:
            stack.pop()
            k -= 1
        stack.append(d)
    if k > 0:  # 내림차순으로 끝나서 덜 지운 경우: 뒤에서 자르기
        stack = stack[:-k]
    return "".join(stack)


def brute_force(number, k):
    # 남길 위치 조합을 모두 시도: O(C(n, k) * n)
    from itertools import combinations

    keep = len(number) - k
    return max("".join(number[i] for i in idx) for idx in combinations(range(len(number)), keep))
