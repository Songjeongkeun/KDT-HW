# 자료구조 조사 및 구현 과제: 링크드 리스트

## 1. 링크드 리스트란?

링크드 리스트(Linked List)는 여러 데이터를 **노드(Node)**라는 단위로 저장하고, 각 노드가 다음 노드를 가리키는 방식으로 연결된 선형 자료구조이다.

배열은 데이터가 메모리상에 연속적으로 저장되는 구조인 반면, 링크드 리스트는 각 데이터가 흩어져 있어도 **다음 데이터의 위치를 가리키는 정보**를 가지고 있기 때문에 하나의 목록처럼 연결될 수 있다.

```text
[데이터 | 다음 노드 주소] -> [데이터 | 다음 노드 주소] -> [데이터 | None]
```

링크드 리스트는 데이터를 중간에 추가하거나 삭제할 때 유용하다. 배열처럼 뒤쪽 데이터를 모두 한 칸씩 밀거나 당길 필요가 없고, 노드의 연결만 바꾸면 되기 때문이다.

------

## 2. 링크드 리스트의 구조

링크드 리스트는 기본적으로 다음 세 가지 요소로 이루어진다.

| 요소         | 설명                                 |
| :----------- | :----------------------------------- |
| Node         | 데이터를 저장하는 하나의 단위        |
| Data         | 노드가 실제로 가지고 있는 값         |
| Next Pointer | 다음 노드를 가리키는 참조(reference) |

### 2.1 Node

노드(Node)는 링크드 리스트의 기본 구성 요소이다. 각 노드는 데이터와 다음 노드를 가리키는 참조를 가진다.

```text
Node
+--------+------+
| data   | next |
+--------+------+
```

### 2.2 Data

`data`는 노드가 저장하는 실제 값이다. 예를 들어 숫자, 문자열, 객체 등을 저장할 수 있다.

```text
+--------+------+
| 10     | next |
+--------+------+
```

### 2.3 Next Pointer

`next`는 다음 노드를 가리킨다. 마지막 노드는 더 이상 가리킬 노드가 없으므로 `None`을 가진다.

```text
head
 ↓
+--------+------+    +--------+------+    +--------+------+
| 10     |  ●---+---> | 20     |  ●---+---> | 30     | None |
+--------+------+    +--------+------+    +--------+------+
```

여기서 `head`는 링크드 리스트의 첫 번째 노드를 가리키는 변수이다. 링크드 리스트는 보통 `head`에서 시작해 `next`를 따라가며 데이터를 탐색한다.

------

## 3. 링크드 리스트의 동작 원리

링크드 리스트는 `head`부터 시작해서 각 노드의 `next`를 따라 이동한다.

```text
head -> 10 -> 20 -> 30 -> None
```

이 구조에서 중요한 동작은 삽입, 삭제, 탐색이다.

------

## 4. 데이터 추가

링크드 리스트에 데이터를 추가하는 방식은 위치에 따라 달라진다.

### 4.1 맨 앞에 추가

새 노드를 만들고, 새 노드의 `next`가 기존 `head`를 가리키게 한다. 그 다음 `head`를 새 노드로 바꾼다.

```text
기존:
head -> 20 -> 30 -> None

10 추가:
new_node -> 20 -> 30 -> None

head를 new_node로 변경:
head -> 10 -> 20 -> 30 -> None
```

맨 앞 삽입은 연결만 바꾸면 되므로 빠르다.

### 4.2 맨 뒤에 추가

마지막 노드까지 이동한 뒤, 마지막 노드의 `next`가 새 노드를 가리키게 한다.

```text
기존:
head -> 10 -> 20 -> None

30 추가:
head -> 10 -> 20 -> 30 -> None
```

단일 링크드 리스트에서 `tail`을 따로 관리하지 않으면 마지막 노드까지 이동해야 하므로 시간이 걸릴 수 있다.

### 4.3 중간에 추가

삽입할 위치의 이전 노드를 찾고, 연결을 바꾼다.

```text
기존:
head -> 10 -> 30 -> None

20 삽입:
head -> 10 -> 20 -> 30 -> None
```

