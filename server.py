import asyncio
import random
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
    try:
        if(int(pincode.decode()) not in [100000,999999]):
            data=""
            raise ValueError
        filename="merchants.db"
        tree=BPlusTree(f"./TestDB/{filename}") 
        serverOperator=ServerOps(tree,cache)
        data,recordCount=serverOperator.retrieve_merchants(int(pincode.decode("utf-8")))
        tree.close()

        if data is not None:
            data=f"<Found existing pincode {int(pincode.decode('utf-8'))} with {recordCount} merchants>\n"+data
        else:
            data=f"<No merchants found for pincode:{int(pincode.decode('utf-8'))}>"
    except ValueError as e:
        data="Pincodes must be a 6 digit number"
    

    data=data.encode()
   
    writer.write(data)
    await writer.drain()
    writer.close()
    
async def handle_superUser(reader,writer):
    
    menu = "Enter 1 for addition of merchants\nEnter 2 for removal of merchants\n"
    writer.write(menu.encode())
    await writer.drain()
    
    choice = await reader.read(4096)
    choice = choice.decode().strip()
    
    filename="merchants.db"
    tree=BPlusTree(f"./TestDB/{filename}") 
    serveroperator = ServerOps(tree , cache)

    try:
        if choice == "1":
            response = "Option 1 selected: Addition of merchants:\n"
            writer.write(response.encode())
            await writer.drain()
            
            response = "Enter the pincode for merchants to be added\n"
            writer.write(response.encode())
            await writer.drain()
            
            byte_data=await reader.read(4096)
            byte_data = byte_data.decode().strip()
            merchant_dict = generate_merchant_ids(byte_data)
            serveroperator.add_merchant_to_cache(merchant_dict)
            if(serveroperator.curr_length()==128):
                r=os.fork() # creates a new process
                if(r==0):
                    serveroperator.tree=BPlusTree(f"./TestDB/{filename}") 
                    serveroperator.move_to_cache()
                    serveroperator.tree.close()
                    exit(0)
                else:
                    pass
        
        elif choice == "2":
            
            response = "Option 2 selected: Removal of merchants\nPlease enter the PINCODE first followed by merchant id's to be removed from that pincode:\n"
            writer.write(response.encode())
            await writer.drain()
            
            removal_input = await reader.read(4096)
            removal_input = removal_input.decode().strip()
            pincode, *merchant_ids = removal_input.split()
            merchant_ids = list(merchant_ids)
            serveroperator.remove_merchants_from_pincode(int(pincode), merchant_ids)
            response = f'Merchants removed from Pincode {pincode}\n'
        
        else:
            
            response = "Invalid  Option. Please enter again.\n"
            writer.write(response.encode())
            await writer.drain()
            
    except Exception as e:
        response = f"Error: {str(e)}\n"
        writer.write(response.encode())
        await writer.drain()
    
    finally:
        # Close the connection.
        tree.close()
        writer.close()

    # data=data.encode()
    # writer.write(data)
    # await writer.drain()
    # writer.close()

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