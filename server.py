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

    welcome_message = f"Welcome to the client side portal. Enter a command in the format GET_MERCHANT <pincode>"
    newline = f"\n"
    writer.write(welcome_message.encode())
    writer.write(newline.encode())
    await writer.drain()

    # pincode = await reader.read(4096)
    prompt = ""

    while (True):
        prompt = await reader.readline()
        line = prompt.decode().strip().split()
        # writer.write(f'{line}'.encode())
        # await writer.drain()

        if line[0].upper() == "GET_MERCHANT" and len(line) == 2:
            print("test")
            pincode = line[1]
            break
        else:
            error_message = f"Invalid operation, try again\n"
            writer.write(error_message.encode())
            writer.write(newline.encode())
            await writer.drain()

    # print(pincode.decode())
    start=time.time()
    try:
        if(999999<int(pincode) or 100000>int(pincode)):
            data=""
            raise ValueError("Incorrect value")
        filename="merchants.db"
        tree=BPlusTree(f"./TestDB/{filename}") 
        serverOperator=ServerOps(tree,cache)
        data,recordCount=serverOperator.retrieve_merchants(int(pincode))
        tree.close()

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
   
    welcome_message = f"Welcome to the super user side portal. You can use the following commands"
    newline = f"\n"
    writer.write(welcome_message.encode())
    writer.write(newline.encode())
    writer.write("ADD_MERCHANTS <pincode> <number of merchants>. This adds the given number of merchants (randomly generated) to the pincode".encode())
    writer.write(newline.encode())
    writer.write("REMOVE_MERCHANTS <pincode> <merchant1> <merchant2>... This removes the specified merchants from the pincode".encode())
    writer.write(newline.encode())
    writer.write("ADD_NEW_MERCHANT <merchant_id> <pincode1> <pincode2>... Adds a new merchant which will service the given pincodes".encode())
    writer.write(newline.encode())
    await writer.drain()


    while(True):
        inp=await(reader.readline())
        inp=inp.decode().strip().split()
        if(inp[0].upper()=="ADD_MERCHANTS"):
            try:
                pincode = inp[1]
                no_of_merchants = inp[2]

                if (len(pincode) != 6):
                    raise ValueError
         
                merchants_dict = generate_merchant_ids(int(pincode),int(no_of_merchants),{})#if the byte data is pincode and you want to add merchant id's to the pincode
                #merchants_dict = decode_merchant_data(byte_data) if the byte data contains input of the format 'id pincode_1 pincode_2 ...'
                filename="merchants.db"

                tree=BPlusTree(f"./TestDB/{filename}") 
                serverOperator=ServerOps(tree,cache)
                x = serverOperator.add_merchant_to_cache(merchants_dict)
                tree.close()
                
                if(serverOperator.curr_length()>=500):
                    r=os.fork() # creates a new process
                    try:
                        if(r==0):
                            serverOperator.tree=BPlusTree(f"./TestDB/{filename}") 
                            serverOperator.move_to_cache()
                            serverOperator.tree.close()
                            os._exit(0)
                    except:
                        pass

                if (x == 1):
                    data="Added Successfully\n"
                else:
                    data="Pincode does not exist.\n"
                break

            except ValueError as e:
                data= "Pincode should be 6 digits\n"

        elif inp[0].upper() == "REMOVE_MERCHANTS":
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
            break

        elif inp[0].upper()== "ADD_NEW_MERCHANT":
            merchant_id,*pincodes=inp[1:]
            filename="merchants.db"
            tree=BPlusTree(f"./TestDB/{filename}") 
            serverOperator=ServerOps(tree,cache)
            merchants={int(pincode):(merchant_id,) for pincode in pincodes}
            serverOperator.add_merchant_to_cache(merchants)
            tree.close()
            try:
                if(serverOperator.curr_length()>=500):
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
                break
            except:
                data="Could not add data"

        else:
            data="Not a Valid Option, Try Again \n"
        
                
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
