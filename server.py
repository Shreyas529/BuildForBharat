import asyncio
import time
from bplustree import BPlusTree
from server_operations import ServerOps
from writeCache import WriteCache
from update_query import generate_merchant_ids
    
async def handle_client(reader, writer):

    prompt = ""

    prompt = await reader.readline()
    line = prompt.decode().strip().split()
    print(line)
    if line[0].upper() == "GET_MERCHANT" and len(line) == 2:
        
        pincode = line[1]
        
    start=time.time()
    try:
        if(999999<int(pincode) or 100000>int(pincode)):
            data=""
            raise ValueError("Incorrect value")
        
        data,recordCount=serverOperator.retrieve_merchants(int(pincode))

        if data is not None:
            data=f"<Found existing pincode {int(pincode)} with {recordCount} merchants>\n"+data+"\n"
        else:
            data=f"<No merchants found for pincode:{int(pincode)}>"
    except ValueError as e:
        
        data="Pincodes must be a 6 digit number"
    

    data=data.encode()
    
    writer.write(data)
    await writer.drain()
    end=time.time()
    writer.write(f"(Time taken by the request:{end-start} seconds)\n".encode())
    writer.close()
    
async def handle_superUser(reader,writer):
   
    inp=await(reader.readline())
    inp=inp.decode().strip().split()
    if(inp[0].upper()=="ADD_MERCHANTS"):
        try:
            pincode = inp[1]
            no_of_merchants = inp[2]

            if (len(pincode) != 6):
                raise ValueError
         
            merchants_dict = generate_merchant_ids(int(pincode),int(no_of_merchants),{})#if the byte data is pincode and you want to add merchant id's to the pincode
            x = serverOperator.add_merchant_to_cache(merchants_dict)
                
            if(serverOperator.curr_length()>=500):
               serverOperator.move_to_cache()

            if (x == 1):
                data="Added Successfully\n"
            else:
                data="Pincode does not exist.\n"
                

        except ValueError as e:
            data= "Pincode should be 6 digits\n"

    elif inp[0].upper() == "REMOVE_MERCHANTS":
        pincode, *merchant_ids = inp[1:]
        merchant_ids = list(merchant_ids)
        
        try:
            serverOperator.remove_merchants_from_pincode(int(pincode), merchant_ids)
            data = f'Merchants removed from Pincode {pincode}\n'
        except ValueError as e:
            data=e.__str__()

    elif inp[0].upper()== "ADD_NEW_MERCHANT":
        merchant_id,*pincodes=inp[1:]
        merchants={int(pincode):(merchant_id,) for pincode in pincodes}
        serverOperator.add_merchant_to_cache(merchants)
        try:
            if(serverOperator.curr_length()>=500):
                serverOperator.move_to_cache()
                data="Added Successfully\n"
                
        except:
            data="Could not add data\n"
  
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
    server1_host = '127.0.0.1'
    server1_port = 3389

    server2_host = '127.0.0.1'
    server2_port = 8080

    await asyncio.gather(
        start_server1(server1_host, server1_port),
        start_server2(server2_host, server2_port)
    )

 
cache=WriteCache()
tree=BPlusTree("./TestDB/merchants.db")
serverOperator=ServerOps(tree,cache)
try:
    asyncio.run(main())
except KeyboardInterrupt:
    tree.close()
