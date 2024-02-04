# CSC506 - Design and Analysis of Algorithms
# Michael Luker
# Discussion 3

# Prompt: One way to improve the quick sort is to use an insertion sort on lists that have a small
# length ("partition limit"). Why does this make sense? Re-implement the quick sort and use it to
# sort a random list of integers. Share your sort in your initial thread.

# Sources:
# Using timeit
#   https://docs.python.org/3/library/timeit.html
#   https://stackoverflow.com/questions/5086430/how-to-pass-parameters-of-a-function-when-using-timeit-timer
# Python random numbers
#   https://docs.python.org/3/library/random.html#random.randint
# List deep copy
#   https://www.dataquest.io/blog/python-copy-list/
# Insertion Sort pseudo code
#   https://csuglobal.instructure.com/courses/87885/pages/3-dot-2-insertion-sort?module_item_id=4566562
# Quicksort pseudo code
#   https://csuglobal.instructure.com/courses/87885/pages/3-dot-3-quicksort?module_item_id=4566564
#   https://en.wikipedia.org/wiki/Quicksort#Lomuto_partition_scheme

import timeit
import random
from typing import List


def insertion_sort(input_list: List[int], low_index: int, high_index: int):
    # Index over the list
    # for i, current_val in enumerate(input_list):
    # print(f"Insertion sort from {low_index} to {high_index}")
    for i in range(low_index, high_index + 1):
        current_val = input_list[i]
        j = i - 1
        # Slowly scan the list eventually finding the spot where the current value belongs
        # Taking advantage of the fact that each time a new number gets checked the list will be
        # sorted from 0 to i-1
        while j >= 0 and input_list[j] > current_val:
            input_list[j + 1] = input_list[j]
            j -= 1
            input_list[j + 1] = current_val


isq_recursion_count = 0
qs_recursion_count = 0


def insertion_quicksort(
    input_list: List[int], partition_limit: int, low_index: int, high_index: int
):
    global isq_recursion_count
    isq_recursion_count += 1
    # print(f"Working on {input_list} from {low_index} to {high_index}")
    # Make sure the index values never cross or go out of bounds
    if low_index >= high_index or low_index < 0:
        return
    if len(list(range(low_index, high_index))) <= partition_limit:
        insertion_sort(input_list, low_index, high_index)
        return

    # Find the partition point / pivot point
    # p = lomuto_partition(input_list, low_index, high_index)
    p = median_of_three(input_list, low_index, high_index)

    # Then sort both sides by recursively calling it again on each side
    insertion_quicksort(input_list, partition_limit, low_index, p - 1)
    insertion_quicksort(input_list, partition_limit, p + 1, high_index)


def lomuto_partition(input_list: List[int], low_index: int, high_index: int) -> int:
    # Lomuto partition picks the last element in the list as the pivot value
    # Oh, I think this partition step is where it makes sure values in the left half are below
    #   the pivot point, and values above the pivot are in the right half, by recursing down to where
    #   lists are 1 or 2 elements then rebuilding them you ensure a sorted list comes out
    # pivot = input_list[-1] Ah, in python -1 will always give you the end of the list, but the
    # high_index value isn't always going to be at the end of the list, whoops
    pivot = input_list[high_index]
    # Start the pivot index below the current low_index
    i = low_index - 1
    # For each element in the partition range step the pivot index up for lower value numbers
    # and swap their positions
    for j in range(low_index, high_index):
        if input_list[j] <= pivot:
            i += 1
            temp = input_list[i]
            input_list[i] = input_list[j]
            input_list[j] = temp
    # Make sure to keep the pivot index in bounds
    i += 1
    temp = input_list[i]
    input_list[i] = input_list[high_index]
    input_list[high_index] = temp
    # Now the pivot has been found
    return i


def median_of_three(input_list: List[int], low_index: int, high_index: int) -> int:
    mid_index = (low_index + high_index) // 2
    # Sort low, mid, high
    if input_list[high_index] < input_list[low_index]:
        input_list[low_index], input_list[high_index] = (
            input_list[high_index],
            input_list[low_index],
        )
    if input_list[mid_index] < input_list[low_index]:
        input_list[mid_index], input_list[low_index] = (
            input_list[low_index],
            input_list[mid_index],
        )
    if input_list[high_index] < input_list[mid_index]:
        input_list[high_index], input_list[mid_index] = (
            input_list[mid_index],
            input_list[high_index],
        )
    # Place median at the end as pivot
    input_list[mid_index], input_list[high_index] = (
        input_list[high_index],
        input_list[mid_index],
    )
    pivot = input_list[high_index]

    i = low_index - 1
    for j in range(low_index, high_index):
        if input_list[j] <= pivot:
            i += 1
            input_list[i], input_list[j] = input_list[j], input_list[i]
    input_list[i + 1], input_list[high_index] = (
        input_list[high_index],
        input_list[i + 1],
    )
    return i + 1


