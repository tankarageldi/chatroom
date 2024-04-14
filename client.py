import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            print(message)
        except OSError:
            break

def send_message(sock):
    while True:
        message = input()
        sock.send(message.encode())

def main():
    # Set up the client socket
    server_address = ('localhost', 12345)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    # Start a separate thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Send messages from the main thread
    send_message(client_socket)

    # Clean up
    client_socket.close()

if __name__ == '__main__':
    main()