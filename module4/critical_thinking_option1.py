# CSC 506 - Design and Analysis of Algorithms
# Module 4 - Critical Thinking - Option 1
# Michael Luker
# Feb 11, 2024
"""
Prompt:
Design and implement an experiment that will compare the performance of the Python list based stack 
and queue with the linked list implementation. Provide a brief discussion of both stacks and queues 
for this activity.

Your Python Programming submission materials must include your source code and screenshots of the 
Python interface executing the application and the results.
"""

# I have a theory that there will be different performance and memory characteristics between the
# built-in Python list, and dict vs slots based linked list implementations.

from abc import ABC
from dataclasses import dataclass
from typing import List, Any, Self
from pympler import asizeof
import timeit
from matplotlib import pyplot as plt


# 2 types of LL node
@dataclass(slots=False)
class DictNode:
    data: Any
    next: Self = None


@dataclass(slots=True)
class SlotNode:
    data: Any
    next: Self = None


# 3 types of stack
class PyListStack:
    stack: List[Any] = []
    size = 0

    def push(self, new_node: Any) -> None:
        self.stack.append(new_node)
        self.size += 1

    def pop(self) -> Any:
        if self.size > 0:
            self.size -= 1
            return self.stack.pop()
        else:
            return None

    def print_stack(self) -> str:
        if self.size == 0:
            return ""
        ret = ""
        for i in range(self.size):
            ret += f"{self.stack[i]}\n"
        return ret


class DictLLStack:
    top: DictNode = None
    size = 0

    def push(self, new_node: DictNode) -> None:
        if self.top is not None:
            new_node.next = self.top
            self.top = new_node
        else:
            self.top = new_node
        self.size += 1

    def pop(self) -> DictNode:
        if self.top is not None:
            ret = self.top
            self.top = ret.next
            self.size -= 1
            ret.next = None
            return ret
        else:
            return None

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


class SlotLLStack:
    top: SlotNode = None
    size = 0

    def push(self, new_node: SlotNode) -> None:
        if self.top is not None:
            new_node.next = self.top
            self.top = new_node
        else:
            self.top = new_node
        self.size += 1

    def pop(self) -> SlotNode:
        if self.top is not None:
            ret = self.top
            self.top = ret.next
            self.size -= 1
            ret.next = None
            return ret
        else:
            return None

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


# 3 types of queue
class PyListQueue:
    queue: List[Any] = []
    size = 0

    def enqueue(self, new_node: Any) -> None:
        self.queue.append(new_node)
        self.size += 1

    def dequeue(self) -> Any:
        if self.size > 0:
            self.size -= 1
            return self.queue.pop(0)
        else:
            return None

    def print_queue(self) -> str:
        if self.size == 0:
            return ""
        ret = ""
        for i in range(self.size):
            ret += f"{self.queue[i]}\n"
        return ret


class DictLLQueue:
    front = DictLLStack()
    back = DictLLStack()
    size = 0

    def enqueue(self, new_node: DictNode) -> None:
        self.back.push(new_node)
        self.size += 1

    def dequeue(self) -> DictNode:
        if self.size > 0:
            if self.front.size == 0:
                while self.back.size > 0:
                    self.front.push(self.back.pop())
            self.size -= 1
            return self.front.pop()
        else:
            return None

    def print_queue(self) -> str:
        if self.size == 0:
            return ""
        ret = ""
        ret += "Front: " + self.front.print_stack()
        ret += "\n"
        ret += "Back : " + self.back.print_stack()
        return ret


class SlotLLQueue:
    front = SlotLLStack()
    back = SlotLLStack()
    size = 0

    def enqueue(self, new_node: SlotNode) -> None:
        self.back.push(new_node)
        self.size += 1

    def dequeue(self) -> SlotNode:
        if self.size > 0:
            if self.front.size == 0:
                while self.back.size > 0:
                    self.front.push(self.back.pop())
            self.size -= 1
            return self.front.pop()
        else:
            return None

    def print_queue(self) -> str:
        if self.size == 0:
            return ""
        ret = ""
        ret += "Front: " + self.front.print_stack()
        ret += "\n"
        ret += "Back : " + self.back.print_stack()
        return ret


def sizeof(obj, type="dict"):
    if type == "dict":
        return asizeof.asizeof(DictNode(1)) * obj.size
    elif type == "slot":
        return asizeof.asizeof(SlotNode(1)) * obj.size
    else:
        try:
            if obj.stack:
                return asizeof.asizeof(obj.stack)
        except:
            return asizeof.asizeof(obj.queue)


