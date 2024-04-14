
# Chatroom

This is a simple chat room application implemented in Python. It consists of a server and a client component.

## Server

The server is responsible for handling incoming connections from clients and facilitating communication between them. It performs the following tasks:

- Listens for incoming connections on a specific port.
- Accepts client connections and assigns them a unique identifier.
- Broadcasts messages received from one client to all connected clients.
- Manages the list of connected clients.

To run the server, you can use the following code:

python server.py <server_ip> <server_port>



## Client
The client is responsible for connecting to the server and sending/receiving messages. It performs the following tasks:

- Connects to the server using the server's IP address and port number.
- Sends messages to the server to be broadcasted to other clients.
- Receives messages from the server and displays them to the user.

To run the client, you can use the following code:

python client.py <server_ip> <server_port>

Replace `<server_ip>` with the IP address of the server and `<server_port>` with the port number on which the server is listening.