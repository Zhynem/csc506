# CSC 506 - Design and Analysis of Algorithms
# Module 5 - Discussion
# Michael Luker
# Feb 15, 2024

# Prompt:
# Explain the concept of a hash table. Then, compare it to other collection types such as dictionaries
# and sets.
# Now, let's utilize this sample data to discuss and analyze the differences between hash tables and
# dictionaries or sets. Examine how these data structures are used to store the sample data. 
# Importantly, please provide an example of executable code using both hash tables and 
# dictionaries/sets to store the data.


class HashTable:
    def __init__(self, size: int):
        self.size = size
        self.table = [None] * size
        self.collisions = 0

    # With hash sets you need to address the possability of a collision, where two different values
    # map to the same index. There are a few ways to handle this but one simple solution is to 
    # move to the next index and check again. 
    # Called linear probing https://en.wikipedia.org/wiki/Linear_probing
    def _probe(self, index: int, value) -> int:
        initial_index = index
        # If the index is already taken by something else, move to the next index
        while self.table[index] is not None and self.table[index] != value:
            index += 1
            self.collisions += 1
            if index == self.size:
                index = 0 
            if index == initial_index:
                raise ValueError("Table is full")
        return index
        
    def hash(self, value) -> int:
        # Convert the value into an integer index of a location in the table
        return sum([ord(char) for char in str(value)]) % self.size
        

    def insert(self, value) -> None:
        # Get the index to store the value at
        index = self._probe(self.hash(value), value)
        if self.table[index] is None:
            self.table[index] = value
        else:
            raise ValueError("Table is full")

    def delete(self, value) -> None:
        # Get the index to delete the value from
        index = self.hash(value)
        while self.table[index] != value:
            index += 1
            if index == self.size:
                index = 0
            if index == self.hash(value):
                raise ValueError("Value not found")
        self.table[index] = None

    def search(self, value) -> tuple[int, int]:
        # Get the initial index to search at
        initial_index = self.hash(value)
        index = initial_index
        
        # Start looking through the table for the value starting at the index and moving to the next
        # looping back to the start if needed.
        items_checked = 1
        while self.table[index] != value:
            index += 1
            items_checked += 1
            if index == self.size:
                index = 0
            # If we've looped back to the initial index, the value isn't in the table
            if index == initial_index:
                return -1
        return index, items_checked

    def print_table(self) -> None:
        for i, item in enumerate(self.table):
            if item is not None:
                print(f"Index {i}: {item}")

table = HashTable(10)
data = [
    (12345, "John Smith"),
    (67890, "Jane Doe"),
    (54321, "Alice Johnson"),
    (98765, "Bob Williams"),
    (24680, "Eve Brown"),
    (13579, "Charlie Davis"),
    (11223, "Grace Wilson"),
    (44556, "David Lee"),
    (99999, "Olivia Martinez"),
    (77777, "Sophia Anderson")
]

print("Inserting data into the table...")
for item in data:
    print(f"Inserting {item[1]} : Hashes to {table.hash(item[1])}")
    table.insert(item[1])

print()
print(f"Collisions: {table.collisions}")
print()

table.print_table()

# Let's plot the collisions and table size
import matplotlib.pyplot as plt

sizes = list(range(10, 410, 10))
collisions = [0] * len(sizes)
for i, size in enumerate(sizes):
    table = HashTable(size)
    for item in data:
        table.insert(item[1])
    collisions[i] = table.collisions
plt.plot(sizes, collisions)
plt.xlabel("Table Size")
plt.ylabel("Collisions")
plt.title("Collisions vs Table Size")
plt.show()

# Compare insertion and search times for hash tables, dictionaries, and sets
from timeit import timeit

ins_hash_timings = []
ins_dict_timings = []
ins_set_timings = []
srch_hash_timings = []
srch_dict_timings = []
srch_set_timings = []

sizes = [10, 20, 40, 80, 100]
for size in sizes:
    

    # Couple of inline functions to make inserting into the dictionary and set easier to time
    def insert_hash(data):
        for item in data:
            table.insert(item[1])
    def insert_dict(data):
        for item in data:
            my_dict[item[0]] = item[1]
    def insert_set(item):
        for item in data:
            my_set.add(item[1])
    def search_dict(item):
        return item[0] in my_dict
    def search_set(item):
        return item[1] in my_set

    # For insertion tests we'll need to insert the item, then delete it
    temp_timings = {"hash": [], "dict": [], "set": []}
    for _ in range(1000):
        # Start with new empty structures
        table = HashTable(size)
        my_dict = {}
        my_set = set()

        temp_timings["hash"].append(timeit(lambda: insert_hash(data), number=1))
        temp_timings["dict"].append(timeit(lambda: insert_dict(data), number=1))
        temp_timings["set"].append(timeit(lambda: insert_set(data), number=1))

    ins_hash_timings.append(sum(temp_timings["hash"])/1000)
    ins_dict_timings.append(sum(temp_timings["dict"])/1000)
    ins_set_timings.append(sum(temp_timings["set"])/1000)
    # Now the search timings after re-adding the item to look for
    item = data[0]
    table = HashTable(size)
    my_dict = {}
    my_set = set()
    insert_hash(data)
    insert_dict(data)
    insert_set(data)
    srch_hash_timings.append(timeit(lambda: table.search(item[1]), number=1000))
    srch_dict_timings.append(timeit(lambda: search_dict(item), number=1000))
    srch_set_timings.append(timeit(lambda: search_set(item), number=1000))

plt.plot(sizes, ins_hash_timings, label="Hash Table Insert")
plt.plot(sizes, ins_dict_timings, label="Dictionary Insert")
plt.plot(sizes, ins_set_timings, label="Set Insert")
plt.xlabel("Table Size")
plt.ylabel("Time (s)")
plt.title("Insertion Time vs Table Size")
plt.legend()
plt.show()

plt.plot(sizes, srch_hash_timings, label="Hash Table Search")
plt.plot(sizes, srch_dict_timings, label="Dictionary Search")
plt.plot(sizes, srch_set_timings, label="Set Search")
plt.xlabel("Table Size")
plt.ylabel("Time (s)")
plt.title("Search Time vs Table Size")
plt.legend()
plt.show()