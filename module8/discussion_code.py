# CSC 506 - Design and Analysis of Algorithms
# Module 8 - Discussion
# Michael Luker
# March 7, 2024
import sys

sys.setrecursionlimit(5000)

"""
Prompt:
A bubble sort can be modified to "bubble" in both directions. The first pass moves "up" the list, 
and the second pass moves "down." This alternating pattern continues until no more passes are 
necessary. 

Implement this variation and describe under what circumstances it might be appropriate.

From Dr. Dong Nguyen
In your post, please provide a description of the modification, including complexity analysis, and, 
if possible, conduct benchmark analysis on the code using a variety of datasets.

As a side note, below are the time complexities of different sort algorithms:

Bubble Sort: O(n^2)
Selection Sort: O(n^2)
Insertion Sort: O(n^2)
Merge Sort: O(n log n)
Quick Sort: O(n log n) on average
Heap Sort: O(n log n)

"""
# According to ChatGPT this is called a cocktail shaker sort. It also mentioned that in sorting
# there is the idea of "rabbit" and "turtle" movers. Rabbits move through the list quickly while
# turtles move slowly. An example being a small number toward the end of the unsorted list for
# bubble sort. With a standard bubble sort that small number will take many (possibly N) iterations
# to move to the beginning of the list. By doing the cocktail shaker method it can more quickly
# move these types of numbers to where they belong.


import json
import random
from typing import List
from time import perf_counter


shaker_outer_loops = {"sorted": {}, "reversed": {}, "random": {}}
bubble_outer_loops = {"sorted": {}, "reversed": {}, "random": {}}

shaker_total_loops = {"sorted": {}, "reversed": {}, "random": {}}
bubble_total_loops = {"sorted": {}, "reversed": {}, "random": {}}

shaker_total_comparisons = {"sorted": {}, "reversed": {}, "random": {}}
bubble_total_comparisons = {"sorted": {}, "reversed": {}, "random": {}}


def bubble_up(num_list: List, list_size: int, loop_num: int) -> bool:
    swap_happened = False
    total_loops = 0
    comparisons = 0
    # for i in range(loop_num, list_size - (1 + loop_num)):
    for i in range(list_size - 1):
        # print(f"Bubble Up  : Checking {i} & {i+1}")
        n1 = num_list[i]
        n2 = num_list[i + 1]
        comparisons += 1
        if n1 > n2:
            num_list[i], num_list[i + 1] = num_list[i + 1], num_list[i]
            swap_happened = True
        total_loops += 1
    return swap_happened, total_loops, comparisons


def bubble_down(num_list: List, list_size: int, loop_num: int) -> bool:
    swap_happened = False
    total_loops = 0
    comparisons = 0
    # for i in range(list_size - (1 + loop_num), loop_num, -1):
    for i in range(list_size - 1, 1, -1):
        # print(f"Bubble Down: Checking {i} & {i-1}")
        n1 = num_list[i]
        n2 = num_list[i - 1]
        comparisons += 1
        if n1 < n2:
            num_list[i], num_list[i - 1] = num_list[i - 1], num_list[i]
            swap_happened = True
        total_loops += 1
    return swap_happened, total_loops, comparisons


def shaker_sort(num_list: List, early_cutoff: int = None) -> None:
    if early_cutoff == 0:
        return
    outer_loop = 0
    total_loop = 0
    comparisons = 0
    list_size = len(num_list)
    # Worst case we have to loop over everything
    while outer_loop < list_size:
        if outer_loop == early_cutoff:
            break

        up_swap, up_loops, up_comparisons = bubble_up(num_list, list_size, outer_loop)

        total_loop += up_loops
        comparisons += up_comparisons

        # If there were no swaps going up then the list is sorted and we can end early
        if not up_swap:
            break

        down_swap, down_loops, down_comparisons = bubble_down(
            num_list, list_size, outer_loop
        )

        total_loop += down_loops
        comparisons += down_comparisons

        outer_loop += 1
    # print(f"Shaker Loops taken: {loop}")
    return outer_loop, total_loop, comparisons


def std_bubble(num_list: List) -> int:
    outer_loop = 0
    total_loop = 0
    comparisons = 0
    list_size = len(num_list)
    # Worst case we have to loop over everything
    while outer_loop < list_size:
        swap_happened = False

        # Each time this completes one more number will have moved to its appropriate spot at the
        # end of the list, meaning next time we don't have to do as many checks
        # for i in range(list_size - (1 + outer_loop)):
        for i in range(list_size - 1):
            n1 = num_list[i]
            n2 = num_list[i + 1]
            comparisons += 1
            if n1 > n2:
                num_list[i], num_list[i + 1] = num_list[i + 1], num_list[i]
                swap_happened = True
            total_loop += 1

        # If no swaps were done at all then the list is sorted and we can end early
        if not swap_happened:
            break
        outer_loop += 1
    # print(f"Bubble Loops taken: {loop}")
    return outer_loop, total_loop, comparisons


