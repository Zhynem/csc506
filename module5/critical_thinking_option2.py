class Heap:
  def __init__(self):
    self.size = 0
    self.heap = []

  def heapify(self, array):
    self.size = len(array)
    self.heap = array
    for i in range(self.size, -1, -1):
      self.bubble_down(i)

  def insert(self, value):
    self.heap.append(value)
    self.size += 1
    self.bubble_up(self.size - 1)
  
  def bubble_up(self, index):
    parent_index = (index - 1) // 2
    if index > 0 and self.heap[index] < self.heap[parent_index]:
      self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
      self.bubble_up(parent_index)

  def remove(self):
    if self.size == 0:
      return None
    self.size -= 1
    self.heap[0], self.heap[self.size] = self.heap[self.size], self.heap[0]
    self.bubble_down(0)
    return self.heap.pop()
  
  def bubble_down(self, index):
    left_index = 2 * index + 1
    right_index = 2 * index + 2
    smallest = index
    if left_index < self.size and self.heap[left_index] < self.heap[smallest]:
      smallest = left_index
    if right_index < self.size and self.heap[right_index] < self.heap[smallest]:
      smallest = right_index
    if smallest != index:
      self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
      self.bubble_down(smallest)



min_heap = Heap()
orig_nums = [25, 44, 55, 99, 30, 37, 15, 10, 2, 4]
# Deep copy the list
nums = orig_nums.copy()
min_heap.heapify(nums)

print(f"Min-heap: {min_heap.heap}")

sorted_list = []
while min_heap.size > 0:
  next_smallest = min_heap.remove()
  sorted_list.append(next_smallest)
  print(f"  Next smallest: {next_smallest}")
  print(f"  Heap: {min_heap.heap}")

print()
print(f"Sorted list: {sorted_list}")
assert sorted_list == sorted(orig_nums)
print("Assertion worked")