# PccpNeetcode

**PCCP(프로그래머스 코딩전문역량인증)** 와 **미국 테크 기업 코딩 인터뷰**를 함께 준비하는 파이썬 학습 저장소입니다.
NeetCode 로드맵 순서로 개념 문서를 읽고, 로컬 채점기로 문제를 풀고, 웹 학습 허브에서 퀴즈·시각화·코드 퍼즐로 복습합니다.

```
인터랙티브 코스 (web/course.html)  →  개념 문서 (docs/)  →  로컬 채점기 (practice.py)  →  웹 학습 허브 (web/index.html)
 12장 스크롤 에세이 + 브라우저 실습       개념 + 템플릿 코드       정확성/효율성 채점          퀴즈 · 시각화 · 퍼즐 · 모의고사
```

## 빠른 시작

파이썬 3.9 이상만 있으면 됩니다. 설치할 패키지는 없습니다.

```bash
git clone https://github.com/SungHyunC/PccpNeetcode.git
cd PccpNeetcode

python practice.py list                 # 문제 목록
python practice.py start two-sum        # workspace/02-arrays-hashing/two-sum.py 생성
# ... 에디터로 풀이 작성 ...
python practice.py test two-sum         # 채점 (정확성 + 효율성)
python practice.py hint two-sum         # 힌트를 하나씩
python practice.py solution two-sum     # 모범 풀이 + 해설
```

채점 결과 예시:

```
▶ Two Sum (두 수의 합) 채점 (workspace/02-arrays-hashing/two-sum.py)
  정확성 테스트  1 〉 통과 (0.01ms)
  ...
  효율성 테스트  〉 실패 (3000.2ms) 시간 초과 (> 3.0s)

정확성 6/6 · 효율성 실패
```

## 채점기 명령어

| 명령어 | 설명 |
|---|---|
| `python practice.py list [--topic 12] [--level Medium]` | 문제 목록과 진행 상황 (✔ 해결 · … 진행중) |
| `python practice.py show <문제>` | 문제 설명 보기 |
| `python practice.py start <문제>` | `workspace/` 에 풀이 파일 만들기 |
| `python practice.py test <문제> [--file 경로]` | 채점. 실패한 케이스의 입력·기댓값·내 출력·print 출력을 보여 줌 |
| `python practice.py hint <문제> [--all]` | 힌트를 단계별로 공개 |
| `python practice.py solution <문제>` | 모범 풀이, 다른 풀이, 해설(복잡도·면접 포인트) |
| `python practice.py random [--topic ..] [--level ..]` | 안 푼 문제 랜덤 출제 |
| `python practice.py stats` | 주제별 진행률 |
| `python practice.py quiz [-n 10]` | 문제 설명만 보고 주제 맞히기 |
| `python practice.py mock start --mode pccp\|oa\|interview` | 모의고사 (PCCP 4문제 120분 · OA 3문제 90분 · 인터뷰 2문제 45분) |
| `python practice.py mock status` / `mock submit` | 남은 시간 / 제출 후 1000점 만점 채점 |

`<문제>` 에는 `list` 의 번호, slug(`two-sum`), slug 일부(`anagram`) 를 쓸 수 있습니다.

## 인터랙티브 코스: 모든 연산

`web/course.html` 을 브라우저로 열면 12장짜리 스크롤형 코스가 나옵니다.
"코드가 연산을 몇 번 하는가" 라는 질문 하나로 복잡도 → 해시 → 투 포인터 → 스택 → 이분 탐색 → 트리 → 힙 → BFS → 다익스트라 → DP → 구간 → 시뮬레이션까지 이어집니다.

- 장마다 직접 조작하는 그림 (복잡도 스크롤리텔링, 해시맵·단조 스택·힙·다익스트라 단계 재생, 숫자 맞히기 게임, 미로 BFS/DFS, 피보나치 호출 트리 등)
- 장마다 확인 퀴즈 1개와 **브라우저에서 바로 실행·채점하는 파이썬 실습** 1개 (Brython 사용, 인터넷 연결 필요)
- 왼쪽 목차에 장별 완료 표시, 진도는 브라우저에 저장

코스 원본은 `web/src/course.html`, `web/src/course.js` 이고, `python tools/export_web.py` 가 문제 데이터를 넣어 `web/course.html` 을 만듭니다.

## 웹 학습 허브

`web/index.html` 을 브라우저로 열면 됩니다 (서버 불필요, 진행 상황은 브라우저에 저장).

