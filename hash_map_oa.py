# Name: Joshua Hutson
# OSU Email: hutsonjo@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap
# Due Date: 12/5/2024
# Description: This program is an Open Addressing HashMap that uses the indices of a dynamic array as buckets to hold
#              HashEntry objects that contain a key/value pair, along with a data member to signify if the value is a
#              tombstone. The HashMap class includes methods for putting and removing a key/value pair in the map,
#              getting the value of a known key, determining the table load, determining the amount of empty buckets,
#              resizing the HashMap, clearing the HashMap, as well as obtaining an array of all key/value pairs.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
            key (str): key to be added or updated within the HashMap.
            value (object): value to be added to the HashMap.
        """
        # Resize HashMap if table load is too high
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Initialize the initial hash index, a variable for the associated bucket, and a value for the probe
        hash_index = self._hash_function(key) % self._capacity
        bucket = self._buckets[hash_index]
        probe = 1

        # Quadratically probe for an empty bucket, matching key, or tombstoned value
        while bucket is not None and not bucket.is_tombstone and bucket.key != key:
            hash_index = (self._hash_function(key) + probe ** 2) % self._capacity
            bucket = self._buckets[hash_index]
            probe += 1

        # If bucket is "empty", place the new entry in bucket
        if bucket is None or bucket.is_tombstone:
            self._buckets.set_at_index(hash_index, HashEntry(key, value))
            self._size += 1
            return

        # If key already exists, update the value
        if bucket.key == key:
            self._buckets.set_at_index(hash_index, HashEntry(key, value))
            return

    def resize_table(self, new_capacity: int) -> None:
        """This method changes the capacity of the underlying table, rehashing all elements in the process.

        Args:
            new_capacity (int): new capacity of the underlying dynamic array
        """
        # Ensure new capacity is large enough to hold the map
        if new_capacity < self._size:
            return

        # Evaluate if new capacity is prime, if not increment to next prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Initialize conditions for new HashMap, create variable to hold values of old array
        self._size = 0
        self._capacity = new_capacity
        old_array = self._buckets
        self._buckets = DynamicArray()

        # Fill in new array with None objects to adjust underlying indices
        for i in range(new_capacity):
            self._buckets.append(None)

        # Iterate over entries of old array, if valid, hash and put into new map
        for i in range(old_array.length()):
            hash_entry = old_array.get_at_index(i)
            if hash_entry:
                if hash_entry.is_tombstone is False:
                    self.put(hash_entry.key, hash_entry.value)

    def table_load(self) -> float:
        """This method returns the current hash table load factor.

        Returns:
            float: hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """This method returns the number of empty buckets in the hash table.

        Returns:
            int: number of empty buckets in the HashMap.
        """
        return self._capacity - self._size

    def get(self, key: str) -> object:
        """This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.

        Args:
            key (str): key of the value to be retrieved.

        Returns:
            object: value associated with the passed key.
        """
        # Call to quadratic probe to find empty space or matching key
        bucket = self._quadratic_probe(key)

        #  # If a matching valid Hash Entry exists, return its value
        if bucket and bucket.key == key and not bucket.is_tombstone:
            return bucket.value

    def contains_key(self, key: str) -> bool:
        """This method returns True if the given key is in the hash map, otherwise it returns False.

        Args:
            key (str): key to be searched for in the hashMap.

        Returns:
            bool: True if the given key is in the HashMap, otherwise False.
        """
        # Call to quadratic probe to find empty space or matching key
        bucket = self._quadratic_probe(key)

        # Return bool indicating if a Hash Entry was found
        if bucket:
            return True
        return False

    def remove(self, key: str) -> None:
        """This method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing.

        Args:
            key (str): key of the object to be removed.
        """
        # Call to quadratic probe to find empty space or matching key
        bucket = self._quadratic_probe(key)

        # If a matching valid Hash Entry exists, tombstone it and decrement size
        if bucket and bucket.key == key and not bucket.is_tombstone:
            self._size -= 1
            bucket.is_tombstone = True

    def get_keys_and_values(self) -> DynamicArray:
        """This method returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map.

        Returns:
            DynamicArray: A dynamic array containing all the key value pairs of the HashMap.
        """
        # Initialize array to hold tuples and be returned
        return_array = DynamicArray()

        # Iterate through list, appending tuples of any valid entries, return array
        for i in range(self._capacity):
            entry = self._buckets[i]
            if entry is not None and not entry.is_tombstone:
                return_array.append((entry.key, entry.value))
        return return_array

    def clear(self) -> None:
        """This method clears the contents of the hash map without changing the underlying hash table capacity."""
        # Set the value of every bucket to None, set size to zero
        for i in range(self._capacity):
            self._buckets.set_at_index(i, None)
        self._size = 0

    def __iter__(self):
        """his method enables the hash map to iterate across itself."""
        self._index = 0
        return self

    def __next__(self):
        """This method will return the next item in the hash map, based on the current location of the
        iterator. Only Active entries are iterated over."""
        # If the next step in iteration is not a valid HashEntry, continue to iterate
        try:
            entry = self._buckets[self._index]
            while entry is None or entry.is_tombstone:
                self._index += 1
                entry = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return entry

    def _quadratic_probe(self, key: str) -> object | None:
        """This private method returns the appropriate hash index of a given key while accounting for collision using
        quadratic open addressing.

        Returns:
            object: if there exists a matching key, then the corresponding object is returned. Otherwise, None.
        """
        # Initialize the initial hash index, a variable for the associated bucket, and a value for the probe
        hash_index = self._hash_function(key) % self._capacity
        bucket = self._buckets[hash_index]
        probe = 1

        # Quadratically probe for an empty bucket or matching key. Skip over tombstones. Return result.
        while bucket is not None and bucket.key != key:
            hash_index = (self._hash_function(key) + probe ** 2) % self._capacity
            bucket = self._buckets[hash_index]
            probe += 1
        return bucket


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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
