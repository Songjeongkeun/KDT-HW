# basic_sort.py

def bubble_sort(data, reverse=False):
    # 버블 정렬: 인접한 두 값을 비교해 큰 값을 뒤로 보낸다.
    # 원본 리스트가 변경되지 않도록 복사본을 만들어 정렬한다.
    result = data.copy()
    length = len(result)

    # 반복이 한 번 끝날 때마다 뒤쪽 값 하나가 정렬된다.
    # 따라서 다음 반복에서는 비교 범위를 한 칸 줄인다.
    for end in range(length - 1, 0, -1):
        # 이번 반복에서 값의 교환이 있었는지 기록한다.
        swapped = False

        # 현재 값과 바로 다음 값을 차례로 비교한다.
        for index in range(end):
            # 오름차순은 앞의 값이 더 클 때 교환한다.
            # 내림차순은 앞의 값이 더 작을 때 교환한다.
            should_swap = (
                result[index] < result[index + 1]
                if reverse
                else result[index] > result[index + 1]
            )

            if should_swap:
                # Python의 다중 할당을 이용해 두 값의 위치를 바꾼다.
                result[index], result[index + 1] = (
                    result[index + 1],
                    result[index],
                )
                swapped = True

        # 교환이 없었다면 이미 정렬된 상태이므로 반복을 종료한다.
        if not swapped:
            break

    return result


def selection_sort(data, reverse=False):
    # 선택 정렬: 정렬되지 않은 영역에서 최솟값 또는 최댓값을 선택한다.
    # 원본 데이터를 보호하기 위해 리스트를 복사한다.
    result = data.copy()
    length = len(result)

    # start 앞쪽은 이미 정렬된 영역이다.
    for start in range(length - 1):
        # 우선 정렬되지 않은 영역의 첫 위치를 선택한다.
        selected = start

        # 남은 영역에서 최솟값 또는 최댓값의 위치를 찾는다.
        for index in range(start + 1, length):
            # 오름차순은 더 작은 값을, 내림차순은 더 큰 값을 선택한다.
            should_select = (
                result[index] > result[selected]
                if reverse
                else result[index] < result[selected]
            )

            if should_select:
                selected = index

        # 선택한 값이 현재 위치에 있지 않을 때만 교환한다.
        if selected != start:
            result[start], result[selected] = result[selected], result[start]

    return result


def insertion_sort(data, reverse=False):
    # 삽입 정렬: 현재 값을 앞쪽의 정렬된 영역에 삽입한다.
    # 원본 리스트 대신 복사본을 정렬한다.
    result = data.copy()

    # 첫 번째 값은 이미 정렬되었다고 보고 두 번째 값부터 시작한다.
    for index in range(1, len(result)):
        # 정렬된 영역에 삽입할 현재 값을 임시로 저장한다.
        current = result[index]
        position = index - 1

        # 현재 값이 들어갈 위치를 찾을 때까지 앞쪽 값을 이동한다.
        while position >= 0:
            # 오름차순은 현재 값보다 큰 값을 오른쪽으로 이동한다.
            # 내림차순은 현재 값보다 작은 값을 오른쪽으로 이동한다.
            should_move = (
                result[position] < current
                if reverse
                else result[position] > current
            )

            # 이동할 필요가 없다면 현재 값의 삽입 위치를 찾은 것이다.
            if not should_move:
                break

            result[position + 1] = result[position]
            position -= 1

        # 값의 이동으로 생긴 빈자리에 현재 값을 삽입한다.
        result[position + 1] = current

    return result

