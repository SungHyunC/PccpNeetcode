# 미국 테크 기업 코딩 인터뷰 가이드

> 미국 빅테크(FAANG/MANGA 등) 코딩 인터뷰는 "정답 코드" 만큼 **생각을 말로 풀어내는 과정**을 평가합니다. PCCP 와 같은 알고리즘 실력 위에 커뮤니케이션을 얹는 연습을 합니다.

## 채용 과정에서 코딩이 나오는 단계

| 단계 | 형식 | 시간 | 이 저장소에서 연습 |
|---|---|---|---|
| OA (Online Assessment) | HackerRank·CodeSignal 등 자동 채점, 2~4문제 | 60~90분 | `python practice.py mock start --mode oa` |
| Phone / Virtual Screen | 공유 에디터(CoderPad 등)에서 면접관과 1~2문제 | 45~60분 | `python practice.py mock start --mode interview` |
| Onsite (Virtual Onsite) | 코딩 2~3라운드 + 시스템 디자인 + 행동(behavioral) | 라운드당 45분 | 같은 모드를 하루 2~3번 |

- 코딩 라운드는 보통 Medium 1~2문제입니다. NeetCode 150 수준을 안정적으로 풀면 대부분 대비됩니다.
- 실행 환경이 없을 수도 있습니다(화이트보드/구글 독스). **실행하지 않고도 손으로 테스트**하는 연습이 필요합니다.

## 45분 진행 순서 (UMPIRE)

```
 0 ─  5분  U  Understand   문제 다시 말하기, 질문하기 (입력 크기, 정렬 여부, 중복, 음수, 빈 입력)
 5 ─ 10분  M  Match        어떤 패턴인가? (해시, 투 포인터, BFS, DP ...)
10 ─ 15분  P  Plan         브루트포스 → 최적화 아이디어를 말로 설명, 복잡도 합의
15 ─ 35분  I  Implement    말하면서 코딩. 변수 이름은 의미 있게
35 ─ 40분  R  Review       예제로 손 디버깅 (dry run), 엣지 케이스
40 ─ 45분  E  Evaluate     시간/공간 복잡도, 개선 가능성, 후속 질문 대응
```

**코드를 쓰기 전에 면접관의 동의를 받으세요.** "Does this approach sound good before I start coding?"

## 평가 기준 (대부분 기업 공통)

1. **Problem Solving** — 최적 풀이에 도달했는가, 힌트를 잘 활용했는가
2. **Coding** — 깔끔하고 읽기 쉬운 코드, 적절한 자료구조, 버그 없음
3. **Communication** — 생각을 설명하고, 질문하고, 피드백에 반응했는가
4. **Verification** — 스스로 테스트하고 버그를 찾았는가

> 침묵이 가장 나쁩니다. 막혀도 "지금 무엇을 생각하고 있는지" 를 말하세요.

## 상황별 영어 표현

### 문제 확인 (Clarifying)
- "Just to make sure I understand, the input is ... and I need to return ..."
- "Can the array be empty? Can it contain negative numbers or duplicates?"
- "Is the input sorted?" / "What's the range of n?"
- "If there are multiple valid answers, can I return any of them?"
- "Should I optimize for time or for space?"

### 접근법 설명 (Planning)
- "The brute-force solution would be to ..., which takes O(n²) time."
- "We're doing repeated lookups, so a hash map can bring this down to O(n)."
- "This looks like a shortest path on an unweighted graph, so BFS is a natural fit."
- "I think this has optimal substructure, so let me define dp[i] as ..."

### 코딩 중 (Implementing)
- "I'll write a helper function for this to keep the main logic clean."
- "Let me handle the edge case where the input is empty first."
- "I'm initializing the pointers at both ends of the array."

### 검증 (Testing)
- "Let me walk through the example: when i is 0, ..."
- "Let me also try an edge case, like a single element."
- "I think there's an off-by-one error here; let me fix that."

### 막혔을 때 (Getting unstuck)
- "Let me think about this for a moment." (10~20초 침묵은 괜찮습니다)
- "I'm considering two options: ... Which direction would you like me to explore?"
- "Could I get a small hint?" (힌트를 요청하는 것 자체는 감점이 크지 않습니다)

### 마무리 (Complexity)
- "The time complexity is O(n log n) because of the sort, and space is O(n)."
- "If the input were too large for memory, I'd consider ..."

## PCCP 와 무엇이 다른가

| 항목 | PCCP | 미국 인터뷰 |
|---|---|---|
| 채점 | 자동 채점(정확성·효율성) | 사람 평가(+ 일부 자동) |
| 함수 이름 | `solution` | 문제마다 다름 (LeetCode 스타일 클래스 메서드) |
| 핵심 | 정답 + 시간 내 통과 | 사고 과정 + 의사소통 + 코드 품질 |
| 자주 나오는 것 | 구현·시뮬레이션 비중 큼 | 자료구조 설계(LRU Cache 등), 트리/그래프, 인터벌 |
| 엣지 케이스 | 테스트 케이스가 찾아 줌 | **본인이 먼저 말해야 함** |

## 자주 나오는 "설계형" 문제

클래스를 직접 구현하는 문제가 자주 나옵니다. 이 저장소에서는 명령어 리스트를 받는 형태로 바꿔 연습합니다.

- Min Stack (`05-stack/min-stack`)
- LRU Cache (`07-linked-list/lru-cache`)
- Implement Trie (`09-tries/implement-trie`)
- Find Median from Data Stream (`10-heap/find-median-from-data-stream`)

면접에서는 아래처럼 클래스로 작성하면 됩니다.

```python
class LRUCache:
    def __init__(self, capacity: int):
        ...
    def get(self, key: int) -> int:
        ...
    def put(self, key: int, value: int) -> None:
        ...
```

## 8주 인터뷰 플랜 (NeetCode 순서)

| 주차 | 주제 |
|---|---|
| 1 | 02 해시, 03 투 포인터, 04 슬라이딩 윈도우 |
| 2 | 05 스택, 06 이분 탐색, 07 연결 리스트 |
| 3 | 08 트리, 09 트라이 |
| 4 | 10 힙, 11 백트래킹 |
| 5 | 12 그래프, 13 고급 그래프 |
| 6 | 14 1차원 DP, 15 2차원 DP |
| 7 | 16 그리디, 17 구간, 18 수학·비트 |
| 8 | 모의 인터뷰 (`mock --mode interview`) 매일 1회 + 말하면서 풀기 녹음 |

**말하면서 풀기 연습법**: 휴대폰으로 녹음하며 문제를 풀고 다시 들어 보세요. 침묵 구간과 설명이 모호한 부분이 바로 보입니다.

## 행동 면접 한 줄 팁

코딩만큼 behavioral 라운드(예: Amazon Leadership Principles)도 중요합니다. STAR(Situation, Task, Action, Result) 형식으로 경험 5~6개를 영어로 준비하세요: 갈등 해결, 실패와 배운 점, 주도적으로 개선한 일, 마감 압박, 기술적 의사결정.
