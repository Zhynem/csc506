# CSC506 - Module 2 Critical Thinking - Option 1
# Michael Luker
# January 28, 2024

# ==================================================================================================
# Prompt:
# Suppose that you want to transform the word "algorithm" into the word "alligator." For each letter
# you can either copy the letter from one word to another at a cost of 5, you can delete a letter at
# cost of 20, or insert a letter at a cost of 20. The total cost to transform one word into another
# is used by spell check programs to provide suggestions for words that are close to one another.
# Use dynamic programming techniques to develop an algorithm that gives you the smallest edit
# distance between any two words.
#
# Your Python Programming submission materials must include your source code and screenshots of the
# Python interface executing the application and the results.
#
# Additionally, you must include one paragraph describing how you completed this activity or where
# you had trouble executing the code.
# ==================================================================================================


# ==================================================================================================
# Research:
# This seems to be based on the idea of Levenshtein distance, an idea from Vladimir Levenshtein in
# 1965, in Russian (https://en.wikipedia.org/wiki/Levenshtein_distance#cite_note-1)
# The edit distance between two words is calculated based on the minimum number of single-character
# edits (insert / delete / substitute) required to go from one word to the
#
# One implementation of this idea is the Wagner-Fischer algorithm developed in 1975 by Robert Wagner
# and Michael Fischer. Using iteration, bottom-up dynamic programming, and a distance table they
# can find the edit distance between single character substring differences and essentially do a
# building up of the table of distances of gradually larger substrings until you reach the bottom
# right side of the table, where all numbers are filled and it will contain your final distance.
# It does this by combining neighboring distance values with the cost associated with each action to
# reach the ending letter of the substring and selecting the minimum value to place in the cell.
# (https://en.wikipedia.org/wiki/Levenshtein_distance#cite_note-4)
#
# This method requires having a pre-filled table that compares empty strings to full words to have
# complete values in the first row and column, ie.
#
# '' | '' | a | l | g | o | r | i | t | h | m |
# '' | 0  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
#  a | 1  | _ | _ | _ | _ | _ | _ | _ | _ | _ |
#  l | 2  | _ | _ | _ | _ | _ | _ | _ | _ | _ |
#  l | 3  | _ | _ | _ | _ | _ | _ | _ | _ | _ |
#  i | 4  | _ | _ | _ | _ | _ | _ | _ | _ | _ |
#  g | 5  | _ | _ | _ | _ | _ | _ | _ | _ | _ |
#  a | 6  | _ | _ | _ | _ | _ | _ | _ | _ | _ |
#  t | 7  | _ | _ | _ | _ | _ | _ | _ | _ | _ |
#  o | 8  | _ | _ | _ | _ | _ | _ | _ | _ | _ |
#  r | 9  | _ | _ | _ | _ | _ | _ | _ | _ | D |    where D is the final distance output by the algo.
#
# So what essentially happened here is first comparing the distance of two empty strings (0) and
# then slowly building one side or the other, so '' vs 'a', '' vs 'al', '' vs 'alg' etc. each time
# a new letter is getting inserted with a cost of 1 from the Wagner-Fischer method where all actions
# have a cost of 1 (ins, del, sub) or 0 if the letters are equal in a position.
#
# Here's a smaller example of turning 'abcdef' into 'azced'
# If you just iterate over the letters and compare them directly you would get something like
# a b c d e f
# a z c e d
# 0 1 1 2 3 4
#
# 4 ins't the optimal distance as shown by this table provided by online calculator at
# https://phiresky.github.io/levenshtein-demo/
#
# 3 is the optimal distance where you want to substitute b & z, delete d to align the e, then insert
# an f for a total of 3 edits instead of 4
#
#   | _ | a | z | c | e | d |
# _ | 0 | 1 | 2 | 3 | 4 | 5 |
# a | 1 | 0 | 1 | 2 | 3 | 4 |
# b | 2 | 1 | 1 | 2 | 3 | 4 |
# c | 3 | 2 | 2 | 1 | 2 | 3 |
# d | 4 | 3 | 3 | 2 | 2 | 2 |
# e | 5 | 4 | 4 | 3 | 2 | 3 |
# f | 6 | 5 | 5 | 4 | 3 | 3 |
#
# It also appears that word1 (starting word) runs along the vertical while word2 (ending word) is on
# the horizontal axis
# ==================================================================================================

# Imports
from typing import List
from time import perf_counter

