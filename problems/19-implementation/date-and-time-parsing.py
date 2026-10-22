TITLE = "Date and Time Parsing (창고 보관 기한 확인)"
LEVEL = "Easy"
SOURCE = "PCCP 기출 유형 (프로그래머스 '개인정보 수집 유효기간' 유형)"
PATTERN = "날짜 문자열 → 하나의 정수(총 일수)로 변환해 비교"

DESCRIPTION = """
식품 물류 창고는 물건을 들여온 날(입고일)부터 품목 등급별 보관 기한까지만 보관할 수 있습니다.
이 회사의 달력은 단순화되어 있어 '모든 달은 정확히 28일', 1년은 12개월입니다.

오늘 날짜 today, 등급별 보관 기한 terms, 창고의 물건 목록 items 가 주어집니다.
- today : "YYYY.MM.DD" 형식
- terms : "등급 기한" 형식의 문자열 목록. 기한은 숫자 뒤에 단위가 붙습니다.
          'M' 은 개월(1개월 = 28일), 'D' 는 일입니다. 예: "A 6M", "F 15D"
- items : "YYYY.MM.DD 등급" 형식. 입고일과 그 물건의 등급입니다.

보관 기한이 6M 인 물건을 2023.05.10 에 입고했다면 2023.11.09 까지 보관할 수 있고,
2023.11.10 부터는 폐기 대상입니다. (입고일 + 기한 일수가 되는 날부터 폐기)
15D 인 물건을 2023.05.20 에 입고했다면 2023.06.06 까지 보관하고 2023.06.07 부터 폐기 대상입니다.

오늘 기준으로 폐기 대상인 물건의 번호(items 의 1부터 시작하는 순번)를 오름차순으로 return 하세요.
폐기 대상이 없으면 빈 리스트를 return 합니다.

제한사항
- 날짜의 연도는 2000 ~ 2030, 월은 01 ~ 12, 일은 01 ~ 28 입니다. 월·일은 항상 두 자리입니다.
- 1 ≤ len(terms) ≤ 26, 등급은 서로 다른 알파벳 대문자 한 글자
- 기한: 1M ~ 100M 또는 1D ~ 1000D
- 1 ≤ len(items) ≤ 100, 모든 물건의 등급은 terms 에 있습니다.
- 입고일은 오늘이거나 오늘보다 이전입니다.

입출력 예
today = "2024.03.10", terms = ["A 6M", "B 15D", "C 1M"],
items = ["2023.09.10 A", "2024.02.24 B", "2024.02.11 C", "2023.09.11 A"]
→ [1]
  1번: 2023.09.10 + 6개월 = 2024.03.10 부터 폐기 → 오늘 폐기 대상
  2번: 2024.02.24 + 15일 = 2024.03.11 부터 폐기 → 아직 보관 가능
  3번: 2024.02.11 + 1개월 = 2024.03.11 부터 폐기 → 보관 가능
  4번: 2023.09.11 + 6개월 = 2024.03.11 부터 폐기 → 보관 가능
"""

SIGNATURE = "def solution(today: str, terms: list[str], items: list[str]) -> list[int]:"

HINTS = [
    "날짜를 연·월·일로 따로 비교하면 받아올림 처리가 복잡해집니다. 날짜 하나를 '기준일로부터 며칠째인가' 정수 하나로 바꿔 보세요.",
    "모든 달이 28일이므로 일수 = 연 × 12 × 28 + (월 - 1) × 28 + (일 - 1). 파싱은 y, m, d = map(int, date.split('.')).",
    "기한은 dict 로: '6M' → 6 × 28 일, '15D' → 15 일. 폐기 조건은 오늘 일수 ≥ 입고 일수 + 기한 일수 입니다.",
]

