from bplustree import BPlusTree
import random
import uuid
import argparse

def retrieval_testcases():
    tree=BPlusTree("./TestDB/merchants.db",order=50)
    L=[]
    L1=[]

    try:
        j=0
        for key in tree.keys():
            if(j==10000):
                break
            if(len(L1)==256):
                L.extend(random.sample(L1,10))
                L1=[]
            L.append(key)
            L1.append(key)
            j+=1
    except:
        pass
    finally:
        tree.close()
        with open("pincodes.txt","w") as f:
            f.write("\n".join(str(i) for i in L))
            
def insert_test_cases():    
    # Each line will have the format:
    # pincode,merchant_id1,merchant_id2,...
    filename = "insert_pincodes.txt"
    num_entries = 15000
    pincodes = random.sample(range(100000, 999999), num_entries)  # Generate unique pincodes
    with open(filename, "w") as f:
        for pincode in pincodes:
            merchants = [str(uuid.uuid4()) for _ in range(random.randint(1, 100))]  # Random merchants
            f.write(f"{pincode},{','.join(merchants)}\n")

    print(f"Generated {num_entries} test cases in {filename}")

if __name__ == "__main__":
    #Taking arguments to see which test cases to generate
    parser=argparse.ArgumentParser()
    parser.add_argument("--retrieval",help="Generate retrieval test cases",action="store_true")
    parser.add_argument("--insert",help="Generate insert test cases",action="store_true")
    args=parser.parse_args()
    if args.retrieval:
        retrieval_testcases()
    if args.insert:
        insert_test_cases()