def test_stack(stack, type="dict"):
    print("Pushing 1, 2, 3")
    if type == "dict":
        stack.push(DictNode(1))
        stack.push(DictNode(2))
        stack.push(DictNode(3))
    elif type == "slot":
        stack.push(SlotNode(1))
        stack.push(SlotNode(2))
        stack.push(SlotNode(3))
    else:
        stack.push(1)
        stack.push(2)
        stack.push(3)
    print(stack.print_stack())
    print()
    print("Popping 2 items then pushing 4, 5, 6")

    stack.pop()
    stack.pop()
    if type == "dict":
        stack.push(DictNode(4))
        stack.push(DictNode(5))
        stack.push(DictNode(6))
    elif type == "slot":
        stack.push(SlotNode(4))
        stack.push(SlotNode(5))
        stack.push(SlotNode(6))
    else:
        stack.push(4)
        stack.push(5)
        stack.push(6)
    print(stack.print_stack())
    print()
    print(f"Size of {type} stack: {sizeof(stack, type)} bytes")
    print("========================================================")


def test_queue(queue, type="dict"):
    print("Enqueuing 1, 2, 3")
    if type == "dict":
        queue.enqueue(DictNode(1))
        queue.enqueue(DictNode(2))
        queue.enqueue(DictNode(3))
    elif type == "slot":
        queue.enqueue(SlotNode(1))
        queue.enqueue(SlotNode(2))
        queue.enqueue(SlotNode(3))
    else:
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)
    print(queue.print_queue())
    print()
    print("Dequeuing 2 items, then enqueuing 4, 5, 6")
    queue.dequeue()
    queue.dequeue()
    if type == "dict":
        queue.enqueue(DictNode(4))
        queue.enqueue(DictNode(5))
        queue.enqueue(DictNode(6))
    elif type == "slot":
        queue.enqueue(SlotNode(4))
        queue.enqueue(SlotNode(5))
        queue.enqueue(SlotNode(6))
    else:
        queue.enqueue(4)
        queue.enqueue(5)
        queue.enqueue(6)
    print(queue.print_queue())
    print()
    print(f"Size of {type} queue: {sizeof(queue, type)} bytes")
    print("========================================================")


