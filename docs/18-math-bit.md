# 18. 수학 · 비트 · 행렬 (Math, Bit Manipulation & Geometry)

> 외워 두면 바로 써먹는 도구 상자입니다. XOR 로 짝 지우기, `x & (x-1)`, 유클리드 호제법, 에라토스테네스의 체, `pow(a, b, m)`, `zip(*m[::-1])` 만 손에 익혀도 많은 문제가 한 줄로 끝납니다.

## 이런 문제에서 떠올리세요

- "한 번만 등장", "짝이 없는 원소", "빠진 수" → XOR (`a ^ a = 0`)
- "2진수로 나타냈을 때 1 의 개수", "2의 거듭제곱인가" → `x & (x - 1)`
- "n 개 중 일부를 고르는 모든 경우" 이고 n ≤ 20 → 비트마스크(bitmask)로 부분집합 열거 (2^20 ≈ 100만)
- "최대공약수 / 최소공배수 / 약분 / 주기" → 유클리드 호제법 `math.gcd`
- "N 이하의 소수", 소수 판별을 여러 번 → 에라토스테네스의 체 (N ≤ 10^7 정도까지)
- "답을 1,000,000,007 로 나눈 나머지" → 모듈러 연산, `pow(a, b, m)`, 모듈러 역원
- "x 의 n 제곱" 에서 n 이 매우 큼 → 빠른 거듭제곱 O(log n)
- "k 진수로 바꿔서 ~" → `int(s, k)`, 직접 나눗셈 변환
- "행렬을 회전 / 나선형 / 전치" → 좌표 공식 또는 `zip(*m)` 트릭
- "32비트 정수 범위를 넘으면 0" → 파이썬은 오버플로가 없으니 직접 범위 검사

## 핵심 개념

### 1) 비트 연산 표

| 연산 | 의미 | 예 (a = 1100₂ = 12, b = 1010₂ = 10) |
|---|---|---|
| `a & b` | AND: 둘 다 1 | `1000₂ = 8` |
| `a \| b` | OR: 하나라도 1 | `1110₂ = 14` |
| `a ^ b` | XOR: 서로 다르면 1 | `0110₂ = 6` |
| `~a` | NOT: `-a - 1` (파이썬) | `~12 = -13` |
| `a << k` | 왼쪽 시프트: `a * 2^k` | `12 << 2 = 48` |
| `a >> k` | 오른쪽 시프트: `a // 2^k` | `12 >> 2 = 3` |
| `x & 1` | 홀짝 / 맨 아래 비트 | `12 & 1 = 0` (짝수) |
| `(x >> k) & 1` | k 번째 비트 확인 | `(12 >> 2) & 1 = 1` |
| `x \| (1 << k)` | k 번째 비트 켜기 | |
| `x & ~(1 << k)` | k 번째 비트 끄기 | |
| `x ^ (1 << k)` | k 번째 비트 뒤집기 | |
| `x & (x - 1)` | 가장 낮은 1 비트 끄기 | `1100 → 1000` |
| `x & -x` | 가장 낮은 1 비트만 남기기 | `1100 → 0100` (펜윅 트리에서 사용) |
| `x & (x-1) == 0` | x 가 2의 거듭제곱? (x > 0) | `8 → True` |

```
x & (x - 1) 이 가장 낮은 1 을 지우는 이유

  x      = 1 0 1 1 0 0 0
  x - 1  = 1 0 1 0 1 1 1     ← 가장 낮은 1 이 0 으로, 그 아래 0 들이 1 로 바뀜
  x&(x-1)= 1 0 1 0 0 0 0     ← 위쪽은 그대로, 가장 낮은 1 만 사라짐

XOR 로 짝 지우기
  4 ^ 1 ^ 2 ^ 1 ^ 2 = 4 ^ (1^1) ^ (2^2) = 4 ^ 0 ^ 0 = 4
```

### 2) 비트마스크로 부분집합 표현

원소 n 개의 부분집합 하나 = 0 ~ 2^n - 1 사이의 정수 하나. i 번째 비트가 1 이면 i 번째 원소를 고른 것입니다.