# Constants
COPY_COST = 5
DELETE_COST = 20
INSERT_COST = 20
# Used values of 1 while testing and validating against results from https://phiresky.github.io/levenshtein-demo/
# COPY_COST = 1
# DELETE_COST = 1
# INSERT_COST = 1


# Functions
def get_path(distance_table: List[List[List]]) -> List[List]:
    # Based on https://phiresky.github.io/levenshtein-demo/
    # I like that it shows a list of all the actions taken after computing the distance
    # I want to try and do the same thing
    # Apparently the best way is to start at the last element in the table and backtrack to the
    # beginning of the words at distance_table[0][0], I should be able to easily do that with
    # the actions being saved in the cells
    # n or c mean go to the kitty corner cell, i means move left one col, d means move up one row
    row = len(distance_table) - 1
    col = len(distance_table[0]) - 1
    row_done = False
    col_done = False
    path = []
    while not row_done and not col_done:
        cell = distance_table[row][col]
        path.append([cell[1], row, col])
        if cell[1] == "n" or cell[1] == "c":
            row -= 1
            col -= 1
        elif cell[1] == "i":
            col -= 1
        elif cell[1] == "d":
            row -= 1
        if row < 0:
            row_done = True
            row = 0
        if col < 0:
            col_done = True
            col = 0
    # Reverse the list to have the correct order of actions
    path = list(reversed(path))
    return path


def print_table(
    distance_table: List[List[List]], word1: str, word2: str, path: List[List]
) -> None:
    # We're using non-standard values for edits so distance values may be large / need extra room
    # We can set it dynamically though using the largest value in the table
    biggest_num = str(max([col[0] for row in distance_table for col in row]))
    cell_width = len(biggest_num) + 4  # add 2 for brackets and 2 for spaces

    # Add a symbol to beginning of each word to print an empty string indicator
    vert_header = f"*{word2}"
    hori_header = f"*{word1}"
    # Print the header
    print_line = f"{' ':^{cell_width}}|"
    for c in vert_header:
        if c == "*":
            empty = '""'
            print_line += f"{empty:^{cell_width}}|"
        else:
            print_line += f"{c:^{cell_width}}|"
    print(print_line)
    # Then a separator
    print("-" * len(print_line))
    # Then print all the table data
    print_line = ""
    for i, row in enumerate(distance_table):
        if hori_header[i] == "*":
            empty = '""'
            print_line += f"{empty:^{cell_width}}|"
        else:
            print_line = f"{hori_header[i]:^{cell_width}}|"
        for col, item in enumerate(row):
            d = item[0]
            on_path = False
            for action in path:
                if action[1] == i and action[2] == col:
                    cell_str = f"[{d}]"
                    on_path = True
                    break
            if not on_path:
                cell_str = f"{d}"

            print_line += f"{cell_str:^{cell_width}}|"
        print(print_line)
    # And a final separator
    print("-" * len(print_line))


def print_actions(path: List[List], word1: str, word2: str) -> List[List]:
    # Remove the unused no action at 0, 0 that compares empty strings
    path = path[1:]
    letter_list = list(word1)
    del_count = 0
    for i, action in enumerate(path):
        act = action[0]
        row = action[1]
        col = action[2]
        prev_list = letter_list.copy()
        idx = i - del_count
        if act == "n":
            act_string = "+0 | No action to go from"
        elif act == "c":
            letter_list[idx] = word2[col - 1]
            act_string = f"+{COPY_COST} | Copy {word2[col-1]} to go from"
        elif act == "i":
            letter_list.insert(idx, word2[col - 1])
            act_string = f"+{INSERT_COST} | Insert {word2[col-1]} to go from"
        elif act == "d":
            letter_list.remove(word1[row - 1])
            del_count += 1
            act_string = f"+{DELETE_COST} | Delete {word1[row-1]} to go from"

        prev_list_letters = prev_list.copy()
        prev_list_letters.insert(idx, "[")
        prev_list_letters.insert(idx + 2, "]")
        print_letters = letter_list.copy()
        if "Delete" in act_string:
            if idx == 0:
                print_letters.insert(0, "[")
                print_letters.insert(1, "_")
                print_letters.insert(2, "]")
            else:
                print_letters.insert(idx, "[")
                print_letters.insert(idx + 1, "_")
                print_letters.insert(idx + 2, "]")
        else:
            if idx == 0:
                print_letters.insert(0, "[")
            else:
                print_letters.insert(idx, "[")
            print_letters.insert(idx + 2, "]")
        prev_string = "".join(prev_list_letters)
        curr_string = "".join(print_letters)
        print(f"{act_string} {prev_string} to {curr_string}")
    return path