중간 삽입에서는 새 노드가 다음 노드를 먼저 가리키게 하고, 이전 노드가 새 노드를 가리키게 해야 한다.

------

## 5. 데이터 삭제

삭제는 제거할 노드를 찾은 뒤, 이전 노드가 삭제할 노드의 다음 노드를 가리키게 만드는 방식으로 이루어진다.

```text
기존:
head -> 10 -> 20 -> 30 -> None

20 삭제:
head -> 10 ------> 30 -> None
```

삭제할 노드가 `head`라면 `head`를 다음 노드로 변경한다.

```text
기존:
head -> 10 -> 20 -> 30 -> None

10 삭제:
head -> 20 -> 30 -> None
```

------

## 6. 데이터 탐색

링크드 리스트는 배열처럼 인덱스로 바로 접근하기 어렵다.
원하는 데이터를 찾으려면 `head`부터 시작해 `next`를 따라가며 하나씩 확인해야 한다.

```text
head -> 10 -> 20 -> 30 -> None

30 탐색:
10 확인 -> 20 확인 -> 30 확인
```

따라서 링크드 리스트의 탐색은 데이터가 많을수록 오래 걸릴 수 있다.

------

## 7. 배열과 링크드 리스트의 차이점

| 구분        | 배열(Array)               | 링크드 리스트(Linked List)       |
| :---------- | :------------------------ | :------------------------------- |
| 저장 방식   | 연속된 메모리 공간에 저장 | 노드가 다음 노드를 가리키며 연결 |
| 접근 방식   | 인덱스로 바로 접근        | head부터 순차 탐색               |
| 조회 속도   | 빠름                      | 느릴 수 있음                     |
| 중간 삽입   | 뒤쪽 데이터를 이동해야 함 | 연결만 바꾸면 됨                 |
| 중간 삭제   | 뒤쪽 데이터를 이동해야 함 | 연결만 바꾸면 됨                 |
| 메모리 사용 | 데이터만 저장             | 데이터 + 다음 노드 참조 저장     |
| 구현 난이도 | 비교적 쉬움               | 포인터/참조 관리가 필요          |

### 7.1 배열이 유리한 경우

- 인덱스로 자주 조회해야 할 때
- 데이터 개수가 비교적 고정되어 있을 때
- 순차적으로 반복 처리하는 일이 많을 때

### 7.2 링크드 리스트가 유리한 경우

- 중간 삽입과 삭제가 자주 발생할 때
- 데이터 개수가 자주 변할 때
- 데이터의 순서를 연결 관계로 관리하고 싶을 때

------

## 8. 링크드 리스트의 장점과 단점

### 8.1 장점

- 데이터 추가와 삭제 시 연결만 바꾸면 되므로 효율적이다.
- 크기를 미리 정하지 않아도 된다.
- 메모리상에서 데이터가 연속되어 있을 필요가 없다.
- 노드 단위로 동적으로 데이터를 관리할 수 있다.

### 8.2 단점

- 특정 위치의 데이터를 조회하려면 앞에서부터 순서대로 탐색해야 한다.
- 각 노드가 다음 노드 참조를 저장해야 하므로 추가 메모리가 필요하다.
- 구현이 배열보다 복잡하다.
- 단일 링크드 리스트는 이전 노드로 돌아가기 어렵다.

------

## 9. 링크드 리스트의 실제 활용 사례

링크드 리스트는 데이터의 삽입과 삭제가 자주 일어나는 구조에서 활용된다.

### 9.1 음악 플레이리스트

노래들이 순서대로 연결되어 있고, 중간에 새 노래를 추가하거나 삭제할 수 있다.

```text
노래A -> 노래B -> 노래C -> None
```

노래B 뒤에 노래D를 추가하면 연결만 바꾸면 된다.

```text
노래A -> 노래B -> 노래D -> 노래C -> None
```

### 9.2 브라우저 방문 기록

뒤로가기와 앞으로가기 기능은 스택이나 더블 링크드 리스트 구조로 설명할 수 있다.
현재 페이지를 기준으로 이전 페이지와 다음 페이지를 연결하면 양방향 이동이 가능하다.

### 9.3 운영체제의 프로세스 관리