```
items = [A, B, C]      mask   2진수   부분집합
                        0     000     {}
                        1     001     {A}
                        5     101     {A, C}
                        7     111     {A, B, C}
```

n ≤ 20 이면 2^n · n ≈ 2천만 번 연산 → 파이썬에서도 대략 가능. n ≤ 15 면 넉넉합니다. 외판원(TSP) 같은 비트마스크 DP 의 상태로도 씁니다.

### 3) 파이썬 정수의 특징 (C++/Java 와 다름)

- **오버플로가 없습니다.** 정수는 임의 정밀도(big int). `2**100` 도 정확합니다.
- 그래서 "32비트 범위를 넘으면 ~" 류의 문제는 `-2**31 <= x <= 2**31 - 1` 을 직접 검사해야 합니다.
- 음수는 "왼쪽으로 1 이 무한히 이어진" 2의 보수처럼 동작합니다. `bin(-5) == '-0b101'` 이지 32비트 표현이 아닙니다.
- 32비트 부호 없는 값으로 보고 싶으면 `x & 0xFFFFFFFF`. 다시 부호 있는 값으로: `x - (1 << 32) if x >= 1 << 31 else x`.
- 음수 나눗셈은 내림(floor): `-7 // 2 == -4`, `-7 % 2 == 1` (C/Java 는 `-3`, `-1`). 0 방향 버림이 필요하면 `int(a / b)` 또는 절댓값으로 계산 후 부호를 붙입니다.

### 4) 유클리드 호제법 (Euclidean algorithm)

`gcd(a, b) = gcd(b, a % b)`, `gcd(a, 0) = a`. 매 두 단계마다 수가 절반 이하로 줄어 O(log min(a, b)).

```
gcd(48, 18) → gcd(18, 12) → gcd(12, 6) → gcd(6, 0) = 6
lcm(48, 18) = 48 // 6 * 18 = 144
```

### 5) 에라토스테네스의 체 (sieve of Eratosthenes)

```
n = 30 미만의 소수
  2  3  ×  5  ×  7  ×  ×  ×  11 ×  13 ×  ×  ×  17 ×  19 ×  ×  ×  23 ×  ×  ×  ×  ×  29
  p=2: 4,6,8,... 지움   p=3: 9,15,21,27 지움 (3*3 부터)   p=5: 25 지움   p=6: 36 ≥ 30 종료
```

- p 의 배수는 `p*p` 부터 지웁니다(더 작은 배수는 이미 지워짐). p 는 `p*p < n` 까지만.
- O(n log log n). 파이썬에서는 `bytearray` + 슬라이스 대입이 매우 빠릅니다.
- 수 하나만 판별: `√k` 까지 나눠 보기 O(√k). k 가 크고(10^12) 개수가 적으면 이쪽.

### 6) 모듈러 연산 (modular arithmetic)

"답이 너무 크니 `1_000_000_007` 로 나눈 나머지를 return" 이 나오면:

- 덧셈·뺄셈·곱셈은 중간중간 `% MOD` 해도 결과가 같습니다: `(a + b) % m`, `(a * b) % m`, `(a - b) % m` (파이썬은 음수도 알아서 0 ~ m-1 로).
- **나눗셈은 안 됩니다.** 대신 모듈러 역원(modular inverse)을 곱합니다. m 이 소수면 `a^(m-2) mod m` (페르마 소정리).
- 파이썬 내장: `pow(a, b, m)` 은 빠른 거듭제곱 O(log b), `pow(a, -1, m)` 은 역원(3.8+).
- 파이썬은 오버플로가 없으니 마지막에 한 번만 `% MOD` 해도 맞지만, 수가 너무 커지면 느려지므로 DP 중간에 나눠 주는 것이 좋습니다.

```python
MOD = 10**9 + 7
pow(2, 10**18, MOD)           # 빠른 거듭제곱
inv3 = pow(3, -1, MOD)        # 3 의 역원 → (6 * inv3) % MOD == 2
nCr = fact[n] * pow(fact[r] * fact[n - r], -1, MOD) % MOD
```

