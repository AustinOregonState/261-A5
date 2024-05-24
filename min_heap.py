# Name: Austin Holcomb
# OSU Email: holcomau@OregonState.edu
# Course: CS261 - Data Structures
# Assignment: A5: MinHeap Implementation
# Due Date: 5/28/2024
# Description: MinHeap class that has an add and remove function that auto-balances the heap. A get_min,
# size, and clear method. It also has a build_heap method that will build a MinHeap from an invalid heap
# array. There is also an outside function that will use a heapsort to sort an unsorted array.


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MinHeap with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MinHeap content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return "HEAP " + str(heap_data)

    def add(self, node: object) -> None:
        """
        Adds an element to the MinHeap
        """
        if self.is_empty():
            self._heap.append(node)
            return

        # Append node to the end of the priority queue\
        self._heap.append(node)

        # Find correct node position in priority queue
        node_index = self._heap.length() - 1
        parent_index = (node_index - 1) // 2
        parent_value = self._heap.get_at_index(parent_index)

        while node < parent_value:
            # Swap
            self._heap.set_at_index(node_index, parent_value)
            self._heap.set_at_index(parent_index, node)
            # Update indices
            node_index = parent_index
            parent_index = (node_index - 1) // 2
            # If node not at end of queue, update parent value
            if parent_index >= 0:
                parent_value = self._heap.get_at_index(parent_index)
            else:
                break

    def is_empty(self) -> bool:
        """
        Checks if the MinHeap is empty
        """
        if self._heap.is_empty():
            return True
        return False

    def get_min(self) -> object:
        """
        Returns the minimum key
        """
        if self._heap.is_empty():
            raise MinHeapException
        return self._heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        Returns an object with the minimum key, andd removes it from the heap. If the
        heap is empty, the method raises a MinHeapException
        """
        if self._heap.is_empty():
            raise MinHeapException

        # Heap contains only one value
        min_value = self._heap[0]
        if self._heap.length() == 1:
            self.clear()
            return min_value

        # Find successor
        successor = self._heap.get_at_index(self._heap.length() - 1)
        self._heap.remove_at_index(self._heap.length() - 1)  # Remove successor at end of heap
        self._heap[0] = successor  # Overwrite current MinKey with successor

        # Percolate new successor down
        _percolate_down(self._heap, 0)

        return min_value

    def build_heap(self, da: DynamicArray) -> None:
        """
        Overwrites the current heap, and creates a new one with the given dynamic aray
        """
        self.clear()
        # Input da into cleared heap
        for index in range(da.length()):
            self._heap.insert_at_index(index, da.get_at_index(index))
        # Create valid MinHeap (not a MinHeap object) from da
        heapify(self._heap)


    def size(self) -> int:
        """
        Returns the size of the heap
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        Clears the heap
        """
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    Takes a dynamic array, creates a valid heap out of it, then completes heap sort
    """
    # Create a valid MinHeap
    heapify(da)

    # Heapsort
    last_index = da.length() - 1
    while last_index > 0:
        # Swap first and last nodes
        last_value = da.get_at_index(last_index)
        da.set_at_index(last_index, da.get_at_index(0))
        da.set_at_index(0, last_value)
        _percolate_down_heap_sort(da, last_index)  # Percolate down to > last_index
        # Decrement last_index
        last_index -= 1


def _percolate_down_heap_sort(da: DynamicArray, end_of_sort_index) -> None:
    """
    Percolates down a heap until it can no longer, or it reaches the end of the sort index.
    """
    if da.is_empty():
        raise MinHeapException

    # Percolate down always starts at index 0
    node_index = 0
    node_value = da.get_at_index(node_index)
    # end_of_sort_index -= 1  # Ignore the last index of the heap

    # Initiate children values
    left_child_index = (node_index * 2) + 1
    right_child_index = (node_index * 2) + 2
    left_child = None
    right_child = None
    if left_child_index < da.length():
        left_child = da.get_at_index(left_child_index)
    if right_child_index < da.length():
        right_child = da.get_at_index(right_child_index)

    # Edge case for final node
    if end_of_sort_index == 1:
        if left_child and left_child > node_value:  # Left swap
            da.set_at_index(left_child_index, node_value)
            da.set_at_index(node_index, left_child)
        elif right_child and right_child > node_value:  # Right swap
            da.set_at_index(right_child_index, node_value)
            da.set_at_index(node_index, right_child)
        else:
            return

    while left_child or right_child:
        # Both children exist
        if left_child and right_child:
            if (left_child < right_child or left_child == right_child) and left_child < node_value and \
                    left_child_index < end_of_sort_index:  # Left Swap
                da.set_at_index(left_child_index, node_value)
                da.set_at_index(node_index, left_child)
                node_index = left_child_index  # Update node index
            elif right_child < node_value and right_child_index < end_of_sort_index:
                da.set_at_index(right_child_index, node_value)
                da.set_at_index(node_index, right_child)
                node_index = right_child_index  # Update node index
            else:  # Left and right child are greater than node
                break
        # Only one child exists
        elif left_child and left_child < node_value and left_child_index < end_of_sort_index:  # Left child swap
            da.set_at_index(left_child_index, node_value)
            da.set_at_index(node_index, left_child)
            node_index = left_child_index  # Update node index
        elif right_child and right_child < node_value and right_child_index < end_of_sort_index:  # Right child swap
            da.set_at_index(right_child_index, node_value)
            da.set_at_index(node_index, right_child)
            node_index = right_child_index  # Update node index
        else:  # End of heap reached
            break

        # Update node and children values
        node_value = da.get_at_index(node_index)
        left_child_index = (node_index * 2) + 1
        right_child_index = (node_index * 2) + 2
        left_child = None
        right_child = None
        if left_child_index < da.length():
            left_child = da.get_at_index(left_child_index)
        if right_child_index < da.length():
            right_child = da.get_at_index(right_child_index)


