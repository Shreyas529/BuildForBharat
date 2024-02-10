import struct
from functools import lru_cache
from writeCache import WriteCache
class ServerOps:
    def __init__(self,tree,cache):
        self.tree=tree
        self.cache = cache

    def curr_length(self):
        return self.cache.getSize()

    
    def add_merchants(self, merchants_dict: dict) -> None:

    
        for pincode in merchants_dict.keys():
            byte_data = self.tree.get(pincode)
            if(byte_data is None):
                return 
            num_merchants = len(byte_data) // 36
            merchants = struct.unpack(f'!{num_merchants * 36}s', byte_data)
            merchants = [s[i:i+36].decode() for s in merchants for i in range(0, len(s), 36)]
            merchants = merchants + \
                tuple(
                    merchant_id for merchant_id in merchants_dict[pincode] if merchant_id not in merchants)
            
            byte_data = b''.join([ merchant_id.encode() 
                                 for merchant_id in merchants ] )
            self.tree.insert(pincode, byte_data, replace=True)
            


    def add_merchant_to_cache(self,merchants:dict):
        for i in merchants.items():
            self.cache.addRecord(i[0],i[1])
            if (self.tree.get(i[0]) == None):
                return 0
            else:
                return 1

    def move_to_cache(self):
        records = self.cache.returnAllRecords()
       
        self.add_merchants(records)
        
        self.cache.clearCache()
    
    def retrieve_from_cache(self,pincode):
        retrieved_tuple = self.cache.getRecord_by_pincode(pincode)
        return retrieved_tuple
    
    def remove_merchants_from_pincode(self , pincode:int, removal_merchant_id:list) -> None:
        cached_data=self.cache.getRecord_by_pincode(pincode)
        if cached_data:
            cached_data=list(cached_data)
            count=0
            for merchant_id in removal_merchant_id:
                if merchant_id in cached_data:
                    cached_data.remove(merchant_id)
                    count+=1
            self.cache.deleteKey(pincode)
            self.cache.addRecord(tuple(cached_data))
            if(count==len(removal_merchant_id)):
                return            
            
        byte_data = self.tree.get(pincode)
        if byte_data is None:
            return
        num_merchants = len(byte_data) // 36
        merchants = struct.unpack(f'!{num_merchants * 36}s', byte_data)
        merchants = [s[i:i+36].decode() for s in merchants for i in range(0, len(s), 36)]

        print(merchants)
        
        for merchant_id  in removal_merchant_id:
            if merchant_id not in merchants:
                raise ValueError(f"Merchant ID {merchant_id} does not serve the Pincode {pincode}\n")
                # raise ValueError(f'Merchant ID {merchant_id} does not serve the Pincode {pincode}.')
            
            
        retrieved_list = tuple(merchant_id for merchant_id in merchants if merchant_id not in removal_merchant_id)
        byte_data = b''.join(merchant_id.encode()
                            for merchant_id in retrieved_list)
        self.tree.insert(pincode, byte_data, replace=True)
        

    @lru_cache(maxsize=128)
    def retrieve_merchants(self, pincode: int) -> str:
        cached_data=self.retrieve_from_cache(pincode)
        if cached_data is None:
            cached_data=()
        byte_data = self.tree.get(pincode)
        if byte_data is None:
            return None,0
        num_merchants = len(byte_data) // 36
        merchants = struct.unpack(f'!{num_merchants * 36}s', byte_data)
        merchants = [s[i:i+36].decode() for s in merchants for i in range(0, len(s), 36)]
        merchants=merchants+list(cached_data)
        return "\n".join([str(j) for j in merchants]),len(merchants)