### 7) 진법 변환 (base conversion)

| 하고 싶은 것 | 코드 |
|---|---|
| k 진수 문자열 → 10진수 | `int("1011", 2) == 11`, `int("ff", 16) == 255` (2 ≤ k ≤ 36) |
| 10진수 → 2/8/16진수 문자열 | `bin(11)[2:]`, `oct(8)[2:]`, `hex(255)[2:]`, `format(11, "b")`, `format(5, "08b")` (8자리 0 채움) |
| 10진수 → 임의 k 진수 | 아래 템플릿 (나머지를 모아 뒤집기) |

### 8) 행렬 회전 트릭

```
원본        시계 90°         반시계 90°       전치 (transpose)
1 2 3       7 4 1            3 6 9            1 4 7
4 5 6       8 5 2            2 5 8            2 5 8
7 8 9       9 6 3            1 4 7            3 6 9

시계 90°:   [list(r) for r in zip(*m[::-1])]       (r, c) → (c, n-1-r)
반시계 90°: [list(r) for r in zip(*m)][::-1]       (r, c) → (n-1-c, r)
180°:       [row[::-1] for row in m[::-1]]
전치:       [list(r) for r in zip(*m)]
```

`zip(*m)` 은 행렬의 "열" 들을 튜플로 돌려줍니다. 직사각형 행렬(rows × cols)에도 그대로 동작해 결과가 cols × rows 가 됩니다.

## 코드 템플릿

```python
# 1) 비트 기본기
def popcount(x):                 # 1 비트 개수 (3.10+ 에서는 x.bit_count())
    cnt = 0
    while x:
        x &= x - 1               # 가장 낮은 1 비트 제거
        cnt += 1
    return cnt

def subsets(items):              # 비트마스크로 모든 부분집합 열거
    n = len(items)
    for mask in range(1 << n):
        yield [items[i] for i in range(n) if mask >> i & 1]

def to_int32(x):                 # 파이썬 정수를 32비트 부호 있는 정수로 해석
    x &= 0xFFFFFFFF
    return x - (1 << 32) if x >= 1 << 31 else x
```

```python
# 2) 정수론: gcd / lcm / 소수 / 약수
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a // gcd(a, b) * b    # math.lcm (3.9+)

def sieve(n):                    # n 미만 소수 여부 (bytearray)
    is_prime = bytearray([1]) * n
    is_prime[0:2] = b"\x00\x00"[: min(n, 2)]
    p = 2
    while p * p < n:
        if is_prime[p]:
            is_prime[p * p :: p] = bytes(len(range(p * p, n, p)))
        p += 1
    return is_prime              # [i for i in range(n) if is_prime[i]] 로 목록화

def is_prime(k):                 # 수 하나 판별 O(√k)
    if k < 2:
        return False
    for d in range(2, math.isqrt(k) + 1):
        if k % d == 0:
            return False
    return True

def divisors(k):                 # 약수 목록 O(√k)
    small, large = [], []
    for d in range(1, math.isqrt(k) + 1):
        if k % d == 0:
            small.append(d)
            if d != k // d:
                large.append(k // d)
    return small + large[::-1]
```

```python
# 3) 빠른 거듭제곱 / 모듈러 / 진법
MOD = 10**9 + 7

def fast_pow(x, n, mod=None):    # pow(x, n, mod) 를 직접 구현
    result = 1
    while n:
        if n & 1:
            result = result * x if mod is None else result * x % mod
        x = x * x if mod is None else x * x % mod
        n >>= 1
    return result

def to_base(num, k):             # 10진수 → k 진수 문자열 (k ≤ 36)
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num == 0:
        return "0"
    out = []
    while num:
        num, r = divmod(num, k)
        out.append(digits[r])
    return "".join(reversed(out))
```

