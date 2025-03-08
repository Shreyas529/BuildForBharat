from bplustree import BPlusTree
import random

def retrieval_testcases():
    tree=BPlusTree("../TestDB/merchants.db",order=50)
    L=[]
    L1=[]

    try:
        j=0
        for key in tree.keys():
            if(j==10000):
                break
            if(len(L1)==256):
                L.extend(random.sample(L1,40))
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

if __name__ == "__main__":
    retrieval_testcases()