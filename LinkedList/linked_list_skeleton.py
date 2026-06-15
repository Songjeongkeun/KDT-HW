# linked_list.py

# 링크드리스트의 노드 하나를 표현하는 클래스
class Node:
    def __init__(self, value):
        # TODO 1. 노드가 저장할 실제 값을 self.value에 저장하세요.
        # 예: self.value = value
        self.value = value
        # TODO 2. 다음 노드를 가리키는 self.next를 None으로 초기화하세요.
        # 처음 노드를 만들 때는 아직 다음 노드가 연결되어 있지 않습니다.
        self.next = None



# 단일 링크드리스트를 표현하는 클래스
class LinkedList:

    def __init__(self):
        # TODO 1. 링크드리스트의 첫 번째 노드를 가리키는 self.head를 만드세요.
        # 처음 리스트는 비어 있으므로 self.head는 None이어야 합니다.
        self.head = None

    # 링크드리스트의 맨 뒤에 값을 추가
    def append(self, value):
        
        # TODO 1. value를 저장할 새 Node를 만드세요.
        new_node = Node(value)
        # TODO 2. 리스트가 비어 있는지 확인하세요.
        if self.head is None:
            self.head = new_node
            return 
        # self.head가 None이면 새 노드가 첫 번째 노드가 됩니다.

        # TODO 3. 리스트가 비어 있지 않다면 head부터 시작해서 마지막 노드까지 이동하세요.
        # 마지막 노드는 current.next가 None인 노드입니다.
        current = self.head
        while current.next is not None:
            current = current.next
        # TODO 4. 마지막 노드의 next가 새 노드를 가리키도록 연결하세요.
        
        current.next = new_node

    # 링크드리스트의 맨 앞에 값을 추가
    def prepend(self, value):
        
        # TODO 1. value를 저장할 새 Node를 만드세요.

        # TODO 2. 새 노드의 next가 기존 head를 가리키도록 하세요.

        # TODO 3. self.head를 새 노드로 변경하세요.
        pass

    # 원하는 인덱스 위치에 값을 추가
    def insert(self, index, value):
        
        # TODO 1. index가 0보다 작으면 삽입할 수 없으므로 False를 반환하세요.

        # TODO 2. index가 0이면 prepend(value)를 호출하고 True를 반환하세요.

        # TODO 3. value를 저장할 새 Node를 만드세요.

        # TODO 4. head부터 시작해서 삽입할 위치 바로 앞 노드까지 이동하세요.
        # 예: index가 2라면 1번 인덱스 노드까지 이동해야 합니다.

        # TODO 5. 이동 중 current가 None이 되면 index가 리스트 길이보다 큰 것입니다.
        # 이 경우 False를 반환하세요.

        # TODO 6. 새 노드를 current와 current.next 사이에 연결하세요.
        # 새 노드의 next가 먼저 current.next를 가리키게 하고,
        # 그 다음 current.next가 새 노드를 가리키게 해야 합니다.

        # TODO 7. 삽입에 성공하면 True를 반환하세요.
        pass

    # 입력한 값을 가진 첫 번째 노드를 삭제
    def delete(self, value):
        
        # TODO 1. 리스트가 비어 있으면 삭제할 수 없으므로 False를 반환하세요.

        # TODO 2. 삭제할 값이 head에 있는지 확인하세요.
        # 맞다면 self.head를 다음 노드로 옮기고 True를 반환하세요.

        # TODO 3. head부터 시작해서 current.next를 확인하며 삭제할 값을 찾으세요.
        # current가 아니라 current.next를 보는 이유는,
        # 삭제할 노드의 이전 노드가 next 연결을 바꿔야 하기 때문입니다.

        # TODO 4. current.next.value가 삭제할 값과 같다면
        # current.next를 current.next.next로 바꿔 삭제할 노드를 건너뛰세요.

        # TODO 5. 삭제에 성공하면 True를 반환하세요.

        # TODO 6. 끝까지 찾지 못했다면 False를 반환하세요.
        pass

    # 입력한 값이 있는 인덱스를 반환합니다. 없으면 -1을 반환
    def find(self, value):
        
        # TODO 1. head부터 탐색을 시작할 current 변수를 만드세요.

        # TODO 2. 현재 위치를 나타낼 index 변수를 0으로 초기화하세요.

        # TODO 3. current가 None이 될 때까지 반복하세요.

        # TODO 4. current.value가 찾는 value와 같다면 index를 반환하세요.

        # TODO 5. 값이 다르다면 current를 다음 노드로 이동하고 index를 1 증가시키세요.

        # TODO 6. 끝까지 찾지 못했다면 -1을 반환하세요.
        pass
       
       
    # 입력한 인덱스에 있는 노드의 값을 반환합니다. 인덱스가 유효하지 않으면 None을 반환
    def get(self, index):
        # TODO 1. index가 0보다 작으면 유효하지 않으므로 None을 반환하세요.

        # TODO 2. head부터 탐색할 current 변수를 만드세요.

        # TODO 3. 현재 위치를 나타낼 current_index 변수를 0으로 초기화하세요.

        # TODO 4. current가 None이 될 때까지 반복하세요.

        # TODO 5. current_index가 index와 같다면 current.value를 반환하세요.

        # TODO 6. 아직 원하는 위치가 아니라면 다음 노드로 이동하고 current_index를 1 증가시키세요.

        # TODO 7. 끝까지 도착했는데 index를 찾지 못했다면 None을 반환하세요.
        pass
    
    # 입력한 인덱스에 있는 노드가 가리키는 다음 노드를 반환합니다. 없으면 None을 반환합니다
    def get_next(self, index):
        # TODO 1. index가 0보다 작으면 유효하지 않으므로 None을 반환하세요.

        # TODO 2. head부터 탐색할 current 변수를 만드세요.

        # TODO 3. 현재 위치를 나타낼 current_index 변수를 0으로 초기화하세요.

        # TODO 4. current가 None이 될 때까지 반복하세요.

        # TODO 5. current_index가 index와 같다면 current.next를 반환하세요.
        # current.next는 다음 노드의 참조입니다. 마지막 노드라면 None입니다.

        # TODO 6. 아직 원하는 위치가 아니라면 다음 노드로 이동하고 current_index를 1 증가시키세요.

        # TODO 7. 끝까지 도착했는데 index를 찾지 못했다면 None을 반환하세요.
        pass
    
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