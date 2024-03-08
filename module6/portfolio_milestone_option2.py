# CSC 506 - Design and Analysis of Algorithms
# Module 8 - Portfolio Project - Option 2
# Michael Luker
# March 10, 2024

"""
Prompt:
In this portfolio project, retroactive search trees will be implemented - both partially and fully 
retroactive search trees. The update operations to the (non-retroactive) search tree should be 
Insert(x) and Delete(x), and the query operation should be Pred(x) that returns the largest element 
stored in the subtree ≤x. The tasks of the project are to:

Define an appropriate interface to a partially and a fully retroactive search tree.
Implement a search tree, a partially retroactive search tree, and a fully retroactive search tree.
Test if your retroactive solutions are correct by comparing them with simple rollback solutions.
Compare the performance of the different data structures. Compare the performance of the fully 
retroactive search tree with a simple rollback solution. What are the thresholds where the 
complicated solution is superior to the rollback solution?
"""
# Imports
from dataclasses import dataclass
import random
from typing import Any, List, Self
from functools import total_ordering


# To me this seems like it should be broken down into a few different objects to make things easier
# First, is a node in the binary search tree, it contains a value and links to the left (lower value)
# and right (higher value) nodes
@dataclass(repr=False, eq=False, order=False)
@total_ordering
class TreeNode:
    value: int
    parent: Self = None
    left: Self = None
    right: Self = None
    bf: int = 0
    __eq__: Any = lambda self, other: self.value == other
    __lt__: Any = lambda self, other: self.value < other