| 탭 | 하는 일 |
|---|---|
| 로드맵 | NeetCode 순서 + PCCP 구현 유형. 주제별 진행률, 문제 설명·힌트·모범 풀이 |
| 패턴 퀴즈 | 문제 설명만 보고 어떤 주제로 풀지 고르기. 자주 틀리는 주제 표시 |
| 복잡도 퀴즈 | 제한사항 N → 목표 복잡도, 코드 조각 → 시간 복잡도 |
| 코드 퍼즐 | 섞인 모범 풀이 줄을 올바른 순서로 쌓기 (Parsons problem) |
| 알고리즘 시각화 | 이분 탐색, 슬라이딩 윈도우, 격자 BFS vs DFS, LCS DP 표를 한 단계씩 |
| 템플릿 카드 | 24개 핵심 코드 템플릿 플래시카드 |
| 모의고사 | PCCP/OA/인터뷰 타이머, 인터뷰 모드는 UMPIRE 단계 표시 |

문제를 추가하거나 고친 뒤에는 `python tools/export_web.py` 로 웹 허브 데이터를 갱신합니다.

## 학습 순서

| 단계 | 문서 | 주제 |
|---|---|---|
| 준비 | [00](docs/00-python-for-coding-tests.md) · [01](docs/01-complexity.md) | 코테용 파이썬, 시간 복잡도와 입력 크기 |
| 기초 | [02](docs/02-arrays-hashing.md) · [19](docs/19-implementation.md) | 배열·해시, 구현·시뮬레이션 (PCCP 특화) |
| 1 | [03](docs/03-two-pointers.md) · [05](docs/05-stack.md) | 투 포인터, 스택 |
| 2 | [04](docs/04-sliding-window.md) · [06](docs/06-binary-search.md) · [07](docs/07-linked-list.md) | 슬라이딩 윈도우, 이분 탐색, 연결 리스트 |
| 3 | [08](docs/08-trees.md) | 트리 |
| 4 | [09](docs/09-tries.md) · [10](docs/10-heap.md) · [11](docs/11-backtracking.md) | 트라이, 힙, 백트래킹 |
| 5 | [12](docs/12-graphs.md) · [14](docs/14-dp-1d.md) | 그래프 BFS/DFS, 1차원 DP |
| 6 | [13](docs/13-advanced-graphs.md) · [15](docs/15-dp-2d.md) · [16](docs/16-greedy.md) · [17](docs/17-intervals.md) · [18](docs/18-math-bit.md) | 최단 경로·MST, 2차원 DP, 그리디, 구간, 수학·비트 |

- 시험별 전략: [PCCP 가이드](docs/pccp-guide.md) · [미국 인터뷰 가이드](docs/interview-guide.md)
- 주차별 계획: [STUDY_PLAN.md](STUDY_PLAN.md)

각 개념 문서는 같은 구성입니다: 이런 문제에서 떠올리세요 → 핵심 개념(그림) → 코드 템플릿 → 복잡도 → 자주 하는 실수 → 연습 문제 → 더 풀어 볼 문제 → 영어로 설명하기 → 체크리스트.

## 저장소 구조

```
docs/                  개념 문서 (주제별 + 시험 가이드)
problems/<주제>/       문제 정의: 설명, 힌트, 테스트, 모범 풀이, 해설
workspace/             내 풀이 (practice.py start 가 만듦)
lib/structures.py      ListNode, TreeNode 와 변환 헬퍼
practice.py            로컬 채점기
web/app.html           웹 학습 허브 원본 (데이터 내장)
web/index.html         웹 학습 허브 - 브라우저로 바로 여는 파일 (export 가 생성)
web/src/               인터랙티브 코스 원본 (course.html, course.js)
web/course.html        인터랙티브 코스 - 브라우저로 바로 여는 파일 (export 가 생성)
tools/export_web.py    문제 데이터를 웹 허브에 내장
STUDY_PLAN.md          4주 / 8주 / 12주 학습 계획
CONTRIBUTING.md        문제·문서 작성 규칙
```

## 문제 출처에 대하여

문제는 LeetCode·프로그래머스의 유명 문제와 **같은 유형**을 직접 다시 쓴 설명으로 담았습니다. 원문 문제를 함께 풀고 싶다면 각 문제의 `SOURCE` 와 문서의 "더 풀어 볼 문제" 목록을 참고하세요.
