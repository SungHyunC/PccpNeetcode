# 학습 계획

목표에 맞는 플랜 하나를 고르세요. 모든 플랜은 같은 하루 루틴을 씁니다.

## 하루 루틴 (60~120분)

```
1. 개념 (15분)   docs/<주제>.md 읽기 → 코드 템플릿을 손으로 한 번 따라 쓰기
2. 퍼즐 (10분)   웹 학습 허브 → 코드 퍼즐 / 템플릿 카드로 템플릿 암기
3. 풀이 (40분+)  python practice.py start <문제> → 20분 고민 → 막히면 hint 하나씩
4. 채점          python practice.py test <문제>  (효율성 테스트까지 통과)
5. 복기 (10분)   python practice.py solution <문제> 로 모범 풀이와 비교,
                 "핵심 아이디어 한 줄" 을 풀이 파일 맨 위 주석에 적기
6. 말로 설명     (인터뷰 준비 시) 영어로 접근법을 1분 동안 말해 보기
```

**20분 규칙**: 20분 동안 아이디어가 전혀 없으면 힌트를 봅니다. 힌트를 보고 푼 문제는 3일 뒤, 7일 뒤에 다시 풉니다.

## 플랜 A — PCCP 4주 집중

| 주차 | 개념 문서 | 연습 | 목표 |
|---|---|---|---|
| 1 | [00 파이썬](docs/00-python-for-coding-tests.md), [01 복잡도](docs/01-complexity.md), [02 해시](docs/02-arrays-hashing.md), [05 스택](docs/05-stack.md), [19 구현](docs/19-implementation.md) | 이 저장소 해당 주제 + 프로그래머스 Lv.1 20문제 | 구현 문제를 실수 없이 |
| 2 | [12 BFS/DFS](docs/12-graphs.md), [06 이분 탐색](docs/06-binary-search.md), [10 힙](docs/10-heap.md), [16 그리디](docs/16-greedy.md) | 해당 주제 + Lv.2 15문제 | 격자 BFS 를 10분 안에 |
| 3 | [14 1차원 DP](docs/14-dp-1d.md), [15 2차원 DP](docs/15-dp-2d.md), [13 최단 경로](docs/13-advanced-graphs.md), [03](docs/03-two-pointers.md)·[04](docs/04-sliding-window.md) | 해당 주제 + Lv.2~3 15문제 | 점화식을 스스로 세우기 |
| 4 | [PCCP 가이드](docs/pccp-guide.md) 복습 | `python practice.py mock start --mode pccp` 주 3회 + 프로그래머스 PCCP 기출 | 120분 안에 600점 이상 |

## 플랜 B — 미국 테크 인터뷰 8주 (NeetCode 순서)

| 주차 | 주제 | 비고 |
|---|---|---|
| 1 | [02 해시](docs/02-arrays-hashing.md), [03 투 포인터](docs/03-two-pointers.md), [04 슬라이딩 윈도우](docs/04-sliding-window.md) | 매 문제 "영어로 설명하기" 섹션 소리 내어 읽기 |
| 2 | [05 스택](docs/05-stack.md), [06 이분 탐색](docs/06-binary-search.md), [07 연결 리스트](docs/07-linked-list.md) | LRU Cache 는 반드시 직접 구현 |
| 3 | [08 트리](docs/08-trees.md), [09 트라이](docs/09-tries.md) | 재귀/반복 두 가지로 |
| 4 | [10 힙](docs/10-heap.md), [11 백트래킹](docs/11-backtracking.md) | |
| 5 | [12 그래프](docs/12-graphs.md), [13 고급 그래프](docs/13-advanced-graphs.md) | |
| 6 | [14 1차원 DP](docs/14-dp-1d.md), [15 2차원 DP](docs/15-dp-2d.md) | top-down → bottom-up 변환 연습 |
| 7 | [16 그리디](docs/16-greedy.md), [17 구간](docs/17-intervals.md), [18 수학·비트](docs/18-math-bit.md) | |
| 8 | [인터뷰 가이드](docs/interview-guide.md) | `mock start --mode interview` 매일 1회, 녹음하며 풀기 |

## 플랜 C — 둘 다 (12주)

1. 1~4주: 플랜 A 의 1~3주 + 07·08 (기초 체력)
2. 5~10주: 플랜 B 의 2~7주 중 아직 안 한 주제
3. 11주: PCCP 응시 (모의고사 + 기출)
4. 12주~: 인터뷰 모의 면접 위주

## 진행 상황 확인

```bash
python practice.py stats         # 주제별 진행률 막대
python practice.py list          # ✔ 해결 / … 진행중 / · 미시도
python practice.py random        # 안 푼 문제 랜덤 출제
python practice.py quiz          # 패턴 맞히기 퀴즈 (터미널)
```

웹 학습 허브의 로드맵 체크 표시는 브라우저에 따로 저장됩니다 (터미널 진행 상황과는 별개).
