
import uuid
import struct
import random
from bplustree import BPlusTree

"""
This class is used to generate a test database for the merchants.db file.
The database will contain 10,000,000 merchant IDs and 30,000 unique pincodes.
"""
class TestDB:
    def __init__(self):
        self.tree = BPlusTree("./merchants.db", order=50)
        self.unique_numbers = set()
        self.pincodes = []
        self.merchant_id_hash = {}
        self.merchant_ids = []
        self.assigned_merchants = set()

    def _generate_unique_numbers(self):
        while len(self.unique_numbers) < 30000:
            self.unique_numbers.add(random.randint(100000, 999999))
        self.pincodes = list(self.unique_numbers)
        random.shuffle(self.pincodes)

    def _generate_merchant_ids(self):
        while len(self.merchant_id_hash) < 10000000:
            uuid_string = str(uuid.uuid4())
            self.merchant_id_hash[uuid_string] = None
        self.merchant_ids = list(self.merchant_id_hash.keys())
    
    def _add_mapping(self, pincode):
        num_merchants = random.randint(0, 600)
        merchants = random.sample(self.merchant_ids, num_merchants)
        self.assigned_merchants.update(merchants)
        byte_data = b''.join(merchant_id.encode() for merchant_id in merchants)
        self.tree.insert(pincode, byte_data, replace=True)
    

    def populate(self):
        self._generate_unique_numbers()
        self._generate_merchant_ids()

        for pincode in self.pincodes:
            self._add_mapping(pincode)
        unasigned_merchants = set(self.merchant_ids) - self.assigned_merchants

        for merchant_id in unasigned_merchants:
            pincode = random.choice(self.pincodes)
            byte_data = self.tree.get(pincode)
            num_merchants = len(byte_data) // 36
            merchants = struct.unpack(f'!{num_merchants * 36}s', byte_data)
            merchants = [s[i:i+36].decode() for s in merchants for i in range(0, len(s), 36)]
            merchants = merchants + [merchant_id,]
            byte_data = b''.join([merchant_id.encode() for merchant_id in merchants])
            self.tree.insert(pincode, byte_data, replace=True)
        
        self.tree.close()
if __name__ == "__main__":
    test_db = TestDB()
    test_db.populate()