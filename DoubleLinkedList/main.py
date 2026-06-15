from double_linked_list import DoubleLinkedList


def print_menu():
    """터미널에 더블 링크드 리스트 조작 메뉴를 출력한다."""
    print()
    print("=== Double Linked List Terminal Viewer ===")
    print("1. append  : 맨 뒤에 노드 추가")
    print("2. prepend : 맨 앞에 노드 추가")
    print("3. insert  : 원하는 인덱스에 노드 추가")
    print("4. delete  : 값으로 노드 삭제")
    print("5. find    : 값으로 노드 검색")
    print("6. get     : 인덱스로 노드와 연결 정보 조회")
    print("7. show    : 정방향과 역방향 출력")
    print("0. exit    : 종료")
    print()


def display_list(linked_list):
    """리스트를 head 방향과 tail 방향에서 각각 출력한다."""
    print("\n[정방향]")
    print(linked_list.display())

    print("\n[역방향]")
    print(linked_list.display_reverse())


def input_insert(linked_list):
    """올바른 인덱스를 입력할 때까지 삽입 정보를 다시 입력받는다."""
    while True:
        index_text = input("추가할 인덱스를 입력하세요: ").strip()

        if not index_text.lstrip("-").isdigit():
            print("인덱스는 정수로 입력해야 합니다. 다시 입력해 주세요.")
            continue

        index = int(index_text)
        value = input("추가할 값을 입력하세요: ").strip()

        if linked_list.insert(index, value):
            print(f"{index}번 인덱스에 '{value}' 값을 추가했습니다.")
            return

        max_index = linked_list.length()
        print(
            f"유효하지 않은 인덱스입니다. "
            f"현재 삽입 가능한 인덱스는 0부터 {max_index}까지입니다."
        )
        print("다시 입력해 주세요.")


def node_value(node):
    """Node 객체가 있으면 저장된 값을 반환하고, 없으면 None을 반환한다."""
    if node is None:
        return None

    return node.value


def input_get(linked_list):
    """인덱스에 있는 노드의 값, prev, next 정보를 출력한다."""
    index_text = input("조회할 인덱스를 입력하세요: ").strip()

    if not index_text.lstrip("-").isdigit():
        print("인덱스는 정수로 입력해야 합니다.")
        return

    index = int(index_text)
    node = linked_list.get_node(index)

    if node is None:
        max_index = linked_list.length() - 1

        if max_index < 0:
            print("현재 더블 링크드 리스트가 비어 있습니다.")
        else:
            print(
                f"유효하지 않은 인덱스입니다. "
                f"현재 조회 가능한 인덱스는 0부터 {max_index}까지입니다."
            )
        return

    prev_value = node_value(linked_list.get_prev(index))
    next_value = node_value(linked_list.get_next(index))

    print(f"\n{index}번 인덱스의 노드 정보")
    print(f"value : {node.value}")
    print(f"prev  : {prev_value}")
    print(f"next  : {next_value}")

    print("\n연결 구조")
    print(f"[{prev_value}] <-> [{node.value}] <-> [{next_value}]")


def main():
    linked_list = DoubleLinkedList()

    while True:
        print_menu()
        display_list(linked_list)

        command = input("\n명령어를 입력하세요: ").strip().lower()

        if command in ("1", "append"):
            value = input("추가할 값을 입력하세요: ").strip()
            linked_list.append(value)
            print(f"'{value}' 값을 맨 뒤에 추가했습니다.")

        elif command in ("2", "prepend"):
            value = input("추가할 값을 입력하세요: ").strip()
            linked_list.prepend(value)
            print(f"'{value}' 값을 맨 앞에 추가했습니다.")

        elif command in ("3", "insert"):
            input_insert(linked_list)

        elif command in ("4", "delete"):
            value = input("삭제할 값을 입력하세요: ").strip()

            if linked_list.delete(value):
                print(f"'{value}' 값을 삭제했습니다.")
            else:
                print(f"'{value}' 값을 찾지 못했습니다.")

        elif command in ("5", "find"):
            value = input("검색할 값을 입력하세요: ").strip()
            index = linked_list.find(value)

            if index == -1:
                print(f"'{value}' 값을 찾지 못했습니다.")
            else:
                print(f"'{value}' 값은 {index}번 인덱스에 있습니다.")

        elif command in ("6", "get"):
            input_get(linked_list)

        elif command in ("7", "show"):
            display_list(linked_list)

        elif command in ("0", "exit", "quit", "q"):
            print("프로그램을 종료합니다.")
            break

        else:
            print("알 수 없는 명령어입니다.")


if __name__ == "__main__":
    main()
