# linked_list.py

# 링크드리스트의 노드 하나를 표현하는 클래스
class Node:
    def __init__(self, value):
        # 노드가 가지고 있는 실제 값
        self.value = value

        # 다음 노드를 가리키는 변수, 초기값은 None
        self.next = None


# 단일 링크드리스트를 표현하는 클래스
class LinkedList:

    def __init__(self):
        # 링크드리스트의 첫 번째 노드를 가리킨다.
        self.head = None

    # 링크드리스트의 맨 뒤에 값을 추가
    def append(self, value):
        new_node = Node(value)

        # 리스트가 비어 있으면 새 노드가 첫 번째 노드
        if self.head is None:
            self.head = new_node
            return

        # 마지막 노드까지 이동
        current = self.head
        while current.next is not None:
            current = current.next

        # 마지막 노드 뒤에 새 노드를 연결
        current.next = new_node

    # 링크드리스트의 맨 앞에 값을 추가
    def prepend(self, value):
        new_node = Node(value)

        # 새 노드가 기존 head를 가리킨다.
        new_node.next = self.head

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

        new_node = Node(value)
        current = self.head
        current_index = 0

        # 삽입할 위치의 바로 앞 노드까지 이동
        while current is not None and current_index < index - 1:
            current = current.next
            current_index += 1

        # current가 None이면 인덱스가 현재 리스트 길이보다 큰 경우
        if current is None:
            return False

        # current와 current.next 사이에 새 노드를 끼워 넣는다.
        new_node.next = current.next
        current.next = new_node
        return True

    # 입력한 값을 가진 첫 번째 노드를 삭제
    def delete(self, value):
        if self.head is None:
            return False

        # 삭제할 값이 첫 번째 노드에 있는 경우
        if self.head.value == value:
            self.head = self.head.next
            return True

        current = self.head

        while current.next is not None:
            if current.next.value == value:
                current.next = current.next.next
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
    
    # 입력한 인덱스에 있는 노드가 갖고 있는 reference 를 반환. 없으면 None을 반환
    def get_next(self, index):
        if index < 0:
            return None
        
        current = self.head
        current_index = 0
        
        while current is not None:
            if current_index == index:
                return current.next
            
            current = current.next
            current_index += 1
        
        return None

    # 현재 링크드리스트의 노드 개수를 반환
    def length(self):
        count = 0
        current = self.head

        while current is not None:
            count += 1
            current = current.next

        return count
    
    # 링크드리스트를 터미널에서 보기 좋은 문자열로 반환
    def display(self):
        if self.head is None:
            return "HEAD -> None"

        result = ["HEAD"]
        current = self.head

        while current is not None:
            result.append(f"[{current.value}]")
            current = current.next

        result.append("None")
        return " -> ".join(result)