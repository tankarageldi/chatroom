import socket 
import threading
import sys
import select 

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