```python
# 4) 행렬 조작
def rotate_cw(m):        return [list(r) for r in zip(*m[::-1])]
def rotate_ccw(m):       return [list(r) for r in zip(*m)][::-1]
def transpose(m):        return [list(r) for r in zip(*m)]

def spiral(m):           # 네 경계 좁히기
    res = []
    top, bottom, left, right = 0, len(m) - 1, 0, len(m[0]) - 1
    while top <= bottom and left <= right:
        res += [m[top][c] for c in range(left, right + 1)]; top += 1
        res += [m[r][right] for r in range(top, bottom + 1)]; right -= 1
        if top <= bottom:
            res += [m[bottom][c] for c in range(right, left - 1, -1)]; bottom -= 1
        if left <= right:
            res += [m[r][left] for r in range(bottom, top - 1, -1)]; left += 1
    return res
```

## 시간 · 공간 복잡도

| 기법 | 시간 | 공간 |
|---|---|---|
| XOR 누적 | O(n) | O(1) |
| popcount (`x & (x-1)`) | O(1 의 개수) ≤ O(비트 수) | O(1) |
| 부분집합 열거 | O(2^n · n) | O(n) |
| 유클리드 호제법 | O(log min(a, b)) | O(1) |
| 에라토스테네스의 체 | O(n log log n) | O(n) |
| √k 소수 판별 / 약수 | O(√k) | O(1) |
| 빠른 거듭제곱 | O(log n) | O(1) |
| 행렬 회전 / 나선 / 0 채우기 | O(m · n) | O(1) ~ O(m · n) |

## 자주 하는 실수

- 연산자 우선순위: 파이썬은 `+ -` → `<< >>` → `&` → `^` → `|` → 비교 순으로 묶습니다. `1 << n - 1` 은 `1 << (n - 1)`, `x >> 1 + 1` 은 `x >> 2` 입니다. (C/Java 에서는 `x & 1 == 0` 이 `x & (1 == 0)` 이 되는 함정도 있음) **비트 연산에는 항상 괄호**를 치는 습관을 들이세요
- `~x` 를 "비트 반전된 양수" 로 기대함 → 파이썬에서는 `-x - 1`. 32비트 반전은 `x ^ 0xFFFFFFFF`
- "32비트 오버플로 시 0" 조건을 파이썬이라고 무시함
- 음수의 `//`, `%` 결과가 C/Java 와 다른 것을 잊음 (`-123 % 10 == 7`)
- 체를 `range(2, n)` 의 모든 p 에 대해 돌리거나, `p * 2` 부터 지워서 느려짐 (`p * p` 부터, `p * p < n` 까지)
- 소수 판별에서 0, 1 을 소수로 처리함
- lcm 을 `a * b // gcd` 로 쓰는 것은 파이썬에서는 괜찮지만, 다른 언어에서는 `a // gcd * b` 로 써야 오버플로를 피함
- 모듈러 문제에서 나눗셈을 그냥 `//` 로 함 → 역원을 곱해야 함
- 실수(float) 비교를 `==` 로 함 → `abs(a - b) < 1e-9`. 정확한 값이 필요하면 정수 연산이나 `fractions.Fraction`
- 행렬을 `[[0] * m] * n` 으로 만들어 모든 행이 같은 리스트를 공유하는 버그 → `[[0] * m for _ in range(n)]`
- 행렬을 제자리에서 바꾸는 중에 아직 읽지 않은 값을 덮어씀 (Set Matrix Zeroes 에서 즉시 0 으로 바꾸는 실수)

## 연습 문제 (이 저장소)