# The acutal search tree contains a root and the functions related to any given instance of a tree
# Doing an AVL BST seems like it might be nice as well? https://en.wikipedia.org/wiki/AVL_tree
class AVLTree:

    def __init__(self, starting_data: List[Any] = None) -> None:
        self.root = None

        # If there is starting data, it can be inserted into the tree (after sanitizing)
        if starting_data is not None and len(starting_data) > 0:
            starting_data = sorted(list(set(starting_data)))
            for data in starting_data:
                self.insert(TreeNode(data))

    def insert(self, newNode: TreeNode) -> None:
        # If the tree is empty, the new node becomes the root
        if self.root is None:
            self.root = newNode
            return
        # Otherwise, the tree is traversed to find the correct spot for the new node
        current = self.root
        while current is not None:
            if newNode.value < current.value:
                if current.left is None:
                    current.left = newNode
                    newNode.parent = current
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = newNode
                    newNode.parent = current
                    break
                current = current.right
        # After the new node is inserted, the balance factors need to be updated for whichever
        # subtree it was inserted into
        self._update_balance_factors(newNode)
        # And the tree needs to be rebalanced
        self._rebalance(newNode)

    def _bst_delete(self, current_node: TreeNode, data: int) -> None:
        # Standard BST delete from https://www.geeksforgeeks.org/deletion-in-binary-search-tree/?ref=lbp
        # If the current node is None then we can't delete anything
        if current_node is None:
            return current_node

        # If the data is less than the current node then we need to go left
        if data < current_node:
            current_node.left = self._bst_delete(current_node.left, data)
            return current_node
        # If the data is greater than the current node then we need to go right
        elif data > current_node:
            current_node.right = self._bst_delete(current_node.right, data)
            return current_node

        # If the current node is the one we want to delete
        # If there are no children then just delete the node
        if current_node.left is None and current_node.right is None:
            if current_node == self.root:
                self.root = None
            del current_node
            return None
        # If it only has one child node
        elif current_node.left is None and current_node.right is not None:
            temp = current_node.right
            temp.parent = current_node.parent
            if current_node == self.root:
                self.root = temp
            del current_node
            return temp
        elif current_node.right is None and current_node.left is not None:
            temp = current_node.left
            temp.parent = current_node.parent
            if current_node == self.root:
                self.root = temp
            del current_node
            return temp
        # If the current node has two children
        else:
            parent = current_node
            # Find the smallest node in the right subtree
            temp = current_node.right
            while temp.left is not None:
                parent = temp
                temp = temp.left
            # Delete the "successor" node (temp)
            if parent != current_node:
                parent.left = temp.right
            else:
                parent.right = temp.right

            # move the data
            current_node.value = temp.value

            # delete the successor node

            del temp
            return current_node

    def delete(self, data: int) -> None:
        removed_from = self._bst_delete(self.root, data)
        # Update the balance factors
        self._update_balance_factors(self.root)
        # start rebalancing the tree starting from around where the node was deleted from
        # Make sure the parent has both children balanced, may be over the top
        if removed_from is not None and removed_from.right is not None:
            self._rebalance(removed_from.right)
        if removed_from is not None and removed_from.left is not None:
            self._rebalance(removed_from.left)

    def print_tree(self) -> None:
        if self.root is None:
            print("Tree is empty")
            return
        print("Current tree state: ")
        self._print_tree(self.root, 0, from_left=False, from_right=False)
        print()

    def print_balances(self) -> None:
        if self.root is None:
            print("Tree is empty")
            return
        print("Current tree balance factors: ")
        self._print_tree(self.root, 0, from_left=False, from_right=False, bf=True)

    def _print_tree(
        self,
        start: TreeNode,
        level: int,
        from_left: bool,
        from_right: bool,
        bf: bool = False,
    ) -> None:
        if start is not None:
            val_to_print = str(start.bf) if bf else str(start.value)
            self._print_tree(
                start.right, level + 1, from_left=False, from_right=True, bf=bf
            )
            if from_left:
                print(" " * 3 * level + "\\" + val_to_print)
            elif from_right:
                print(" " * 3 * level + "/" + val_to_print)
            else:
                print(val_to_print)
            self._print_tree(
                start.left, level + 1, from_left=True, from_right=False, bf=bf
            )

    def _rebalance(self, start: TreeNode) -> None:
        if start is None:
            return
        # Start at the leaf and work up towards the root
        current = start
        while current is not None:
            # If the balance factor is -2, the right subtree is too tall
            if current.bf <= -2:
                # If the right subtree's balance factor is 1, a double rotation is needed
                if current.right.bf == 1:
                    self._rotate_right(current.right)
                    self._rotate_left(current)
                # Otherwise, a single rotation is needed
                else:
                    self._rotate_left(current)
            # If the balance factor is 2, the left subtree is too tall
            elif current.bf >= 2:
                # If the left subtree's balance factor is -1, a double rotation is needed
                if current.left.bf == -1:
                    self._rotate_left(current.left)
                    self._rotate_right(current)
                # Otherwise, a single rotation is needed
                else:
                    self._rotate_right(current)
            # Move to the next node
            current = current.parent

    def _rotate_left(self, pivot: TreeNode) -> None:
        # The pivot's right child becomes the new root
        new_root = pivot.right
        # The pivot's right child's left child becomes the pivot's right child
        pivot.right = new_root.left
        # If the pivot's right child's left child exists, the pivot's right child's left child's parent
        # becomes the pivot
        if new_root.left is not None:
            new_root.left.parent = pivot
        # The pivot's parent becomes the new root's parent
        new_root.parent = pivot.parent
        # If the pivot's parent is None, the new root becomes the root of the tree
        if pivot.parent is None:
            self.root = new_root
        # Otherwise, if the pivot is the left child of its parent, the new root becomes the left child
        # of the pivot's parent
        elif pivot is pivot.parent.left:
            pivot.parent.left = new_root
        # Otherwise, the new root becomes the right child of the pivot's parent
        else:
            pivot.parent.right = new_root
        # The pivot becomes the left child of the new root
        new_root.left = pivot
        # The pivot's parent becomes the new root
        pivot.parent = new_root
        # The balance factors need to be updated for the pivot and the new root
        self._update_balance_factors(pivot)
        self._update_balance_factors(new_root)

    def _rotate_right(self, pivot: TreeNode) -> None:
        # The pivot's left child becomes the new root
        new_root = pivot.left
        # The pivot's left child's right child becomes the pivot's left child
        pivot.left = new_root.right
        # If the pivot's left child's right child exists, the pivot's left child's right child's parent
        # becomes the pivot
        if new_root.right is not None:
            new_root.right.parent = pivot
        # The pivot's parent becomes the new root's parent
        new_root.parent = pivot.parent
        # If the pivot's parent is None, the new root becomes the root of the tree
        if pivot.parent is None:
            self.root = new_root
        # Otherwise, if the pivot is the left child of its parent, the new root becomes the left child
        # of the pivot's parent
        elif pivot is pivot.parent.left:
            pivot.parent.left = new_root
        # Otherwise, the new root becomes the right child of the pivot's parent
        else:
            pivot.parent.right = new_root
        # The pivot becomes the right child of the new root
        new_root.right = pivot
        # The pivot's parent becomes the new root
        pivot.parent = new_root
        # The balance factors need to be updated for the pivot and the new root
        self._update_balance_factors(pivot)
        self._update_balance_factors(new_root)

    def _update_balance_factors(self, start: TreeNode) -> None:
        if start is None:
            return
        # If the node has no children, the balance factor is 0
        if start.left is None and start.right is None:
            start.bf = 0
        # Otherwise the balance factor is the difference in height between the left and right children
        else:
            start.bf = self._height(start.left) - self._height(start.right)
        # Update the balance factors for the nodes above
        if start.parent is not None:
            self._update_balance_factors(start.parent)

    def _height(self, start: TreeNode) -> int:
        # If the node is None, the height is 0
        if start is None:
            return 0
        # Otherwise, the height is 1 plus the maximum height of the left or right children
        else:
            return 1 + max(self._height(start.left), self._height(start.right))


