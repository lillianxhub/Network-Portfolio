import socket
import time
from config import HOST, PORT, BUFFER_SIZE

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

msg = [
    "Hello, can you help",
    "I have a problem with my account.",
    "Thank you for your assistance!, Goodbye!"
]

for message in msg:
    client_socket.sendall(message.encode())

    response = client_socket.recv(BUFFER_SIZE)
    print(f"[ADVANCED CLIENT] Received: {response.decode()}")
    
    time.sleep(1)
    
client_socket.close()
print("[ADVANCED CLIENT] Connection closed")