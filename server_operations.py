import struct 

class ServerOps:
    def __init__(self,tree):
        self.tree=tree

    def add_merchants(self,merchants:dict) -> None:
        
        reversed_merchant_dict = {pincode: merchant_id for merchant_id, pincodes in merchants.items() for pincode in pincodes}
        for pincode in reversed_merchant_dict.keys():
            byte_data=self.tree.get(pincode)
            retrieved_list = struct.unpack('!{}I'.format(len(byte_data)//4),byte_data)
            retrieved_list = retrieved_list + tuple(merchant_id for merchant_id in reversed_merchant_dict[pincode] if merchant_id not in retrieved_list)
            byte_data = struct.pack('!{}I'.format(len(retrieved_list)), *retrieved_list)
            self.tree.insert(pincode,byte_data,replace=True)
            
    def retrieve_merchants(self,pincode:int)->str:
        byte_data=self.tree.get(pincode)
        retrieved_list = struct.unpack('!{}I'.format(len(byte_data)//4),byte_data)
        return "\n".join([str(j) for j in retrieved_list])
    
    def add_in_cache(self, pincodes:dict) -> None:
        pass
