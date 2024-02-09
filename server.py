import asyncio
import socket
from bplustree import BPlusTree
from server_operations import ServerOps
from writeCache import WriteCache

def decode_merchant_data(byte_data:bytes) -> dict:
    string_data = byte_data.decode('utf-8')
    parts = string_data.strip().split()
    merchant_id = parts[0]
    pincodes = []
    for code in parts[1:]:
        if code.isdigit() and 100000<=int(code)<=999999:
            pincodes.append(int(code))
        else:
            raise ValueError("Invalid pincode: {}".format(code))

    data_dict = {merchant_id : pincodes}
    return data_dict
    
async def handle_client(reader, writer,filename):
    data = await reader.read(4096)
    
    # Handle client request here
    tree=BPlusTree(f"./TestDB/{filename}")
    serverOperator=ServerOps(tree)
   
    data=serverOperator.retrieve_merchants(int(data.decode("utf-8")))
    data=data.encode()
    tree.close()
   
    writer.write(data)
    await writer.drain()
    writer.close()
    
async def handle_superUser(reader,writer):
    
    byte_data=await reader.read(4096)
    filename = await reader.read(4096)
    try:
        merchants_dict = decode_merchant_data(byte_data) 
        data=""
    except ValueError as e:
        data=e+" : Pincode should be 6 digits" # Decode the received dict from bytes to string and then to dictionary
   
    data=data.encode()
    writer.write(data)
    await writer.drain()
    writer.close()



async def start_server1(host, port,filename):
    server = await asyncio.start_server(lambda r, w: handle_client(r, w, filename), host, port)
    async with server:
        print(f'Server started at {host}:{port}')
        await server.serve_forever()
async def start_server2(host,port,filename):
    server=await asyncio.start_server(lambda r, w: handle_superUser(r, w,filename), host, port)
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
        start_server1(server1_host, server1_port,"merchant.db"),
        start_server2(server2_host, server2_port,"merchant.db")
    )

asyncio.run(main())
