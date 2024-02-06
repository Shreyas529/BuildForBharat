import asyncio
from bplustree import BPlusTree
from server_operations import ServerOps
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

async def start_server(host, port,filename):
    server = await asyncio.start_server(lambda r, w: handle_client(r, w, filename), host, port)
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
        start_server(server1_host, server1_port,"local.db"),
        start_server(server2_host, server2_port,"local.db")
    )

asyncio.run(main())