TESTS = [
    {"input": ["2024.03.10", ["A 6M", "B 15D", "C 1M"], ["2023.09.10 A", "2024.02.24 B", "2024.02.11 C", "2023.09.11 A"]],
     "output": [1]},
    {"input": ["2025.01.01", ["Z 12M"], ["2024.01.01 Z", "2024.01.02 Z"]], "output": [1]},
    {"input": ["2024.01.02", ["B 10D"], ["2023.12.20 B", "2023.12.21 B"]], "output": [1]},
    {"input": ["2020.06.15", ["Q 1D"], ["2020.06.15 Q", "2020.06.14 Q"]], "output": [2]},
    {"input": ["2022.02.28", ["A 100M", "B 1000D"], ["2022.02.28 A", "2022.02.28 B"]], "output": []},
    {"input": ["2030.12.28", ["X 1M", "Y 30D"], ["2000.01.01 X", "2030.11.28 X", "2030.11.27 Y", "2030.11.26 Y"]],
     "output": [1, 2, 4]},
    {"input": ["2023.11.10", ["S 6M", "T 15D"], ["2023.05.10 S", "2023.05.11 S", "2023.05.20 T", "2023.10.27 T"]],
     "output": [1, 3]},
]

EXPLANATION = """
핵심: 날짜 비교는 '하나의 정수(총 일수)로 변환' 하면 덧셈 한 번, 비교 한 번으로 끝납니다.

  to_days("2023.09.10") = 2023 × 336 + (9 - 1) × 28 + (10 - 1)      (1년 = 12 × 28 = 336일)
  폐기일 = to_days(입고일) + 기한 일수
  폐기 대상 ⇔ to_days(today) ≥ 폐기일

1. period = {등급: 일수}  ("6M" → 6 × 28, "15D" → 15)
2. now = to_days(today)
3. 각 물건 i (1부터): date, grade = item.split()
   to_days(date) + period[grade] ≤ now 이면 answer 에 i 추가
4. return answer

  2023.12.20 + 10일:  20 + 10 = 30 > 28 → 다음 달 2일 → 2024.01.02 부터 폐기
  (정수로 바꾸면 이런 받아올림을 신경 쓸 필요가 없습니다)

시간 O(T + N), 공간 O(T)
실전 포인트:
- '~까지 보관 가능' 과 '~부터 폐기' 의 하루 차이(off-by-one)를 예제로 반드시 확인하세요.
- 날짜를 다시 문자열로 만들어야 하면 f"{y}.{m:02d}.{d:02d}" 또는 str(m).zfill(2).
  자릿수가 고정된 "YYYY.MM.DD" 문자열끼리는 문자열 비교(<)만으로도 날짜 순서가 맞습니다.
- 시각 "HH:MM" 도 같은 원리로 분 단위 정수로 바꿉니다: h * 60 + m.
- 실제 달력(월마다 일수가 다름)이 필요하면 datetime.date 와 timedelta 를 쓰세요.
"""


def reference(today, terms, items):
    def to_days(date):
        y, m, d = map(int, date.split("."))
        return y * 12 * 28 + (m - 1) * 28 + (d - 1)  # 모든 달 28일

    period = {}
    for term in terms:
        grade, length = term.split()
        amount, unit = int(length[:-1]), length[-1]
        period[grade] = amount * 28 if unit == "M" else amount

    now = to_days(today)
    answer = []
    for i, item in enumerate(items, 1):  # 번호는 1부터
        date, grade = item.split()
        if to_days(date) + period[grade] <= now:  # 폐기일이 오늘이거나 지났음
            answer.append(i)
    return answer


def alternative(today, terms, items):
    # 폐기 시작일을 "YYYY.MM.DD" 문자열로 되돌려 문자열 비교 (자릿수 고정이면 사전 순 = 날짜 순)
    period = {}
    for term in terms:
        grade, length = term.split()
        period[grade] = int(length[:-1]) * (28 if length.endswith("M") else 1)
    answer = []
    for i, item in enumerate(items, 1):
        date, grade = item.split()
        y, m, d = map(int, date.split("."))
        total = y * 336 + (m - 1) * 28 + (d - 1) + period[grade]
        y, rest = divmod(total, 336)
        m, d = divmod(rest, 28)
        expire = f"{y}.{m + 1:02d}.{d + 1:02d}"  # 0 채우기로 두 자리 맞춤
        if expire <= today:
            answer.append(i)
    return answer
