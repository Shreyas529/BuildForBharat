import asyncio
from bplustree import BPlusTree
from server_operations import ServerOps
from writeCache import WriteCache
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
    
async def handle_superUser(reader,writer,filename):
    
    username=await reader.read(4096)
    key=await reader.read(4096)
    data="abcd"
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
        start_server1(server1_host, server1_port,"local.db"),
        start_server2(server2_host, server2_port,"local.db")
    )

asyncio.run(main())
