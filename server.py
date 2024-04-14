import socket 
import sys
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object

# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
    print("Wrong input arguments!")
    print("Please enter as follows: python server.py <IP address> <port number>")
    exit()

ip = str(sys.argv[1]) # Get the IP address from the command line
port = int(sys.argv[2]) # Get the port number from the command line
server.bind((ip, port)) # Bind the socket to the IP address and port number

server.listen(10) # Listen for incoming connections
clients = [] # List of clients connected to the server.
client_names = [] # List of names of clients connected to the server.

def broadcast(message):
    for client in clients:
        client.send(message)
def thread(connection,address):
    while True:
            chat = client.recv(1024) # Receive a message from the client
            if chat: 
                print(client_names[clients.index(client)] + " < " + address[0] + "> " +  chat)
                chat_to_send = client_names[clients.index(client)] + " < " + address[0] + "> " + chat
                broadcast(chat_to_send,connection) # Broadcast the message to all clients
            else:  
                if connection in clients:
                    clients.remove(connection) # Remove the client from the list of clients
                    client_names.remove(client_names[clients.index(connection)]) # Remove the name of the client from the list of names
           
while True:
    client,address = server.accept() # Accept a connection from a client
    print("Connection established with: ", address) # Print the address of the client
    client.send("Please enter your name: ".encode()) # Send a message to the client to enter their name
    name = client.recv(1024).decode() # Receive the name of the client
    client_names.append(name) # Append the name of the client to the list of names
    clients.append(client) # Append the client to the list of clients

    print("Name of the client is: ", name) # Print the name of the client
    broadcast("{} has joined the chat room!".format(name).encode()) # Broadcast the message that the client has joined the chat room
    client.send("You have joined the chat room!".encode()) # Send a message to the client that they have joined the chat room

    start_new_thread(thread,(client,address)) # Start a new thread for the client


client.close() # Close the connection with the client
server.close() # Close the server
