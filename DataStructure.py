class MyArray:
    def __init__(self):
        # 데이터를 저장할 내부 리스트
        self.data = []

    def append(self, value):
        # 배열의 맨 뒤에 값을 추가
        self.data.append(value)

    def remove_at(self, index):
        # index 위치의 값을 삭제하기 전에 인덱스가 올바른지 확인
        self._check_index(index)
        
        # pop(index) 는 해당 위치의 값을 삭제하고, 삭제한 값 반환
        return self.data.pop(index)

    def size(self):
        # 배열에 들어있는 데이터 개수 반환
        return len(self.data)

    def _check_index(self, index):
        if index < 0 or index >= len(self.data):
            raise IndexError("인덱스 범위를 벗어났습니다.")

    def __len__(self):
        # len(arr) 형태로 배열의 길이를 구할 수 있게 해준다.
        return len(self.data)

    def __getitem__(self, index):
        # arr[index] 형태로 값을 조회할 수 있게 해준다.
        return len(self.data)

    def __setitem__(self, index, value):
        # arr[index] = value 형태로 값을 수정할 수 있게 해준다.
        self._check_index(index)
        self.data[index] = value

    def __str__(self):
        # print(arr) 를 했을 때 내부 리스트 형태로 출력되게 해준다.
        return str(self.data)


class MyQueue:
    def __init__(self):
        # 데이터를 저장할 내부 리스트
        self.data = []

    def enqueue(self, value):
        # 큐의 맨 뒤에 값을 추가한다.
        self.data.append(value)

    def dequeue(self):
        # 큐가 비어 있으면 값을 꺼낼 수 없다.
        if self.is_empty():
            raise IndexError("큐가 비어 있습니다.")

        # 가장 먼저 들어온 값을 꺼낸다.
        # 리스트의 0번 인덱스가 큐의 앞쪽이다.
        return self.data.pop(0)

    def peek(self):
        # 큐가 비어 있으면 맨 앞 값을 확인할 수 없다.
        if self.is_empty():
            raise IndexError("큐가 비어 있습니다.")

        # 가장 앞에 있는 값을 삭제하지 않고 확인한다.
        return self.data[0]

    def is_empty(self):
        # 큐가 비어 있는지 확인한다.
        return len(self.data) == 0

    def size(self):
        # 큐에 들어있는 데이터 개수를 반환한다.
        return len(self.data)

    def __len__(self):
        # len(queue) 형태로 큐의 길이를 구할 수 있게 해준다.
        return len(self.data)

    def __str__(self):
        # print(queue)를 했을 때 내부 리스트 형태로 출력되게 해준다.
        return str(self.data)
    
    
class MyStack:
    def __init__(self):
        # 데이터를 저장할 내부 리스트
        self.data = []

    def push(self, value):
        # 스택의 맨 위에 값을 추가한다.
        self.data.append(value)

    def pop(self):
        # 스택이 비어 있으면 값을 꺼낼 수 없다.
        if self.is_empty():
            raise IndexError("스택이 비어 있습니다.")

        # 가장 마지막에 들어온 값을 꺼낸다.
        return self.data.pop()

    def peek(self):
        # 스택이 비어 있으면 맨 위 값을 확인할 수 없다.
        if self.is_empty():
            raise IndexError("스택이 비어 있습니다.")

        # 가장 위에 있는 값을 삭제하지 않고 확인한다.
        return self.data[-1]

    def is_empty(self):
        # 스택이 비어 있는지 확인한다.
        return len(self.data) == 0

    def size(self):
        # 스택에 들어있는 데이터 개수를 반환한다.
        return len(self.data)

    def __len__(self):
        # len(stack) 형태로 스택의 길이를 구할 수 있게 해준다.
        return len(self.data)

    def __str__(self):
        # print(stack)을 했을 때 내부 리스트 형태로 출력되게 해준다.
        return str(self.data)
    
    
    
# Array
arr = MyArray()

arr.append(10)
arr.append(20)
arr.append(30)

print(arr)
# [10, 20, 30]

print(len(arr))
# 3

arr[1] = 99
print(arr)
# [10, 99, 30]

deleted_value = arr.remove_at(0)
print(deleted_value)
# 10

print(arr)
# [99, 30]


# MyQueue 
queue = MyQueue()

queue.enqueue("A")
queue.enqueue("B")
queue.enqueue("C")

print(queue)
# ['A', 'B', 'C']

print(queue.peek())
# A

print(queue.dequeue())
# A

print(queue)
# ['B', 'C']

print(queue.size())
# 2

print(queue.is_empty())
# False

# MyStack
stack = MyStack()

stack.push("A")
stack.push("B")
stack.push("C")

print(stack)
# ['A', 'B', 'C']

print(stack.peek())
# C

print(stack.pop())
# C

print(stack)
# ['A', 'B']

print(stack.size())
# 2

print(stack.is_empty())
# False