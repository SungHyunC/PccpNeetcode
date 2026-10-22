TITLE = "File Name Sort (파일명 자연 정렬)"
LEVEL = "Medium"
SOURCE = "PCCP 기출 유형 (프로그래머스 '파일명 정렬' 유형)"
PATTERN = "문자열을 (HEAD, NUMBER, TAIL) 로 파싱 → 튜플 정렬 키 + 안정 정렬"

DESCRIPTION = """
사진 관리 프로그램은 파일 이름을 사람이 보기 자연스러운 순서로 정렬하려고 합니다.
일반적인 사전 순 정렬로는 "img12.png" 가 "img2.png" 보다 앞에 오기 때문입니다.

파일 이름은 앞에서부터 세 부분으로 나뉩니다.
- HEAD   : 숫자가 아닌 문자로만 이루어진 앞부분. 최소 한 글자 이상입니다.
- NUMBER : HEAD 바로 뒤에 이어지는 숫자. 1 ~ 5 글자이며 앞에 0 이 붙을 수 있습니다("007").
           숫자가 5 글자보다 길게 이어지면 앞의 5 글자까지만 NUMBER 입니다.
- TAIL   : 나머지 전부. 숫자나 문자가 다시 나올 수 있고, 비어 있을 수도 있습니다.

정렬 규칙
1. HEAD 를 대소문자 구분 없이 사전 순으로 비교합니다. ("IMG" 와 "img" 는 같음)
2. HEAD 가 같으면 NUMBER 를 정수로 비교합니다. ("9" < "10" == "010")
3. HEAD 와 NUMBER 가 모두 같으면 원래 입력 순서를 유지합니다. (TAIL 은 비교하지 않음)

정렬된 파일 이름 목록을 return 하세요.

제한사항
- 1 ≤ len(files) ≤ 1,000
- 각 파일 이름의 길이는 1 이상 100 이하이며 영문 대소문자, 숫자, 공백(" "), 마침표("."), 빼기("-") 로만 이루어집니다.
- 모든 파일 이름은 숫자가 아닌 문자로 시작하고, 숫자를 적어도 하나 포함합니다.

입출력 예
files = ["img12.png", "img10.png", "IMG02.png", "img1.png"]
→ ["img1.png", "IMG02.png", "img10.png", "img12.png"]

files = ["Report 3 final.doc", "report-1.doc", "Report 3.doc", "report 03 v2.doc"]
→ ["Report 3 final.doc", "Report 3.doc", "report 03 v2.doc", "report-1.doc"]
  ("report " 와 "report-" 는 다른 HEAD 이며 공백(32) < 빼기(45). HEAD·NUMBER 가 같은 세 파일은 입력 순서 유지)
"""

SIGNATURE = "def solution(files: list[str]) -> list[str]:"

HINTS = [
    "파이썬의 sorted 는 안정 정렬(stable sort)입니다. 키가 같은 원소는 원래 순서가 유지되므로 3번 규칙은 공짜입니다.",
    "파일 이름 하나를 (head.lower(), int(number)) 튜플로 바꾸는 함수를 만들고 sorted(files, key=그 함수) 를 쓰세요.",
    "파싱: 인덱스 i 를 앞에서부터 옮기며 숫자가 아닌 동안 HEAD, 이어서 숫자이고 길이 5 미만인 동안 NUMBER. str.isdigit() 을 활용하세요.",
]

TESTS = [
    {"input": [["img12.png", "img10.png", "IMG02.png", "img1.png"]],
     "output": ["img1.png", "IMG02.png", "img10.png", "img12.png"]},
    {"input": [["Report 3 final.doc", "report-1.doc", "Report 3.doc", "report 03 v2.doc"]],
     "output": ["Report 3 final.doc", "Report 3.doc", "report 03 v2.doc", "report-1.doc"]},
    {"input": [["a1"]], "output": ["a1"]},
    {"input": [["B1", "a2", "A1", "b0"]], "output": ["A1", "a2", "b0", "B1"]},
    {"input": [["x0010y", "X10z", "x9", "x010"]], "output": ["x9", "x0010y", "X10z", "x010"]},
    {"input": [["log123456.txt", "log12345.txt", "log99999.txt", "log2.txt"]],
     "output": ["log2.txt", "log123456.txt", "log12345.txt", "log99999.txt"]},
    {"input": [["K-9 Thunder", "K-21", "T-50 Golden Eagle", "K-2 Black Panther", "KF-21"]],
     "output": ["K-2 Black Panther", "K-9 Thunder", "K-21", "KF-21", "T-50 Golden Eagle"]},
    {"input": [["photo.2", "photo 1", "photo-3", "Photo.1"]], "output": ["photo 1", "photo-3", "Photo.1", "photo.2"]},
    {"input": [["song00000.mp3", "song0.mp3", "SONG0001.mp3"]], "output": ["song00000.mp3", "song0.mp3", "SONG0001.mp3"]},
]

EXPLANATION = """
핵심: '복잡한 정렬 규칙' 은 각 원소를 비교 가능한 튜플 키로 바꾸면 끝납니다. 파이썬 정렬은 안정 정렬이라 동점 처리도 자동입니다.

  "IMG02.png" → HEAD "IMG", NUMBER "02", TAIL ".png" → 키 ("img", 2)
  "img10.png" → 키 ("img", 10)
  "log123456" → HEAD "log", NUMBER "12345"(5글자까지), TAIL "6" → 키 ("log", 12345)

1. split_key(name):
   i = 0; while 숫자가 아님: i += 1        → head = name[:i]
   j = i; while j < len and 숫자 and j - i < 5: j += 1 → number = name[i:j]
   return (head.lower(), int(number))
2. return sorted(files, key=split_key)

시간 O(N log N · L) (L = 파일 이름 길이), 공간 O(N)
실전 포인트:
- 비교 함수가 필요할 때는 functools.cmp_to_key(cmp) 를 쓰지만, 대부분 튜플 키가 더 짧고 빠릅니다.
- 정규식으로도 가능합니다: re.match(r"([^0-9]+)([0-9]{1,5})", name).groups()
- '안정 정렬' 이 보장되지 않는 언어(C++ sort)라면 원래 인덱스를 키의 마지막에 넣어야 합니다.
- NUMBER 5글자 제한, 대소문자 무시, 앞자리 0 은 문제에서 반드시 테스트하는 함정입니다.
"""


def reference(files):
    def split_key(name):
        i = 0
        while not name[i].isdigit():  # HEAD: 숫자가 아닌 앞부분
            i += 1
        j = i
        while j < len(name) and name[j].isdigit() and j - i < 5:  # NUMBER: 최대 5글자
            j += 1
        return (name[:i].lower(), int(name[i:j]))

    return sorted(files, key=split_key)  # 안정 정렬 → 동점은 입력 순서 유지


def alternative(files):
    # cmp_to_key 로 비교 함수를 직접 작성하는 방법 (sorted 는 비교 함수를 써도 안정 정렬)
    from functools import cmp_to_key

    def parse(name):
        i = 0
        while not name[i].isdigit():
            i += 1
        j = i
        while j < len(name) and name[j].isdigit() and j - i < 5:
            j += 1
        return name[:i].lower(), int(name[i:j])

    def compare(a, b):
        ha, na = parse(a)
        hb, nb = parse(b)
        if ha != hb:
            return -1 if ha < hb else 1
        if na != nb:
            return -1 if na < nb else 1
        return 0  # 같으면 0 → 원래 순서 유지

    return sorted(files, key=cmp_to_key(compare))