| # | 문제 | 난이도 | 핵심 아이디어 | 명령어 |
|---|---|---|---|---|
| 1 | Single Number | Easy | 전부 XOR → 짝은 사라짐 | `python practice.py start single-number` |
| 2 | Number of 1 Bits | Easy | `n &= n - 1` 반복 횟수 | `python practice.py start number-of-1-bits` |
| 3 | Counting Bits | Easy | `bits[i] = bits[i >> 1] + (i & 1)` | `python practice.py start counting-bits` |
| 4 | Missing Number | Easy | 가우스 합 공식 / 인덱스와 XOR | `python practice.py start missing-number` |
| 5 | GCD and LCM of Array | Easy | 유클리드 호제법, `lcm = a // g * b` | `python practice.py start gcd-lcm-of-array` |
| 6 | Reverse Integer | Medium | `% 10`, `// 10` + 32비트 범위 검사 | `python practice.py start reverse-integer` |
| 7 | Pow(x, n) | Medium | 지수를 반씩: O(log n) 거듭제곱 | `python practice.py start pow-x-n` |
| 8 | Count Primes | Medium | 에라토스테네스의 체 (`p*p` 부터) | `python practice.py start count-primes` |
| 9 | Rotate Image | Medium | 전치 + 행 뒤집기 / `zip(*m[::-1])` | `python practice.py start rotate-image` |
| 10 | Spiral Matrix | Medium | 네 경계 좁히기 / 방향 회전 | `python practice.py start spiral-matrix` |
| 11 | Set Matrix Zeroes | Medium | 표시와 수정 분리, 첫 행·열 재사용 | `python practice.py start set-matrix-zeroes` |

## 더 풀어 볼 문제

- LeetCode 137 Single Number II (비트 자리별 개수 mod 3)
- LeetCode 260 Single Number III (`x & -x` 로 그룹 나누기)
- LeetCode 190 Reverse Bits, LeetCode 371 Sum of Two Integers (32비트 마스킹 연습)
- LeetCode 78 Subsets (비트마스크 열거), LeetCode 1494 / 847 (비트마스크 DP)
- LeetCode 59 Spiral Matrix II, LeetCode 202 Happy Number, LeetCode 43 Multiply Strings
- LeetCode 149 Max Points on a Line (gcd 로 기울기 정규화)
- 프로그래머스 Lv.2 N개의 최소공배수, Lv.1 최대공약수와 최소공배수
- 프로그래머스 Lv.2 k진수에서 소수 개수 구하기 (진법 변환 + √k 판별)
- 프로그래머스 Lv.2 소수 찾기 (순열 + 체), Lv.2 n진수 게임
- 프로그래머스 Lv.3 자물쇠와 열쇠 (행렬 회전 4번), Lv.2 삼각 달팽이 (방향 시뮬레이션)
- 프로그래머스 Lv.2 2개 이하로 다른 비트 (`x & -x` / 비트 관찰)

## 영어로 설명하기 (미국 면접용)

- "XOR is commutative and `a ^ a = 0`, so if I XOR all the numbers together, every pair cancels out and only the single number remains — O(n) time and O(1) space."
- "`n & (n - 1)` clears the lowest set bit, so the loop runs exactly as many times as there are 1-bits."
- "Python integers don't overflow, so I'll explicitly check whether the result fits in the 32-bit signed range and return 0 otherwise."
- "Instead of multiplying x by itself n times, I'll use exponentiation by squaring, which processes one bit of the exponent per step — that's O(log n)."
- "To rotate the matrix in place, I'll transpose it and then reverse each row; both steps are simple swaps, so it's O(n²) time and O(1) extra space."

## 체크리스트

- [ ] 비트 연산 표(`&`, `|`, `^`, `~`, `<<`, `>>`, `x & (x-1)`, `x & -x`)를 예시와 함께 설명할 수 있다
- [ ] 비트마스크로 부분집합을 열거하고 i 번째 원소 포함 여부를 확인할 수 있다
- [ ] 파이썬 정수에는 오버플로가 없다는 점과 `0xFFFFFFFF` 마스킹 방법을 안다
- [ ] 유클리드 호제법을 3줄로 쓰고 lcm 을 gcd 로 구할 수 있다
- [ ] 에라토스테네스의 체를 `p*p` 부터 지우는 형태로 구현할 수 있다
- [ ] `pow(a, b, m)` 과 `pow(a, -1, m)` 의 의미를 알고, 모듈러에서 나눗셈 대신 역원을 쓴다
- [ ] `int(s, k)` / `format(x, "b")` / 직접 나눗셈으로 진법 변환을 할 수 있다
- [ ] `zip(*m[::-1])` 로 시계 방향 회전, `zip(*m)` 으로 전치를 바로 쓸 수 있다