def reset_lists(size: int = 100) -> tuple[List, List, List]:
    """
    Reset the lists with the given size.

    Args:
        size (int): The size of the lists. Defaults to 100.

    Returns:
        tuple[List, List, List]: A tuple containing three lists: pre, rev, and rand.
            - pre: A list of numbers from 1 to size.
            - rev: A list of numbers from size to 1.
            - rand: A list of random numbers between 0 and size*2 (inclusive), shuffled.

    """
    pre = list(range(1, size + 1))
    rev = list(range(size, 0, -1))
    # rand = [random.randint(0, size * 2) for _ in range(size)]
    rand = list(range(1, size))
    rand.append(0)
    # print(rand)
    # random.shuffle(rand)
    return pre, rev, rand


def sort_list(method: callable, type: str, nums: list) -> float:
    start = perf_counter()
    outer_loops, total_loops, comparisons = method(nums)
    end = perf_counter()
    # I decided I wanted to store the loop counts as well now...
    if method == shaker_sort:
        size = len(nums)
        if size in shaker_outer_loops[type].keys():
            shaker_outer_loops[type][size].append(outer_loops)
            shaker_total_loops[type][size].append(total_loops)
            shaker_total_comparisons[type][size].append(comparisons)
        else:
            shaker_outer_loops[type][size] = [outer_loops]
            shaker_total_loops[type][size] = [total_loops]
            shaker_total_comparisons[type][size] = [comparisons]
    else:
        size = len(nums)
        if size in bubble_outer_loops[type].keys():
            bubble_outer_loops[type][size].append(outer_loops)
            bubble_total_loops[type][size].append(total_loops)
            bubble_total_comparisons[type][size].append(comparisons)
        else:
            bubble_outer_loops[type][size] = [outer_loops]
            bubble_total_loops[type][size] = [total_loops]
            bubble_total_comparisons[type][size] = [comparisons]

    if nums == sorted(nums):
        return end - start
    else:
        return -1


def run_sort_test(size: int, num_tests: int) -> tuple[dict, dict]:
    shaker_timings = {"sorted": [], "reversed": [], "random": []}
    bubble_timings = {"sorted": [], "reversed": [], "random": []}
    for _ in range(num_tests):
        if _ % 25 == 0:
            print(f"Test: {_}")
        # Gather result on shaker sort
        pre_sorted, rev_sorted, rand_list = reset_lists(size)
        # Save a copy so std bubble can use the exact same list
        rand_copy = rand_list.copy()
        # print("Pre  shaker")
        # print(pre_sorted)
        # print(rev_sorted)
        # print(rand_list)
        shaker_timings["sorted"].append(sort_list(shaker_sort, "sorted", pre_sorted))
        shaker_timings["reversed"].append(
            sort_list(shaker_sort, "reversed", rev_sorted)
        )
        shaker_timings["random"].append(sort_list(shaker_sort, "random", rand_list))
        # print("Post shaker")
        # print(pre_sorted)
        # print(rev_sorted)
        # print(rand_list)

        # Then reset the lists and gather results on
        pre_sorted = sorted(pre_sorted)
        rev_sorted = sorted(rev_sorted, reverse=True)

        # print("Pre  bubble")
        # print(pre_sorted)
        # print(rev_sorted)
        # print(rand_copy)
        bubble_timings["sorted"].append(sort_list(std_bubble, "sorted", pre_sorted))
        bubble_timings["reversed"].append(sort_list(std_bubble, "reversed", rev_sorted))
        bubble_timings["random"].append(sort_list(std_bubble, "random", rand_copy))
        # print("Post bubble")
        # print(pre_sorted)
        # print(rev_sorted)
        # print(rand_copy)

    # Return the averaged results
    return {
        "sorted": sum(shaker_timings["sorted"]) / num_tests,
        "reversed": sum(shaker_timings["reversed"]) / num_tests,
        "random": sum(shaker_timings["random"]) / num_tests,
    }, {
        "sorted": sum(bubble_timings["sorted"]) / num_tests,
        "reversed": sum(bubble_timings["reversed"]) / num_tests,
        "random": sum(bubble_timings["random"]) / num_tests,
    }


