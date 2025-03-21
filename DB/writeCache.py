import diskcache
import struct

class WriteCache:
    def __init__(self):
        self.cache = diskcache.Cache("../cache")
        self.size = len(self.cache)

    def addRecord(self, key, value):
        getVal=self.cache.get(key)

        if getVal:
            self.cache.set(key,getVal+value)
            self.cache.set(key,tuple(set(getVal+value)))
        else:
            self.cache.set(key,value)
            self.size += 1
        

    def getRecord_by_pincode(self,pincode):
        return self.cache.get(pincode)
        
    
    def returnAllRecords(self):
        records = {key: value for (key, value) in self.iteritems()}
        return records
    
    def clearCache(self):
        self.cache.clear()

    def getSize(self):
        return self.size
    
    def setSize(self, size = 0):
        self.size = size
    
    def iteritems(self):
        retrieved_tuple = ()
        for key in self.cache:
            retrieved_tuple += ((key, self.cache.get(key)),)
        
        return retrieved_tuple
    def deleteKey(self,key):
        self.cache.delete(key)
