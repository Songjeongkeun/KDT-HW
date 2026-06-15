# 해시 테이블의 충돌 해결 방식 : Open Addressing (Linear Probing)

   

해시 테이블(Hash Table)은 `key`를 해시 함수에 넣어 배열의 인덱스로 바꾸고, 해당 위치에 값을 저장하는 자료구조다.

예를 들어 `"apple"`이라는 key가 있다면 해시 함수는 이 key를 숫자 인덱스로 변환한다. 해시 테이블은 계산된 인덱스에 `"apple"`과 연결된 값을 저장한다.

```text
"apple" -> 해시 함수 -> index 0 -> ("apple", 1000) 저장
```

문제는 서로 다른 key가 같은 인덱스로 변환될 수 있다는 점이다. 이것을 **해시 충돌(Hash Collision)** 이라고 한다.

```text
"ab" -> index 0
"ba" -> index 0
```

Chaining은 같은 인덱스에 리스트를 만들어 여러 데이터를 저장한다.  
Open Addressing은 리스트를 추가로 만들지 않고, 충돌이 발생하면 **해시 테이블 안의 다른 빈 칸**을 찾아 데이터를 저장한다.

Linear Probing은 Open Addressing의 가장 기본적인 방법이다. 충돌이 발생하면 바로 다음 칸부터 차례대로 확인한다.

```text
index 0 -> ("ab", "first")
index 1 -> ("ba", "second")  # index 0에서 충돌한 뒤 이동
index 2 -> None
index 3 -> None
index 4 -> None
```

---

## 1. Linear Probing 구현 수도 코드

Linear Probing 방식의 해시 테이블은 다음 기능을 가진다.

- `put(key, value)`: 데이터를 저장하거나 기존 key의 값을 수정한다.
- `get(key)`: key에 해당하는 값을 조회한다.
- `delete(key)`: key에 해당하는 데이터를 삭제한다.
- `hash_function(key)`: key를 배열 인덱스로 변환한다.
- `show()`: 해시 테이블의 전체 상태를 출력한다.

수도 코드로 표현하면 다음과 같다.

```text
HashTable(size):
    table을 size만큼 None으로 초기화한다.
    삭제된 칸을 표시할 DELETED 객체를 준비한다.

hash_function(key):
    total = 0

    key의 각 문자에 대해:
        문자의 숫자 값을 total에 더한다.

    return total % size

put(key, value):
    시작 인덱스 = hash_function(key)
    처음 발견한 삭제 위치 = 없음

    테이블 크기만큼 반복한다.

        현재 칸이 DELETED라면:
            처음 발견한 삭제 위치를 기억한다.

        현재 칸이 None이라면:
            기억해둔 삭제 위치가 있으면 그곳에 저장한다.
            없다면 현재 칸에 저장한다.
            True를 반환한다.

        현재 칸의 key가 입력 key와 같다면:
            기존 value를 새 value로 수정한다.
            True를 반환한다.

        다음 인덱스로 이동한다.

    삭제 위치가 있었다면 그곳에 저장한다.
    빈 위치가 없다면 False를 반환한다.

get(key):
    시작 인덱스 = hash_function(key)

    테이블 크기만큼 반복한다.

        현재 칸이 None이라면:
            None을 반환한다.

        현재 칸이 DELETED라면:
            다음 칸을 확인한다.

        현재 칸의 key가 입력 key와 같다면:
            value를 반환한다.

        다음 인덱스로 이동한다.

    None을 반환한다.

delete(key):
    시작 인덱스 = hash_function(key)

    테이블 크기만큼 반복한다.

        현재 칸이 None이라면:
            False를 반환한다.

        현재 칸의 key가 입력 key와 같다면:
            현재 칸을 DELETED로 바꾼다.
            True를 반환한다.

        다음 인덱스로 이동한다.

    False를 반환한다.
```

핵심은 충돌이 발생했을 때 다음 인덱스를 계산하는 부분이다.

```python
index = (index + 1) % self.size
```

`% self.size`를 사용하기 때문에 마지막 인덱스에 도착하면 다시 `0`번 인덱스로 돌아간다.

---

## 2. 파이썬 구현

아래 코드는 Open Addressing의 Linear Probing 방식으로 해시 충돌을 처리하는 간단한 해시 테이블 구현이다.

