# 해시 테이블의 충돌 해결 방식: Chaining

해시 테이블(Hash Table)은 `key`를 해시 함수에 넣어 배열의 인덱스로 바꾸고, 해당 위치에 값을 저장하는 자료구조다.

예를 들어 `"apple"`이라는 key가 있다면 해시 함수는 이 key를 숫자 인덱스로 변환한다. 그리고 해시 테이블은 그 인덱스 위치에 `"apple"`과 연결된 값을 저장한다.

문제는 서로 다른 key가 같은 인덱스로 변환될 수 있다는 점이다. 이것을 **해시 충돌(Hash Collision)** 이라고 한다.

Chaining은 이런 충돌을 해결하는 대표적인 방법이다. 각 인덱스에 데이터를 하나만 저장하는 대신, 각 칸을 리스트로 만들어 여러 데이터를 함께 저장한다.

```text
index 0 -> []
index 1 -> [("apple", 1000), ("orange", 2000)]
index 2 -> []
index 3 -> [("banana", 1500)]
index 4 -> []
```

위 예시에서 `"apple"`과 `"orange"`가 같은 인덱스 `1`로 해싱되었다고 하자. Chaining 방식에서는 둘 중 하나를 덮어쓰지 않고, 같은 bucket 리스트 안에 함께 저장한다.

## 1. Chaining 구현 수도 코드

Chaining 방식의 해시 테이블은 크게 다음 기능을 가진다.

- `put(key, value)`: 데이터를 저장하거나 기존 key의 값을 수정한다.
- `get(key)`: key에 해당하는 값을 조회한다.
- `delete(key)`: key에 해당하는 데이터를 삭제한다.
- `hash(key)`: key를 배열 인덱스로 변환한다.

수도 코드로 표현하면 다음과 같다.

```text
HashTable(size):
    table을 size만큼의 빈 리스트로 초기화한다

hash(key):
    total = 0

    key의 각 문자에 대해:
        문자의 숫자 값을 total에 더한다

    return total % size

put(key, value):
    index = hash(key)
    bucket = table[index]

    bucket 안에 같은 key가 있는지 확인한다

    같은 key가 있다면:
        기존 value를 새 value로 수정한다
        종료한다

    같은 key가 없다면:
        bucket에 (key, value)를 추가한다

get(key):
    index = hash(key)
    bucket = table[index]

    bucket 안에서 같은 key를 찾는다

    같은 key가 있다면:
        해당 value를 반환한다

    없다면:
        None을 반환한다

delete(key):
    index = hash(key)
    bucket = table[index]

    bucket 안에서 같은 key를 찾는다

    같은 key가 있다면:
        해당 데이터를 삭제한다
        True를 반환한다

    없다면:
        False를 반환한다
```

핵심은 `table[index]`가 단일 값이 아니라 **리스트(bucket)** 라는 점이다. 충돌이 발생하면 같은 bucket에 여러 `(key, value)` 쌍이 들어간다.

## 2. 파이썬 구현

아래 코드는 Chaining 방식으로 해시 충돌을 처리하는 간단한 해시 테이블 구현이다.

```python
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        total = 0

        for char in key:
            total += ord(char)

        return total % self.size

    def put(self, key, value):
        index = self._hash(key)
        bucket = self.table[index]

        for i, pair in enumerate(bucket):
            saved_key, saved_value = pair

            if saved_key == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))

    def get(self, key):
        index = self._hash(key)
        bucket = self.table[index]

        for saved_key, saved_value in bucket:
            if saved_key == key:
                return saved_value

        return None

    def delete(self, key):
        index = self._hash(key)
        bucket = self.table[index]

        for i, pair in enumerate(bucket):
            saved_key, saved_value = pair

            if saved_key == key:
                del bucket[i]
                return True

        return False

    def show(self):
        for index, bucket in enumerate(self.table):
            print(index, bucket)
```

사용 예시는 다음과 같다.

```python
hash_table = HashTable(5)

hash_table.put("apple", 1000)
hash_table.put("banana", 1500)
hash_table.put("orange", 2000)

print(hash_table.get("apple"))
print(hash_table.get("banana"))

hash_table.put("apple", 1200)
print(hash_table.get("apple"))

hash_table.delete("banana")
print(hash_table.get("banana"))

hash_table.show()
```

출력 결과는 다음과 같다.

```text
1000
1500
1200
None
0 [('apple', 1200)]
1 [('orange', 2000)]
2 []
3 []
4 []
```

출력 결과를 순서대로 보면 다음과 같다.

