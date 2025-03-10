from DB.server_operations import ServerOps
import time
from bplustree import BPlusTree
from DB.writeCache import WriteCache
import argparse


tree=BPlusTree("./TestDB/merchants.db",order=50)
cache=WriteCache()
serverOperator=ServerOps(tree,cache)

import psycopg2
import psycopg2.extras
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
    
def compare_insert_time():
    with open("insert_pincodes.txt","r") as f:
        pincodes=f.readlines()
    
    # Convert to dictionary (pincode -> list of merchant IDs)
    pincodes_dict = {}
    for line in pincodes:
        parts = line.strip().split(',')
        pincode = int(parts[0])
        merchants = parts[1:]  # Store merchants as list
        pincodes_dict[pincode] = merchants
    
    # PostgreSQL insert time
    start1 = time.time()
    # for pincode, merchants in pincodes_dict.items():
    #     for merchant_id in merchants:
    #         query = f"INSERT INTO PINCODE_MERCHANT VALUES ({pincode}, '{merchant_id}')"
    #         cur.execute(query)  # Commit happens immediately after each insert
    data_to_insert = [(pincode, merchant_id) for pincode, merchants in pincodes_dict.items() for merchant_id in merchants]

    query = """
    INSERT INTO PINCODE_MERCHANT (pincode, merchant_id) 
    VALUES %s 
    ON CONFLICT DO NOTHING
    """
    psycopg2.extras.execute_values(cur, query, data_to_insert, template="(%s, %s)")

    end1 = time.time()
    print(f"Time taken by PostgreSQL: {end1 - start1} seconds")

    # BPlusTree insert time
    start2 = time.time()
    serverOperator.add_merchants(pincodes_dict)
    end2 = time.time()
    print(f"Time taken by BPlusTree: {end2 - start2} seconds")

if __name__ == "__main__":
    
    #Taking arguments to see which to compare
    parser=argparse.ArgumentParser()
    parser.add_argument("--insert",help="Compare insert time",action="store_true")
    parser.add_argument("--retrieval",help="Compare retrieval time",action="store_true")
    args=parser.parse_args()
    if args.insert:
        compare_insert_time()
    if args.retrieval:
        compare_retrieval_time()
    tree.close()
