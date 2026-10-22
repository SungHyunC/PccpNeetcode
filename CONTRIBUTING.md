# 문제 · 문서 작성 규칙

새 문제나 개념 문서를 추가할 때 이 규칙을 따릅니다. 추가한 뒤에는 반드시 아래를 실행해 모범 풀이가 모든 테스트를 통과하는지 확인합니다.

```bash
python practice.py verify --topic 02-arrays-hashing -v
```

## 1. 문제 파일 형식

경로: `problems/<NN-topic>/<slug>.py` (slug 는 영어 소문자-하이픈, 저장소 전체에서 유일)

예시는 [`problems/02-arrays-hashing/two-sum.py`](problems/02-arrays-hashing/two-sum.py) 를 보세요.

| 이름 | 필수 | 설명 |
|---|---|---|
| `TITLE` | ✅ | `"English Title (한글 제목)"` |
| `LEVEL` | ✅ | `"Easy"` / `"Medium"` / `"Hard"` 중 하나 |
| `SOURCE` | ✅ | 원본 문제 번호 (`"LeetCode 1"`, `"프로그래머스 Lv.2 유형"`, `"PCCP 기출 유형"`) |
| `PATTERN` | ✅ | 핵심 패턴 한 줄 (한국어) |
| `DESCRIPTION` | ✅ | 한국어 문제 설명. 원문 복사 금지, 직접 다시 쓴 설명. `제한사항`, `입출력 예` 포함 |
| `SIGNATURE` | ✅ | 항상 `def solution(...)` (프로그래머스 스타일). 타입 힌트 포함 |
| `HINTS` | ✅ | 2~4개, 점점 구체적으로. 마지막 힌트는 거의 풀이 수준 |
| `TESTS` | ✅ | `[{"input": [인자1, 인자2, ...], "output": 기댓값}, ...]` — 최소 5개, 경계값(빈 입력, 원소 1개, 음수, 중복, 최댓값) 포함 |
| `reference` | ✅ | 모범 풀이 함수. `solution` 과 같은 인자. 깔끔하고 주석이 적당히 있는 "정석" 풀이 |
| `EXPLANATION` | ✅ | 한국어 해설: 핵심 아이디어 → 단계 → 시간/공간 복잡도 → 면접 포인트 |
| `brute_force` / `alternative` | 선택 | 다른 풀이 (verify 에서 정확성도 검증됨) |
| `COMPARE` | 선택 | `"exact"`(기본) / `"unordered"`(바깥 리스트 순서 무관) / `"unordered_nested"`(바깥·안쪽 모두 순서 무관) / `"float"` |
| `check(result, expected, *inputs)` | 선택 | 답이 여러 개 가능할 때 직접 검사 함수. `COMPARE` 보다 우선 |
| `perf_case()` + `PERF_LIMIT` | 선택 | 효율성 테스트. `{"input": [...], "output": None}` 을 반환하면 기댓값은 reference 로 계산. 비효율 풀이(보통 O(n²))는 실패하고 정석 풀이는 `PERF_LIMIT`(초) 안에 넉넉히 통과하도록 크기 설정 (reference 가 0.3초 이내 권장). `random` 은 채점기가 seed 를 고정함 |
| `IMPORTS` | 선택 | 풀이 파일 상단에 넣을 import 문 (예: `"from lib.structures import ListNode"`) |
| `prepare(*inputs)` | 선택 | 원본 입력 → 실제 인자 리스트로 변환 (예: `[1,2,3]` → `ListNode`). `TESTS` 의 input 은 항상 JSON 처럼 단순한 값으로 유지 |
| `present(result)` | 선택 | 반환값 → 비교 가능한 값으로 변환 (예: `ListNode` → 리스트) |

규칙:

- 함수는 항상 **값을 return** 합니다. (LeetCode 의 in-place 문제도 결과를 return 하도록 바꿔서 출제)
- `TESTS` 의 input/output 은 리스트·정수·문자열·bool·None 만 사용합니다 (웹 학습 허브로 JSON 내보내기를 하기 때문).
- 연결 리스트/트리 문제는 `lib/structures.py` 의 `ListNode`, `TreeNode`, `build_linked_list`, `linked_list_to_list`, `build_tree`, `tree_to_list`, `find_node` 를 사용합니다. `IMPORTS = "from lib.structures import TreeNode"` 처럼 풀이 파일에 import 를 넣어 줍니다. 문제 파일 자체에서도 `from lib.structures import ...` 로 import 하면 됩니다.
- 외부 패키지 금지. 표준 라이브러리(`collections`, `heapq`, `bisect`, `itertools`, `functools`, `math`)만 사용.
- 재귀가 깊어질 수 있으면 reference 에서 `sys.setrecursionlimit` 를 쓰거나 반복문으로 작성합니다.

## 2. 개념 문서 형식

경로: `docs/<NN-topic>.md`. 모든 문서는 같은 목차를 씁니다.

```markdown
# NN. 주제 (English Name)

> 한 줄 요약

## 이런 문제에서 떠올리세요
- 문제 문장에서 보이는 신호/키워드 → 이 패턴
- 입력 크기 힌트 (예: N ≤ 100,000 → O(N log N) 이하)

## 핵심 개념
설명 + ASCII 그림/표로 동작 과정 시각화

## 코드 템플릿
주석 달린 Python 템플릿 1~4개 (외워 둘 만한 형태)

## 시간 · 공간 복잡도
표

## 자주 하는 실수
- 체크리스트

## 연습 문제 (이 저장소)
| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Two Sum | Easy | 해시맵에 보수 저장 | `python practice.py start two-sum` |

## 더 풀어 볼 문제
- LeetCode / 프로그래머스 추천 문제 (번호 + 제목)

## 영어로 설명하기 (미국 면접용)
면접관에게 접근법을 설명할 때 쓸 수 있는 영어 문장 예시 3~5개

## 체크리스트
- [ ] 스스로 확인할 항목
```

## 3. 문체

- 한국어로 쓰되 알고리즘 용어는 영어를 병기합니다: 해시맵(hash map), 투 포인터(two pointers)
- 설명은 짧은 문장으로. "~입니다/~합니다" 체.