- `1000`: `"apple"`에 처음 저장한 값
- `1500`: `"banana"`에 저장한 값
- `1200`: `"apple"`의 값을 수정한 뒤 다시 조회한 값
- `None`: `"banana"`를 삭제한 뒤 조회했기 때문에 값이 없음
- 마지막 5줄: 현재 해시 테이블의 전체 bucket 상태

## 3. 각 함수 설명

### `__init__(self, size)`

```python
def __init__(self, size):
    self.size = size
    self.table = [[] for _ in range(size)]
```

해시 테이블을 초기화하는 생성자다.

`size`는 해시 테이블의 전체 칸 개수를 의미한다.

```python
hash_table = HashTable(5)
```

위 코드처럼 생성하면 내부 테이블은 다음과 같은 형태로 만들어진다.

```python
[
    [],
    [],
    [],
    [],
    []
]
```

각 칸을 빈 리스트로 만드는 이유는 충돌을 처리하기 위해서다. 만약 여러 key가 같은 인덱스로 해싱되면, 해당 인덱스의 리스트 안에 여러 데이터를 저장한다.

### `_hash(self, key)`

```python
def _hash(self, key):
    total = 0

    for char in key:
        total += ord(char)

    return total % self.size
```

`key`를 배열 인덱스로 변환하는 함수다.

이 예제에서는 문자열의 각 문자를 `ord()`로 숫자 값으로 바꾼 뒤 모두 더한다. 그리고 그 값을 테이블 크기로 나눈 나머지를 인덱스로 사용한다.

예를 들어 `"apple"`은 다음과 같이 계산된다.

```text
ord("a") + ord("p") + ord("p") + ord("l") + ord("e")
= 97 + 112 + 112 + 108 + 101
= 530
```

테이블 크기가 `5`라면 최종 인덱스는 다음과 같다.

```text
530 % 5 = 0
```

따라서 `"apple"`은 `0`번 인덱스에 저장된다.

### `put(self, key, value)`

```python
def put(self, key, value):
    index = self._hash(key)
    bucket = self.table[index]

    for i, pair in enumerate(bucket):
        saved_key, saved_value = pair

        if saved_key == key:
            bucket[i] = (key, value)
            return

    bucket.append((key, value))
```

`key-value` 데이터를 저장하는 함수다.

먼저 `_hash(key)`를 통해 key가 저장될 인덱스를 구한다. 그 다음 해당 인덱스의 bucket을 가져온다.

```python
index = self._hash(key)
bucket = self.table[index]
```

그 후 bucket 안에 이미 같은 key가 있는지 확인한다.

```python
for i, pair in enumerate(bucket):
    saved_key, saved_value = pair
```

같은 key가 있으면 기존 데이터를 새 값으로 교체한다.

```python
if saved_key == key:
    bucket[i] = (key, value)
    return
```

이 처리 덕분에 같은 key를 여러 번 저장해도 중복 데이터가 생기지 않는다.

```python
hash_table.put("apple", 1000)
hash_table.put("apple", 1200)
```

위 코드에서는 `"apple"` 데이터가 두 개 생기는 것이 아니라, 기존 값이 `1000`에서 `1200`으로 수정된다.

같은 key가 없다면 bucket에 새 데이터를 추가한다.

```python
bucket.append((key, value))
```

### `get(self, key)`

```python
def get(self, key):
    index = self._hash(key)
    bucket = self.table[index]

    for saved_key, saved_value in bucket:
        if saved_key == key:
            return saved_value

    return None
```

key에 해당하는 value를 조회하는 함수다.

먼저 key를 해싱해서 해당 key가 들어 있을 가능성이 있는 bucket을 찾는다.

```python
index = self._hash(key)
bucket = self.table[index]
```

그 다음 bucket 안의 데이터를 하나씩 확인한다.

```python
for saved_key, saved_value in bucket:
    if saved_key == key:
        return saved_value
```

같은 key를 찾으면 해당 value를 반환한다. 찾지 못하면 `None`을 반환한다.

### `delete(self, key)`

```python
def delete(self, key):
    index = self._hash(key)
    bucket = self.table[index]

    for i, pair in enumerate(bucket):
        saved_key, saved_value = pair

        if saved_key == key:
            del bucket[i]
            return True

    return False
```

key에 해당하는 데이터를 삭제하는 함수다.

조회와 마찬가지로 먼저 key를 해싱해서 bucket을 찾는다. 그리고 bucket 안에서 같은 key를 가진 데이터를 찾는다.

같은 key를 찾으면 해당 요소를 삭제한다.

```python
del bucket[i]
return True
```

