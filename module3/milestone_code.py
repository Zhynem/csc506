# CSC 506 - Design and Analysis of Algorithms
# Module 3 - Portfolio Milestone - Option 2
# Michael Luker
# Feb 4, 2024

"""
Prompt:
In the portfolio project, retroactive search trees will be implemented - both partially and fully 
retroactive search trees. The update operations to the (non-retroactive) search tree should be 
Insert(x) and Delete(x), and the query operation should be Pred(x) that returns the largest element 
stored in the subtree ≤x. 

The task of Milestone 1 is to:
 - Define an appropriate interface to a partially and a fully retroactive search tree.
"""
# Imports
from dataclasses import dataclass
from typing import List, Self


# To me this seems like it should be broken down into a few different objects to make things easier
# First, is a node in the binary search tree, it contains a value and links to the left (lower value)
# and right (higher value) nodes
@dataclass
class TreeNode:
    value: int
    parent: Self = None
    left: Self = None
    right: Self = None


# The acutal search tree contains a root and the functions related to any given instance of a tree
# Doing an AVL BST seems like it might be nice as well? https://en.wikipedia.org/wiki/AVL_tree
class BinarySearchTree:
    _root: TreeNode = None
    _left_height = 0
    _right_height = 0

    def insert(self, newNode: TreeNode) -> None:
        pass

    def delete(self, delNode: TreeNode) -> None:
        pass

    # AVL tree needs to be able to do left and right rotations to keep branches heights close together
    def _balance(self) -> None:
        pass

    def _rotate_left(self, pivot: TreeNode) -> None:
        pass

    def _rotate_right(self, pivot: TreeNode) -> None:
        pass

    def _update_height(self) -> None:
        pass

    def search(self, value: int) -> TreeNode:
        pass

    def min(self) -> TreeNode:
        pass

    def max(self) -> TreeNode:
        pass


# This class will handle the retroactive parts
class RetroactiveBST:
    # My assumption is that queries would most typically be called on the current state, so that
    # should always be maintained
    _current = BinarySearchTree()
    # To support the retroactivity a second tree can be used that can travel to wherever the ops go
    _retro = BinarySearchTree()
    # I'm not sure yet, but I think a list of tuples can act as an operation log to store the action
    # and value, so a BST could essentially be rolled backward or forward to a given state
    _operations: List[(str, int)] = []
    # Also need to store where the retro tree currently is to roll forward or backward
    # depending on function calls coming in
    _current_retro: int = 0

    # This function will undo any changes to go from the current point in time to the desired one
    def rollback(self, point: int) -> None:
        pass

    # This function will apply any changes to go from the current point in time to the desired one
    def rollforward(self, point: int) -> None:
        pass

    # I imagine there are times when a tree may need to be fully rebuilt to properly follow the
    # operation log
    def rebuild_full(self, retro: bool = False) -> None:
        pass

    # Insert a new node, with some options that can direct where it goes
    def insert(
        self, newNode: TreeNode, retro: bool = False, retro_point: int = None
    ) -> None:
        # If retro is being used, make sure a point in time is set, and that it doesn't exceed
        # the number of operations that have been stored
        if (
            retro
            and retro_point is not None
            and retro_point < len(self._operations)
            and retro_point >= 0
        ):
            pass
        else:
            pass

    # Insert a new node, with some options that can direct where it goes
    def delete(
        self, newNode: TreeNode, retro: bool = False, retro_point: int = None
    ) -> None:
        # If retro is being used, make sure a point in time is set, and that it doesn't exceed
        # the number of operations that have been stored
        if (
            retro
            and retro_point is not None
            and retro_point < len(self._operations)
            and retro_point >= 0
        ):
            pass
        else:
            pass

    # From the assignment, "Pred(x) returns the largest element stored in the subtree <= x"
    def pred(self, x: int, retro: bool = False, retro_point: int = None) -> int:
        if (
            retro
            and retro_point is not None
            and retro_point < len(self._operations)
            and retro_point >= 0
        ):
            self.rollback(retro_point)
            pass
        else:
            pass
