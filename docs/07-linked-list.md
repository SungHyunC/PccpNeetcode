# 07. 연결 리스트 (Linked List)

> 노드를 `next` 포인터로 이어 붙인 자료구조. 문제의 대부분은 **포인터를 어떤 순서로 바꾸느냐**와 **경계(빈 리스트·첫 노드·마지막 노드) 처리**의 싸움입니다. 더미 노드(dummy), 빠른/느린 포인터(fast & slow), 뒤집기(reverse) 세 가지만 손에 익히면 대부분 풀립니다.

## 이런 문제에서 떠올리세요

- 입력이 `ListNode head` 로 주어진다 → 거의 항상 이 문서의 템플릿 조합
- "뒤집어라", "k 개씩 뒤집어라", "회문(palindrome)인지" → **뒤집기(reverse)**
- "가운데 노드", "끝에서 n 번째", "사이클이 있는가", "사이클 시작점" → **fast / slow 포인터**
- "두 정렬 리스트를 합쳐라", "정렬해라(Sort List)" → **더미 노드 + 병합(merge)**
- "k 개의 정렬된 리스트" → **최소 힙(heap)** 또는 분할 정복 (→ [10. 힙](10-heap.md))
- "O(1) 에 조회하면서 사용 순서도 O(1) 로 관리" (LRU 캐시) → **해시맵 + 이중 연결 리스트**
- "추가 공간 O(1) 로" 라는 조건 → 노드를 배열에 담는 풀이 대신 포인터 조작으로 풀어야 함
- 입력 크기: 노드 수 N ≤ 100,000 이면 O(N) 또는 O(N log N). 매번 끝까지 걸어가는 O(N²) 은 실패

> PCCP(프로그래머스)는 연결 리스트를 직접 주는 문제가 드뭅니다. 대신 **"표 편집"(이중 연결 리스트로 삭제/복구)** 처럼 배열 인덱스로 prev/next 를 흉내 내는 문제가 나옵니다. 미국 면접에서는 `ListNode` 를 직접 다루는 문제가 단골입니다.

## 핵심 개념

### 1) 노드와 포인터

```
head
 │
 ▼
[1|●]──▶[2|●]──▶[3|●]──▶ None
 val next
```

- 배열과 달리 **i 번째 원소에 바로 접근할 수 없습니다** (O(i)). 대신 노드를 알고 있다면 그 뒤에 삽입/삭제는 O(1).
- 파이썬 변수는 노드를 "가리키는 이름표"입니다. `cur = cur.next` 는 이름표를 옮길 뿐, 리스트를 바꾸지 않습니다. 리스트를 바꾸는 것은 `node.next = ...` 대입뿐입니다.

| 연산 | 배열(list) | 연결 리스트 |
|---|---|---|
| i 번째 접근 | O(1) | O(i) |
| 맨 앞 삽입/삭제 | O(n) | O(1) |
| 알고 있는 노드 뒤 삽입/삭제 | O(n) | O(1) |
| 탐색 | O(n) | O(n) |

### 2) 더미 노드 (dummy / sentinel)

결과 리스트를 새로 만들거나, head 자체가 지워질 수 있을 때 head 앞에 가짜 노드를 붙입니다.

```
dummy ──▶ 1 ──▶ 2 ──▶ 3          head 를 지워도: dummy ──▶ 2 ──▶ 3
  ▲                                              return dummy.next
 tail (여기 뒤에 계속 붙여 나감)
```

"첫 노드가 비었나?" 같은 `if` 가 사라져 버그가 크게 줄어듭니다.

### 3) 뒤집기 (reverse) — prev / cur / nxt

```
prev  cur   nxt
None   1 ──▶ 2 ──▶ 3
       │
① nxt = cur.next     (다음을 잃어버리지 않게 저장)
② cur.next = prev    None ◀── 1    2 ──▶ 3
③ prev, cur = cur, nxt                 한 칸 전진
...
None ◀── 1 ◀── 2 ◀── 3      cur = None, prev = 3 → 새 head
```

### 4) 빠른/느린 포인터 (fast & slow, 토끼와 거북이)

```
slow: 1칸,  fast: 2칸

1 ─▶ 2 ─▶ 3 ─▶ 4 ─▶ 5 ─▶ None
s/f
     s    f
          s         f       fast.next == None → slow = 3 (가운데)
```

