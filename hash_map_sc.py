# Name: Joshua Hutson
# OSU Email: hutsonjo@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap
# Due Date: 12/5/2024
# Description: This program is a Separate Chain HashMap that uses a dynamic array in which each index references a
#              linked list. The HashMap class includes methods for putting and removing a key/value pair in the map,
#              getting the value of a known key, determining the table load, determining the amount of empty buckets,
#              resizing the HashMap, clearing the HashMap, as well as obtaining an array of all key/value pairs.
#              There also exists a separate method for finding the mode of a dynamic array using Hash-maping.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """This method updates the key/value pair in the hash map. If the given key already exists in
        the hash map, its associated value must be replaced with the new value. If the given key is
        not in the hash map, a new key/value pair must be added.

        Args:
            key (str): key to be added or updated in the hash map
            value (object): value to be stored in the hash map
        """
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        hash_index = self._hash_function(key) % self._capacity

        if self._buckets[hash_index].contains(key) is None:
            self._buckets[hash_index].insert(key, value)
            self._size += 1
        else:
            self._buckets[hash_index].remove(key)
            self._buckets[hash_index].insert(key, value)

    def resize_table(self, new_capacity: int) -> None:
        """This method changes the capacity of the underlying table. All existing key/value pairs must
        be put into the new table, meaning the hash table links must be rehashed.

        Args:
            new_capacity (int): The new capacity of the overlaying dynamic array
        """
        # Evaluate new capacity for validity, terminating if less than one, incrementing until prime if it is not.
        if new_capacity < 1:
            return
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Initialize a new array to replace the previous and a linked list to temporarily hold the key/value pairs
        new_array = DynamicArray()
        for i in range(new_capacity):
            new_array.append(LinkedList())
        temp_linked_list = LinkedList()

        # Add all HashMap items to the temporary linked list
        for index in range(self._capacity):
            bucket = self._buckets.get_at_index(index)
            if bucket is not None:
                for item in bucket:
                    temp_linked_list.insert(item.key, item.value)

        # Set new data member values for the resized HashMap
        self._size = 0
        self._capacity = new_capacity
        self._buckets = new_array

        # Add every item from the previous HashMap into the new one
        for item in temp_linked_list:
            self.put(item.key, item.value)

    def table_load(self) -> float:
        """This method returns the current hash table load factor.

        Returns:
            float: hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """This method returns the number of empty buckets in the hash table.

        Returns:
            int: number of empty buckets
        """
        # Initialize a return value
        return_value = 0

        # Examine each bucket, determine if empty, increment return value if so, return the # of empty buckets
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                return_value += 1
        return return_value

    def get(self, key: str) -> object:
        """This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.

        Args:
            key (str): key to be found from the hash map.

        Returns:
            object: value associated with the given key.
        """
        # Find the hash index associated with the key, if a value occurs at that index return it
        hash_index = self._hash_function(key) % self._capacity
        if self._buckets[hash_index].contains(key):
            return self._buckets[hash_index].contains(key).value
        return None

    def contains_key(self, key: str) -> bool:
        """This method returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.

        Args:
            key (str): key to be found from the hash map.

        Returns:
            bool: True if the given key is in the hash map, otherwise False.
        """
        # Find the hash index associated with the key, determine if key occurs in the bucket, return bool accordingly
        hash_index = self._hash_function(key) % self._capacity
        if self._buckets[hash_index].contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """This method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing.

        Args:
            key (str): key to be removed from the hash map.
        """
        # Locate the bucket associated with the key, remove the associated key/value pair, decrement size
        hash_index = self._hash_function(key) % self._capacity
        removal = self._buckets[hash_index].remove(key)
        if removal:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """This method returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map.

        Returns:
            DynamicArray: dynamic array where each index contains a tuple of a key/value pair.
        """
        # Initialize return array
        return_array = DynamicArray()

        # For every item in each bucket, append a tuple of that item's key/value pair to the array, return it
        for index in range(self._capacity):
            bucket = self._buckets.get_at_index(index)
            if bucket is not None:
                for item in bucket:
                    return_array.append((item.key, item.value))
        return return_array

    def clear(self) -> None:
        """This method clears the contents of the hash map."""
        # Initialize a new empty Linked List at each bucket space in the array, reset size
        for index in range(self._capacity):
            self._buckets.set_at_index(index, LinkedList())
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """This function receives a dynamic array and returns a tuple containing, in this order, a dynamic array
    comprising the mode (most frequently occurring) value(s) of the given array, and an integer representing
    the highest frequency of occurrence for the mode value(s).

    Args:
        da (DynamicArray): The dynamic array to be evaluated for mode.

    Returns:
        tuple[DynamicArray, int]: The mode and the frequency of its occurrence.
    """
    # Initialize a map to add values to with associated frequency, a value to hold mode frequency, and the return array
    map = HashMap(da.length())
    freq = 0
    return_array = DynamicArray()

    # Iterate through keys of input array, check if the key is present in the map
    for i in range(da.length()):
        value = map.get(da[i])

        # If the key is present, increment its value and update
        if value is not None:
            value += 1
            map.put(da[i], value)

        # If the key is not present, add the key to the map with a value of 1
        else:
            value = 1
            map.put(da[i], value)

        # If a new mode is found, reset the return array and add this key to it
        if value > freq:
            freq = value
            return_array = DynamicArray()
            return_array.append(da[i])

        # If a key's occurrence is equal to the current mode frequency, append it to the return array
        elif value == freq:
            return_array.append(da[i])

    return return_array, freq


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
