import struct 
from BplusTree import tree

def add_merchants(merchant_list=[],merchants=[]):
    updated_merchant_list = merchant_list+merchants
    reversed_merchant_dict = {pincode: merchant_id for merchant_id, pincodes in merchants.items() for pincode in pincodes}
    for pincode in reversed_merchant_dict.keys():
        retrieved_list = struct.unpack('!{}I'.format(len(tree.get(pincode)//4)),tree.get(pincode))
        # byte_data = struct.pack('!{}I'.format(len(merchants[pincode])), *(merchants[pincode]))
        retrieved_list = retrieved_list + tuple(merchant_id for merchant_id in reversed_merchant_dict[pincode])
        byte_data = struct.pack('!{}I'.format(len(retrieved_list)), *retrieved_list)
        tree.insert(pincode,byte_data,replace=True)