# Partial retroactive: The data structure is partially retroactive if, in addition to supporting updates
#   and queries on the “current state” of the data structure (present time), it supports
#   insertion and deletion of updates at past times as well.
# From https://erikdemaine.org/papers/Retroactive_TALG/paper.pdf written by
# ERIK D. DEMAINE
# Massachusetts Institute of Technology
# and
# JOHN IACONO
# Polytechnic University
# and
# STEFAN LANGERMAN
# Universit´e Libre de Bruxelles
class PartialRetroactiveAVL:
    def __init__(self) -> None:
        self._tree = AVLTree()
        # I'm not sure yet, but I think a list of tuples can act as an operation log to store the action
        # and value, so a BST could essentially be rolled backward or forward to a given state
        self._operations: List[(str, int)] = []

    # Wipe out the current tree and rebuild based on the list of operations
    def _rebuild(self) -> None:
        del self._tree
        self._tree = AVLTree()
        for op in self._operations:
            if op[0] == "insert":
                self._tree.insert(TreeNode(op[1]))
            elif op[0] == "delete":
                self._tree.delete(op[1])

    # Partial supports insertion in the past, and the current state
    def insert(self, data: int, retro: bool = False, retro_point: int = None) -> None:
        newNode = TreeNode(data)
        # If retro isn't being used then insert to the current state as normal
        if not retro:
            self._tree.insert(newNode)
            self._operations.append(("insert", newNode.value))
        else:
            # If retro is being used, make sure a point in time is set, and that it doesn't go out
            # of bounds for the operation list
            if (
                retro_point is None
                or retro_point < 0
                or retro_point > len(self._operations) - 1
            ):
                print("Invalid retro point")
                return
            # Insert the operation into the list at the given point, then rebuild the tree
            # to achieve making the modification in the past, but still being at the current state
            self._operations.insert(retro_point, ("insert", newNode.value))
            self._rebuild()

    # Partial supports deletion in the past, and the current state
    def delete(self, data: int, retro: bool = False, retro_point: int = None) -> None:
        if not retro:
            self._tree.delete(data)
            self._operations.append(("delete", data))
        else:
            if (
                retro_point is None
                or retro_point < 0
                or retro_point > len(self._operations) - 1
            ):
                print("Invalid retro point")
                return
            self._operations.insert(retro_point, ("delete", data))
            self._rebuild()

    # Partial only queries the current state
    # From the assignment, "Pred(x) returns the largest element stored in the subtree <= x"
    def pred(self, x: int) -> int:
        # Get a list of nodes that are less than or equal to x
        node_list = []
        self._get_nodes_less_than_or_equal_to_x(self._tree.root, x, node_list)
        # If the list is empty, there are no nodes less than or equal to x
        if len(node_list) == 0:
            return -1
        print([node.value for node in node_list])
        # Otherwise, return the largest value in the list
        return max([node.value for node in node_list])

    def _get_nodes_less_than_or_equal_to_x(
        self, start: TreeNode, x: int, node_list: List[TreeNode]
    ) -> None:
        if start is not None:
            if start.value <= x:
                node_list.append(start)
            self._get_nodes_less_than_or_equal_to_x(start.left, x, node_list)
            self._get_nodes_less_than_or_equal_to_x(start.right, x, node_list)

    def print_tree(self) -> None:
        self._tree.print_tree()

    def print_log(self) -> None:
        if len(self._operations) == 0:
            print("Operation log is empty")
            return
        print("Operation log: ")
        for op in self._operations:
            print(op)


