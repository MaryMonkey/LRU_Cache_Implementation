from queue import Queue
        
class LRUCache(object):
    '''
    Implement the LRUCache using hashmap and queue.
    '''
    
    def __init__(self, capacity):
        # Initialize a cache with a maximum size
        self.capacity = capacity
        
        self.hash_map = {}
        self.q1 = Queue()
        self.q2 = Queue()
        
        # Keep track of the current size of the LRUCache
        self.current_size = 0
    
    def _swap(self):
        '''
        swapping names of q1 and q2;
        q2 is always kept empty.
        '''
        
        self.q = self.q1
        self.q1 = self.q2
        self.q2 = self.q
        
    def put(self, key, value):
        '''
        put the value of a key, return nothing;
        1. when adding new keys that cause the capacity to be exceeded, 
        the "least recently used" key will be identified and removed.
        2. updating an existing key with a different value.
        '''
        
        # if key is in the map
        if key in self.hash_map:
            self.hash_map[key] = value
            # if key is at the top, do nothing
            if key == self.q1.queue[0]:
                return
            # else bring the key to top
            self.q2.put(key)
            while not self.q1.empty():
                self.q2.put(self.q1.get())
                if not self.q1.empty() and self.q1.queue[0] == key:
                    self.q1.get()
            
        # if key is not in the map
        if key not in self.hash_map:
            # update key and value
            self.q2.put(key)
            self.hash_map[key] = value
            # if current size exceeds the capacity
            if self.current_size >= self.capacity:
                while not self.q1.empty():
                    self.q2.put(self.q1.get())
                    if self.q1.qsize() == 1:
                        self.hash_map.pop(self.q1.queue[0])
                        self.q1.get()
                        self.current_size -= 1
            # else just move everything down by 1 entry
            else:
                while not self.q1.empty():
                    self.q2.put(self.q1.get())
            self.current_size += 1
        
        self._swap()
    
    def get(self, key):
        '''get the value of a key, return the value'''
        
        # if key is not in map, then return -1
        if key not in self.hash_map:
            return -1
        
        # if key is at the top, return the value at the top
        if key == self.q1.queue[0]:
            return self.hash_map[key]
        
        # otherwise move the key to top,
        # and return that corresponding value
        self.q2.put(key)
        while not self.q1.empty():
            self.q2.put(self.q1.get())
            if not self.q1.empty() and self.q1.queue[0] == key:
                self.q1.get()
        self._swap()
        return self.hash_map[key]
    
    def delete(self, key):
        '''delete a key'''
        
        # attempting to delete a key that doesn't exit, then just return
        if key not in self.hash_map:
            return
        
        # otherwise, remove the key and its value
        while not self.q1.empty():
            if key == self.q1.queue[0]:
                self.q1.get()
                self.hash_map.pop(key)
            self.q2.put(self.q1.get())  
        self.current_size -= 1
        self._swap()
    
    def reset(self):
        '''reset the cache which removes all items in the cache.'''
        
        self.q1 = Queue()
        self.hash_map.clear()
        self.current_size = 0
        print("cache has been cleared.")
        
    def cache(self):
        '''return the current cache'''
        
        self.current_cache = {}
        while not self.q1.empty():
            k = self.q1.queue[0]
            self.current_cache[k] = self.hash_map[k]
            self.q2.put(k)
            self.q1.get()
        self._swap()
        return self.current_cache
        
    def size(self):
        '''return the current size'''
        
        return self.current_size