def quicksort_only(input_list: List[int], low_index: int, high_index: int):
    global qs_recursion_count
    qs_recursion_count += 1
    # print(f"Working on {input_list} from {low_index} to {high_index}")
    # Make sure the index values never cross or go out of bounds
    if low_index >= high_index or low_index < 0:
        return
    # Find the partition point / pivot point
    # p = lomuto_partition(input_list, low_index, high_index)
    p = median_of_three(input_list, low_index, high_index)

    # Then sort both sides by recursively calling it again on each side
    quicksort_only(input_list, low_index, p - 1)
    quicksort_only(input_list, p + 1, high_index)


def run_test(list_size: int, partition_size: int, print_lists: bool = False) -> None:
    # Generate a list at the desired size with numbers from 0 to 100_000
    number_list = [random.randint(0, 100_000) for _ in range(list_size)]
    # Make sure it's good and mixed up
    random.shuffle(number_list)
    random.shuffle(number_list)
    random.shuffle(number_list)

    # Copy the list before it goes through the sorting process
    verify_list = number_list.copy()

    if print_lists:
        print("Number list before sort:")
        print(number_list)
        print()

    # If partition size is -1 I'll use it as a flag to test that my insertion sort works properly
    if partition_size == -1:
        insertion_sort(number_list, 0, list_size - 1)
    # If partition size is 0 it's quick only, otherwise run the combined one
    elif partition_size == 0:
        quicksort_only(number_list, 0, list_size - 1)
    else:
        insertion_quicksort(number_list, partition_size, 0, list_size - 1)

    if print_lists:
        print("Number list after sort:")
        print(number_list)
        print()

    # Verify the number list is now sorted
    verify_list.sort()
    assert number_list == verify_list
    if print_lists:
        print("Assertion worked")
        print()


# Code to handle generating lists and running tests
if __name__ == "__main__":
    # Create a grid of list length and partition limit to compare results
    # test_list_sizes = [64, 128, 1024, 4096, 8192, 16384, 65536, 131072]
    # test_partition_limit_sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
    test_list_sizes = [10_000_000]
    test_partition_limit_sizes = [64, 256, 1024]

    insertion_quick_results = {}
    quick_only_results = {}

    # Start with a small test to make sure insertion sort is working
    # run_test(8, -1, True)
    # run_test(8, 0, True)
    # run_test(100_000, -1) # Takes about 1 min 40 sec to insertion sort the list of 100k numbers
    # run_test(65536, -1)  # Takes about 40 seconds to insertion sort list of 65k numbers
    # run_test(8, 0)

    # With quicksort working it takes about 10 seconds to sort 100 unique lists, way faster
    # print(timeit.timeit(lambda: run_test(65536, 0), number=100))
    # run_test(100_000, 0) # Takes 0.218 seconds to run quicksort on list of 100k numbers

    # With insertion + quicksort it takes about 10 seconds again with limit of 32
    # print(timeit.timeit(lambda: run_test(65536, 32), number=100))
    # run_test(100_000, 0) # Takes 0.218 seconds to run quicksort on list of 100k numbers

    # Verify the insertion quicksort has a lower recursion / function call amount as expected
    # run_test(100_000, 0)
    # run_test(100_000, 256)
    # print(f"InsQuick  max recursion depth: {isq_recursion_count}")
    # print(f"Quicksort max recursion depth: {qs_recursion_count}")
    # print()

    num_tests = 1

    # Run the full range of tests
    for list_size in test_list_sizes:
        print(f"Testing list size: {list_size}")
        insertion_quick_results[list_size] = {}
        for partition_size in test_partition_limit_sizes:
            insertion_quick_results[list_size][partition_size] = timeit.timeit(
                lambda: run_test(list_size, partition_size, False), number=num_tests
            )
        quick_only_results[list_size] = timeit.timeit(
            lambda: run_test(list_size, 0, False), number=num_tests
        )
    print()
    print("Insertion + Quicksort Results: ")
    # Print the grid of results

    print_header = f"{'list size':^10} | "
    for pl in test_partition_limit_sizes:
        print_header += f"{pl:^7} | "
    print("           |" + f"{'partition limit size':^{len(print_header)-14}}|")
    print(print_header)
    print("           |" + "=" * (len(print_header) - 13))
    for ls_key in insertion_quick_results.keys():
        print_string = f"{ls_key:^10} | "
        for pl_key in insertion_quick_results[ls_key].keys():
            print_string += f"{insertion_quick_results[ls_key][pl_key]:0.4f}s | "
        print(print_string)
    print()

    print("Standard Quicksort Results:")
    for ls_key in quick_only_results.keys():
        print_string = f"{ls_key:^10} | "
        print_string += f"{quick_only_results[ls_key]:0.4f}s | "
        print(print_string)
    print()
