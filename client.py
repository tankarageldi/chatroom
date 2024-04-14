import socket
import sys
import threading


name = input("Enter your name: ") # Get the name of the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object

# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
    print("Wrong input arguments!")
    print("Please enter as follows: python client.py <Server IP address> <Server port number>")
    exit()

ip = str(sys.argv[1]) # Get the IP address from the command line
port = int(sys.argv[2]) # Get the port number from the command line
client.connect((ip, port)) # Connect to the server

# Function to send messages to the server
def send():
    while True:
        message = '{} : {}'.format(name, input(''))
        client.send(message.encode()) # Send the message to the server

# Function to receive messages from the server        
def get(): 
    while True:
        try: # Try to receive messages from the server
            message = client.recv(2048).decode()
            if message == 'Please enter your name:': # If the server asks for the name, send the name
                client.send(name.encode())
            else:
                print(message)
        except: # If an error occurs, close the connection with the server
            client.close()
            break

thread_get = threading.Thread(target=get)
thread_get.start()

thread_send = threading.Thread(target=send)
thread_send.start()
