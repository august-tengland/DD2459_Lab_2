
# ------------ SORT & BINARY SEARCH -----------------
# Implementation in Python, by August Tengland & Michael Ask

import os.path
import numpy as np
import signal

# Sorting of integer arrays of arbitrary length (i)
# Implemented using bubble-sort
def bubble_sort(array: list) -> None:
    
    for _ in range(len(array)-1):
        swapped = False 
        for i in range(len(array)-1):
            if array[i] > array[i+1]:
                # Swap elements
                temp = array[i]
                array[i] = array[i+1]
                array[i+1] = temp
                swapped = True
        if not swapped: 
            break
    
    return array

# membership queries on sorted arrays of arbitrary length 
# using binary search (ii)
def binary_search(ordered_array: list, elem: int) -> bool:

    l = 0 
    r = len(ordered_array) -1

    while (l <= r): 
        midpoint = int((l + r) / 2)
        if ordered_array[midpoint] == elem:
            return True
        elif ordered_array[midpoint] < elem:
            l = midpoint + 1
        else:
            r = midpoint - 1
    return False

# membership queries on unsorted arrays of arbitrary length, 
# by combining previous functions (iii)
def unordered_binary_search(array: list, elem: int) -> bool:

    arr_copy = array.copy()
    bubble_sort(arr_copy)
    return binary_search(arr_copy, elem)

# ------------ TESTING & TEST GENERATION -----------------

test_list_length = 20

def generate_random_test_file() -> None:
    f = open("random_tests.txt", "w")
    num_elems_in_lists = 0
    for num_tests in range(100):
        random_list = np.random.randint(-1000,1000,test_list_length).tolist()
        # approx. 50/50 chance that the element is actually in the list (pass test)
        if num_tests % 2 == 0: 
            random_index = np.random.randint(0,20)
            elem_to_find = random_list[random_index]
        else:
            elem_to_find = np.random.randint(-1500,1500) 
        if elem_to_find in random_list:
            num_elems_in_lists += 1
        f.write(str(elem_to_find) + "\n")
        f.write(" ".join(str(x) for x in random_list) + "\n")
    # Running this line should give you a percentage of 50% +- 1%
    # print(str(num_elems_in_lists/100)) 
    f.close()

# def generate_pairwise_test_file():
    
def random_tester() -> int:
    num_tests_until_error_found = 0
    if os.path.isfile("random_tests.txt"):

        f = open("random_tests.txt", "r")
        for new_test in f:
            num_tests_until_error_found += 1
            elem_to_find = int(new_test)
            test_list = [eval(i) for i in list(f.readline().split())]
            expected_result = search_oracle(test_list,elem_to_find)  
            actual_result = unordered_binary_search(test_list,elem_to_find)
            if not expected_result == actual_result:
                f.close()
                return num_tests_until_error_found
        else:
            f.close() 
            return -1    
    else:
        raise FileNotFoundError

def get_average_random_test_result(num_tests: int) -> None:
    avg_result = 0
    for i in range(num_tests):
        generate_random_test_file()
        test_result = random_tester() 
        if test_result == -1:
            avg_result += 101 / num_tests
        else: 
            avg_result += test_result / num_tests
        
    print(str(round(avg_result,2)))

def search_oracle(array: list, elem: int) -> bool:
    return elem in array
 

get_average_random_test_result(100)


