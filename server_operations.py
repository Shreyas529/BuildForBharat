import struct
from functools import lru_cache
from writeCache import WriteCache
class ServerOps:
    def __init__(self,tree,cache):
        self.tree=tree
        self.cache = cache

    def curr_length(self):
        return self.cache.getSize()

    
    def add_merchants(self, merchants: dict) -> None:

        reversed_merchant_dict = {pincode: merchant_id for merchant_id,
                                  pincodes in merchants.items() for pincode in pincodes}
        for pincode in reversed_merchant_dict.keys():
            byte_data = self.tree.get(pincode)
            if(byte_data is None):
                return 
            num_merchants = len(byte_data) // 36
            merchants = struct.unpack(f'!{num_merchants * 36}s', byte_data)
            retrieved_list = retrieved_list + \
                tuple(
                    merchant_id for merchant_id in reversed_merchant_dict[pincode] if merchant_id not in retrieved_list)
            byte_data = b''.join(merchant_id.encode()
                                 for merchant_id in merchants)
            self.tree.insert(pincode, byte_data, replace=True)


    def add_merchant_to_cache(self,merchants:dict):
        for i in merchants.items:
            self.cache.addRecord(i.key,i.value)

    def move_to_cache(self):
        records = self.cache.returnAllRecords()
        self.add_merchants(records)
        self.cache.clearCache()
    
    def retrieve_from_cache(self,pincode):
        retrieved_tuple = self.cache.getRecord_by_pincode(pincode)
        return retrieved_tuple
    
    def remove_merchants_from_pincode(self , pincode:int, removal_merchant_id) -> None:
        byte_data = self.tree.get(pincode)
        if byte_data is None:
            return
        num_merchants = len(byte_data) // 36
        merchants = struct.unpack(f'!{num_merchants * 36}s', byte_data)
        
        try:
            error_list=[]
            for merchant_id  in removal_merchant_id:
                if merchant_id not in merchants:
                    error_list.append(merchant_id)
                    # raise ValueError(f'Merchant ID {merchant_id} does not serve the Pincode {pincode}.')
            
            if(len(error_list) >=1):
                error_message = f'Merchant ID {merchant_id} does not serve the Pincode/Pincodes {", ".join(str(e) for e in error_list)}'
                raise ValueError(error_message)
            
            retrieved_list = tuple(merchant_id for merchant_id in merchants if merchant_id not in removal_merchant_id)
            byte_data = b''.join(merchant_id.encode()
                                    for merchant_id in retrieved_list)
            self.tree.insert(pincode, byte_data, replace=True)
        except ValueError as e:
            print(e)

    @lru_cache(maxsize=128)
    def retrieve_merchants(self, pincode: int) -> str:
        byte_data = self.tree.get(pincode)
        if byte_data is None:
            return None,0
        num_merchants = len(byte_data) // 36
        merchants = struct.unpack(f'!{num_merchants * 36}s', byte_data)
        merchants = [s[i:i+36].decode() for s in merchants for i in range(0, len(s), 36)]
        
        return "\n".join([str(j) for j in merchants]),len(merchants)
