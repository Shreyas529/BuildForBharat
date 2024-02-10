import uuid
import random
from BplusTree import tree

def generate_merchant_ids(pincode: int,merchant_dict:dict) -> None: #To generate  unique merchant for each pincode if the number of merchants serving the pincode is not given.
    merchant_ids = set()
    for i in range(0,random.randint(10,100)):
        uuid_string = str(uuid.uui4())
        merchant_ids.add(uuid_string)

    merchant_dict[pincode] = tuple(merchant_ids)
    return merchant_dict
    
def generate_merchant_ids(pincode: int,no_of_merchants:int,merchant_dict:dict) -> None: #To generate unique merchant for each pincode give how many merchants serve the pincode 
    merchant_ids = set()
    for i in range(0,no_of_merchants):
        uuid_string = str(uuid.uui4())
        merchant_ids.add(uuid_string)

    merchant_dict[pincode] = tuple(merchant_ids)
    return merchant_dict

    