운영체제는 실행 대기 중인 프로세스들을 연결 리스트 형태로 관리할 수 있다. 프로세스가 추가되거나 종료될 때 연결을 바꿔 효율적으로 관리할 수 있다.

### 9.4 해시 테이블의 충돌 처리

해시 테이블에서 같은 위치에 여러 값이 들어오는 충돌이 발생할 수 있다. 이때 같은 위치의 데이터들을 링크드 리스트로 연결하는 방식을 사용할 수 있다.

```text
index 0: None
index 1: keyA -> keyB -> keyC
index 2: None
```

------

## 10. 단일 링크드 리스트 구현

단일 링크드 리스트(Singly Linked List)는 각 노드가 다음 노드만 가리키는 구조이다.

```text
head -> data -> data -> data -> None
```

이제 Python으로 직접 구현한다.

### 10.1 Node 클래스

```python
class Node:
    def __init__(self, data):
        # 노드가 저장할 실제 값
        self.data = data

        # 다음 노드를 가리키는 참조
        # 처음 생성할 때는 연결된 다음 노드가 없으므로 None으로 둔다.
        self.next = None
```

출력 결과:

```text
출력 결과 없음
```

`Node`는 링크드 리스트의 가장 작은 단위이다. `data`에는 실제 값을 저장하고, `next`에는 다음 노드의 위치를 저장한다.

### 10.2 LinkedList 클래스 기본 구조

```python
class LinkedList:
    def __init__(self):
        # head는 링크드 리스트의 첫 번째 노드를 가리킨다.
        # 처음에는 아무 노드도 없으므로 None이다.
        self.head = None
```

출력 결과:

```text
출력 결과 없음
```

`LinkedList` 클래스는 여러 노드를 관리하는 역할을 한다.
가장 중요한 속성은 첫 번째 노드를 가리키는 `head`이다.

------

## 11. 삽입 기능 구현

### 11.1 맨 뒤에 삽입하기

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        # 새 데이터를 담은 노드를 만든다.
        new_node = Node(data)

        # 리스트가 비어 있다면 새 노드가 첫 번째 노드가 된다.
        if self.head is None:
            self.head = new_node
            return

        # 마지막 노드를 찾기 위해 head부터 이동한다.
        current = self.head
        while current.next is not None:
            current = current.next

        # 마지막 노드의 next가 새 노드를 가리키게 한다.
        current.next = new_node

    def print_list(self):
        current = self.head

        while current is not None:
            print(current.data, end=" -> ")
            current = current.next

        print("None")


linked_list = LinkedList()
linked_list.append(10)
linked_list.append(20)
linked_list.append(30)

linked_list.print_list()
```

출력 결과:

```text
10 -> 20 -> 30 -> None
```

`append()`는 마지막 노드까지 이동한 뒤 새 노드를 연결한다.

### 11.2 맨 앞에 삽입하기

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def prepend(self, data):
        # 새 노드를 만든다.
        new_node = Node(data)

        # 새 노드가 기존 head를 가리키게 한다.
        new_node.next = self.head

        # head를 새 노드로 변경한다.
        self.head = new_node

    def print_list(self):
        current = self.head

        while current is not None:
            print(current.data, end=" -> ")
            current = current.next

        print("None")


linked_list = LinkedList()
linked_list.prepend(30)
linked_list.prepend(20)
linked_list.prepend(10)

linked_list.print_list()
```

출력 결과:

```text
10 -> 20 -> 30 -> None
```

맨 앞 삽입은 새 노드와 기존 `head`의 연결만 바꾸면 되므로 빠르게 처리할 수 있다.

------

## 12. 삭제 기능 구현

삭제할 값을 가진 노드를 찾아 연결에서 제외한다.

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next is not None:
            current = current.next

        current.next = new_node

    def delete(self, data):
        # 리스트가 비어 있으면 삭제할 수 없다.
        if self.head is None:
            print("리스트가 비어 있다.")
            return

        # 삭제할 데이터가 head에 있는 경우
        if self.head.data == data:
            self.head = self.head.next
            return

        # 삭제할 노드의 이전 노드를 찾는다.
        current = self.head
        while current.next is not None:
            if current.next.data == data:
                # current.next가 삭제 대상이다.
                # current가 삭제 대상 다음 노드를 가리키도록 연결을 바꾼다.
                current.next = current.next.next
                return

            current = current.next

        print("삭제할 데이터를 찾지 못했다.")

    def print_list(self):
        current = self.head

        while current is not None:
            print(current.data, end=" -> ")
            current = current.next

        print("None")


