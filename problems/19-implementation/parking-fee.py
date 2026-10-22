TITLE = "Parking Fee (주차 요금 정산)"
LEVEL = "Medium"
SOURCE = "PCCP 기출 유형 (프로그래머스 '주차 요금 계산' 유형)"
PATTERN = "문자열 파싱 + 시각을 분으로 변환 + dict 누적 + 올림 나눗셈"

DESCRIPTION = """
아파트 지하 주차장은 하루 단위로 요금을 정산합니다. 요금표 fees 와 차량 출입 기록 records 가 주어집니다.

fees = [기본 시간(분), 기본 요금(원), 단위 시간(분), 단위 요금(원)]

records 의 각 원소는 "HH:MM 차량번호 IN" 또는 "HH:MM 차량번호 OUT" 형식의 문자열이며 시각 순으로 정렬되어 있습니다.
차량번호는 숫자 4자리 문자열입니다("0000" ~ "9999").

정산 규칙
1. 차량별로 그날 주차한 시간을 모두 더해 '누적 주차 시간' 을 구합니다. 같은 차가 여러 번 드나들 수 있습니다.
2. 들어간(IN) 뒤 나간(OUT) 기록이 없는 차량은 23:59 에 나간 것으로 봅니다.
3. 누적 주차 시간이 기본 시간 이하이면 기본 요금만 냅니다.
4. 기본 시간을 넘으면: 기본 요금 + ⌈(누적 시간 - 기본 시간) / 단위 시간⌉ × 단위 요금
   (⌈ ⌉ 는 올림입니다. 예: 35분을 10분 단위로 나누면 4단위)

그날 기록이 있는 모든 차량의 요금을 차량번호가 작은 순서대로 담아 return 하세요.

제한사항
- fees 의 각 값: 1 ≤ 기본 시간 ≤ 1,439, 0 ≤ 기본 요금 ≤ 100,000, 1 ≤ 단위 시간 ≤ 1,439, 1 ≤ 단위 요금 ≤ 10,000
- 1 ≤ len(records) ≤ 1,000
- 같은 차량이 IN 상태에서 다시 IN 하거나, IN 없이 OUT 하는 잘못된 기록은 없습니다.
- 00:00 ~ 23:59 사이의 기록만 주어집니다.

입출력 예
fees = [120, 3000, 30, 500]
records = ["07:00 1234 IN", "08:10 0500 IN", "09:30 1234 OUT", "11:00 1234 IN",
           "12:20 0500 OUT", "13:05 1234 OUT", "22:50 0042 IN"]
→ [3000, 5500, 6000]

  0042: 22:50 ~ 23:59(미출차) = 69분      → 69 ≤ 120 → 3000
  0500: 08:10 ~ 12:20 = 250분             → 3000 + ⌈130/30⌉ × 500 = 3000 + 5 × 500 = 5500
  1234: 150분 + 125분 = 275분             → 3000 + ⌈155/30⌉ × 500 = 3000 + 6 × 500 = 6000
"""

SIGNATURE = "def solution(fees: list[int], records: list[str]) -> list[int]:"

HINTS = [
    "\"HH:MM\" 은 분 단위 정수로 바꾸면 계산이 쉬워집니다: h, m = map(int, t.split(':')); h * 60 + m.",
    "dict 두 개를 쓰세요: in_time[차량] = 들어온 시각(현재 주차 중인 차), total[차량] = 누적 분.",
    "OUT 이 나오면 total += 지금 - in_time 후 in_time 에서 삭제. 기록을 다 본 뒤 in_time 에 남은 차는 23:59(=1439분)에 나간 것으로 처리하세요.",
    "올림 나눗셈은 math.ceil(a / b) 또는 정수만 쓰는 -(-a // b). 결과는 sorted(total) 순서로 만드세요.",
]

