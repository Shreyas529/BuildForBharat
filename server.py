import socket
import threading
from BplusTree import tree
from server_operations import ServerOps
def handle_client(client_socket,serverOperator:ServerOps):
    # Receive data from the client
    data = client_socket.recv(1024)
    # Send data back to the client
    data=serverOperator.retrieve_merchants(int(data.decode("utf-8")))
    
    client_socket.sendall(data.encode("utf-8"))

    # Close the connection
    client_socket.close()
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('', 3389)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)
serverOperator=ServerOps(tree)
print('Server is listening on {}:{}'.format(*server_address))

while True:
    client_socket, client_address = server_socket.accept()

    # Handle the client connection in a separate thread
    threading.Thread(target=handle_client, args=(client_socket,serverOperator)).start()
    
