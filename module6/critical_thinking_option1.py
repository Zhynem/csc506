# CSC 506 - Design and Analysis of Algorithms
# Module 6 - Critical Thinking - Option 1
# Michael Luker
# Feb 25, 2024
"""
Prompt:
You'll build a simple binary search tree in this activity.

Build a Node class. It is should have attributes for the data it stores as well as its left and 
right children. As a bonus, try including the Comparable module and make nodes compare using their 
data attribute.

Build a Tree class that accepts an array when initialized. The Tree class should have a root 
attribute that uses the return value of #build_tree which you'll write next.

Write a #build_tree method that takes an array of data 
(e.g. [1, 7, 4, 23, 8, 9, 4, 3, 5, 7, 9, 67, 6345, 324]) and turns it into a balanced binary tree 
full of Node objects appropriately placed (don't forget to sort and remove duplicates!). 
The #build_tree method should return the level-1 root node.

Write an #insert and #delete method which accepts a value to insert/delete.

Compile and submit your source code and screenshots of the application executing the application and
the results in a single document.
"""

# Simplify tree visualization with networkx
import networkx as nx
import matplotlib.pyplot as plt
import random

from typing import Any, Self, List

# ChatGPT recommended using the total_ordering decorator and implementing the equal and less than
# methods then the total_ordering will take care of all the other compare functions
from functools import total_ordering

# Lots of referencing from the wiki on AVL tree (balanced BST)
# https://en.wikipedia.org/wiki/AVL_tree

# Also https://www.geeksforgeeks.org/introduction-to-avl-tree/
# https://www.geeksforgeeks.org/insertion-in-an-avl-tree/
# https://www.geeksforgeeks.org/deletion-in-an-avl-tree/
# https://www.geeksforgeeks.org/insertion-in-binary-search-tree/


