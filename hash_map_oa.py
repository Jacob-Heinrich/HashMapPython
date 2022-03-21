# Name: Jacob Heinrich
# Description: Implements a hash map using open addressing for collision


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
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
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out


    def hash_index(self,key,capacity = None,temp_buckets = None) -> int:
        """
        Helper function that will calculate the hash index
        when called. Receives key, capacity, and temp buckets if
        there is any.
        """
        hash_key = self.hash_function(key)
        hash_key %= capacity
        quad_prob = 1
        hash_hold = hash_key

        # if the values don't need to be switched over to new buckets
        if temp_buckets == None:
                while self.buckets.get_at_index(hash_key) != None:
                    if self.buckets.get_at_index(hash_key) != None:
                        if self.buckets.get_at_index(hash_key).key == key:
                            return hash_key
                    hash_key = (hash_hold + quad_prob ** 2) % capacity
                    quad_prob += 1
                return hash_key

        # Index based off new capacity if the values need to be switched over for resizing
        elif temp_buckets != None:
            if temp_buckets.get_at_index(hash_key) != None:
                while temp_buckets.get_at_index(hash_key) != None:
                    hash_key = (hash_hold + quad_prob ** 2) % capacity
                    quad_prob += 1
        return hash_key


    def clear(self) -> None:
        """
        Clears the contents of the hash map. Will not change
        capacity.
        """
        new_buckets = DynamicArray()
        for i in range(self.capacity):
            new_buckets.append(None)
        self.buckets = new_buckets
        self.size = 0


    def get(self, key: str) -> object:
        """
        Returns the value associated with
        the given key.
        """
        # quadratic probing required
        hash_key = self.hash_index(key,self.capacity)
        loc = self.buckets.get_at_index(hash_key)
        if loc != None:
            if loc.is_tombstone == False:
                return loc.value
        else:
            return None


    def put(self, key: str, value: object) -> None:
        """
        Adds the key value pair to the hash map.
        Will update the value if there is already the
        same key.
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        #
        # quadratic probing required

        entry = HashEntry(key,value)
        # calls resize table if load factor is greater than or equal to .5
        if self.size != 0:
            if self.table_load() >= 0.5:
                self.resize_table(self.capacity * 2)

        hash_key = self.hash_index(key,self.capacity)
        loc = self.buckets.get_at_index(hash_key)
        # if loc is not None it means that there is a duplicate key that needs to be updated
        if loc:
            loc.value = value if loc.key == key else loc.value
            return

        self.buckets.set_at_index(hash_key,entry)
        self.size += 1


    def remove(self, key: str) -> None:
        """
        Removes the key and value associated with the
        key.
        """
        # quadratic probing required
        hash_key = self.hash_index(key,self.capacity)
        loc = self.buckets.get_at_index(hash_key)

        if loc == None:
            return None
        if loc.is_tombstone == True:
            return None
        else:
            loc.is_tombstone = True
            self.size -= 1
            return None


    def contains_key(self, key: str) -> bool:
        """
        Checks the hash map to see if
        it contains the given key.
        Returns True if so and False
        otherwise.
        """
        # quadratic probing required
        hash_key = self.hash_index(key,self.capacity)
        loc = self.buckets.get_at_index(hash_key)
        if loc == None:
            return False
        if loc.key == key and loc.is_tombstone == False:
            return True
        else:
            return False


    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets
        in the array.
        """
        count = 0
        for i in range(self.capacity):
            bucket = self.buckets.get_at_index(i)
            # has to check tombstone value to see if that value was removed
            if bucket == None or bucket.is_tombstone:
                count += 1
        return count


    def table_load(self) -> float:
        """
        Gets the current load factor of the hash map.
        """
        load_factor = self.size / self.capacity
        return load_factor


    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map while maintaining all
        key value pairs.
        """

        if new_capacity < self.size or new_capacity < 1:
            return None

        new_hash = HashMap(new_capacity,self.hash_function)
        temp_buckets = DynamicArray()
        new_hash.buckets = temp_buckets

        for i in range(new_hash.capacity):
            temp_buckets.append(None)

        for i in range(self.capacity):
            hash_entry = self.buckets.get_at_index(i)
            if hash_entry != None and hash_entry.is_tombstone == False:
                new_hash.put(hash_entry.key,hash_entry.value)
        self.buckets = new_hash.buckets
        self.capacity = new_hash.capacity


    def get_keys(self) -> DynamicArray:
        """
        Returns a dynamic array containing all the keys.
        """
        new_da = DynamicArray()
        for i in range(self.buckets.length()):
            if self.buckets.get_at_index(i) and self.buckets.get_at_index(i).is_tombstone == False:
                new_da.append(self.buckets.get_at_index(i).key)
        return new_da


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
    # this test assumes that put() has already been correctly implemented
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
    #
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
    m.resize_table(0)
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
