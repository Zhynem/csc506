"""Critical Thinking 1: Option 2 code"""

from typing import List
from itertools import permutations
from time import perf_counter


def identify_swap_value(pivot_num: int, seen_nums: List[int]) -> int:
    """
    Given a number and the list of seen numbers return the next largest number
    Takes parameter pivot_num (value to compare against) and seen_nums (values to consider)
    Returns an int of the next largest number
    """
    # Start by sorting the list of numbers
    seen_nums = sorted(seen_nums)
    # Iterate through the numbers until the first ocurrence of the value being larger than the pivot
    # number
    for n in seen_nums:
        if n > pivot_num:
            return n
    # It should never get here, but just in case
    return -99


def identify_pivot(starting_value: List[int]) -> (int, int):
    """
    Given a list of numbers identify the rightmost digit containing larger digits to the right of it
    (ie. identify_pivot([5,6,4,7,3,8,2,9,0,1]) would return index 8 pointing to value 0, since
    index 9 with a 1 in it is larger and it's the rightmost occurence of it)
    Takes parameter starting_value as a list of integers representing the starting 10 digit number
    Returns a tuple containing (pivot_index, swap_num) as they are both useful to the algorithm
    If no pivot is found it will return (-99, -99)
    """
    # Reverse the list to look from the right side to the left in terms of digit order, but in an
    # order that's easier to program with
    # Need to do a deep copy of the list so it doesn't reverse the original number
    value_copy = [n for n in starting_value]
    value_copy.reverse()
    seen_nums = []
    for i, current_num in enumerate(value_copy):
        # Check if the number is smaller than any value seen so far
        if any([current_num < seen_num for seen_num in seen_nums]):
            # Convert the pivot back to indexing on the non-reversed list and send the number to swap with as well
            return 9 - i, identify_swap_value(current_num, seen_nums)
        seen_nums.append(current_num)
    return -99, -99


def next_largest_permutation(num: int) -> int:
    """
    Given a number that contains each digit exactly once, find the smallest permutation that is
    larger than the current permutation (ie. from 5647382901 to 5647382910)
    Takes parameter num, the permutation being worked with, as an integer value
    Returns an integer that is the next largest permutation, or -99 if none exists
    """
    # First thing to check is if the number is the largest permutation, reverse sort order
    if num == 9876543210:
        # print(f"{num} is in its largest possible permutation, no larger value exists")
        return -99
    # Then turn the number into a list of its digits to make it easier to work with
    starting_value = [int(d) for d in str(num)]
    # It's possible the 0 was in the left most digit, so make sure we have all 10 digits
    if len(starting_value) == 9:
        starting_value.insert(0, 0)
    # Ensure it has each digit
    if set(starting_value) != set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]):
        raise ValueError(
            f"{num} is not a number containing each digit 0-9 exactly once"
        )
    # To begin the algorithm we need to identify the rightmost digit that has a digit further to
    # the right that is larger than itself, and the next largest value that it will swap places with
    pivot_index, swap_num = identify_pivot(starting_value)
    # Do the pivot swap
    pivot_num = starting_value[pivot_index]
    swap_index = starting_value.index(swap_num)
    starting_value[pivot_index] = swap_num
    starting_value[swap_index] = pivot_num
    # Now ensure all numbers to the right of the pivot are in ascending order for the smallest
    # possible increase in overall value
    sorted_right_digits = sorted(starting_value[pivot_index + 1 :])
    # We can now piece together the next largest permutation as a string, convert it back to an int
    # and return it
    next_largest = int(
        f"{''.join([str(n) for n in starting_value[:pivot_index+1]])}{''.join([str(n) for n in sorted_right_digits])}"
    )
    return next_largest


# Start by showing the next 5 permutations from the assignment start point
permutation_value = 5647382901
print(f"Next 5 largest permutations starting from {permutation_value}")
print_string = f"{permutation_value} -> "
for i in range(5):
    permutation_value = next_largest_permutation(permutation_value)
    print_string += f"{permutation_value} -> "
print(print_string[: len(print_string) - 4])
print()
print(
    "Differences between numbers and the starting point (should be in ascending order)"
)
start_point = permutation_value = 5647382901
print_string = f"{0} -> "
for i in range(5):
    permutation_value = next_largest_permutation(permutation_value)
    print_string += f"{permutation_value - start_point} -> "
print(print_string[: len(print_string) - 4])
print()

# Excessive testing, with all possible permutations by starting at the lowest value permutation
print("Testing against all possible permutations now")
start = perf_counter()
permutation_value = 123456789
value_list = [123456789]
timings = []
count = 1
# And it should end when it reaches the highest value permutation and returns a -99
while permutation_value != -99:
    func_start = perf_counter()
    permutation_value = next_largest_permutation(permutation_value)
    func_end = perf_counter()
    timings.append(func_end - func_start)
    # We don't actually want to append the -99 value to the list though
    if permutation_value != -99:
        value_list.append(permutation_value)
    # Have a print to let us know how progress is coming along
    count += 1
    if count % 500_000 == 0:
        print(f"Generated {count:,} permutations. Working on {permutation_value} now.")
print("Complete! Validating results now ...")
# value_list should now be a list containing all permutations of the number, let's validate a few things
# First validate that the value_list is in sorted order, meaning it's correctly identifying each next largest permutation
sorted_list = sorted(value_list)
# Make sure it's not checking the exact same object against itself, but all values are already in sorted order
assert id(value_list) != id(sorted_list) and value_list == sorted_list
# Then validate that it does actually contain every permutation of digits 0 to 9
p = [
    int("".join([str(n) for n in perm]))
    for perm in permutations(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    )
]
assert len(p) == len(value_list)
assert sorted(p) == sorted(value_list)
end = perf_counter()
print(
    f"{len(value_list):,} permutations were generated in ascending order, and validated to be all possible permutations."
)
print(f"It took {end - start:.4f}s to generate and validate results.")
avg_speed = sum(timings) / len(timings)
print(
    f"On average the algorithm takes {avg_speed:.6f}s to find the next largest permutation."
)