# A data structure
#   is fully retroactive if, in addition to allowing updates in the past, it can answer
#   queries about the past
# From https://erikdemaine.org/papers/Retroactive_TALG/paper.pdf written by
# ERIK D. DEMAINE
# Massachusetts Institute of Technology
# and
# JOHN IACONO
# Polytechnic University
# and
# STEFAN LANGERMAN
# Universit´e Libre de Bruxelles
class FullyRetroactiveAVL:
    def __init__(self) -> None:
        self._tree = AVLTree()
        self._operations: List[(str, int)] = []
        # Store where the retro tree currently is to roll forward or backward depending on function
        # calls coming in
        self._current_retro: int = -1

    # This function will undo any changes to go from the current point in time to the desired one
    def rollback(self, point: int) -> None:
        while self._current_retro > point:
            if self._operations[self._current_retro][0] == "insert":
                # print("Rollback Delete: ", self._operations[self._current_retro][1])
                self._tree.delete(self._operations[self._current_retro][1])
                self._current_retro -= 1
            elif self._operations[self._current_retro][0] == "delete":
                # print("Rollback Insert: ", self._operations[self._current_retro][1])
                self._tree.insert(TreeNode(self._operations[self._current_retro][1]))
                self._current_retro -= 1

    # This function will apply any changes to go from the current point in time to the desired one
    def rollforward(self, point: int) -> None:
        self._current_retro += 1
        while self._current_retro <= point:
            if self._current_retro == len(self._operations):
                break
            if self._operations[self._current_retro][0] == "insert":
                # print("Rollforward Insert: ", self._operations[self._current_retro][1])
                self._tree.insert(TreeNode(self._operations[self._current_retro][1]))
            elif self._operations[self._current_retro][0] == "delete":
                # print("Rollforward Delete: ", self._operations[self._current_retro][1])
                self._tree.delete(self._operations[self._current_retro][1])
            self._current_retro += 1

    # Wipe out the current tree and rebuild based on the list of operations
    def _rebuild(self, stop: int = None) -> None:
        del self._tree
        self._tree = AVLTree()
        self._current_retro = -1
        for op in self._operations:
            if op[0] == "insert":
                self._tree.insert(TreeNode(op[1]))
            elif op[0] == "delete":
                self._tree.delete(op[1])
            self._current_retro += 1
            if stop is not None and self._current_retro == stop:
                break

    # Partial supports insertion in the past, and the current state
    def insert(self, data: int, retro: bool = False, retro_point: int = None) -> None:
        newNode = TreeNode(data)
        # If retro isn't being used then insert to the current state as normal
        if not retro:
            self._tree.insert(newNode)
            self._operations.append(("insert", newNode.value))
            self._current_retro += 1
        else:
            # If retro is being used, make sure a point in time is set, and that it doesn't go out
            # of bounds for the operation list
            if (
                retro_point is None
                or retro_point < 0
                or retro_point > len(self._operations) - 1
            ):
                print("Invalid retro point")
                return
            # Insert the operation into the list at the given point, then rebuild the tree
            # to achieve making the modification in the past, but still being at the current state
            self._operations.insert(retro_point, ("insert", newNode.value))
            self._rebuild()

    # Partial supports deletion in the past, and the current state
    def delete(self, data: int, retro: bool = False, retro_point: int = None) -> None:
        if not retro:
            self._tree.delete(data)
            self._operations.append(("delete", data))
            self._current_retro += 1
        else:
            if (
                retro_point is None
                or retro_point < 0
                or retro_point > len(self._operations) - 1
            ):
                print("Invalid retro point")
                return
            self._operations.insert(retro_point, ("delete", data))
            self._rebuild()

    # Partial only queries the current state
    # From the assignment, "Pred(x) returns the largest element stored in the subtree <= x"
    def pred(self, x: int, retro: bool = False, retro_point: int = None) -> int:
        # If it's a retro pred, set the state to that point in time, saving the current location
        # before hand
        if retro:
            print("Pre Retro Tree Log: ")
            self.print_log()
            print("Pre Retro Tree State: ")
            self._tree.print_tree()
            temp_current_retro = self._current_retro
            if (
                retro_point is None
                or retro_point < 0
                or retro_point > len(self._operations) - 1
            ):
                print("Invalid retro point")
                return
            self._rebuild(retro_point)
            print("Retro Pred Tree State: ")
            self._tree.print_tree()

        # Get a list of nodes that are less than or equal to x
        node_list = []
        self._get_nodes_less_than_or_equal_to_x(self._tree.root, x, node_list)

        if retro:
            # Restore the current state
            if retro_point < temp_current_retro:
                self.rollforward(temp_current_retro)
            elif retro_point > temp_current_retro:
                self.rollback(temp_current_retro)
            print("Post Retro Tree State: ")
            self._tree.print_tree()
            # self._rebuild()
            # self._tree.print_tree()
        print("Candidate nodes were: ", [node for node in node_list])

        # If the list is empty, there are no nodes less than or equal to x
        if len(node_list) == 0:
            return -1

        #  Otherwise, return the largest value in the list
        return max(node_list)

    def _get_nodes_less_than_or_equal_to_x(
        self, start: TreeNode, x: int, node_list: List[TreeNode]
    ) -> None:
        if start is not None:
            if start.value <= x:
                node_list.append(start.value)
            self._get_nodes_less_than_or_equal_to_x(start.left, x, node_list)
            self._get_nodes_less_than_or_equal_to_x(start.right, x, node_list)

    def print_tree(self) -> None:
        self._tree.print_tree()

    def print_log(self) -> None:
        if len(self._operations) == 0:
            print("Operation log is empty")
            return
        print("Operation log: ")
        for op in self._operations:
            print(op)


