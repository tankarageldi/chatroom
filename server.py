import socket 
import sys
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 2: 
    print("Wrong input arguments!")
    print("Please enter as follows: python server.py <port number>")
    exit()

# Listen on all available interfaces using ''
HOST = ''  # Empty string means listen on all available interfaces
port = int(sys.argv[1])

try:
    server.bind((HOST, port))
except socket.error as e:
    print(f"Binding failed: {e}")
    sys.exit()

server.listen(5)  # Allow up to 5 queued connections

clients = []
client_names = []

# Rest of your server code remains the same, but add better error handling
def broadcast(message):
    disconnected_clients = []
    for client in clients:
        try:
            client.send(message)
        except socket.error:
            disconnected_clients.append(client)
    
    # Clean up disconnected clients
    for client in disconnected_clients:
        handle_disconnect(client)

def handle_disconnect(connection):
    if connection in clients:
        i = clients.index(connection)
        clients.remove(connection)
        connection.close()
        name = client_names[i]
        client_names.remove(name)
        broadcast(f"{name} left the chat room!".encode())

def thread(connection, address):
    while True:
        try:
            chat = connection.recv(2048)
            if chat:
                print(f"< {address[0]} > {chat.decode()}")
                broadcast(chat)
            else:
                handle_disconnect(connection)
                break
        except socket.error:
            handle_disconnect(connection)
            break

def start():
    print(f"Server is running on all available interfaces on port: {port}")
    print("Local IP addresses this server is available on:")
    
    # Show all IP addresses where the server is available
    hostname = socket.gethostname()
    addresses = socket.getaddrinfo(hostname, None)
    for addr in addresses:
        if addr[0] == socket.AF_INET:  # Only show IPv4 addresses
            print(f"  - {addr[4][0]}")
    
    print("\nWaiting for connections...")
    
    while True:
        try:
            client, address = server.accept()
            print(f"Connection established with: {address}")

            client.send('Please enter your name:'.encode())
            name = client.recv(2048).decode()

            client_names.append(name)
            clients.append(client)

            print(f"Name of the client is: {name}")
            broadcast(f"{name} joined the chat room!".encode())

            th = threading.Thread(target=thread, args=(client, address))
            th.start()
        except socket.error as e:
            print(f"Error accepting connection: {e}")
            continue

if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        for client in clients:
            client.close()
        server.close()