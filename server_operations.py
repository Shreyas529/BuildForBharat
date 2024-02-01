import struct 
from BplusTree import tree

def add_merchants(merchants:dict) -> None:
    
    reversed_merchant_dict = {pincode: merchant_id for merchant_id, pincodes in merchants.items() for pincode in pincodes}
    for pincode in reversed_merchant_dict.keys():
        retrieved_list = struct.unpack('!{}I'.format(len(tree.get(pincode)//4)),tree.get(pincode))
        retrieved_list = retrieved_list + tuple(merchant_id for merchant_id in reversed_merchant_dict[pincode] if merchant_id not in retrieved_list)
        byte_data = struct.pack('!{}I'.format(len(retrieved_list)), *retrieved_list)
        tree.insert(pincode,byte_data,replace=True)