linked_list = LinkedList()
linked_list.append(10)
linked_list.append(20)
linked_list.append(30)
linked_list.append(40)

linked_list.print_list()

linked_list.delete(20)
linked_list.print_list()

linked_list.delete(10)
linked_list.print_list()
```

출력 결과:

```text
10 -> 20 -> 30 -> 40 -> None
10 -> 30 -> 40 -> None
30 -> 40 -> None
```

삭제의 핵심은 삭제 대상 노드를 직접 지우는 것이 아니라, 이전 노드의 `next`가 삭제 대상 다음 노드를 가리키게 만드는 것이다.

------

## 13. 탐색 기능 구현

탐색은 `head`부터 시작해 `next`를 따라 이동하며 값을 비교한다.

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next is not None:
            current = current.next

        current.next = new_node

    def search(self, data):
        current = self.head
        index = 0

        while current is not None:
            if current.data == data:
                return index

            current = current.next
            index += 1

        return -1


linked_list = LinkedList()
linked_list.append("사과")
linked_list.append("바나나")
linked_list.append("오렌지")

print(linked_list.search("바나나"))
print(linked_list.search("포도"))
```

출력 결과:

```text
1
-1
```

탐색 결과로 찾은 위치의 인덱스를 반환하고, 찾지 못하면 `-1`을 반환하도록 만들었다.

------

## 14. 전체 단일 링크드 리스트 코드

아래 코드는 삽입, 삭제, 조회 기능을 모두 포함한 단일 링크드 리스트 구현이다.

```python
class Node:
    def __init__(self, data):
        # 노드에 저장할 값
        self.data = data

        # 다음 노드를 가리키는 참조
        self.next = None


class LinkedList:
    def __init__(self):
        # 첫 번째 노드를 가리키는 값
        self.head = None

    def append(self, data):
        # 맨 뒤에 새 노드를 추가한다.
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next is not None:
            current = current.next

        current.next = new_node

    def prepend(self, data):
        # 맨 앞에 새 노드를 추가한다.
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
		
    def insert_after(self, target_data, new_data):
        # target_data 값을 가진 노드 뒤에 new_data를 가진 새 노드를 삽입한다.
        current = self.head

        while current is not None:
            if current.data == target_data:
                new_node = Node(new_data)

                # 새 노드가 target 노드의 다음 노드를 가리키게 한다.
                new_node.next = current.next

                # target 노드가 새 노드를 가리키게 한다.
                current.next = new_node

                return True

            current = current.next

        return False
      
    def delete(self, data):
        # 값이 data인 첫 번째 노드를 삭제한다.
        if self.head is None:
            return False

        if self.head.data == data:
            self.head = self.head.next
            return True

        current = self.head
        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                return True
            current = current.next

        return False

    def search(self, data):
        # 값이 data인 노드의 위치를 찾는다.
        current = self.head
        index = 0

        while current is not None:
            if current.data == data:
                return index
            current = current.next
            index += 1

        return -1

    def get(self, index):
        # 인덱스를 이용해 데이터를 조회한다.
        current = self.head
        current_index = 0

        while current is not None:
            if current_index == index:
                return current.data

            current = current.next
            current_index += 1

        return None

    def print_list(self):
        # 전체 노드를 순서대로 출력한다.
        current = self.head

        while current is not None:
            print(current.data, end=" -> ")
            current = current.next

        print("None")


linked_list = LinkedList()

linked_list.append(20)
linked_list.prepend(10)
linked_list.append(40)
linked_list.insert_after(20, 30)

linked_list.print_list()

print("1번 인덱스 조회:", linked_list.get(1))
print("30 탐색:", linked_list.search(30))

print("20 삭제:", linked_list.delete(20))
linked_list.print_list()



print("100 삭제:", linked_list.delete(100))
```

출력 결과:

