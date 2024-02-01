import struct 
from BplusTree import tree

def add_merchants(merchant_list=[],merchants=[]):
    merchant_list = merchant_list+merchants
    byte_data = struct.pack('!{}I'.format(len(merchants)), *merchants)
    for merchant in merchants:
        for pincode in merchant:
            tree.insert(pincode,byte_data,replace=True)
    