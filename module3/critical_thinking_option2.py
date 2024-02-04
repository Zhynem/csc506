# CSC 506 - Design and Analysis of Algorithms
# Michael Luker
# Feb 4, 2024
"""
Prompt:
Write two Python functions to find the minimum number in a list. The first function should compare 
each number to every other number on the list O(n2). The second function should be linear O(n).
"""
# Need some modules to help with generating random numbers and timing the different functions
import timeit
import random
from typing import List


def cross_compare(nums: List[int]) -> int:
    # For each number, compare it against every other number
    smallest_index = 0
    for i in range(len(nums)):
        smallest = True
        for j in range(len(nums)):
            if nums[i] > nums[j]:
                smallest = False
        if smallest:
            smallest_index = i
    return nums[smallest_index]


def cross_early_stop(nums: List[int]) -> int:
    # For each number, compare it against every other number
    for n1 in nums:
        smallest = False
        for n2 in nums:
            if n1 <= n2:
                smallest = True
                continue
            else:
                # Early stop can happen if you run in to any number that is smaller than n1
                smallest = False
                break
        if smallest:
            return n1


def linear_compare(nums: List[int]) -> int:
    # For each number, check if it's the smallest seen so far, at the end return the smallest num
    smallest = nums[0]
    for n in nums[1:]:
        if n < smallest:
            smallest = n
    return smallest


def run_test(length: int, type: int):
    num_list = [random.randint(0, length * 2) for _ in range(length)]
    random.shuffle(num_list)
    if type == 0:
        smallest = cross_compare(num_list)
    if type == 2:
        smallest = cross_early_stop(num_list)
    elif type == 1:
        smallest = linear_compare(num_list)
    else:
        smallest = min(num_list)
    assert num_list.count(smallest) >= 1


# list_length = 2_000_000
list_length = 5000
num_list = [random.randint(0, list_length * 2) for _ in range(list_length)]
random.shuffle(num_list)
my_res1 = cross_compare(num_list)
my_res2 = linear_compare(num_list)
my_res3 = cross_early_stop(num_list)
py_res = min(num_list)
# print(num_list)
print(cross_compare(num_list))
assert my_res1 == py_res
assert my_res2 == py_res
assert my_res3 == py_res
num_tests = 100
print("Min functions work, getting timings.")
print(f"Average of {num_tests:,} tests with list size of {list_length:,} items")
cross_timing: float = (
    timeit.timeit(lambda: run_test(list_length, 0), number=num_tests) / num_tests
)

# cross2_timing: float = (
#     timeit.timeit(lambda: run_test(list_length, 2), number=num_tests) / num_tests
# )

linear_timing: float = (
    timeit.timeit(lambda: run_test(list_length, 1), number=num_tests) / num_tests
)

python_timing: float = (
    timeit.timeit(lambda: run_test(list_length, 3), number=num_tests) / num_tests
)

print(
    f"Fully Cross: {cross_timing:0.5f}s | Linear: {linear_timing:0.5f}s | Python: {python_timing:0.5f}s"
)

# print(
#     f"Fully Cross: {cross_timing:0.5f}s | Early Stop Cross: {cross2_timing:0.5f}s | Linear: {linear_timing:0.5f}s | Python: {python_timing:0.5f}s"
# )
