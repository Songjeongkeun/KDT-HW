# divide_conquer.py

def merge(left, right):
    result = []
    
    left_idx = 0
    right_idx = 0
    
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] <= right[right_idx]:
            result.append(left[left_idx])
            left_idx += 1
        else:
            result.append(right[right_idx])
            right_idx += 1
    
    result.extend(left[left_idx:])
    result.extend(right[right_idx:])
    
    return result

def merge_sort(data):
    
    if len(data) == 1:
        return data
    
    middle = len(data) // 2
    
    left = merge_sort(data[:middle])
    right = merge_sort(data[middle:])
         
    return merge(left, right)

def quick_sort(data):
    
    if len(data) <= 1:
        return data
    
    pivot = data[len(data) // 2]
    
    left = [num for num in data if num < pivot]
    middle = [num for num in data if num == pivot]
    right = [num for num in data if num > pivot] 
    
    return quick_sort(left) + middle + quick_sort(right)


# data = [38, 27, 43, 3, 9, 82, 10]

# sorted_data = merge_sort(data)

# print("정렬 전:", data)
# print("정렬 후:", sorted_data)

# data = [5, 3, 8, 4, 2, 7, 1, 10]

# sorted_daata = quick_sort(data)

# print("정렬 전:", data)
# print("정렬 후:", sorted_data)