```python
class HashTable:
    # 삭제된 칸임을 나타내는 특별한 객체다.
    DELETED = object()

    def __init__(self, size):
        self.size = size
        self.table = [None for _ in range(size)]

    def hash_function(self, key):
        total = 0

        for char in key:
            total += ord(char)

        return total % self.size

    def put(self, key, value):
        index = self.hash_function(key)
        first_deleted_index = None

        for _ in range(self.size):
            item = self.table[index]

            # 삭제된 칸은 재사용할 수 있도록 위치를 기억한다.
            if item is self.DELETED:
                if first_deleted_index is None:
                    first_deleted_index = index

            # 비어 있는 칸을 만나면 데이터를 저장한다.
            elif item is None:
                target_index = (
                    first_deleted_index
                    if first_deleted_index is not None
                    else index
                )
                self.table[target_index] = (key, value)
                return True

            # 같은 key가 이미 존재하면 value만 수정한다.
            else:
                saved_key, saved_value = item

                if saved_key == key:
                    self.table[index] = (key, value)
                    return True

            # 충돌이 발생하면 다음 칸으로 이동한다.
            index = (index + 1) % self.size

        # None은 없지만 삭제된 칸이 있다면 그 위치를 재사용한다.
        if first_deleted_index is not None:
            self.table[first_deleted_index] = (key, value)
            return True

        print("해시 테이블이 가득 찼다.")
        return False

    def get(self, key):
        index = self.hash_function(key)

        for _ in range(self.size):
            item = self.table[index]

            # 한 번도 사용하지 않은 칸을 만나면 탐색을 종료한다.
            if item is None:
                return None

            # 삭제된 칸은 건너뛰고 다음 칸을 확인한다.
            if item is not self.DELETED:
                saved_key, saved_value = item

                if saved_key == key:
                    return saved_value

            index = (index + 1) % self.size

        return None

    def delete(self, key):
        index = self.hash_function(key)

        for _ in range(self.size):
            item = self.table[index]

            if item is None:
                return False

            if item is not self.DELETED:
                saved_key, saved_value = item

                if saved_key == key:
                    self.table[index] = self.DELETED
                    return True

            index = (index + 1) % self.size

        return False

    def show(self):
        for index, item in enumerate(self.table):
            if item is self.DELETED:
                print(index, "DELETED")
            else:
                print(index, item)
```

---

## 3. 실행 예시

```python
hash_table = HashTable(5)

hash_table.put("apple", 1000)
hash_table.put("melon", 3000)
hash_table.put("grape", 2500)

print(hash_table.get("apple"))
print(hash_table.get("melon"))

hash_table.put("apple", 1200)
print(hash_table.get("apple"))

hash_table.delete("melon")
print(hash_table.get("melon"))

hash_table.show()
```

출력 결과:

```text
1000
3000
1200
None
0 ('apple', 1200)
1 None
2 ('grape', 2500)
3 None
4 DELETED
```

각 key의 처음 해시 인덱스는 다음과 같다.

```text
"apple"
530 % 5 = 0

"melon"
539 % 5 = 4

"grape"
527 % 5 = 2
```

`"melon"`을 삭제한 뒤에는 해당 위치가 `None`이 아니라 `DELETED`로 표시된다.

---

## 4. 각 함수 설명

### `__init__(self, size)`

```python
def __init__(self, size):
    self.size = size
    self.table = [None for _ in range(size)]
```

해시 테이블을 초기화하는 생성자다.

`size`는 해시 테이블의 전체 칸 개수를 의미한다.

```python
hash_table = HashTable(5)
```

위 코드처럼 생성하면 내부 테이블은 다음 형태로 만들어진다.

```text
[None, None, None, None, None]
```

Chaining은 각 칸을 빈 리스트로 초기화하지만, Open Addressing은 한 칸에 하나의 데이터만 저장하므로 `None`으로 초기화한다.

---

### `hash_function(self, key)`

```python
def hash_function(self, key):
    total = 0

    for char in key:
        total += ord(char)

    return total % self.size
```

`key`를 배열 인덱스로 변환하는 함수다.

문자열의 각 문자를 `ord()`로 숫자 값으로 바꾼 뒤 모두 더한다. 그리고 그 값을 테이블 크기로 나눈 나머지를 인덱스로 사용한다.

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

따라서 `"apple"`은 처음에 `0`번 인덱스에 저장을 시도한다.

---

### `put(self, key, value)`

```python
def put(self, key, value):
    index = self.hash_function(key)
    first_deleted_index = None

    for _ in range(self.size):
        item = self.table[index]

        if item is self.DELETED:
            if first_deleted_index is None:
                first_deleted_index = index

        elif item is None:
            target_index = (
                first_deleted_index
                if first_deleted_index is not None
                else index
            )
            self.table[target_index] = (key, value)
            return True

        else:
            saved_key, saved_value = item

            if saved_key == key:
                self.table[index] = (key, value)
                return True

        index = (index + 1) % self.size
```