# Function to find the partition position
def partition(array, low, high):

    # choose the rightmost element as pivot
    pivot = array[high]

    # pointer for greater element
    i = low - 1

    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j] <= pivot:

            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1

            # Swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])

    # Swap the pivot element with the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])

    # Return the position from where partition is done
    return i + 1


# function to perform quicksort


def quickSort(array, low, high):
    if low < high:

        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partition(array, low, high)

        # Recursive call on the left of pivot
        quickSort(array, low, pi - 1)

        # Recursive call on the right of pivot
        quickSort(array, pi + 1, high)


if __name__ == "__main__":
    TESTS = 25
    # TESTS = 1
    # TESTS = 1
    # A little too lofty
    # sizes = [100, 500, 1000, 10000, 50000, 100_000, 1_000_000]
    sizes = [
        # 10,
        # 50,
        # 100,
        # 200,
        # 400,
        # 500,
        # 1000,
        # 2000,
        # 5000,
        10_000,
        20_000,
    ]

    # Comparing a limited shaker sort + quicksort vs just quicksort
    combo_sort_timings = {}
    quicksort_timings = {}
    for size in sizes:
        for test in range(TESTS):
            rand_list = [random.randint(0, size * 2) for _ in range(size)]
            random.shuffle(rand_list)

            # cutoffs = list(range(1, int(size * 0.15), 50))
            cutoffs = [0, 5, 10, 50, 100, 250]

            for cutoff in cutoffs:
                rand_copy = rand_list.copy()
                start = perf_counter()
                shaker_sort(rand_copy, cutoff)
                quickSort(rand_copy, 0, size - 1)
                end = perf_counter()
                assert rand_copy == sorted(rand_copy)
                if size in combo_sort_timings.keys():
                    if cutoff in combo_sort_timings[size].keys():
                        combo_sort_timings[size][cutoff].append(end - start)
                    combo_sort_timings[size][cutoff] = [end - start]
                else:
                    combo_sort_timings[size] = {cutoff: [end - start]}

            rand_copy = rand_list.copy()
            start = perf_counter()
            quickSort(rand_copy, 0, size - 1)
            end = perf_counter()
            assert rand_copy == sorted(rand_copy)
            if size in quicksort_timings.keys():
                quicksort_timings[size].append(end - start)
            else:
                quicksort_timings[size] = [end - start]

    print(json.dumps(combo_sort_timings, indent=3))
    print(json.dumps(quicksort_timings, indent=3))

    # Graph the timings
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    for size in sizes:
        ax.plot(
            cutoffs,
            [
                sum(combo_sort_timings[size][c]) / len(combo_sort_timings[size][c])
                for c in cutoffs
            ],
            label=f"Combo Sort: {size}",
        )
        ax.plot(
            [0, cutoffs[-1]],
            [sum(quicksort_timings[size]) / len(quicksort_timings[size])] * 2,
            label=f"Quicksort: {size}",
        )

    ax.set_title("Combo Sort vs Quicksort")
    ax.set_ylabel("Time (s)")
    ax.set_xlabel("Cutoff")
    ax.legend()
    plt.show()

    # # TESTS = 2
    # # sizes = [50, 100]
    # shaker_timings = {"sorted": [], "reversed": [], "random": []}
    # bubble_timings = {"sorted": [], "reversed": [], "random": []}
    # for size in sizes:
    #     print("Testing size: ", size)
    #     s_t, b_t = run_sort_test(size, TESTS)
    #     shaker_timings["sorted"].append(s_t["sorted"])
    #     shaker_timings["reversed"].append(s_t["reversed"])
    #     shaker_timings["random"].append(s_t["random"])
    #     bubble_timings["sorted"].append(b_t["sorted"])
    #     bubble_timings["reversed"].append(b_t["reversed"])
    #     bubble_timings["random"].append(b_t["random"])

    # print("shaker")
    # print(shaker_outer_loops)
    # print(shaker_total_loops)
    # print(shaker_total_comparisons)
    # print("bubble")
    # print(bubble_outer_loops)
    # print(bubble_total_loops)
    # print(bubble_total_comparisons)

    # print("shaker")
    # print(shaker_outer_loops["random"])
    # print("bubble")
    # print(bubble_outer_loops["random"])

    # print(json.dumps(shaker_timings, indent=3))
    # print(json.dumps(shaker_loops, indent=3))
    # print(json.dumps(bubble_timings, indent=3))
    # print(json.dumps(bubble_loops, indent=3))

    # Now that I have all the timing and looping data I can make the graphs comparing everything
    import matplotlib.pyplot as plt

    # fig, ax = plt.subplots(2, 3, figsize=(15, 10))
    # ax[0, 0].plot(sizes, shaker_timings["sorted"], label="Shaker")
    # ax[0, 0].plot(sizes, bubble_timings["sorted"], label="Bubble")

    # ax[0, 1].plot(sizes, shaker_timings["reversed"], label="Shaker")
    # ax[0, 1].plot(sizes, bubble_timings["reversed"], label="Bubble")

    # ax[0, 2].plot(sizes, shaker_timings["random"], label="Shaker")
    # ax[0, 2].plot(sizes, bubble_timings["random"], label="Bubble")

    # ax[1, 0].plot(
    #     sizes,
    #     [
    #         sum(shaker_outer_loops["sorted"][s]) / len(shaker_outer_loops["sorted"][s])
    #         for s in sizes
    #     ],
    #     label="Shaker",
    # )
    # ax[1, 0].plot(
    #     sizes,
    #     [
    #         sum(bubble_outer_loops["sorted"][s]) / len(bubble_outer_loops["sorted"][s])
    #         for s in sizes
    #     ],
    #     label="Bubble",
    # )

    # ax[1, 1].plot(
    #     sizes,
    #     [
    #         sum(shaker_outer_loops["reversed"][s])
    #         / len(shaker_outer_loops["reversed"][s])
    #         for s in sizes
    #     ],
    #     label="Shaker",
    # )
    # ax[1, 1].plot(
    #     sizes,
    #     [
    #         sum(bubble_outer_loops["reversed"][s])
    #         / len(bubble_outer_loops["reversed"][s])
    #         for s in sizes
    #     ],
    #     label="Bubble",
    # )

    # ax[1, 2].plot(
    #     sizes,
    #     [
    #         sum(shaker_outer_loops["random"][s]) / len(shaker_outer_loops["random"][s])
    #         for s in sizes
    #     ],
    #     label="Shaker",
    # )
    # ax[1, 2].plot(
    #     sizes,
    #     [
    #         sum(bubble_outer_loops["random"][s]) / len(bubble_outer_loops["random"][s])
    #         for s in sizes
    #     ],
    #     label="Bubble",
    # )

    # ax[0, 0].set_title("Sorted")
    # ax[0, 1].set_title("Reversed")
    # ax[0, 2].set_title("Random")
    # ax[1, 0].set_title("Sorted")
    # ax[1, 1].set_title("Reversed")
    # ax[1, 2].set_title("Random")

    # ax[0, 0].set_ylabel("Time (s)")
    # ax[1, 0].set_ylabel("Loops")

    # ax[0, 0].set_xlabel("Size")
    # ax[0, 1].set_xlabel("Size")
    # ax[0, 2].set_xlabel("Size")
    # ax[1, 0].set_xlabel("Size")
    # ax[1, 1].set_xlabel("Size")
    # ax[1, 2].set_xlabel("Size")

    # ax[0, 0].legend()
    # ax[0, 1].legend()
    # ax[0, 2].legend()
    # ax[1, 0].legend()
    # ax[1, 1].legend()
    # ax[1, 2].legend()

    # plt.show()

    # Graphs for the loop comparisons
    # fig, ax = plt.subplots(3, 3, figsize=(15, 9))
    # ax[0, 0].plot(
    #     sizes,
    #     [
    #         sum(shaker_outer_loops["sorted"][s]) / len(shaker_outer_loops["sorted"][s])
    #         for s in sizes
    #     ],
    #     label="Shaker",
    # )
    # ax[0, 0].plot(
    #     sizes,
    #     [
    #         sum(bubble_outer_loops["sorted"][s]) / len(bubble_outer_loops["sorted"][s])
    #         for s in sizes
    #     ],
    #     label="Bubble",
    # )

    # ax[0, 1].plot(
    #     sizes,
    #     [
    #         sum(shaker_outer_loops["reversed"][s])
    #         / len(shaker_outer_loops["reversed"][s])
    #         for s in sizes
    #     ],
    #     label="Shaker",
    # )
    # ax[0, 1].plot(
    #     sizes,
    #     [
    #         sum(bubble_outer_loops["reversed"][s])
    #         / len(bubble_outer_loops["reversed"][s])
    #         for s in sizes
    #     ],
    #     label="Bubble",
    # )

    # ax[0, 2].plot(
    #     sizes,
    #     [
    #         sum(shaker_outer_loops["random"][s]) / len(shaker_outer_loops["random"][s])
    #         for s in sizes
    #     ],
    #     label="Shaker",
    # )
    # ax[0, 2].plot(
    #     sizes,
    #     [
    #         sum(bubble_outer_loops["random"][s]) / len(bubble_outer_loops["random"][s])
    #         for s in sizes
    #     ],
    #     label="Bubble",
    # )

    # ax[1, 0].plot(
    #     sizes,
    #     [
    #         sum(shaker_total_loops["sorted"][s]) / len(shaker_total_loops["sorted"][s])
    #         for s in sizes
    #     ],
    #     label="Shaker",
    # )
    # ax[1, 0].plot(
    #     sizes,
    #     [
    #         sum(bubble_total_loops["sorted"][s]) / len(bubble_total_loops["sorted"][s])
    #         for s in sizes
    #     ],
    #     label="Bubble",
    # )

    # ax[1, 1].plot(
    #     sizes,
    #     [
    #         sum(shaker_total_loops["reversed"][s])
    #         / len(shaker_total_loops["reversed"][s])
    #         for s in sizes
    #     ],
    #     label="Shaker",
    # )
    # ax[1, 1].plot(
    #     sizes,
    #     [
    #         sum(bubble_total_loops["reversed"][s])
    #         / len(bubble_total_loops["reversed"][s])
    #         for s in sizes
    #     ],
    #     label="Bubble",
    # )

    # ax[1, 2].plot(
    #     sizes,
    #     [
    #         sum(shaker_total_loops["random"][s]) / len(shaker_total_loops["random"][s])
    #         for s in sizes
    #     ],
    #     label="Shaker",
    # )
    # ax[1, 2].plot(
    #     sizes,
    #     [
    #         sum(bubble_total_loops["random"][s]) / len(bubble_total_loops["random"][s])
    #         for s in sizes
    #     ],
    #     label="Bubble",
    # )

    # ax[2, 0].plot(
    #     sizes,
    #     [
    #         sum(shaker_total_comparisons["sorted"][s])
    #         / len(shaker_total_comparisons["sorted"][s])
    #         for s in sizes
    #     ],
    #     label="Shaker",
    # )
    # ax[2, 0].plot(
    #     sizes,
    #     [
    #         sum(bubble_total_comparisons["sorted"][s])
    #         / len(bubble_total_comparisons["sorted"][s])
    #         for s in sizes
    #     ],
    #     label="Bubble",
    # )

    # ax[2, 1].plot(
    #     sizes,
    #     [
    #         sum(shaker_total_comparisons["reversed"][s])
    #         / len(shaker_total_comparisons["reversed"][s])
    #         for s in sizes
    #     ],
    #     label="Shaker",
    # )
    # ax[2, 1].plot(
    #     sizes,
    #     [
    #         sum(bubble_total_comparisons["reversed"][s])
    #         / len(bubble_total_comparisons["reversed"][s])
    #         for s in sizes
    #     ],
    #     label="Bubble",
    # )

    # ax[2, 2].plot(
    #     sizes,
    #     [
    #         sum(shaker_total_comparisons["random"][s])
    #         / len(shaker_total_comparisons["random"][s])
    #         for s in sizes
    #     ],
    #     label="Shaker",
    # )
    # ax[2, 2].plot(
    #     sizes,
    #     [
    #         sum(bubble_total_comparisons["random"][s])
    #         / len(bubble_total_comparisons["random"][s])
    #         for s in sizes
    #     ],
    #     label="Bubble",
    # )

    # ax[0, 0].set_title("Sorted")
    # ax[0, 1].set_title("Reversed")
    # ax[0, 2].set_title("Random")
    # # ax[1, 0].set_title("Sorted")
    # # ax[1, 1].set_title("Reversed")
    # # ax[1, 2].set_title("Random")
    # # ax[2, 0].set_title("Sorted")
    # # ax[2, 1].set_title("Reversed")
    # # ax[2, 2].set_title("Random")

    # ax[0, 0].set_ylabel("Outer Loops")
    # ax[1, 0].set_ylabel("Total Loops")
    # ax[2, 0].set_ylabel("Comparisons")

    # # ax[0, 0].set_xlabel("Size")
    # # ax[0, 1].set_xlabel("Size")
    # # ax[0, 2].set_xlabel("Size")
    # # ax[1, 0].set_xlabel("Size")
    # # ax[1, 1].set_xlabel("Size")
    # # ax[1, 2].set_xlabel("Size")
    # ax[2, 0].set_xlabel("Size")
    # ax[2, 1].set_xlabel("Size")
    # ax[2, 2].set_xlabel("Size")

    # ax[0, 0].legend()
    # ax[0, 1].legend()
    # ax[0, 2].legend()
    # ax[1, 0].legend()
    # ax[1, 1].legend()
    # ax[1, 2].legend()
    # ax[2, 0].legend()
    # ax[2, 1].legend()
    # ax[2, 2].legend()

    # plt.show()
