from MaxHeap import MaxHeap
from MinHeap import MinHeap


LINE_WIDTH = 72


def print_title(title):
    line = "=" * LINE_WIDTH
    print(f"\n{line}")
    print(title.center(LINE_WIDTH))
    print(line)


def print_step(message):
    print(f"\n{'-' * LINE_WIDTH}")
    print(f"> {message}")
    print("-" * LINE_WIDTH)


def print_array(heap):
    print(f"배열: {heap}")


def print_index_table(heap):
    print("\n인덱스 관계")
    print("-" * LINE_WIDTH)

    if not heap:
        print("비어 있는 힙입니다.")
        return

    print(f"{'index':^8}{'value':^8}{'parent':^10}{'left':^10}{'right':^10}")
    print("-" * 46)

    for index, value in enumerate(heap):
        parent_index = (index - 1) // 2 if index > 0 else None
        left_index = index * 2 + 1
        right_index = index * 2 + 2

        parent = heap[parent_index] if parent_index is not None else None
        left = heap[left_index] if left_index < len(heap) else None
        right = heap[right_index] if right_index < len(heap) else None

        print(
            f"{index:^8}"
            f"{value:^8}"
            f"{str(parent):^10}"
            f"{str(left):^10}"
            f"{str(right):^10}"
        )


def print_tree(heap):
    if not heap:
        print("비어 있는 힙입니다.")
        return

    levels = []
    index = 0

    while index < len(heap):
        level_count = len(levels)
        node_count = 2 ** level_count
        levels.append(heap[index:index + node_count])
        index += node_count

    height = len(levels)
    cell_width = 4
    tree_width = (2 ** height) * cell_width

    print("트리:")

    for level_index, level_values in enumerate(levels):
        node_line = [" "] * tree_width
        branch_line = [" "] * tree_width
        gap = tree_width // (2 ** (level_index + 1))

        for position, value in enumerate(level_values):
            center = gap * (2 * position + 1)
            value_text = str(value)
            start = center - len(value_text) // 2

            for offset, char in enumerate(value_text):
                if 0 <= start + offset < tree_width:
                    node_line[start + offset] = char

            left_child_index = (2 ** level_index - 1 + position) * 2 + 1
            right_child_index = left_child_index + 1

            if level_index < height - 1:
                branch_gap = max(gap // 2, 1)

                if left_child_index < len(heap):
                    left_pos = center - branch_gap
                    if 0 <= left_pos < tree_width:
                        branch_line[left_pos] = "/"

                if right_child_index < len(heap):
                    right_pos = center + branch_gap
                    if 0 <= right_pos < tree_width:
                        branch_line[right_pos] = "\\"

        print("".join(node_line).rstrip())

        if level_index < height - 1:
            print("".join(branch_line).rstrip())


def print_heap_state(heap, label):
    print_step(label)
    print_array(heap.heap)
    print_tree(heap.heap)
    print_index_table(heap.heap)


def insert_with_visual(heap, values):
    for value in values:
        before = heap.heap[:]
        heap.insert(value)
        print_step(f"insert({value})")
        print(f"이전: {before}")
        print_array(heap.heap)
        print_tree(heap.heap)


def delete_with_visual(heap, count):
    for _ in range(count):
        before = heap.heap[:]
        removed = heap.delete()
        print_step(f"delete() -> {removed}")
        print(f"이전: {before}")
        print_array(heap.heap)
        print_tree(heap.heap)


def run_max_heap(values):
    print_title("MAX HEAP VISUALIZER")
    print("규칙: 부모 노드 >= 자식 노드")
    print("삭제: 가장 큰 값이 먼저 제거됨")

    max_heap = MaxHeap()

    insert_with_visual(max_heap, values)
    print_heap_state(max_heap, "최대 힙 최종 상태")
    delete_with_visual(max_heap, 2)


def run_min_heap(values):
    print_title("MIN HEAP VISUALIZER")
    print("규칙: 부모 노드 <= 자식 노드")
    print("삭제: 가장 작은 값이 먼저 제거됨")

    min_heap = MinHeap()

    insert_with_visual(min_heap, values)
    print_heap_state(min_heap, "최소 힙 최종 상태")
    delete_with_visual(min_heap, 2)


def main():
    values = [30, 10, 50, 20, 40]

    print_title("HEAP TERMINAL VISUALIZER")
    print(f"삽입할 값: {values}")
    print("같은 데이터를 MaxHeap과 MinHeap에 넣어 구조 차이를 비교합니다.")

    run_max_heap(values)
    run_min_heap(values)


if __name__ == "__main__":
    main()