삭제에 성공하면 `True`를 반환한다. key가 존재하지 않으면 삭제할 데이터가 없으므로 `False`를 반환한다.

### `show(self)`

```python
def show(self):
    for index, bucket in enumerate(self.table):
        print(index, bucket)
```

현재 해시 테이블의 전체 상태를 출력하는 함수다.

각 인덱스에 어떤 bucket이 들어 있는지 확인할 수 있기 때문에, 충돌이 어떻게 처리되는지 관찰할 때 유용하다.

## 4. 해시 충돌 예제

이제 실제로 충돌이 발생하는 예제를 살펴보자.

현재 해시 함수는 각 문자의 ASCII 값을 더한 뒤 테이블 크기로 나눈 나머지를 사용한다.

```python
def _hash(self, key):
    total = 0

    for char in key:
        total += ord(char)

    return total % self.size
```

테이블 크기를 `5`로 두었을 때 `"apple"`과 `"orange"`의 해시 값을 계산해보자.

```text
"apple"
97 + 112 + 112 + 108 + 101 = 530
530 % 5 = 0

"orange"
111 + 114 + 97 + 110 + 103 + 101 = 636
636 % 5 = 1
```

이 둘은 서로 다른 인덱스로 저장된다.

충돌을 더 쉽게 보기 위해 `"ab"`와 `"ba"`를 사용해보자.

```text
"ab"
ord("a") + ord("b")
= 97 + 98
= 195
195 % 5 = 0

"ba"
ord("b") + ord("a")
= 98 + 97
= 195
195 % 5 = 0
```

`"ab"`와 `"ba"`는 서로 다른 key지만, 문자들의 합이 같기 때문에 같은 인덱스 `0`으로 해싱된다.

다음 코드를 실행해보자.

```python
hash_table = HashTable(5)

hash_table.put("ab", "first")
hash_table.put("ba", "second")

hash_table.show()
```

출력 결과는 다음과 같다.

```text
0 [('ab', 'first'), ('ba', 'second')]
1 []
2 []
3 []
4 []
```

`"ab"`와 `"ba"`가 같은 인덱스 `0`에 저장되었지만, 하나가 다른 하나를 덮어쓰지 않았다. 두 데이터가 같은 bucket 리스트 안에 함께 들어가 있다.

이것이 Chaining의 핵심이다.

## 5. Chaining의 장점과 주의할 점

Chaining의 장점은 구현이 비교적 단순하고, 충돌이 발생해도 데이터를 잃지 않는다는 점이다.

하지만 모든 데이터가 하나의 bucket에 몰리면 조회 성능이 나빠질 수 있다. 해시 테이블의 평균 조회 시간은 보통 `O(1)`에 가깝지만, 특정 bucket에 데이터가 많이 몰리면 해당 bucket 안에서 순차 탐색을 해야 한다.

최악의 경우 하나의 bucket에 모든 데이터가 들어갈 수 있고, 이때 조회 시간은 `O(n)`이 된다.

따라서 좋은 해시 테이블을 만들려면 다음 요소가 중요하다.

- key를 고르게 분산시키는 해시 함수
- 적절한 테이블 크기
- 데이터가 많아졌을 때 테이블 크기를 늘리는 리사이징 전략

이 예제는 학습을 위한 단순한 구현이므로 리사이징은 포함하지 않았다. 실제 언어의 내장 해시 테이블, 예를 들어 파이썬의 `dict`는 훨씬 더 정교한 방식으로 충돌과 성능 문제를 처리한다.

## 정리

Chaining은 해시 테이블에서 충돌이 발생했을 때, 같은 인덱스의 bucket에 여러 데이터를 리스트 형태로 저장하는 방식이다.

이 방식에서는 같은 인덱스로 해싱된 key들이 하나의 리스트 안에 함께 저장된다. 데이터를 조회하거나 삭제할 때는 먼저 해시 함수를 통해 bucket을 찾고, 그 bucket 안에서 실제 key가 일치하는 데이터를 찾는다.

즉, Chaining 방식의 해시 테이블은 다음 흐름으로 동작한다.

```text
key 입력
-> 해시 함수로 인덱스 계산
-> 해당 인덱스의 bucket 접근
-> bucket 안에서 실제 key 비교
-> 저장, 조회, 수정, 삭제 수행
```

해시 충돌은 피할 수 없는 경우가 많다. 중요한 것은 충돌이 발생했을 때 데이터를 안전하게 보관하고, 가능한 한 빠르게 찾을 수 있도록 구조를 설계하는 것이다. Chaining은 그 문제를 직관적이고 이해하기 쉬운 방식으로 해결한다.