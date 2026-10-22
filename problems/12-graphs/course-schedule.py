import random

TITLE = "Course Schedule (수강 계획)"
LEVEL = "Medium"
SOURCE = "LeetCode 207"
PATTERN = "위상 정렬(Kahn 알고리즘)로 사이클 판별"

DESCRIPTION = """
0 번부터 num_courses - 1 번까지의 과목이 있습니다.
prerequisites[i] = [a, b] 는 "과목 a 를 들으려면 과목 b 를 먼저 들어야 한다" 는 뜻입니다.
모든 과목을 수강할 수 있는 순서가 존재하면 True, 아니면 False 를 return 하세요.

제한사항
- 1 ≤ num_courses ≤ 100,000
- 0 ≤ len(prerequisites) ≤ 200,000
- 0 ≤ a, b < num_courses
- 같은 [a, b] 쌍이 여러 번 나올 수 있고, a == b 인 쌍(자기 자신이 선수 과목)도 있을 수 있습니다.

입출력 예
num_courses = 2, prerequisites = [[1, 0]]          →  True   (0 → 1 순서로 수강)
num_courses = 2, prerequisites = [[1, 0], [0, 1]]  →  False  (서로가 서로의 선수 과목: 사이클)
"""

SIGNATURE = "def solution(num_courses: int, prerequisites: list[list[int]]) -> bool:"

HINTS = [
    "과목을 정점, [a, b] 를 b → a 간선으로 보면 방향 그래프가 됩니다. 모든 과목을 들을 수 있다 ⇔ 그래프에 사이클이 없다 (DAG).",
    "진입 차수(in-degree) = 그 과목의 아직 안 들은 선수 과목 수. 진입 차수가 0 인 과목은 지금 바로 들을 수 있습니다.",
    "Kahn 알고리즘: 진입 차수 0 인 과목을 큐에 넣고, 하나 꺼낼 때마다 그 과목 다음 과목들의 진입 차수를 1 씩 줄여 0 이 되면 큐에 넣습니다. 꺼낸 과목 수가 num_courses 와 같으면 True.",
]

TESTS = [
    {"input": [2, [[1, 0]]], "output": True},
    {"input": [2, [[1, 0], [0, 1]]], "output": False},
    {"input": [1, []], "output": True},
    {"input": [3, []], "output": True},
    {"input": [1, [[0, 0]]], "output": False},
    {"input": [4, [[1, 0], [2, 1], [3, 2]]], "output": True},
    {"input": [4, [[1, 0], [2, 1], [3, 2], [1, 3]]], "output": False},
    {"input": [5, [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3]]], "output": True},
    {"input": [6, [[1, 0], [0, 1], [3, 2], [5, 4]]], "output": False},
    {"input": [3, [[1, 0], [1, 0], [2, 1]]], "output": True},
]

PERF_LIMIT = 1.0


def perf_case():
    # 정점 100,000 개, 간선 200,000 개의 큰 DAG (작은 번호 → 큰 번호 간선만 있어 사이클 없음)
    n = 100_000
    prereq = [[i + 1, i] for i in range(n - 1)]            # 긴 사슬: 재귀 DFS 라면 깊이 100,000
    for _ in range(100_001):
        a, b = random.randrange(n), random.randrange(n)
        if a != b:
            prereq.append([max(a, b), min(a, b)])
    random.shuffle(prereq)
    return {"input": [n, prereq], "output": True}


EXPLANATION = """
핵심: 선수 과목 관계 = 방향 그래프. 사이클이 없어야(DAG) 위상 정렬(topological sort)이 존재합니다.

prerequisites = [[1,0],[2,0],[3,1],[3,2],[4,3]]   →   간선 b → a

    0 ──▶ 1 ──▶ 3 ──▶ 4          in-degree: 0:0  1:1  2:1  3:2  4:1
    └───▶ 2 ──┘
큐: [0]        → 꺼냄 0, 1·2 의 차수 감소 → [1, 2]
큐: [1, 2]     → 꺼냄 1, 3 의 차수 2→1 / 꺼냄 2, 3 의 차수 1→0 → [3]
큐: [3]        → 꺼냄 3 → [4] → 꺼냄 4    처리 5개 == 과목 5개 → True

사이클이 있으면 사이클 위의 정점들은 진입 차수가 끝까지 0 이 되지 않아 큐에 들어가지 못합니다.

1. graph[b].append(a), indegree[a] += 1
2. 진입 차수 0 인 정점을 모두 큐에
3. 꺼낼 때마다 taken += 1, 이웃의 차수 감소 → 0 이 되면 큐에
4. taken == num_courses

시간 O(V + E), 공간 O(V + E)

면접 포인트
- 위상 정렬 두 가지: Kahn(BFS, 진입 차수) / DFS 3색 표시(0 미방문, 1 방문 중, 2 완료 — 방문 중인 정점을 다시 만나면 사이클).
- DFS 풀이(alternative)는 사슬이 길면 재귀 깊이가 V 까지 가므로 파이썬에서는 반복문으로 바꾸거나 Kahn 을 쓰세요.
  효율성 테스트에는 길이 100,000 짜리 사슬이 들어 있습니다.
- 수강 "순서" 를 반환하라는 Course Schedule II 는 큐에서 꺼낸 순서를 그대로 기록하면 됩니다.
- 진입 차수 0 인 정점을 매번 처음부터 찾아 헤매면 O(V^2) 입니다. 큐로 관리해야 O(V + E).
"""


def reference(num_courses, prerequisites):
    from collections import deque

    graph = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for a, b in prerequisites:
        graph[b].append(a)              # b 를 들어야 a 를 들을 수 있음: b → a
        indegree[a] += 1

    queue = deque(i for i in range(num_courses) if indegree[i] == 0)
    taken = 0
    while queue:
        course = queue.popleft()
        taken += 1
        for nxt in graph[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:      # 선수 과목을 모두 들었음
                queue.append(nxt)
    return taken == num_courses


def alternative(num_courses, prerequisites):
    # DFS 3색 표시로 사이클 찾기 (반복문 버전: 깊은 사슬에서도 안전)
    graph = [[] for _ in range(num_courses)]
    for a, b in prerequisites:
        graph[b].append(a)
    WHITE, GRAY, BLACK = 0, 1, 2        # 미방문 / 현재 경로 위 / 완료
    color = [WHITE] * num_courses
    for start in range(num_courses):
        if color[start] != WHITE:
            continue
        color[start] = GRAY
        stack = [(start, 0)]            # (정점, 다음에 볼 이웃 인덱스)
        while stack:
            node, i = stack[-1]
            if i < len(graph[node]):
                stack[-1] = (node, i + 1)
                nxt = graph[node][i]
                if color[nxt] == GRAY:
                    return False        # 현재 경로로 되돌아옴 → 사이클
                if color[nxt] == WHITE:
                    color[nxt] = GRAY
                    stack.append((nxt, 0))
            else:
                color[node] = BLACK
                stack.pop()
    return True
