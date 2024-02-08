import struct
from functools import lru_cache


class ServerOps:
    def __init__(self, tree):
        self.tree = tree

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


    @lru_cache(maxsize=128)
    def retrieve_merchants(self, pincode: int) -> str:
        byte_data = self.tree.get(pincode)
        if byte_data is None:
            return "Not found"
        num_merchants = len(byte_data) // 36
        merchants = struct.unpack(f'!{num_merchants * 36}s', byte_data)

        return "\n".join([str(j) for j in merchants])
