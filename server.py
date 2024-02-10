import asyncio
import time
from bplustree import BPlusTree
from server_operations import ServerOps
import os
from writeCache import WriteCache
from update_query import generate_merchant_ids
# def decode_merchant_data(byte_data:bytes) -> dict:
#     string_data = byte_data.decode('utf-8')
#     parts = string_data.strip().split()
#     merchant_id = parts[0]
#     pincodes = []
#     for code in parts[1:]:
#         if code.isdigit() and 100000<=int(code)<=999999:
#             pincodes.append(int(code))
#         else:
#             raise ValueError("Invalid pincode: {}".format(code))

#     data_dict = {merchant_id : pincodes}
#     return data_dict

    
async def handle_client(reader, writer):
    
    pincode = await reader.read(4096)
    # print(pincode.decode())
    start=time.time()
    try:
        if(999999<int(pincode.decode()) or 100000>int(pincode.decode())):
            data=""
            raise ValueError("Incorrect value")
        filename="merchants.db"
        tree=BPlusTree(f"./TestDB/{filename}") 
        serverOperator=ServerOps(tree,cache)
        data,recordCount=serverOperator.retrieve_merchants(int(pincode.decode("utf-8")))
        tree.close()

        if data is not None:
            data=f"<Found existing pincode {int(pincode.decode('utf-8'))} with {recordCount} merchants>\n"+data+"\n"
        else:
            data=f"<No merchants found for pincode:{int(pincode.decode('utf-8'))}>"
    except ValueError as e:
        
        data="Pincodes must be a 6 digit number"
    

    data=data.encode()
    
    writer.write(data)
    await writer.drain()
    end=time.time()
    writer.write(f"(Time taken by the request:{end-start} seconds)\n".encode())
    writer.close()
    
async def handle_superUser(reader,writer):
   
    inp=await(reader.read(4096))
    inp=inp.decode().strip().split()

    if(inp[0]=="1"):
        try:
            pincode,no_of_merchants=inp[1:]
            merchants_dict = generate_merchant_ids(int(pincode),int(no_of_merchants),{})#if the byte data is pincode and you want to add merchant id's to the pincode
            #merchants_dict = decode_merchant_data(byte_data) if the byte data contains input of the format 'id pincode_1 pincode_2 ...'
            filename="merchants.db"
            tree=BPlusTree(f"./TestDB/{filename}") 
            serverOperator=ServerOps(tree,cache)
            serverOperator.add_merchant_to_cache(merchants_dict)
            tree.close()
            if(serverOperator.curr_length()>=128):
                r=os.fork() # creates a new process
                try:
                    if(r==0):
                        serverOperator.tree=BPlusTree(f"./TestDB/{filename}") 
                        serverOperator.move_to_cache()
                        serverOperator.tree.close()
                        os._exit(0)
                except:
                    pass
            data="Added Successfully\n"
        except ValueError as e:
            data=e+" : Pincode should be 6 digits\n"

    elif inp[0] == "2":
                        
        
        pincode, *merchant_ids = inp[1:]
        merchant_ids = list(merchant_ids)
        filename="merchants.db"
        tree=BPlusTree(f"./TestDB/{filename}") 
        serverOperator=ServerOps(tree,cache)
        try:
            serverOperator.remove_merchants_from_pincode(int(pincode), merchant_ids)
            print(merchant_ids)
            data = f'Merchants removed from Pincode {pincode}\n'
        except ValueError as e:
            data=e.__str__()
        serverOperator.tree.close()
    else:
        data="Not valid Option\n"
    data=data.encode()
    writer.write(data)
    await writer.drain()
    writer.close()

async def start_server1(host, port):
    server = await asyncio.start_server(lambda r, w: handle_client(r, w), host, port)
    async with server:
        print(f'Server started at {host}:{port}')
        await server.serve_forever()
async def start_server2(host,port):
    server=await asyncio.start_server(lambda r, w: handle_superUser(r, w), host, port)
    async with server:
        print(f'Server started at {host}:{port}')
        await server.serve_forever()

async def main():
    # Define your server configurations
    server1_host = ''
    server1_port = 3389

    server2_host = ''
    server2_port = 8080

    
    
    # Start both servers concurrently
    await asyncio.gather(
        start_server1(server1_host, server1_port),
        start_server2(server2_host, server2_port)
    )

 
cache=WriteCache()
asyncio.run(main())