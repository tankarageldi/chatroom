import socket 
import sys
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object

# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
    print("Wrong input arguments!")
    print("Please enter as follows: python server.py <IP address> <port number>")
    exit()

ip = str(sys.argv[1]) # Get the IP address from the command line
port = int(sys.argv[2]) # Get the port number from the command line
server.bind((ip, port)) # Bind the socket to the IP address and port number

server.listen() # Listen for incoming connections
clients = [] # List of clients connected to the server.
client_names = [] # List of names of clients connected to the server.


def broadcast(message): # Function to broadcast a message to all clients
    for client in clients: # Iterate through the list of clients
        client.send(message) # Send the message to the client

def thread(connection,address): # Function to handle the connection with the client
    while True: # Infinite loop to keep the connection alive
            chat = connection.recv(2048) # Receive a message from the client
            if chat:
                print("< "+ address[0] +" > " + chat.decode()) # Print the message received from the client
                broadcast(chat) # Broadcast the message to all clients
            else:  
                i = clients.index(connection) # Get the index of the client
                clients.remove(connection) # Remove the client from the list of clients
                connection.close() # Close the connection with the client
                name = client_names[i] # Get the name of the client
                client_names.remove(name) # Remove the name of the client from the list of names

def start():
    print("Server is running on IP: ", ip, " and port: ", port) # Print the IP address and port number of the server
    print("Waiting for connections...") # Print that the server is waiting for connections
    while True:
        client,address = server.accept() # Accept a connection from a client
        print("Connection established with: ", address) # Print the address of the client

        client.send('Please enter your name:'.encode()) # Send a message to the client to enter their name
        name = client.recv(2048).decode() # Receive the name of the client

        client_names.append(name) # Append the name of the client to the list of names
        clients.append(client) # Append the client to the list of clients

        print("Name of the client is: ", name) # Print the name of the client
        broadcast("{} joined the chat room!".format(name).encode()) # Broadcast the message that the client has joined the chat room

        # Start Handling Thread For Client
        th = threading.Thread(target=thread, args=(client,address))
        th.start()


start() # Start the function to accept connections from clients