if __name__ == "__main__":
    # First let's test all the stack and queue implementations by addings 1, 2, 3 then removing 2
    # items, then adding 4, 5, 6
    # print("========================================================")
    # print("Testing PyListStack")
    # test_stack(PyListStack(), "list")
    # print("Testing DictLLStack")
    # test_stack(DictLLStack(), "dict")
    # print("Testing SlotLLStack")
    # test_stack(SlotLLStack(), "slot")
    # print("Testing PyListQueue")
    # test_queue(PyListQueue(), "list")
    # print("Testing DictLLQueue")
    # test_queue(DictLLQueue(), "dict")
    # print("Testing SlotLLQueue")
    # test_queue(SlotLLQueue(), "slot")

    # Performance tests
    list_stack_times = {"push": {}, "pop": {}}
    list_queue_times = {"enqueue": {}, "dequeue": {}}
    dict_stack_times = {"push": {}, "pop": {}}
    dict_queue_times = {"enqueue": {}, "dequeue": {}}
    slot_stack_times = {"push": {}, "pop": {}}
    slot_queue_times = {"enqueue": {}, "dequeue": {}}

    # Memory tests
    list_stack_memory = {}
    list_queue_memory = {}
    dict_stack_memory = {}
    dict_queue_memory = {}
    slot_stack_memory = {}
    slot_queue_memory = {}

    # Gather the data
    num_tests = 100

    for i in range(10_000, 110_000, 10_000):
        print(f"Testing with {i} items")
        inputs = list(range(i))
        py_stack = PyListStack()
        py_queue = PyListQueue()
        dict_stack = DictLLStack()
        dict_queue = DictLLQueue()
        slot_stack = SlotLLStack()
        slot_queue = SlotLLQueue()

        list_stack_times["push"][i] = []
        list_stack_times["pop"][i] = []
        list_queue_times["enqueue"][i] = []
        list_queue_times["dequeue"][i] = []
        dict_stack_times["push"][i] = []
        dict_stack_times["pop"][i] = []
        dict_queue_times["enqueue"][i] = []
        dict_queue_times["dequeue"][i] = []
        slot_stack_times["push"][i] = []
        slot_stack_times["pop"][i] = []
        slot_queue_times["enqueue"][i] = []
        slot_queue_times["dequeue"][i] = []

        # Time how long it takes to insert then remove i number of items, testing it j times for
        # averaging
        for j in range(num_tests):
            list_stack_times["push"][i].append(
                timeit.timeit(lambda: [py_stack.push(x) for x in inputs], number=1)
            )
            list_stack_times["pop"][i].append(
                timeit.timeit(lambda: [py_stack.pop() for _ in inputs], number=1)
            )
            list_queue_times["enqueue"][i].append(
                timeit.timeit(lambda: [py_queue.enqueue(x) for x in inputs], number=1)
            )
            list_queue_times["dequeue"][i].append(
                timeit.timeit(lambda: [py_queue.dequeue() for _ in inputs], number=1)
            )

            dict_stack_times["push"][i].append(
                timeit.timeit(
                    lambda: [dict_stack.push(DictNode(x)) for x in inputs], number=1
                )
            )
            dict_stack_times["pop"][i].append(
                timeit.timeit(lambda: [dict_stack.pop() for _ in inputs], number=1)
            )
            dict_queue_times["enqueue"][i].append(
                timeit.timeit(
                    lambda: [dict_queue.enqueue(DictNode(x)) for x in inputs], number=1
                )
            )
            dict_queue_times["dequeue"][i].append(
                timeit.timeit(lambda: [dict_queue.dequeue() for _ in inputs], number=1)
            )

            slot_stack_times["push"][i].append(
                timeit.timeit(
                    lambda: [slot_stack.push(SlotNode(x)) for x in inputs], number=1
                )
            )
            slot_stack_times["pop"][i].append(
                timeit.timeit(lambda: [slot_stack.pop() for _ in inputs], number=1)
            )
            slot_queue_times["enqueue"][i].append(
                timeit.timeit(
                    lambda: [slot_queue.enqueue(SlotNode(x)) for x in inputs], number=1
                )
            )
            slot_queue_times["dequeue"][i].append(
                timeit.timeit(lambda: [slot_queue.dequeue() for _ in inputs], number=1)
            )
            print(f"  Size: {i} | Test {j + 1} of {num_tests} done")

        # Now get the memory of each of the data structures at this size, need to re-insert though
        # since the data structures are empty
        [py_stack.push(x) for x in inputs]
        [py_queue.enqueue(x) for x in inputs]
        [dict_stack.push(DictNode(x)) for x in inputs]
        [dict_queue.enqueue(DictNode(x)) for x in inputs]
        [slot_stack.push(SlotNode(x)) for x in inputs]
        [slot_queue.enqueue(SlotNode(x)) for x in inputs]

        list_stack_memory[i] = sizeof(py_stack, "list")
        list_queue_memory[i] = sizeof(py_queue, "list")
        dict_stack_memory[i] = sizeof(dict_stack, "dict")
        dict_queue_memory[i] = sizeof(dict_queue, "dict")
        slot_stack_memory[i] = sizeof(slot_stack, "slot")
        slot_queue_memory[i] = sizeof(slot_queue, "slot")

    # Now plot the data
    # First figure will the the times for inserting on each data structure
    figs, axs = plt.subplots(3, 2, figsize=(10, 10))
    stack_ins_ax = axs[0, 0]
    queue_ins_ax = axs[0, 1]
    stack_rem_ax = axs[1, 0]
    queue_rem_ax = axs[1, 1]
    stack_mem_ax = axs[2, 0]
    queue_mem_ax = axs[2, 1]

    # Divide by the size as well to get the average time per operation rather than overall time
    # (we expect the overall time to go up as the list gets longer, but the time per operation
    # should remain constant?)
    stack_ins_ax.plot(
        list_stack_times["push"].keys(),
        [
            (sum(values) / len(values)) / size
            for size, values in list_stack_times["push"].items()
        ],
        label="PyListStack",
    )
    stack_ins_ax.plot(
        dict_stack_times["push"].keys(),
        [
            (sum(values) / len(values)) / size
            for size, values in dict_stack_times["push"].items()
        ],
        label="DictLLStack",
    )
    stack_ins_ax.plot(
        slot_stack_times["push"].keys(),
        [
            (sum(values) / len(values)) / size
            for size, values in slot_stack_times["push"].items()
        ],
        label="SlotLLStack",
    )
    stack_ins_ax.set_xlabel("Number of items")
    stack_ins_ax.set_ylabel("Time (s)")
    stack_ins_ax.set_title("Time to insert items into stacks")
    stack_ins_ax.legend(loc="upper left")

    queue_ins_ax.plot(
        list_queue_times["enqueue"].keys(),
        [
            (sum(values) / len(values)) / size
            for size, values in list_queue_times["enqueue"].items()
        ],
        label="PyListQueue",
    )
    queue_ins_ax.plot(
        dict_queue_times["enqueue"].keys(),
        [
            (sum(values) / len(values)) / size
            for size, values in dict_queue_times["enqueue"].items()
        ],
        label="DictLLQueue",
    )
    queue_ins_ax.plot(
        slot_queue_times["enqueue"].keys(),
        [
            (sum(values) / len(values)) / size
            for size, values in slot_queue_times["enqueue"].items()
        ],
        label="SlotLLQueue",
    )
    queue_ins_ax.set_xlabel("Number of items")
    queue_ins_ax.set_ylabel("Time (s)")
    queue_ins_ax.set_title("Time to insert items into queues")
    queue_ins_ax.legend(loc="upper left")

    # Second figures will the the times for removing on each data structure
    stack_rem_ax.plot(
        list_stack_times["pop"].keys(),
        [
            (sum(values) / len(values)) / size
            for size, values in list_stack_times["pop"].items()
        ],
        label="PyListStack",
    )
    stack_rem_ax.plot(
        dict_stack_times["pop"].keys(),
        [
            (sum(values) / len(values)) / size
            for size, values in dict_stack_times["pop"].items()
        ],
        label="DictLLStack",
    )
    stack_rem_ax.plot(
        slot_stack_times["pop"].keys(),
        [
            (sum(values) / len(values)) / size
            for size, values in slot_stack_times["pop"].items()
        ],
        label="SlotLLStack",
    )
    stack_rem_ax.set_xlabel("Number of items")
    stack_rem_ax.set_ylabel("Time (s)")
    stack_rem_ax.set_title("Time to remove items from stacks")
    stack_rem_ax.legend(loc="upper left")

    queue_rem_ax.plot(
        list_queue_times["dequeue"].keys(),
        [
            (sum(values) / len(values)) / size
            for size, values in list_queue_times["dequeue"].items()
        ],
        label="PyListQueue",
    )
    queue_rem_ax.plot(
        dict_queue_times["dequeue"].keys(),
        [
            (sum(values) / len(values)) / size
            for size, values in dict_queue_times["dequeue"].items()
        ],
        label="DictLLQueue",
    )
    queue_rem_ax.plot(
        slot_queue_times["dequeue"].keys(),
        [
            (sum(values) / len(values)) / size
            for size, values in slot_queue_times["dequeue"].items()
        ],
        label="SlotLLQueue",
    )
    queue_rem_ax.set_xlabel("Number of items")
    queue_rem_ax.set_ylabel("Time (s)")
    queue_rem_ax.set_title("Time to remove items from queues")
    queue_rem_ax.legend(loc="upper left")

    # Third figures will the the memory usage of each data structure
    stack_mem_ax.plot(
        list_stack_memory.keys(), list_stack_memory.values(), label="PyListStack"
    )
    stack_mem_ax.plot(
        dict_stack_memory.keys(), dict_stack_memory.values(), label="DictLLStack"
    )
    stack_mem_ax.plot(
        slot_stack_memory.keys(), slot_stack_memory.values(), label="SlotLLStack"
    )
    stack_mem_ax.set_xlabel("Number of items")
    stack_mem_ax.set_ylabel("Memory (bytes)")
    stack_mem_ax.set_title("Memory usage of stacks")
    stack_mem_ax.legend(loc="upper left")

    queue_mem_ax.plot(
        list_queue_memory.keys(), list_queue_memory.values(), label="PyListQueue"
    )
    queue_mem_ax.plot(
        dict_queue_memory.keys(), dict_queue_memory.values(), label="DictLLQueue"
    )
    queue_mem_ax.plot(
        slot_queue_memory.keys(), slot_queue_memory.values(), label="SlotLLQueue"
    )
    queue_mem_ax.set_xlabel("Number of items")
    queue_mem_ax.set_ylabel("Memory (bytes)")
    queue_mem_ax.set_title("Memory usage of queues")
    queue_mem_ax.legend(loc="upper left")

    # Make sure all the different graphs don't overlap
    plt.tight_layout()

    plt.show()
