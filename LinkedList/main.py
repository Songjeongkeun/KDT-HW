# main.py
from linked_list_skeleton import LinkedList

# 터미널에 메뉴를 출력하는 함수
def print_menu():
    
    print()
    print("=== Linked List Terminal Viewer ===")
    print("1. append  : 맨 뒤에 노드 추가")
    print("2. prepend : 맨 앞에 노드 추가")
    print("3. insert  : 원하는 인덱스에 노드 추가")
    print("4. delete  : 값으로 노드 삭제")
    print("5. find    : 값으로 노드 검색")
    print("6. get     : 인덱스로 노드 정보 조회")
    print("7. show    : 링크드리스트 출력")
    print("0. exit    : 종료")
    print()
    
# 올바른 인덱스를 입력할 때까지 인덱스와 값을 다시 입력받는 구문
def input_insert(linked_list):
    
    while True:
        index_text = input("추가할 인덱스를 입력하세요: ").strip()

        # index_text가 정수로 변환 가능한지 확인, 음수도 허용하게 작성한 코드
        if not index_text.lstrip("-").isdigit():
            print("인덱스는 정수로 입력해야 합니다. 다시 입력해 주세요.")
            continue
        
        index = int(index_text)
        value = input("추가할 값을 입력하세요: ").strip()

        if linked_list.insert(index, value):
            print(f"{index}번 인덱스에 '{value}' 값을 추가했습니다.")
            break
        
        # 인덱스가 유효하지 않은 경우 최대 인덱스를 안내하는 메시지를 출력
        max_index = linked_list.length()
        print(f"유효하지 않은 인덱스입니다. 현재 삽입 가능한 인덱스는 0부터 {max_index}까지입니다.")
        print("다시 입력해 주세요.")


# 인덱스를 입력받아 해당 위치의 값을 출력합니다.
def input_get(linked_list):
    index_text = input("조회할 인덱스를 입력하세요: ").strip()

    if not index_text.lstrip("-").isdigit():
        print("인덱스는 정수로 입력해야 합니다.")
        return

    index = int(index_text)
    # 인덱스에 있는 value와 next를 가져옵니다. 인덱스가 유효하지 않으면 value는 None이 됩니다.
    value = linked_list.get(index)
    next = linked_list.get_next(index)

    if value is None:
        max_index = linked_list.length() - 1

        if max_index < 0:
            print("현재 링크드리스트가 비어 있습니다.")
        else:
            print(f"유효하지 않은 인덱스입니다. 현재 조회 가능한 인덱스는 0부터 {max_index}까지입니다.")
    else:
        print(f"{index}번 인덱스의 값은 '{value}'입니다.")
        if next is not None:
            print(f"{index}번 인덱스가 갖고있는 reference는 '{next}'입니다.")
        else:
            print(f"{index}번 인덱스의 다음 노드는 None입니다.")


# 링크드리스트를 터미널에서 조작하는 메인 함수입니다.
def main():
    linked_list = LinkedList()

    while True:
        print_menu()
        print(linked_list.display())

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
            print(linked_list.display())

        elif command in ("0", "exit", "quit", "q"):
            print("프로그램을 종료합니다.")
            break

        else:
            print("알 수 없는 명령어입니다.")


if __name__ == "__main__":
    main()