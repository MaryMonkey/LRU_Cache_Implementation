from lrucache import LRUCache
import unittest

class TestLRUCache(unittest.TestCase):
    
    def test_put(self):
        c = LRUCache(3)
        c.put(4,2)
        c.put(1,1)
        c.put(2,3)
        self.assertEqual(c.size(), 3)
        self.assertEqual(c.cache(), 
                         {2:3, 1:1, 4:2})
        
        # put a key that's in the map, not at the top;
        # this will bring the key and its value to the top of the cache,
        # since it's been interacted
        c.put(1,10)
        self.assertEqual(c.cache(), 
                         {1:10, 2:3, 4:2})
        
        # put an existing key that's at the top
        c.put(1, 12)
        self.assertEqual(c.cache(), 
                         {1:12, 2:3, 4:2})
        
        # put a key that's not in the map;
        # the LRU cache should be removed,
        # and the new one should be added to the top
        c.put(5,6)
        self.assertEqual(c.size(), 3)
        self.assertEqual(c.cache(), 
                         {5:6, 1:12, 2:3})
        
    def test_get(self):
        c = LRUCache(3)
        c.put(4,2)
        c.put(1,1)
        c.put(2,3)
        
        # get the first key
        self.assertEqual(c.get(2), 3)
        self.assertEqual(c.cache(), {2:3, 1:1, 4:2})
        self.assertEqual(c.size(), 3)
        
        # get the second key
        self.assertEqual(c.get(1), 1)
        self.assertEqual(c.cache(), {1:1, 2:3, 4:2})
        self.assertEqual(c.size(), 3)
        
        # get the last key
        self.assertEqual(c.get(4), 2)
        self.assertEqual(c.cache(), {4:2, 2:3, 1:1})
        self.assertEqual(c.size(), 3)
        
        # get a non-existing key
        self.assertEqual(c.get(40), -1)
        self.assertEqual(c.cache(), {4:2, 2:3, 1:1})
        self.assertEqual(c.size(), 3)
    
    def test_delete(self):
        c = LRUCache(3)
        c.put(4,2)
        c.put(1,1)
        c.put(2,3)
        
        # delete a key that's not in the map,
        # nothing happens
        c.delete(20)
        self.assertEqual(c.size(), 3)
        self.assertEqual(c.cache(), 
                         {2:3, 1:1, 4:2})
        
        # delete an existing key
        c.delete(1)
        self.assertEqual(c.size(), 2)
        self.assertEqual(c.cache(), {2:3, 4:2})
        
    def test_reset(self):
        c = LRUCache(3)
        c.put(4,2)
        c.put(1,1)
        c.put(2,3)
        
        # after reset, nothing existing in the cache
        c.reset()
        self.assertEqual(c.size(), 0)
        self.assertEqual(c.cache(), {})
        
    def test_all(self):
        c = LRUCache(5)
        c.put(1,'one')
        c.put(2,'two')
        c.put(3,'three')
        
        c.delete(3)
        self.assertEqual(c.size(), 2)
        self.assertEqual(c.cache(), {2:'two', 1:'one'})
        
        c.put(4,'four')
        c.put(6,'six')
        self.assertEqual(c.get(1), 'one')
        self.assertEqual(c.size(), 4)
        self.assertEqual(c.cache(), 
                         {1:'one', 6:'six', 4:'four', 2:'two'})
        
        self.assertEqual(c.get(3), -1)
        
        c.put(1,'five')
        self.assertEqual(c.cache(),
                        {1:'five', 6:'six', 4:'four', 2:'two'})
        
        c.put(12,'twelve')
        self.assertEqual(c.cache(),
                        {12:'twelve', 1:'five', 6:'six', 4:'four', 2:'two'})
        c.put(5,'five')
        self.assertEqual(c.cache(),
                        {5:'five', 12:'twelve', 1:'five', 6:'six', 4:'four'})
        
        self.assertEqual(c.get(2), -1)
        
        c.reset()
        self.assertEqual(c.size(), 0)
        self.assertEqual(c.cache(), {})
        
if __name__ == '__main__':
    unittest.main()