def _percolate_down(da: DynamicArray, parent: int) -> None:
    """
    Percolates an element of the queue to its correct spot in the MinHeap
    """
    if da.is_empty():
        raise MinHeapException

    node_index = parent
    node_value = da.get_at_index(parent)

    # Initiate children values
    left_child_index = (node_index * 2) + 1
    right_child_index = (node_index * 2) + 2
    left_child = None
    right_child = None
    if left_child_index < da.length():
        left_child = da.get_at_index(left_child_index)
    if right_child_index < da.length():
        right_child = da.get_at_index(right_child_index)

    while left_child or right_child:
        # Both children exist
        if left_child and right_child:
            if (left_child < right_child or left_child == right_child) and left_child < node_value:  # Left Swap
                da.set_at_index(left_child_index, node_value)
                da.set_at_index(node_index, left_child)
                node_index = left_child_index  # Update node index
            elif right_child < node_value:
                da.set_at_index(right_child_index, node_value)
                da.set_at_index(node_index, right_child)
                node_index = right_child_index  # Update node index
            else:  # Left and right child are greater than node
                break
        # Only one child exists
        elif left_child and left_child < node_value:  # Left child swap
            da.set_at_index(left_child_index, node_value)
            da.set_at_index(node_index, left_child)
            node_index = left_child_index  # Update node index
        elif right_child and right_child < node_value:  # Right child swap
            da.set_at_index(right_child_index, node_value)
            da.set_at_index(node_index, right_child)
            node_index = right_child_index  # Update node index
        else:  # End of heap reached
            break

        # Update node and children values
        node_value = da.get_at_index(node_index)
        left_child_index = (node_index * 2) + 1
        right_child_index = (node_index * 2) + 2
        left_child = None
        right_child = None
        if left_child_index < da.length():
            left_child = da.get_at_index(left_child_index)
        if right_child_index < da.length():
            right_child = da.get_at_index(right_child_index)


def heapify(da: DynamicArray) -> None:
    """
    Takes a dynamic array and creates a valid MinHeap out of it
    """
    # Create a valid heap
    node_index = ((da.length() - 1) // 2)  # Find first node to check
    while node_index >= 0:  # Percolate nodes down
        _percolate_down(da, node_index)
        node_index -= 1


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':
    # print("\nPDF - add example 1")
    # print("-------------------")
    # h = MinHeap()
    # print(h, h.is_empty())
    # for value in range(300, 200, -15):
    #     h.add(value)
    #     print(h)
    #
    # print("\nPDF - add example 2")
    # print("-------------------")
    # h = MinHeap(['fish', 'bird'])
    # print(h)
    # for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
    #     h.add(value)
    #     print(h)
    #
    # print("\nPDF - is_empty example 1")
    # print("-------------------")
    # h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    # print(h.is_empty())
    #
    # print("\nPDF - is_empty example 2")
    # print("-------------------")
    # h = MinHeap()
    # print(h.is_empty())
    #
    # print("\nPDF - get_min example 1")
    # print("-----------------------")
    # h = MinHeap(['fish', 'bird'])
    # print(h)
    # print(h.get_min(), h.get_min())
    #
    # print("\nPDF - remove_min example 1")
    # print("--------------------------")
    # h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    # while not h.is_empty() and h.is_empty() is not None:
    #     print(h, end=' ')
    #     print(h.remove_min())
    #
    # print("\nPDF - build_heap example random")
    # print("--------------------------")
    # da = DynamicArray([-530, 71164, 62383, 39083, -87538, 25270, -16366, 39083, -530, 89498, 79887, -14127])
    # h = MinHeap(['zebra', 'apple'])
    # print(h)
    # h.build_heap(da)
    # print(h)
    # print("Should be: [-87538, -530, -16366, -530, 71164, -14127, 62383, 39083, 39083, 89498, 79887, 25270]")

    # print("\nPDF - build_heap example 1")
    # print("--------------------------")
    # da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    # h = MinHeap(['zebra', 'apple'])
    # print(h)
    # h.build_heap(da)
    # print(h)
    #
    # print("--------------------------")
    # print("Inserting 500 into input DA:")
    # da[0] = 500
    # print(da)
    #
    # print("Your MinHeap:")
    # print(h)
    # if h.get_min() == 500:
    #     print("Error: input array and heap's underlying DA reference same object in memory")
    #
    # print("\nPDF - size example 1")
    # print("--------------------")
    # h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    # print(h.size())
    #
    # print("\nPDF - size example 2")
    # print("--------------------")
    # h = MinHeap([])
    # print(h.size())
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    # print(h)
    # print(h.clear())
    # print(h)
    # #
    print("\nPDF - heapsort example random")
    print("------------------------")
    da = DynamicArray(["qYh`MQwrpZv", "ANoghcwSl", "bHTVQbc", "OTeD"])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    # print("\nPDF - heapsort example 1")
    # print("------------------------")
    # da = DynamicArray([5, 2, 11, 8, 6, 20, 1, 3, 7])
    # print(f"Before: {da}")
    # heapsort(da)
    # print(f"After:  {da}")

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")
    #
    # print("\nPDF - heapsort example 2")
    # print("------------------------")
    # da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    # print(f"Before: {da}")
    # heapsort(da)
    # print(f"After:  {da}")