`key-value` 데이터를 저장하는 함수다.

먼저 해시 함수를 사용해 처음 확인할 인덱스를 구한다.

```python
index = self.hash_function(key)
```

현재 칸이 비어 있다면 데이터를 저장한다.

```python
self.table[index] = (key, value)
```

현재 칸에 다른 데이터가 있다면 충돌이 발생한 것이다. 이때 다음 칸으로 이동한다.

```python
index = (index + 1) % self.size
```

이미 같은 key가 있다면 새로운 데이터를 추가하지 않고 기존 value를 수정한다.

```python
hash_table.put("apple", 1000)
hash_table.put("apple", 1200)
```

위 코드에서는 `"apple"` 데이터가 두 개 생기지 않는다. 기존 값이 `1000`에서 `1200`으로 변경된다.

---

### `get(self, key)`

```python
def get(self, key):
    index = self.hash_function(key)

    for _ in range(self.size):
        item = self.table[index]

        if item is None:
            return None

        if item is not self.DELETED:
            saved_key, saved_value = item

            if saved_key == key:
                return saved_value

        index = (index + 1) % self.size

    return None
```

key에 해당하는 value를 조회하는 함수다.

저장할 때 충돌로 인해 원래 인덱스가 아닌 다른 위치에 데이터가 들어갈 수 있다. 따라서 처음 인덱스만 확인하지 않고 Linear Probing과 같은 순서로 다음 칸을 계속 확인해야 한다.

```text
해시 인덱스 확인
    ↓
key가 다르면 다음 칸 확인
    ↓
같은 key를 찾으면 value 반환
```

`None`을 만나면 그 뒤에는 찾는 key가 저장되어 있지 않다고 판단하고 탐색을 종료한다.

단, `DELETED`는 이전에 데이터가 있던 칸이므로 탐색을 멈추지 않고 다음 칸을 확인한다.

---

### `delete(self, key)`

```python
def delete(self, key):
    index = self.hash_function(key)

    for _ in range(self.size):
        item = self.table[index]

        if item is None:
            return False

        if item is not self.DELETED:
            saved_key, saved_value = item

            if saved_key == key:
                self.table[index] = self.DELETED
                return True

        index = (index + 1) % self.size

    return False
```

key에 해당하는 데이터를 삭제하는 함수다.

Open Addressing에서는 삭제할 데이터를 단순히 `None`으로 바꾸면 안 된다.

다음과 같은 상태를 생각해보자.

```text
index 0 -> ("ab", "first")
index 1 -> ("ba", "second")
```

`"ab"`와 `"ba"`는 모두 처음 인덱스가 `0`이다. `"ba"`는 충돌 때문에 `1`번에 저장되었다.

여기에서 `"ab"`를 삭제하면서 `0`번 칸을 `None`으로 바꾸면, `"ba"`를 검색할 때 `0`번에서 탐색이 끝날 수 있다.

```text
index 0 -> None
index 1 -> ("ba", "second")

"ba" 검색:
index 0이 None이므로 탐색 종료
실제로 index 1에 있지만 찾지 못함
```

그래서 삭제된 칸은 `None`이 아니라 `DELETED`라는 특별한 값으로 표시한다.

```text
index 0 -> DELETED
index 1 -> ("ba", "second")
```

탐색 중 `DELETED`를 만나면 다음 칸을 계속 확인한다.

---

### `show(self)`

```python
def show(self):
    for index, item in enumerate(self.table):
        if item is self.DELETED:
            print(index, "DELETED")
        else:
            print(index, item)
```

현재 해시 테이블의 전체 상태를 출력하는 함수다.

각 데이터가 원래 해시 인덱스에 저장되었는지, 충돌로 인해 다른 위치로 이동했는지 확인할 때 유용하다.

---

## 5. 해시 충돌 예제

실제로 충돌이 발생하는 예제를 살펴보자.

현재 해시 함수는 문자열을 구성하는 각 문자의 숫자 값을 모두 더한다.

`"ab"`와 `"ba"`의 해시 값을 계산하면 다음과 같다.

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

두 key는 서로 다르지만 같은 인덱스 `0`을 얻는다.

```python
hash_table = HashTable(5)

hash_table.put("ab", "first")
hash_table.put("ba", "second")

hash_table.show()
```

출력 결과:

```text
0 ('ab', 'first')
1 ('ba', 'second')
2 None
3 None
4 None
```

`"ab"`는 원래 위치인 `0`번에 저장된다.

`"ba"`도 처음에는 `0`번에 저장을 시도하지만 이미 `"ab"`가 있으므로 충돌이 발생한다. Linear Probing은 다음 위치인 `1`번을 확인하고, 비어 있으므로 그곳에 저장한다.

