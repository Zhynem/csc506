# CSC 506 - Design and Analysis of Algorithms
# Module 4 - Discussion
# Michael Luker
# Feb 8, 2024

# Prompt:
# Create a queue data structure using two stacks and post a screenshot to the forum. Provide a
# discussion of how you completed your activity. Additionally, you may pose any outstanding
# questions for your peers if you ran into any issues.

# Stack: Last-in First-Out, like a stack of plates. The last plate you put on top, is the first one
#        you grab when it's needed
#
# Queue: First-in First-out, just like people lining up to get on a ride, the person at the front of
#        the line will be the first one to get on the ride when they let people on. People get in
#        the queue at the back and are released at the front.

from dataclasses import dataclass
from typing import Any, Self

# First thing's first, I need a working stack. From this weeks content that is done with a node and
# then the data structure class


@dataclass
class Node:
    data: Any
    next: Self = None


# 3-P Operations, Push / Pop / Peek
class Stack:
    top: Node = None
    size = 0

    def push(self, new_node: Node) -> None:
        if self.top is not None:
            new_node.next = self.top
            self.top = new_node
        else:
            self.top = new_node
        self.size += 1

    def pop(self) -> Node:
        if self.top is not None:
            ret = self.top
            self.top = ret.next
            self.size -= 1
            ret.next = None
            return ret
        else:
            return None

    def peek(self) -> Node:
        return self.top

    def print_stack(self) -> str:
        if self.size == 0:
            return ""

        current = self.top
        next = current.next
        print_string = ""
        while True:
            if current is not None:
                print_string += f"{current.data} -> "
            if next is None:
                break
            else:
                current = next
                next = current.next

        return print_string[:-4]


# To create a queue with 2 stacks, I'm pretty sure we'll need to have one watching the front,
# and one for the back. Functions are to enqueue and dequeue only?
class Queue:
    front = Stack()
    back = Stack()
    size = 0

    def print_queue(self):
        print(f"Queue size: {self.size}")
        print(f"Back stack: {self.back.print_stack()}")
        print(f"Frnt stack: {self.front.print_stack()}")
        print()

    # Enqueuing will always add new nodes to the back stack ie. back of the line
    def enqueue(self, new_node: Node) -> None:
        self.back.push(new_node)
        self.size += 1

    # I thought this might be good to have, but realized that the ONLY time you should be moving
    # data from the back stack to the front is when the front is completely empty. Otherwise you
    # will get out-of-order data back from the queue which we don't want at all...
    # I guess I can enable it to prove via the assert below?
    # Yuppers
    # def move_stack_data(self) -> None:
    #     while True:
    #         node: Node = self.back.pop()
    #         if node is not None:
    #             self.front.push(node)
    #         else:
    #             break

    # Dequeuing needs to pull the top item from the front
    def dequeue(self) -> Node:
        # If the front stack is empty then we need to make sure there are expected items at all
        # Or if the queue in general is empty, return nothing
        if self.size == 0:
            return None

        item = self.front.pop()
        if item is not None:
            self.size -= 1
            return item
        else:
            # If there are items in the queue, but the front is empty, we need to get items from the
            # back stack somehow?
            # popping from the back stack will return what is intended to be the very last item in
            # the queue. By pushing that to the front stack and repeating, it will push that last
            # item to the bottom of the `front` stack, meaning it would be the last item dequeued?
            while True:
                node: Node = self.back.pop()
                if node is not None:
                    self.front.push(node)
                else:
                    break
            # After all the back-stack items move to the front stack, we still need to return the
            # first item in the queue
            item = self.front.pop()
            if item is not None:
                self.size -= 1
                return item
            else:
                return None


# Stuff for testing the stack bases queue works
test_queue = Queue()
test_queue.print_queue()

print("Adding 10, 20, 30, 40, 50")
test_queue.enqueue(Node(10))
test_queue.enqueue(Node(20))
test_queue.enqueue(Node(30))
test_queue.enqueue(Node(40))
test_queue.enqueue(Node(50))
test_queue.print_queue()

print("Removing 2 numbers")
print(test_queue.dequeue().data)
print(test_queue.dequeue().data)
test_queue.print_queue()

print("Adding 60, 70, 80, 90, 100")
test_queue.enqueue(Node(60))
test_queue.enqueue(Node(70))
test_queue.enqueue(Node(80))
test_queue.enqueue(Node(90))
test_queue.enqueue(Node(100))
test_queue.print_queue()

print("Removing all remaining numbers")
while True:
    item = test_queue.dequeue()
    if item is not None:
        print(item.data)
    else:
        break
print()
test_len = 20
print(f"Testing list of {test_len} numbers")
inputs = list(range(test_len))
test_queue2 = Queue()

for i in inputs:
    test_queue2.enqueue(Node(i))

outputs = []
while True:
    item = test_queue2.dequeue()
    if item is not None:
        outputs.append(item.data)
    else:
        break

print(inputs)
print(outputs)
assert inputs == outputs
print("Assert worked, output is in same order as input")


# Stuff for testing the stack works
# print(test_queue.size)
# test_queue.back.print_stack()
# test_queue.front.print_stack()
# print(test_queue.dequeue().data)
# print(test_queue.size)
# test_queue.back.print_stack()
# test_queue.front.print_stack()

# test_stack = Stack()
# test_stack.push(Node(10))
# test_stack.push(Node(20.5))
# test_stack.push(Node("beans"))
# test_stack.print_stack()
# print()
# print(test_stack.size)
# print()
# while True:
#     node: Node = test_stack.pop()
#     if node is not None:
#         print(node.data)
#     else:
#         break
# print()
# print(test_stack.size)
# print()
