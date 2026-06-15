class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, value):
        self.heap.append(value)
        self.heapify_up(len(self.heap) - 1)

    def delete(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down(0)

        return root

    def heapify_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2

            if self.heap[parent_index] <= self.heap[index]:
                break

            self.heap[parent_index], self.heap[index] = (
                self.heap[index],
                self.heap[parent_index],
            )
            index = parent_index

    def heapify_down(self, index):
        size = len(self.heap)

        while True:
            left_index = index * 2 + 1
            right_index = index * 2 + 2
            smallest_index = index

            if left_index < size and self.heap[left_index] < self.heap[smallest_index]:
                smallest_index = left_index

            if right_index < size and self.heap[right_index] < self.heap[smallest_index]:
                smallest_index = right_index

            if smallest_index == index:
                break

            self.heap[index], self.heap[smallest_index] = (
                self.heap[smallest_index],
                self.heap[index],
            )
            index = smallest_index

    def print_heap(self):
        print(self.heap)


