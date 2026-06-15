# double_linked_list.py

# 더블 링크드리스트의 노드 하나를 표현하는 클래스
class Node:
    def __init__(self, value):
        # 노드가 가지고 있는 실제 값
        self.value = value

        # 이전 노드를 가리키는 변수, 초기값은 None
        self.prev = None

        # 다음 노드를 가리키는 변수, 초기값은 None
        self.next = None


# 더블 링크드리스트를 표현하는 클래스
class DoubleLinkedList:

    def __init__(self):
        # 더블 링크드리스트의 첫 번째 노드를 가리킨다.
        self.head = None

        # 더블 링크드리스트의 마지막 노드를 가리킨다.
        self.tail = None

    # 더블 링크드리스트의 맨 뒤에 값을 추가
    def append(self, value):
        new_node = Node(value)

        # 리스트가 비어 있으면 새 노드가 첫 번째이자 마지막 노드
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        # 기존 마지막 노드와 새 노드를 서로 연결
        new_node.prev = self.tail
        self.tail.next = new_node

        # tail을 새 노드로 변경
        self.tail = new_node

    # 더블 링크드리스트의 맨 앞에 값을 추가
    def prepend(self, value):
        new_node = Node(value)

        # 리스트가 비어 있으면 새 노드가 첫 번째이자 마지막 노드
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return

        # 새 노드와 기존 첫 번째 노드를 서로 연결
        new_node.next = self.head
        self.head.prev = new_node

        # head를 새 노드로 변경
        self.head = new_node

    # 원하는 인덱스 위치에 값을 추가
    def insert(self, index, value):
        if index < 0:
            return False

        # 0번 인덱스는 맨 앞에 추가하는 것과 같다.
        if index == 0:
            self.prepend(value)
            return True

        # 마지막 다음 위치는 맨 뒤에 추가하는 것과 같다.
        if index == self.length():
            self.append(value)
            return True

        new_node = Node(value)
        current = self.head
        current_index = 0

        # 삽입할 위치의 노드까지 이동
        while current is not None and current_index < index:
            current = current.next
            current_index += 1

        # current가 None이면 인덱스가 현재 리스트 길이보다 큰 경우
        if current is None:
            return False

        # current 앞에 새 노드를 끼워 넣는다.
        prev_node = current.prev

        new_node.prev = prev_node
        new_node.next = current
        prev_node.next = new_node
        current.prev = new_node

        return True

    # 입력한 값을 가진 첫 번째 노드를 삭제
    def delete(self, value):
        if self.head is None:
            return False

        current = self.head

        while current is not None:
            if current.value == value:
                # 삭제할 노드가 첫 번째 노드인 경우
                if current.prev is None:
                    self.head = current.next
                else:
                    current.prev.next = current.next

                # 삭제할 노드가 마지막 노드인 경우
                if current.next is None:
                    self.tail = current.prev
                else:
                    current.next.prev = current.prev

                return True

            current = current.next

        return False

    # 입력한 값이 있는 인덱스를 반환. 없으면 -1을 반환
    def find(self, value):
        current = self.head
        index = 0

        while current is not None:
            if current.value == value:
                return index

            current = current.next
            index += 1

        return -1

    # 입력한 인덱스에 있는 노드의 값을 반환. 인덱스가 유효하지 않으면 None을 반환
    def get(self, index):
        if index < 0:
            return None

        current = self.head
        current_index = 0

        while current is not None:
            if current_index == index:
                return current.value

            current = current.next
            current_index += 1

        return None

    # 입력한 인덱스에 있는 노드가 갖고 있는 next reference를 반환. 없으면 None을 반환
    def get_next(self, index):
        node = self.get_node(index)

        if node is None:
            return None

        return node.next

    # 입력한 인덱스에 있는 노드가 갖고 있는 prev reference를 반환. 없으면 None을 반환
    def get_prev(self, index):
        node = self.get_node(index)

        if node is None:
            return None

        return node.prev

    # 입력한 인덱스에 있는 노드 자체를 반환. 없으면 None을 반환
    def get_node(self, index):
        if index < 0:
            return None

        current = self.head
        current_index = 0

        while current is not None:
            if current_index == index:
                return current

            current = current.next
            current_index += 1

        return None

    # 현재 더블 링크드리스트의 노드 개수를 반환
    def length(self):
        count = 0
        current = self.head

        while current is not None:
            count += 1
            current = current.next

        return count

    # 더블 링크드리스트를 head부터 tail까지 보기 좋은 문자열로 반환
    def display(self):
        if self.head is None:
            return "HEAD -> None"

        result = ["HEAD"]
        current = self.head

        while current is not None:
            result.append(f"[{current.value}]")
            current = current.next

        result.append("None")
        return " <-> ".join(result)

    # 더블 링크드리스트를 tail부터 head까지 보기 좋은 문자열로 반환
    def display_reverse(self):
        if self.tail is None:
            return "TAIL -> None"

        result = ["TAIL"]
        current = self.tail

        while current is not None:
            result.append(f"[{current.value}]")
            current = current.prev

        result.append("None")
        return " <-> ".join(result)