# Found this stack overflow post about using the networkx package and this function to create
# pyplot images of the binary tree in a hierarchical way
def hierarchy_pos(G, root=None, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    """
    if not nx.is_tree(G):
        raise TypeError("cannot use hierarchy_pos on a graph that is not a tree")

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(
                iter(nx.topological_sort(G))
            )  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(
        G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None
    ):
        """
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        """

        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(
                    G,
                    child,
                    width=dx,
                    vert_gap=vert_gap,
                    vert_loc=vert_loc - vert_gap,
                    xcenter=nextx,
                    pos=pos,
                    parent=root,
                )
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


@total_ordering
class Node:
    def __init__(
        self, data: Any, parent: Self = None, left: Self = None, right: Self = None
    ) -> None:
        self.data = data
        self.parent = parent
        self.left = left
        self.right = right
        self.bf = 0

    # For the comparables make sure nodes are of the same data type, then do the comparison
    def __eq__(self, __value: Self) -> bool:
        return (
            __value is not None
            and isinstance(__value.data, type(self.data))
            and self.data == __value.data
        )

    def __lt__(self, __value: Self) -> bool:
        return (
            __value is not None
            and isinstance(__value.data, type(self.data))
            and self.data < __value.data
        )

    def __str__(self) -> str:
        if self.parent is None:
            return f"Self: {self.data} | BF: {self.bf} | Parent: None | Left: {self.left is not None} | Right: {self.right is not None}"
        else:
            return f"Self: {self.data} | BF: {self.bf} | Parent: {self.parent.data} | Left: {self.left is not None} | Right: {self.right is not None}"


class AVLTree:
    def __init__(self, start_data: List[Any] = None) -> None:
        self.root = None
        self.count = 0
        if start_data:
            self._build_tree(start_data)

    def _build_tree(self, start_data: List[Any]) -> Node:
        # The prompt calls for sorting and removing duplicates from the data before turning it into
        # a balanced tree?
        # This removes duplicates by casting the list as a set, then back to a list, then sort it
        start_data = sorted(list(set(start_data)))
        for i in start_data:
            self.insert(i)

    def _is_balanced(self, node: Node) -> bool:
        # Wiki says nodes can all have a balance factor, and the tree (or subtree?) is balanced
        # when the balance factor is in the set of {-1, 0, 1}
        # Computed by BF(x) := Height(RightSubtree(X)) - Height(LeftSubtree(X))
        return node.bf in {-1, 0, 1}

    def _rotate_left(self, node: Node) -> None:
        # From https://www.geeksforgeeks.org/introduction-to-avl-tree/
        # From a->b->c make it b->a(left) and b->c(right, unmoved)
        # basically swapping the blase of a and b
        a = node
        b = a.right
        # The right child of a becomes the left child of b
        a.right = b.left
        # If the left child of b is not None then the left child's parent becomes a
        if b.left is not None:
            b.left.parent = a
        # The parent of b becomes the parent of a
        b.parent = a.parent
        # If a's parent is None then b becomes the root of the tree
        if a.parent is None:
            self.root = b
        # If a is the left child of its parent then b becomes the left child
        elif a.parent is not None and a == a.parent.left:
            a.parent.left = b
        # If a is the right child of its parent then b becomes the right child
        else:
            a.parent.right = b
        # The left child of b becomes a
        b.left = a
        # The parent of a becomes b
        a.parent = b
        # Update the balance factors
        self._update_bf(b)

    def _rotate_right(self, node: Node) -> None:
        # Similar to rotate left, but c->b->a becomes b->c(left, unmoved) and b->a(right)
        # basically swapping the base of a and b
        a = node
        b = a.left
        # The left child of a becomes the right child of b
        a.left = b.right
        # If the right child of b is not None then the right child's parent becomes a
        if b.right is not None:
            b.right.parent = a
        # The parent of b becomes the parent of a
        b.parent = a.parent
        # If a's parent is None then b becomes the root of the tree
        if a.parent is None:
            self.root = b
        # If a is the left child of its parent then b becomes the left child
        elif a.parent is not None and a == a.parent.left:
            a.parent.left = b
        # If a is the right child of its parent then b becomes the right child
        else:
            a.parent.right = b
        # The right child of b becomes a
        b.right = a
        # The parent of a becomes b
        a.parent = b
        # Update the balance factors
        self._update_bf(b)

    def _rebalance(self, node: Node) -> None:
        # Since we start at a node and work up, at some point we reach the root / root parent that
        # is none
        if node is None:
            return

        # If it's not nothing then we should check before doing any kind of rebalancing
        if self._is_balanced(node):
            # If it's balanced at this layer then just keep moving up
            self._rebalance(node.parent)
            return

        # If it's not balanced, then this is where we need to start applying the rotations
        # Because balance factor is calculated as right_height - left_height, it means that a bf of
        # -2 or lower has more height of the left side, and bf of 2 or greater has more on the right
        # So we'll need to rotate accordingly
        # if node.bf >= 2:
        #     self._rotate_left(node)
        # else:
        #     self._rotate_right(node)
        # Need to account for 4 cases of rotation: LeftLeft, LeftRight, RightRight, and RightLeft
        # LeftLeft
        if node.bf > 1 and node.right.bf >= 0:
            self._rotate_left(node)
        # LeftRight
        elif node.bf > 1 and node.right.bf < 0:
            self._rotate_right(node.right)
            self._rotate_left(node)
        # RightRight
        elif node.bf < -1 and node.left.bf <= 0:
            self._rotate_right(node)
        # RightLeft
        elif node.bf < -1 and node.left.bf > 0:
            self._rotate_left(node.left)
            self._rotate_right(node)

        # After the rotation we can continue upward
        self._rebalance(node.parent)

    def insert(self, data: Any) -> None:
        # From https://www.geeksforgeeks.org/insertion-in-an-avl-tree
        # Insert the node to the tree via standard BST insertion
        print(f"Inserting {data}")
        if self.root is not None:
            new_node = Node(data)
            self._bst_insert(self.root, new_node, self.root)
        else:
            self.root = Node(data)
            print()
            return
        # Update the balance factors
        print(f"New Node: {new_node}")
        self._update_bf(self.root)
        # Start rebalancing the tree starting from the new node and moving up
        self._rebalance(new_node)
        # self.print_tree()
        # print()

    def _update_bf(self, node: Node) -> None:
        if node is None:
            return
        node.bf = self._height(node.right) - self._height(node.left)
        self._update_bf(node.left)
        self._update_bf(node.right)

    def _height(self, node: Node) -> int:
        if node is None:
            return 0
        return 1 + max([self._height(node.left), self._height(node.right)])

    def _bst_insert(
        self, current_node: Node, new_node: Node, parent_node: Node
    ) -> Node:
        # Standard BST insert from https://www.geeksforgeeks.org/insertion-in-binary-search-tree/
        # If there is no "current node" at the location then set it to be the new node
        if current_node is None:
            new_node.parent = parent_node
            return new_node
        else:
            # If the value is already in the BST then just keep using the current node
            if current_node == new_node:
                return current_node
            # New being greater goes to the right
            elif current_node < new_node:
                current_node.right = self._bst_insert(
                    current_node.right, new_node, current_node
                )
            # New being less than goes to the left
            else:
                current_node.left = self._bst_insert(
                    current_node.left, new_node, current_node
                )
        return current_node

    def delete(self, data: Any) -> None:
        # Find the node to delete get its parent
        # removed_from = None
        temp = Node(data)
        # If the root is the only node in the tree and it's being deleted, that's an easy case
        if temp == self.root and self.root.left is None and self.root.right is None:
            self.root = None
            return
        current_node = self.root
        removed_from = None
        while current_node is not None:
            if current_node == temp:
                removed_from = current_node
                break
            elif current_node < temp:
                current_node = current_node.right
            else:
                current_node = current_node.left
        # Standard BST delete
        if removed_from and removed_from.parent is not None:
            print(f"Removing {data} from {removed_from.parent.data}")
        else:
            print(f"Removing {data} from root")
        removed_from = self._bst_delete(self.root, temp)
        # Update the balance factors
        self._update_bf(self.root)
        # start rebalancing the tree starting from around where the node was deleted from
        # Make sure the parent has both children balanced, may be over the top
        self._rebalance(removed_from.left)
        self._rebalance(removed_from.right)

    def _bst_delete(self, current_node: Node, data: Node) -> Node:
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
            del current_node
            return None
        # If it only has one child node
        elif current_node.left is None and current_node.right is not None:
            temp = current_node.right
            temp.parent = current_node.parent
            current_node = None
            return temp
        elif current_node.right is None and current_node.left is not None:
            temp = current_node.left
            temp.parent = current_node.parent
            current_node = None
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
            current_node.data = temp.data

            # delete the successor node
            del temp
            return current_node

    def print_tree(self, title="Tree State") -> None:
        if self.root is None:
            return
        graph = nx.Graph()
        self._add_graph_node(graph, self.root)
        pos = hierarchy_pos(graph, self.root.data)
        nx.draw(graph, pos=pos, with_labels=True)
        # plt.show()
        self.count += 1
        plt.title(title)
        # plt.savefig(f"gif/tree{self.count:03d}.png")
        plt.savefig(f"build_tree.png")
        plt.clf()

    def _add_graph_node(self, graph: nx.Graph, node: Node) -> None:
        if node:
            print(node)
            graph.add_node(node.data)
            if node.parent is not None:
                graph.add_edge(node.parent.data, node.data)
            self._add_graph_node(graph, node.left)
            self._add_graph_node(graph, node.right)


# This all seemed to work :D
avl = AVLTree([72, 70, 79, 12, 52, 80, 75, 55, 88, 83, 31, 37, 73, 54, 38])
avl.print_tree()
exit()
# # Test delete an upper branch with two children
# avl.delete(79)
# avl.print_tree()
# # Test delete a leaf
# avl.delete(37)
# avl.print_tree()
# # Test delete a node with one child
# avl.delete(31)
# avl.print_tree()
# # Another leaf
# avl.delete(12)
# avl.print_tree()
# # Delete the root
# avl.delete(70)
# avl.print_tree()


# Let's make a gif for funsies
nums = list(set([random.randint(0, 100) for _ in range(20)]))
random.shuffle(nums)
# nums = [72, 70, 79, 12, 52, 80, 75, 55, 88, 83, 31, 37, 73, 54, 38]
avl = AVLTree()
avl.print_tree()
# Make frames for each number insertion
for i in nums:
    avl.insert(i)
    avl.print_tree()

# Add some buffer frames before starting the delteions
avl.print_tree()
avl.print_tree()
avl.print_tree()
avl.print_tree()
avl.print_tree()

# Then for each random deletion
random.shuffle(nums)
while len(nums) > 0 and avl.root is not None:
    removed_num = random.choice(nums)
    nums.remove(removed_num)
    avl.delete(removed_num)
    avl.print_tree()
