# Name: Austin Holcomb
# OSU Email: Holcomau@OregonState.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 2: Dynamic Array and ADT Implementation
# Due Date: April 29th
# Description:


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Change dynamic array capacity. Creates a new StaticArray and points
        self._data to the new StaticArray of desired size
        """
        # Validate new_capacity is a positive integer greater than _size
        if new_capacity <= self._size or new_capacity < 1:
            return

        # Create new StaticArray of appropriate capacity
        self._capacity = new_capacity
        new_array = StaticArray(new_capacity)

        # Populate new static array with old array values
        for index in range(self._size):
            new_array.set(index, self.get_at_index(index))

        self._data = new_array

    def append(self, value: object) -> None:
        """
        Appends value to the end of the dynamic array. Doubles
        the capacity of the dynamic array if the dynamic is full.
        """
        # Double dynamic array capacity if full
        if self._size == self._capacity:
            self.resize(self._size * 2)

        # Append value to the end of the dynamic array
        self._size += 1
        self.set_at_index(self._size - 1, value)

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts a value at the given index. Doubles capacity of the dynamic array if
        the array is full. Raises an error for invalid indices.
        """
        if index < 0 or index > self._size:  # Invalid index [0, N]
            raise DynamicArrayException
        if self._size == self._capacity:  # Dynamic array is full
            self.resize(self._size * 2)

        # Shift all values past and including the insertion index up by 1
        self._size += 1
        low_value = self.get_at_index(index)
        for shift_index in range(index, self._size - 1):
            high_value = self.get_at_index(shift_index + 1)
            self.set_at_index(shift_index + 1, low_value)
            low_value = high_value

        # Store new value    
        self.set_at_index(index, value)

    def remove_at_index(self, index: int) -> None:
        """
        Removes the element at the requested index and shifts values
        in higher indices down by 1.
        """
        if index < 0 or index >= self._size:  # Invalid index [0, N-1]
            raise DynamicArrayException

        # Reduce capacity of the array to TWICE the amount of current elements if size < capacity//4
        if self._size < (self._capacity / 4) and self._capacity >= 10:
            if self._size * 2 > 10:
                self.resize(self._size * 2)
            else:
                self.resize(10)

        # Shift all values past the insertion index down by 1, overwriting the removed value
        high_value = None
        for shift_index in range(self._size - 1, index - 1, -1):
            low_value = self.get_at_index(shift_index)
            self.set_at_index(shift_index, high_value)
            high_value = low_value

        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Slices the requested array from start_index to (start_index + size).
        Returns the slice as a new dynamic array.
        """
        if start_index < 0 or start_index >= self._size:  # Invalid index [0, N-1]
            raise DynamicArrayException

        if size < 0 or start_index + size > self._capacity:  # Invalid size input, or overran array bounds
            raise DynamicArrayException

        # Create new dynamic array
        new_array = DynamicArray()

        # Populate new dynamic array
        for index in range(start_index, start_index + size):
            new_array.append(self.get_at_index(index))

        # Resize the returning dynamic array so size == capacity
        new_array.resize(new_array._size)

        return new_array

    def map(self, map_func) -> "DynamicArray":
        """
        Creates a new dynamic array with each element derived from the
        given dynamic array and function
        """
        new_array = DynamicArray()
        for index in range(self._size):
            new_array.append(map_func(self.get_at_index(index)))

        return new_array

    def filter(self, filter_func) -> "DynamicArray":
        """
        Creates a new dynamic array with each element derived from the
        given dynamic array and filter function
        """
        new_array = DynamicArray()

        for index in range(self._size):
            if filter_func(self.get_at_index(index)):
                new_array.append(self.get_at_index(index))

        # Remove excess capacity off new array
        new_array.resize(new_array._size)

        return new_array

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Applies the reduce_func to all elements of the given dynamic array.
        Mimics the built int Python reduce() function
        """
        # Check for empty array w/ no initializer
        if self.is_empty() and initializer is None:
            return None

        # Handle array size of 1
        if self._size == 1 and initializer is None:
            output = reduce_func(self.get_at_index(0), 0)
        elif self._size == 1 and initializer is not None:
            output = reduce_func(initializer, self.get_at_index(0))
        # Array size is > 1
        else:
            # Initializer is first element of array (None)
            # starting_range starts at element 1 of array
            if initializer is None:
                initializer = self.get_at_index(0)
                starting_range = 1
            # Initializer is given, starting_range starts at element 0 of array
            else:
                starting_range = 0

            output = initializer  # Running reduce function sum
            for index in range(starting_range, self._size):
                output = reduce_func(output, self.get_at_index(index))

        return output


def chunk(arr: DynamicArray) -> "DynamicArray":
    """
    Chunks the given dynamic array by creating an array of arrays. The nested
    arrays contain only ascending values in index order of the given
    dynamic array.
    """

    # If arr is empty
    if arr.is_empty():
        return DynamicArray()

    # Initialize start chunk array
    chunk = DynamicArray()
    chunk.append(DynamicArray())
    chunk_index = 0

    # Append previous val to initial chunk array
    previous_val = arr.get_at_index(0)
    arr_to_append = chunk.get_at_index(chunk_index)
    arr_to_append.append(previous_val)

    # If arr is a single element
    if arr._size == 1:
        return chunk

    # Iterate through given dynamic array
    for index in range(1, arr._size):
        current_val = arr.get_at_index(index)
        # If values are in ascending order
        if current_val >= previous_val:
            arr_to_append = chunk.get_at_index(chunk_index)
            arr_to_append.append(current_val)  # Append to current array
            previous_val = current_val
        # Current value in descending order, create new nested array
        else:
            chunk_index += 1
            chunk.append(DynamicArray())
            arr_to_append = chunk.get_at_index(chunk_index)
            arr_to_append.append(current_val)  # Append to new nested array
            previous_val = current_val

    return chunk


def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Find the mode value(s) of the given dynamic array. Returns a tuple containing a
    dynamic array containing all mode value(s), and the mode count as an integer.
    """
    mode_arr = DynamicArray()

    # Set previous element, starting mode arr, mode count, and current element count
    previous_element = arr.get_at_index(0)
    mode_arr.append(previous_element)
    mode_count = 1
    current_element_count = 1

    for index in range(1, arr._size):
        current_element = arr.get_at_index(index)
        # If the current element is the same as the previous, increase current count
        if previous_element == current_element:
            current_element_count += 1
            previous_element = current_element
        # New element, restart count
        else:
            current_element_count = 1
            previous_element = current_element

        # Check if there's another mode (equal)
        if current_element_count == mode_count:
            mode_arr.append(previous_element)
            mode_count = current_element_count
            previous_element = current_element

        # Check if there's a new singular mode (overtaking mode_count)
        if current_element_count > mode_count:
            # Create a new mode array
            mode_arr = DynamicArray()
            mode_arr.append(previous_element)
            mode_count = current_element_count

    return mode_arr, mode_count


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))


    def print_chunked_da(arr: DynamicArray):
        if len(str(arr)) <= 100:
            print(arr)
        else:
            print(f"DYN_ARR Size/Cap: {arr.length()}/{arr.get_capacity()}")
            print('[\n' + ',\n'.join(f'\t{chunk}' for chunk in arr) + '\n]')


    print("\n# chunk example 1")
    test_cases = [
        [10, 20, 30, 30, 5, 10, 1, 2, 3, 4],
        ['App', 'Async', 'Cloud', 'Data', 'Deploy',
         'C', 'Java', 'Python', 'Git', 'GitHub',
         'Class', 'Method', 'Heap']
    ]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# chunk example 2")
    test_cases = [[], [261], [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
