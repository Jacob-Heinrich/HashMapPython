# Name: Jacob Heinrich
# Description: Implements a hash map using chaining for collision


from a6_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out


    def hash_index(self,key,capacity = None) -> int:
        """
        Helper function that receives a key and then returns
        the hash index for that key.
        """

        hash_index = self.hash_function(key)
        hash_index %= capacity if capacity != 0 else hash_index
        return hash_index


    def clear(self) -> None:
        """
        Clears the contents of the hash map.
        """

        self.buckets,self.size = DynamicArray(),0
        for i in range(self.capacity):
            self.buckets.append(LinkedList())


    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key.
        """

        index = self.hash_index(key,self.capacity)
        for node in self.buckets.get_at_index(index):
            if node.key == key:
                return node.value
        return None


    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map.
        If the key is already present in the hash map
        then that value will be replaced with the new value.
        """

        index = self.hash_index(key,self.capacity)
        loc = self.buckets.get_at_index(index)
        duplicate_key = loc.contains(key)

        # check to see if the bucket is empty or not

        if loc.length() == 0:
            loc.insert(key,value)
            self.size += 1

        # checks for duplicate keys in the bucket
        elif duplicate_key != None:
            duplicate_key.value = value

        else:
            loc.insert(key,value)
            self.size += 1


    def remove(self, key: str) -> None:
        """
        Removes the given key and value from the
        hash map.
        """

        index = self.hash_index(key,self.capacity)

        if self.contains_key(key) == False:
            return None
        else:
            self.buckets.get_at_index(index).remove(key)
            self.size -= 1


    def contains_key(self, key: str) -> bool:
        """
        Will check to see if the key is in the
        hash map. Returns True if it is or False otherwise.
        """

        index = self.hash_index(key,self.capacity)
        for node in self.buckets.get_at_index(index):
            if node.key == key:
                return True
        return False


    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets
        in the hash map.
        """

        count = 0
        for i in range(self.buckets.length()):
            # if the bucket is empty then count will be incremented by 1
            if self.buckets.get_at_index(i).length() == 0:
                count += 1
        return count


    def table_load(self) -> float:
        """
        Will return the table load of the hash map.
        Table load = total elements/ total buckets
        """

        load_factor = self.size / self.capacity
        return load_factor


    def resize_table(self, new_capacity: int) -> None:
        """
        Updates capacity to new capacity and updates
        all associated elements hash index.
        """

        cur_cap = self.capacity
        temp_buckets = DynamicArray()

        # checks to see if the new capacity is a valid capacity
        if new_capacity < 1:
            return None

        # adds linked lists to the new buckets with the new capacity
        for i in range(new_capacity):
            temp_buckets.append(LinkedList())

        # loop through the old buckets to transfer over the elements
        for i in range(self.capacity):
            if self.is_empty(i) == False:
                for node in self.buckets.get_at_index(i):
                    index = self.hash_index(node.key,new_capacity)
                    temp_buckets.get_at_index(index).insert(node.key,node.value)

        self.buckets,self.capacity = temp_buckets,new_capacity


    def get_keys(self) -> DynamicArray:
        """
        Creates a dynamic array with all
        the keys in the hash map.
        """

        keys = DynamicArray()
        for i in range(self.capacity):
            if self.is_empty(i) == False:
                for node in self.buckets.get_at_index(i):
                    keys.append(node.key)
        return keys


    def is_empty(self, index) -> bool:
        """
        Will check to see if the bucket is empty.
        Returns True if empty or False
        otherwise.
        """

        if self.buckets.get_at_index(index).length() == 0:
            return True
        else:
            return False


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
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
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)


    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
