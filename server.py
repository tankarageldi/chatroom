import socket
import threading

# Server configuration
HOST = 'localhost'
PORT = 5000

# List to store connected clients
clients = []

# Function to handle client connections
def handle_client(client_socket, client_address):
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # Broadcast message to all connected clients
                broadcast(message, client_socket)
            else:
                # If no message received, remove client from list and close connection
                remove_client(client_socket)
                break
        except:
            # If error occurs, remove client from list and close connection
            remove_client(client_socket)
            break

# Function to broadcast message to all connected clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message.encode('utf-8'))

# Function to remove client from list
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

# Function to start the server
def start_server():
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server started on {HOST}:{PORT}")

    while True:
        # Accept client connection
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        # Start a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Start the server
start_server()