- **가운데 찾기**: fast 가 끝에 닿을 때 slow 는 가운데
- **사이클 탐지**: 사이클이 있으면 fast 가 slow 를 따라잡아 같은 노드에서 만남 (Floyd)
- **끝에서 n 번째**: fast 를 n 칸 먼저 보낸 뒤 같은 속도로 함께 이동

```
사이클:  1 ─▶ 2 ─▶ 3 ─▶ 4
              ▲         │
              └─────────┘
  사이클에 들어간 뒤 매 단계 둘 사이 거리가 1씩 줄어듦 → 반드시 만남
```

### 5) 이중 연결 리스트 + 해시맵 (LRU 캐시)

```
map: {key: node}
[head] ⇄ (k1) ⇄ (k3) ⇄ (k2) ⇄ [tail]
 오래됨                        최근

get(k3): map 으로 노드 O(1) 탐색 → 떼어내기 O(1) → tail 앞에 붙이기 O(1)
용량 초과: head.next 를 떼어내고 map 에서도 삭제 (그래서 노드에 key 를 저장)
```

파이썬의 `collections.OrderedDict` 가 내부적으로 이 구조입니다 (`move_to_end`, `popitem(last=False)`).

## 코드 템플릿

### 템플릿 1. 뒤집기 (반복)

```python
def reverse(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next        # 1) 다음 저장
        cur.next = prev       # 2) 방향 뒤집기
        prev, cur = cur, nxt  # 3) 전진
    return prev               # 새 head
```

### 템플릿 2. 가운데 찾기 + 사이클 탐지

```python
def middle(head):
    # 길이가 짝수면 '뒤쪽 가운데'를 반환합니다. (앞쪽 가운데가 필요하면 fast = head.next 로 시작)
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:      # 값(==)이 아니라 객체(is) 비교
            return True
    return False
```

### 템플릿 3. 더미 노드로 병합

```python
def merge(a, b):
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b        # 남은 꼬리 통째로
    return dummy.next
```

### 템플릿 4. 끝에서 n 번째 (간격 유지 투 포인터)

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    slow = fast = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next   # slow 다음이 삭제 대상
    return dummy.next
