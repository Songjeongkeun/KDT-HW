class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None


class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, value):
        # TODO: 리스트의 맨 뒤에 새 노드를 추가한다.
        pass

    def prepend(self, value):
        # TODO: 리스트의 맨 앞에 새 노드를 추가한다.
        pass

    def insert(self, index, value):
        # TODO: 원하는 인덱스에 새 노드를 삽입한다.
        pass

    def delete(self, value):
        # TODO: 입력한 값을 가진 첫 번째 노드를 삭제한다.
        pass

    def find(self, value):
        # TODO: 입력한 값이 저장된 첫 번째 인덱스를 찾는다.
        pass

    def get(self, index):
        # TODO: 입력한 인덱스에 저장된 값을 반환한다.
        pass

    def get_next(self, index):
        node = self.get_node(index)

        if node is None:
            return None

        return node.next

    def get_prev(self, index):
        node = self.get_node(index)

        if node is None:
            return None

        return node.prev

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

    def length(self):
        count = 0
        current = self.head

        while current is not None:
            count += 1
            current = current.next

        return count

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
