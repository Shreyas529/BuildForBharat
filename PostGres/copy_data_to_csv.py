from bplustree import BPlusTree
import struct
if __name__ == "__main__":
    bpt = BPlusTree("../TestDB/merchants.db", order=50)
    try:
        with open("./merchants.csv", "w") as f:
            for key in bpt.keys():
                value = bpt.get(key)
                num_merchants = len(value)//36
                merchants = struct.unpack(f'!{num_merchants * 36}s', value)
                merchants = [s[i:i+36].decode() for s in merchants for i in range(0, len(s), 36)]
                for v in merchants:
                    f.write(f"{key},{v}\n")
    except:
        pass
    finally:    
        bpt.close()
