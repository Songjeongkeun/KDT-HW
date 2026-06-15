import random
import time
import basic_sort as basicSort
import divide_conquer as divideConquer


basic_sort_functions = {
    "버블 정렬": basicSort.bubble_sort,
    "선택 정렬": basicSort.selection_sort,
    "삽입 정렬": basicSort.insertion_sort
}

divide_conquer_sort_functions = {
    "병합 정렬": divideConquer.merge_sort,
    "퀵 정렬" : divideConquer.quick_sort
}


def basic_sort_benchmark(sizes=(100, 1000, 10000), repeat=1, seed=100):
    # seed 고정 : 다시 실행해도 같은 랜덤 데이터를 생성하기 위해서
    random_data = random.Random(seed)

    print()
    print(f"성능 비교: 각 조건 {repeat}회 평균")
    print(f"{'data 크기':5} {'알고리즘':>10} {'방향(오름/내림)':>6} {'평균 시간':14}")
    print("-" * 50)

    for size in sizes:
        origin_data = [random_data.randint(1, size * 100)
                       for _ in range(size)]

        for name, sort_funtion in basic_sort_functions.items():
            for reverse, direction in ((False, "오름차순"), (True, "내림차순")):
                elapsed_times = []
                
                for _ in range(repeat):
                    start_time = time.time()
                    # 파이썬 내장 함수 sort 로 정렬한 data 와 비교 필요
                    # 내가 짠 함수가 정렬을 잘 했는지 확인
                    # 어디서 비교를 해야 하지?
                    result = sort_funtion(origin_data, reverse)
                    elapsed_times.append(time.time() - start_time)
                    
                avg_time = sum(elapsed_times) / repeat * 1000
                
                print(f"{size:7,} {name:>10} {direction:>6} {avg_time:10.2f}ms")
        
def divide_conquer_benchmark(sizes=(100, 1000, 10000, 100000, 1000000), repeat=3, seed=1000):
    # seed 고정 : 다시 실행해도 같은 랜덤 데이터를 생성하기 위해서
    random_data = random.Random(seed)
    
    print()
    print(f"성능 비교: 각 조건 {repeat}회 평균")
    print(f"{'크기':5} {'알고리즘':>10} {'평균 시간':14}")
    print("-" * 50)

    for size in sizes:
        origin_data = [random_data.randint(1, size * 100)
                       for _ in range(size)]

        for name, sort_funtion in divide_conquer_sort_functions.items():
            elapsed_times = []
            
            for _ in range(repeat):
                start_time = time.time()
                # 파이썬 내장 함수 sort 로 정렬한 data 와 비교 필요
                # 내가 짠 함수가 정렬을 잘 했는지 확인
                # 어디서 비교를 해야 하지?
                result = sort_funtion(origin_data)
                elapsed_times.append(time.time() - start_time)
                    
            avg_time = sum(elapsed_times) / repeat * 1000
                
            print( f"{size:7,} {name:>10} {avg_time:10.2f}ms")


if __name__ == "__main__":
    # basic_sort_benchmark()
    divide_conquer_benchmark()