def test_avltree():
    # prefilled_tree = AVLTree([5, 3, 7, 2, 4, 6, 8])
    # prefilled_tree.print_tree()

    # empty_tree = AVLTree()
    # empty_tree.print_tree()
    # empty_tree.insert(TreeNode(5))
    # empty_tree.print_tree()
    # empty_tree.insert(TreeNode(3))
    # empty_tree.print_tree()
    # empty_tree.insert(TreeNode(7))
    # empty_tree.print_tree()
    # empty_tree.insert(TreeNode(2))
    # empty_tree.print_tree()
    # empty_tree.insert(TreeNode(4))
    # empty_tree.print_tree()
    # empty_tree.insert(TreeNode(6))
    # empty_tree.print_tree()
    # empty_tree.insert(TreeNode(8))

    random_tree = AVLTree()
    nums = list(set([random.randint(0, 100) for _ in range(10)]))
    random.shuffle(nums)
    for num in nums:
        random_tree.insert(TreeNode(num))
        random_tree.print_tree()
        random_tree.print_balances()


def test_partial_retroactive_avl():
    tree = PartialRetroactiveAVL()
    tree.insert(10)
    tree.insert(20)
    tree.insert(5)
    tree.delete(10)
    tree.insert(15)
    tree.delete(5)
    tree.insert(25)
    tree.insert(30)
    tree.delete(20)
    tree.insert(18)

    # First pred call
    print(f"Pred(17): {tree.pred(17)}")  # Should be the largest element <= 17

    tree.print_log()
    print()
    tree.print_tree()
    print()

    tree.insert(7, retro=True, retro_point=2)
    tree.delete(15, retro=True, retro_point=4)
    tree.insert(8, retro=True, retro_point=1)
    tree.delete(25, retro=True, retro_point=6)
    tree.delete(5, retro=True, retro_point=3)
    tree.insert(12, retro=True, retro_point=3)

    # Second pred call
    print(f"Pred(10): {tree.pred(10)}")  # Should be the largest element <= 10

    tree.print_log()
    print()
    tree.print_tree()
    print()

    # Third pred call
    print(f"Pred(20): {tree.pred(20)}")  # Should be the largest element <= 20


def test_fully_retroactive_avl():
    tree = FullyRetroactiveAVL()
    tree.insert(10)
    tree.insert(20)
    tree.insert(5)
    tree.delete(10)
    tree.insert(15)
    tree.delete(5)
    tree.insert(25)
    tree.insert(30)
    tree.delete(20)
    tree.insert(18)
    tree.insert(7, retro=True, retro_point=2)
    tree.delete(15, retro=True, retro_point=4)
    tree.insert(8, retro=True, retro_point=1)
    tree.delete(25, retro=True, retro_point=6)
    tree.delete(5, retro=True, retro_point=3)
    tree.insert(12, retro=True, retro_point=3)

    print(f"Retroactive Pred(20, 5): {tree.pred(20, retro=True, retro_point=5)}")


if __name__ == "__main__":
    # test_avltree()
    # test_partial_retroactive_avl()
    test_fully_retroactive_avl()