```text
"ab" -> index 0 저장

"ba" -> index 0 충돌
     -> index 1 확인
     -> index 1 저장
```

Chaining과 달리 같은 인덱스에 두 데이터를 함께 저장하지 않는다는 점이 핵심이다.

---

## 6. 테이블 끝에 도착하면 어떻게 될까?

Linear Probing은 테이블의 마지막 칸에서 충돌이 발생하면 다시 처음으로 돌아간다.

```python
index = (index + 1) % self.size
```

테이블 크기가 `5`일 때 이동 결과는 다음과 같다.

```text
현재 index = 3
(3 + 1) % 5 = 4

현재 index = 4
(4 + 1) % 5 = 0
```

탐사 순서는 원형처럼 이어진다.

```text
0 -> 1 -> 2 -> 3 -> 4 -> 0 -> 1 -> ...
```

무한 반복을 막기 위해 최대 `self.size`번까지만 위치를 확인한다.

---

## 7. Linear Probing의 장점과 주의할 점

Linear Probing의 장점은 구조가 단순하고 구현하기 쉽다는 점이다.

- 별도의 리스트나 연결 리스트가 필요하지 않다.
- 모든 데이터를 하나의 배열 안에 저장한다.
- 연속된 배열 공간을 사용하므로 메모리 접근이 단순하다.

하지만 데이터가 연속된 위치에 몰리는 **Primary Clustering** 문제가 발생할 수 있다.

```text
index 0 -> ("ab", "first")
index 1 -> ("ba", "second")
index 2 -> ("apple", 1000)
index 3 -> ("other", 2000)
```

데이터가 연속적으로 모이면 새로운 데이터를 저장하거나 조회할 때 여러 칸을 확인해야 한다.

해시 테이블이 많이 차 있을수록 빈 칸을 찾기 어려워진다. 이를 판단할 때 적재율(Load Factor)을 사용한다.

```text
적재율 = 저장된 데이터 개수 / 전체 테이블 크기
```

테이블 크기가 `10`이고 데이터가 `7`개라면 적재율은 `0.7`이다.

Open Addressing에서는 적재율이 높아지면 충돌과 탐사 횟수가 증가한다. 따라서 일정 수준 이상 데이터가 쌓이면 더 큰 테이블을 만들고 기존 데이터를 다시 저장하는 리사이징이 필요하다.

이 예제는 Linear Probing의 동작을 이해하기 위한 학습용 구현이므로 자동 리사이징은 포함하지 않았다.

---

## 8. Chaining과 Linear Probing 비교

| 구분 | Chaining | Linear Probing |
| --- | --- | --- |
| 저장 방식 | 각 인덱스에 리스트를 둔다 | 테이블 안의 다른 빈 칸을 찾는다 |
| 한 칸의 데이터 수 | 여러 개 가능 | 하나만 가능 |
| 충돌 처리 | 같은 bucket에 추가 | 다음 인덱스로 이동 |
| 삭제 | 리스트에서 제거 | `DELETED` 표시가 필요 |
| 테이블이 가득 찬 경우 | bucket에 계속 저장 가능 | 새로운 데이터를 저장할 수 없음 |
| 주요 문제 | 특정 bucket이 길어질 수 있음 | 데이터가 연속해서 뭉칠 수 있음 |

---

## 정리

Open Addressing은 해시 충돌이 발생했을 때, 같은 인덱스에 여러 데이터를 저장하지 않고 해시 테이블 안의 다른 빈 칸을 찾아 저장하는 방식이다.

Linear Probing은 현재 위치에서 충돌이 발생하면 다음 인덱스를 순서대로 확인한다.

```text
key 입력
    ↓
해시 함수로 시작 인덱스 계산
    ↓
현재 칸 확인
    ↓
비어 있으면 저장
    ↓
다른 데이터가 있으면 다음 칸으로 이동
```

데이터 조회와 삭제도 저장할 때와 같은 탐사 순서를 따라야 한다.  
삭제된 위치를 단순히 `None`으로 바꾸면 탐색 경로가 끊어질 수 있으므로 `DELETED`와 같은 Tombstone 표시를 사용한다.

해시 충돌은 완전히 피하기 어렵다. 따라서 해시 테이블은 충돌이 발생했을 때 데이터를 안전하게 저장하고, 이후에도 원하는 값을 정확하게 찾을 수 있어야 한다.

Linear Probing은 이러한 충돌을 단순한 탐사 규칙으로 해결하는 대표적인 Open Addressing 방식이다.