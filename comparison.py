from DB.server_operations import ServerOps
import time
from bplustree import BPlusTree
from DB.writeCache import WriteCache


tree=BPlusTree("./TestDB/merchants.db",order=50)
cache=WriteCache()
serverOperator=ServerOps(tree,cache)

import psycopg2
from dotenv import load_dotenv
import os
import time
load_dotenv()

conn=psycopg2.connect(
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)
cur=conn.cursor()

def get_pincode_psql(query):
    cur.execute(query)
    return cur.fetchall()

def compare_retrieval_time():
    with open("pincodes.txt","r") as f:
        pincodes=f.readlines()
    pincodes=list(map(int,pincodes))

    start1=time.time()
    
    for i in pincodes:
        query=f"SELECT merchant_id FROM PINCODE_MERCHANT WHERE pincode='{i}'"
        get_pincode_psql(query)
    end1=time.time()

    print(f"Time taken by Postgres:{end1-start1} seconds")

    start2=time.time()
    for i in pincodes:
        serverOperator.retrieve_merchants(i)
    end2=time.time()
    print(f"Time taken by BPlusTree:{end2-start2} seconds")

if __name__ == "__main__":
    compare_retrieval_time()
    tree.close()