def get_distance(word1: str, word2: str, show_table=True) -> int:
    # Start by creating a 3d array and filling in the first row and column
    # Going with 3d so we track the rows, columns and then within a cell we can track the value and
    # the action taken to get that value
    # n = no action, i = insert, d = delete, c = copy
    distance_table = [
        [[0, "n"] for col in range(0, len(word2) + 1)]
        for row in range(0, len(word1) + 1)
    ]
    # Inserting to go from empty string to letters in word 2
    distance_table[0] = [[i * INSERT_COST, "i"] for i in range(0, len(word2) + 1)]
    # Set the first cell action to none, empty vs empty is no action
    distance_table[0][0][0] = 0
    distance_table[0][0][1] = "n"

    # Action is delete to go from letters in word1 to an empty string
    for i in range(1, len(word1) + 1):
        distance_table[i][0][0] = i * DELETE_COST
        distance_table[i][0][1] = "d"

    # Iterate over every remaining cell in the table
    for row in range(1, len(word1) + 1):
        for col in range(1, len(word2) + 1):
            # Compute the distance values for all the actions
            # First case is if the letters match, then no action is needed which takes on the value
            # of the cell in the upper left kitty corner to the current one
            prev_diag = distance_table[row - 1][col - 1]
            if word1[row - 1] == word2[col - 1]:
                distance_table[row][col] = [prev_diag[0], "n"]
                continue
            # Next compute the options for copy / insert / delete actions
            copy_action = [prev_diag[0] + COPY_COST, "c"]  # Uses the kitty corner again
            # Insert is like looking at the value in the cell to the left then inserting
            insert_action = [distance_table[row][col - 1][0] + INSERT_COST, "i"]
            # Deleting is like looking at the cell above
            delete_action = [distance_table[row - 1][col][0] + DELETE_COST, "d"]

            # Select the minimum cost option by sorting on the distance value and choosing the first
            # option
            options = sorted(
                [copy_action, insert_action, delete_action], key=lambda x: x[0]
            )

            # If the distance values are the same prioritize one action over the other depending
            # on the string lengths
            # equal length use a copy, w1 > w2 use delete, w1 < w2 use insert
            # Turns out this isn't necessary at all, but it makes sense in my head to have
            lowest_dist = options[0][0]
            word1_substr_len = len(word1[:row])
            word2_substr_len = len(word2[:col])
            if (copy_action[0] == lowest_dist) and (
                word1_substr_len == word2_substr_len
            ):
                distance_table[row][col] = copy_action
                continue
            if (delete_action[0] == lowest_dist) and (
                word1_substr_len > word2_substr_len
            ):
                distance_table[row][col] = delete_action
                continue
            if (insert_action[0] == lowest_dist) and (
                word1_substr_len < word2_substr_len
            ):
                distance_table[row][col] = insert_action
                continue

            # Default case, just take the lowest value option
            distance_table[row][col] = options[0]

    if show_table:
        path = get_path(distance_table)
        print_table(distance_table, word1, word2, path)
        print_actions(path, word1, word2)

    # Get the distance value from the last element in the table
    return distance_table[-1][-1][0]


# Start of the script
if __name__ == "__main__":
    tests = [
        # Simple test cases
        # Test no action
        ("a", "a", True),
        # Test insert
        ("a", "ab", True),
        # Test delete
        ("ab", "a", True),
        # Test copy
        ("ab", "ac", True),
        # Short example
        ("beans", "brews", True),
        # Assignment example
        ("algorithm", "alligator", True),
        # Medium examples (again, from https://phiresky.github.io/levenshtein-demo/)
        ("elephant", "relevant", True),
        ("Saturday", "Sunday", True),
        ("Google", "Facebook", True),
        # Long example, too long to be able to even properly look at the table
        (
            "antidisestablishmentarianism",
            "pneumonoultramicroscopicsilicovolcanoconiosis",
            False,
        ),
    ]

    # Run and time each test set of words
    for test in tests:
        W1 = test[0]
        W2 = test[1]
        start = perf_counter()
        D = get_distance(
            W1,
            W2,
            show_table=test[2],
        )
        end = perf_counter()
        print(f"Distance between {W1} and {W2}: {D}")
        print(f"Took {end - start:.4f}s to compute the distance")
        print()
        print()
