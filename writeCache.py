import diskcache
import struct

class WriteCache:
    def __init__(self):
        self.cache = diskcache.Cache("cache")
        self.size = 0

    def addRecord(self, key, value):
        self.cache.add(key, value)
        self.size += 1

    def getRecord(self, key):
        retrievedRecord = self.cache.get(key,None)
        return retrievedRecord
    
    def returnAllRecords(self):
        records = {key: value for key, value in self.cache.iteritems()}
        return records
    
    def clearCache(self):
        self.cache.clear()

    def getSize(self):
        return self.size
    
    def setSize(self, size = 0):
        self.size = size
