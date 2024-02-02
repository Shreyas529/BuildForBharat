import struct
from BplusTree import tree

def reverse_mapping(merchants):
    reversed_merchants = {}
    for merchant_id, pincodes in merchants.items():
        for pincode in pincodes:
            reversed_merchants.setdefault(pincode, []).append(merchant_id)
    return reversed_merchants

def add_merchants(merchants:dict)->None:
    reversed_merchant_dict = reverse_mapping(merchants)
    
    for pincode in reversed_merchant_dict.keys():
        
        retrieved_data = tree.get(pincode)
        # merchant_ids = reversed_merchant_dict[pincode]
        retrieved_list =struct.unpack('!{}I'.format(len(retrieved_data)//4), retrieved_data)
        retrieved_list = retrieved_list + tuple(merchant_id for merchant_id in reversed_merchant_dict[pincode] if merchant_id not in retrieved_list)
        add_in_cache({pincode : retrieved_list})
        byte_data = struct.pack('!{}I'.format(len(retrieved_list)), *retrieved_list)
        tree.insert(pincode, byte_data, replace=True)

def  get_merchants(pincode={}):
    
    if len(pincode) == 0 : return
    
    retrieved_data = tree.get(pincode)
    retrieved_list = struct.unpack('!{}I'.format(len(retrieved_data)//4), retrieved_data)
    
    if retrieved_list ==  None:
        return []
    else:
        add_in_cache({pincode : retrieved_list})
        return retrieved_list
    
def add_in_cache(pincode_dict=[]):
    pass