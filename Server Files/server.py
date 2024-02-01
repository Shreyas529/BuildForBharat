import socket
import threading
def handle_client(client_socket):
    # Receive data from the client
    data = client_socket.recv(1024)

    # Send data back to the client
    client_socket.sendall(data)

    # Close the connection
    client_socket.close()
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('', 3389)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)

print('Server is listening on {}:{}'.format(*server_address))

while True:
    client_socket, client_address = server_socket.accept()

    # Handle the client connection in a separate thread
    threading.Thread(target=handle_client, args=(client_socket,)).start()
    
