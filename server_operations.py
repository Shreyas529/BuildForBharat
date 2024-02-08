import struct 
from functools import lru_cache
from writeCache import WriteCache
class ServerOps:
    def __init__(self,tree):
        self.tree=tree
        self.cache = WriteCache()

    def curr_length(self):
        return self.cache.getSize()

    def add_merchants(self,merchants:dict) -> None:
        reversed_merchant_dict = {pincode: merchant_id for merchant_id, pincodes in merchants.items() for pincode in pincodes}
        for pincode in reversed_merchant_dict.keys():
            byte_data=self.tree.get(pincode)
            retrieved_list = struct.unpack('!{}I'.format(len(byte_data)//4),byte_data)
            retrieved_list = retrieved_list + tuple(merchant_id for merchant_id in reversed_merchant_dict[pincode] if merchant_id not in retrieved_list)
            byte_data = struct.pack('!{}I'.format(len(retrieved_list)), *retrieved_list)
            self.tree.insert(pincode,byte_data,replace=True)

    def add_merchant_to_cache(self,merchants:dict):
        for i in merchants.items:
            self.cache.addRecord(i.key,i.value)

    def move_to_cache(self):
        records = self.cache.returnAllRecords()
        self.add_merchants(records)
            
    @lru_cache(maxsize=128)
    def retrieve_merchants(self,pincode:int)->str:
        byte_data=self.tree.get(pincode)
        retrieved_list = struct.unpack('!{}I'.format(len(byte_data)//4),byte_data)
        retrieved_list += self.retrieve_from_cache(pincode)
        return "\n".join([str(j) for j in retrieved_list])
    
    def retrieve_from_cache(self,pincode):
        retrieved_tuple = self.cache.getRecord_by_pincode(pincode)
        return retrieved_tuple