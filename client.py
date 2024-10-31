import socket
import sys
import threading
import time

def create_client():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class ChatClient:
    def __init__(self):
        self.name = input("Enter your name: ")
        self.client = create_client()
        self.connected = False

    def connect(self, ip, port, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                self.client.connect((ip, port))
                self.connected = True
                print(f"Connected to server at {ip}:{port}")
                return True
            except socket.error as e:
                print(f"Connection attempt {retries + 1} failed: {e}")
                retries += 1
                if retries < max_retries:
                    print("Retrying in 3 seconds...")
                    time.sleep(3)
                    self.client = create_client()
        
        print("Failed to connect to server after multiple attempts")
        return False

    def send_message(self):
        while self.connected:
            try:
                message = input('')
                if message.lower() == 'quit':
                    self.connected = False
                    break
                full_message = f'{self.name} : {message}'
                self.client.send(full_message.encode())
            except socket.error as e:
                print(f"Error sending message: {e}")
                self.connected = False
                break

    def receive_messages(self):
        while self.connected:
            try:
                message = self.client.recv(2048).decode()
                if not message:
                    break
                if message == 'Please enter your name:':
                    self.client.send(self.name.encode())
                else:
                    print(message)
            except socket.error as e:
                print(f"Error receiving message: {e}")
                self.connected = False
                break

    def start(self):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        send_thread = threading.Thread(target=self.send_message)
        send_thread.daemon = True
        send_thread.start()

        while self.connected:
            time.sleep(0.1)
        
        print("Disconnected from server")
        self.client.close()

def main():
    if len(sys.argv) != 3:
        print("Wrong input arguments!")
        print("Please enter as follows: python client.py <Server IP address> <Server port number>")
        return

    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    
    client = ChatClient()
    if client.connect(ip, port):
        client.start()

if __name__ == "__main__":
    main()