```

## 시간 · 공간 복잡도

| 작업 | 시간 | 공간 | 비고 |
|---|---|---|---|
| 뒤집기 (반복) | O(n) | O(1) | 재귀 버전은 공간 O(n), 파이썬 재귀 한도 주의 |
| 가운데 찾기 / 사이클 탐지 | O(n) | O(1) | set 으로 방문 체크하면 공간 O(n) |
| 정렬 리스트 2개 병합 | O(n + m) | O(1) | 노드 재사용 |
| 정렬 리스트 k개 병합 (힙) | O(N log k) | O(k) | 순차 병합은 O(kN) |
| LRU get / put | O(1) | O(capacity) | dict + 이중 연결 리스트 |
| 노드를 배열에 담기 | O(n) | O(n) | 쉬운 대안. "O(1) 공간" 조건이 없으면 충분히 좋은 풀이 |

## 자주 하는 실수

- [ ] `cur.next = prev` 를 하기 **전에** `nxt = cur.next` 를 저장하지 않아 나머지 리스트를 잃어버림
- [ ] 빈 리스트(`head is None`)나 노드 1개일 때 `head.next.next` 에 접근해 `AttributeError`
- [ ] 리스트를 둘로 나눈 뒤 앞 절반의 끝을 `None` 으로 끊지 않아 **사이클**이 생김 (Reorder List)
- [ ] 사이클 판별에서 노드 **값**을 비교 (`slow.val == fast.val`) → 값이 중복되면 오답. 항상 `is`
- [ ] `while fast and fast.next` 대신 `while fast.next` 만 써서 fast 가 None 일 때 에러
- [ ] head 가 지워지는 경우(n == 길이)를 따로 처리하다 실수 → 더미 노드를 쓰세요
- [ ] `heapq` 에 `(val, node)` 를 넣었다가 값이 같을 때 `ListNode` 끼리 비교되어 `TypeError` → `(val, i, node)`
- [ ] Add Two Numbers 에서 마지막 올림(carry) 을 빠뜨림 → `while l1 or l2 or carry`
- [ ] LRU 에서 put 으로 **기존 key 를 갱신**할 때도 최근 사용으로 옮겨야 함
- [ ] 재귀 풀이를 그대로 제출 → 노드 수가 수천 이상이면 `RecursionError` (PCCP 에서 특히 주의)

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Reverse Linked List | Easy | prev / cur / nxt 로 화살표 뒤집기 | `python practice.py start reverse-linked-list` |
| 2 | Merge Two Sorted Lists | Easy | 더미 노드 + 작은 쪽 붙이기 | `python practice.py start merge-two-sorted-lists` |
| 3 | Linked List Cycle | Easy | Floyd 토끼와 거북이 | `python practice.py start linked-list-cycle` |
| 4 | Reorder List | Medium | 가운데 찾기 + 뒤 절반 뒤집기 + 번갈아 병합 | `python practice.py start reorder-list` |
| 5 | Remove Nth Node From End | Medium | n 칸 간격 두 포인터 + 더미 | `python practice.py start remove-nth-node-from-end` |
| 6 | Add Two Numbers | Medium | 자릿수 덧셈 + carry | `python practice.py start add-two-numbers` |
| 7 | LRU Cache | Medium | dict + 이중 연결 리스트 / OrderedDict | `python practice.py start lru-cache` |
| 8 | Merge K Sorted Lists | Hard | 크기 k 최소 힙, (val, i, node) | `python practice.py start merge-k-sorted-lists` |

## 더 풀어 볼 문제

- LeetCode 876 Middle of the Linked List — 가운데 찾기 기본
- LeetCode 234 Palindrome Linked List — 가운데 찾기 + 뒤집기 + 비교
- LeetCode 142 Linked List Cycle II — 사이클 시작점 (만난 뒤 한 포인터를 head 로)
- LeetCode 160 Intersection of Two Linked Lists — 두 포인터가 서로의 리스트로 갈아타기
- LeetCode 138 Copy List with Random Pointer — 해시맵(원본 → 복사본)
- LeetCode 287 Find the Duplicate Number — 배열을 연결 리스트로 보고 Floyd
- LeetCode 25 Reverse Nodes in k-Group (Hard) — 구간 뒤집기
- LeetCode 148 Sort List — 연결 리스트 병합 정렬
- 프로그래머스 Lv.3 표 편집 (2021 카카오 인턴) — 배열로 만든 이중 연결 리스트 + 삭제 스택
- 프로그래머스 Lv.2 캐시 (2018 카카오 블라인드) — LRU 시뮬레이션

## 영어로 설명하기 (미국 면접용)

- "I'll use a dummy head node so I don't have to special-case an empty result or removing the original head."
- "To reverse the list in place, I keep three pointers — prev, current, and next — and flip each next pointer as I walk forward. That's O(n) time and O(1) extra space."
- "I'll use the fast and slow pointer technique: the fast pointer moves two steps for every one step of the slow pointer, so when fast reaches the end, slow is at the middle — and if there's a cycle, they're guaranteed to meet."
- "For the LRU cache, a hash map gives me O(1) lookup, and a doubly linked list lets me move a node to the most-recent end or evict the least-recent one in O(1)."
- "To merge k sorted lists, I keep the current head of each list in a min-heap of size k, so each pop and push costs O(log k), giving O(N log k) overall."

## 체크리스트

- [ ] 반복문으로 리스트 뒤집기를 1분 안에 보지 않고 쓸 수 있다
- [ ] 더미 노드가 필요한 상황(새 리스트 만들기, head 삭제 가능)을 바로 알아본다
- [ ] fast/slow 로 가운데·사이클·끝에서 n번째를 각각 구현할 수 있다
- [ ] 짝수 길이에서 가운데가 앞쪽/뒤쪽 중 어디로 잡히는지 시작 조건별로 설명할 수 있다
- [ ] Reorder List 를 세 단계(가운데, 뒤집기, 병합)로 나눠 설명할 수 있다
- [ ] LRU 캐시를 OrderedDict 없이 dict + 이중 연결 리스트로 구현할 수 있다
- [ ] heapq 에 노드를 넣을 때 tie-breaker 가 왜 필요한지 설명할 수 있다
- [ ] 재귀 풀이의 공간 복잡도(O(n))와 파이썬 재귀 한도 문제를 언급할 수 있다