TESTS = [
    {
        "input": [[120, 3000, 30, 500], ["07:00 1234 IN", "08:10 0500 IN", "09:30 1234 OUT", "11:00 1234 IN",
                                          "12:20 0500 OUT", "13:05 1234 OUT", "22:50 0042 IN"]],
        "output": [3000, 5500, 6000],
    },
    {"input": [[60, 1000, 10, 100], ["00:00 0001 IN"]], "output": [1000 + 138 * 100]},
    {"input": [[1, 0, 1, 1], ["23:59 9999 IN"]], "output": [0]},
    {"input": [[30, 2000, 15, 300], ["10:00 0007 IN", "10:30 0007 OUT"]], "output": [2000]},
    {"input": [[30, 2000, 15, 300], ["10:00 0007 IN", "10:31 0007 OUT"]], "output": [2300]},
    {
        "input": [[100, 1500, 20, 250], ["06:00 3333 IN", "06:40 3333 OUT", "07:00 3333 IN", "07:40 3333 OUT",
                                          "08:00 3333 IN", "08:21 3333 OUT"]],
        "output": [1500 + 1 * 250],
    },
    {
        "input": [[90, 4000, 12, 350], ["05:10 4821 IN", "06:00 0310 IN", "06:45 0310 OUT", "08:02 4821 OUT",
                                         "08:02 0077 IN", "18:30 0310 IN", "19:15 0077 OUT", "22:40 4821 IN",
                                         "23:05 4821 OUT"]],
        "output": [21150, 12400, 7150],
    },
    {
        "input": [[10, 100, 5, 7], ["01:00 2000 IN", "01:00 0100 IN", "02:00 0100 OUT", "02:00 2000 OUT",
                                     "03:00 0100 IN"]],
        "output": [1934, 170],
    },
]

EXPLANATION = """
핵심: 긴 지문을 '자료구조 결정 + 파싱 + 공식' 으로 정리하면 단순 구현 문제입니다.

조건 정리 (지문을 읽으며 메모할 것)
  - 시각 → 분: "HH:MM" → H*60 + M,  미출차 = 23:59 = 1439분
  - 요금은 '누적 시간' 기준 (입출차마다가 아니라 하루 합계)
  - 올림 ⌈a/b⌉
  - 출력 순서: 차량번호 오름차순 (4자리 문자열이라 문자열 정렬 = 숫자 정렬)

1. in_time = {}, total = defaultdict(int)
2. 각 기록: t, car, kind = rec.split()
   - IN  → in_time[car] = 분
   - OUT → total[car] += 분 - in_time.pop(car)
3. 남은 차: total[car] += 1439 - in_time[car]
4. 차량번호 정렬 후 요금 계산:
     base_time, base_fee, unit_time, unit_fee = fees
     fee = base_fee                                          (t ≤ base_time)
     fee = base_fee + ceil((t - base_time) / unit_time) * unit_fee   (그 외)

입출력 예 해설
  0042: 22:50 ~ 23:59 = 69분 → 3000
  0500: 250분 → 3000 + ⌈130/30⌉ × 500 = 3000 + 5 × 500 = 5500
  1234: 150 + 125 = 275분 → 3000 + ⌈155/30⌉ × 500 = 3000 + 6 × 500 = 6000

시간 O(R + C log C) (R = 기록 수, C = 차량 수), 공간 O(C)
실전 포인트:
- 요금을 입출차할 때마다 따로 계산하면 틀립니다. '누적 후 한 번' 계산.
- 23:59 에 IN 하고 끝난 차량은 0분 → 기본 요금. total 에 0 이라도 키가 있어야 결과에 포함됩니다 (defaultdict 에 += 0).
- 올림을 int(a / b) + 1 로 쓰면 나누어떨어질 때 1 이 더해지는 버그가 납니다. -(-a // b) 를 외우세요.
"""


def reference(fees, records):
    from collections import defaultdict
    base_time, base_fee, unit_time, unit_fee = fees

    def to_minutes(hhmm):
        h, m = map(int, hhmm.split(":"))
        return h * 60 + m

    in_time = {}  # 현재 주차 중인 차량 → 입차 시각(분)
    total = defaultdict(int)  # 차량 → 누적 주차 시간(분)
    for rec in records:
        t, car, kind = rec.split()
        if kind == "IN":
            in_time[car] = to_minutes(t)
        else:
            total[car] += to_minutes(t) - in_time.pop(car)
    for car, t in in_time.items():  # 출차 기록이 없으면 23:59 출차
        total[car] += 23 * 60 + 59 - t

    answer = []
    for car in sorted(total):  # 차량번호 오름차순
        minutes = total[car]
        fee = base_fee
        if minutes > base_time:
            fee += -(-(minutes - base_time) // unit_time) * unit_fee  # 올림 나눗셈
        answer.append(fee)
    return answer
