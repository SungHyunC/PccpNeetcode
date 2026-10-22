TITLE = "Group Anagrams (애너그램 묶기)"
LEVEL = "Medium"
SOURCE = "LeetCode 49"
PATTERN = "정규화한 키로 그룹핑 (defaultdict(list))"

DESCRIPTION = """
문자열 배열 strs 가 주어집니다. 서로 애너그램인 문자열끼리 묶어서 그룹들의 리스트를 return 하세요.
그룹의 순서와 그룹 안 문자열의 순서는 상관없습니다.

제한사항
- 1 ≤ len(strs) ≤ 10,000
- 0 ≤ len(strs[i]) ≤ 100, 영어 소문자

입출력 예
["eat","tea","tan","ate","nat","bat"]  →  [["bat"],["nat","tan"],["ate","eat","tea"]]
[""]                                   →  [[""]]
"""

SIGNATURE = "def solution(strs: list[str]) -> list[list[str]]:"

HINTS = [
    "애너그램끼리는 '공통된 무언가' 가 있습니다. 그것을 dict 의 키로 쓰면?",
    "정렬된 문자열 ''.join(sorted(s)) 은 애너그램끼리 같습니다.",
    "defaultdict(list) 에 groups[key].append(s) 로 모은 뒤 list(groups.values()) 를 return.",
]

COMPARE = "unordered_nested"

TESTS = [
    {"input": [["eat", "tea", "tan", "ate", "nat", "bat"]], "output": [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]},
    {"input": [[""]], "output": [[""]]},
    {"input": [["a"]], "output": [["a"]]},
    {"input": [["", ""]], "output": [["", ""]]},
    {"input": [["abc", "bca", "cab", "xyz", "zyx", "q"]], "output": [["abc", "bca", "cab"], ["xyz", "zyx"], ["q"]]},
    {"input": [["ab", "ba", "aab", "aba"]], "output": [["ab", "ba"], ["aab", "aba"]]},
]

EXPLANATION = """
아이디어: 애너그램끼리 똑같아지는 "대표 키" 를 만들어 해시맵으로 묶습니다.

키 선택
- 정렬된 문자열: ''.join(sorted(s)) → 문자열 하나당 O(k log k)
- 글자 빈도 튜플: tuple(count[26]) → 문자열 하나당 O(k)

시간 O(n · k log k) (정렬 키), 공간 O(n · k)
면접 포인트: list 는 dict 키가 될 수 없으므로 tuple 로 바꿔야 한다는 점(해시 가능해야 함)을 언급하세요.
"""


def reference(strs):
    from collections import defaultdict
    groups = defaultdict(list)
    for s in strs:
        groups["".join(sorted(s))].append(s)
    return list(groups.values())


def alternative(strs):
    from collections import defaultdict
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord("a")] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())