```text
10 -> 20 -> 30 -> 40 -> None
1번 인덱스 조회: 20
30 탐색: 2
20 삭제: True
10 -> 30 -> 40 -> None
100 삭제: False
```

------

## 15. 시간 복잡도

링크드 리스트의 주요 연산 시간 복잡도는 다음과 같다.

| 연산                                    | 시간 복잡도 | 이유                             |
| :-------------------------------------- | :---------- | :------------------------------- |
| 맨 앞 삽입                              | O(1)        | head만 바꾸면 된다.              |
| 맨 뒤 삽입                              | O(n)        | 마지막 노드까지 이동해야 한다.   |
| 탐색                                    | O(n)        | head부터 순서대로 확인해야 한다. |
| 삭제                                    | O(n)        | 삭제할 노드를 먼저 찾아야 한다.  |
| 특정 노드를 알고 있을 때 다음 위치 삽입 | O(1)        | 연결만 바꾸면 된다.              |

`tail`을 함께 관리하면 맨 뒤 삽입을 O(1)로 개선할 수 있다.

------

## 16. 더블 링크드 리스트

더블 링크드 리스트(Doubly Linked List)는 각 노드가 다음 노드뿐 아니라 이전 노드도 함께 가리키는 구조이다.

```text
None <- 10 <-> 20 <-> 30 -> None
```

### 16.1 더블 링크드 리스트 구조

| 요소 | 설명                      |
| :--- | :------------------------ |
| data | 노드가 저장하는 값        |
| prev | 이전 노드를 가리키는 참조 |
| next | 다음 노드를 가리키는 참조 |

### 16.2 단일 링크드 리스트와 차이점

| 구분           | 단일 링크드 리스트 | 더블 링크드 리스트       |
| :------------- | :----------------- | :----------------------- |
| 노드 구조      | data, next         | data, prev, next         |
| 이동 방향      | 한 방향            | 양방향                   |
| 메모리 사용    | 더 적음            | prev 참조 때문에 더 많음 |
| 이전 노드 접근 | 어려움             | 쉬움                     |
| 구현 난이도    | 비교적 단순        | 더 복잡                  |

### 16.3 더블 링크드 리스트가 유용한 경우

- 브라우저 뒤로가기/앞으로가기
- 음악 플레이리스트 이전 곡/다음 곡 이동
- 문서 편집기의 커서 이동
- 양방향 탐색이 필요한 데이터 구조

### 16.4 간단한 더블 링크드 리스트 예제

```python
class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = DoublyNode(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node

    def print_forward(self):
        current = self.head

        while current is not None:
            print(current.data, end=" -> ")
            current = current.next

        print("None")

    def print_backward(self):
        current = self.tail

        while current is not None:
            print(current.data, end=" -> ")
            current = current.prev

        print("None")


dll = DoublyLinkedList()
dll.append("A")
dll.append("B")
dll.append("C")

dll.print_forward()
dll.print_backward()
```

출력 결과:

```text
A -> B -> C -> None
C -> B -> A -> None
```

더블 링크드 리스트는 `prev`를 가지고 있기 때문에 뒤에서 앞으로도 이동할 수 있다.

------

## 17. 결론

링크드 리스트는 노드들이 서로 연결된 선형 자료구조이다. 배열과 달리 데이터가 연속적으로 저장될 필요가 없고, 삽입과 삭제가 연결 변경만으로 가능하다는 장점이 있다.

하지만 특정 인덱스에 바로 접근할 수 없기 때문에 탐색은 배열보다 느릴 수 있다. 따라서 링크드 리스트는 **조회보다 삽입과 삭제가 자주 발생하는 상황**에 적합하다.

이번 과제의 핵심은 링크드 리스트 코드를 외우는 것이 아니라, 다음 질문에 답할 수 있게 되는 것이다.

- 왜 노드가 필요한가?
- 왜 `next`가 필요한가?
- 삽입과 삭제는 실제 데이터를 옮기는 것이 아니라 왜 연결을 바꾸는 방식인가?
- 배열보다 링크드 리스트가 유리한 상황은 언제인가?

이 질문을 이해하면 링크드 리스트뿐 아니라 트리, 그래프 같은 더 복잡한 자료구조도 이해하기 쉬워진다.