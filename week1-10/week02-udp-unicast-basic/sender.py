# sender.py
import socket
import time
from config import HOST, PORT, BUFFER_SIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for i in range(100):
    message = f"Fast message {i}"
    sock.sendto(message.encode(), (HOST, PORT))
    
    if(i + 1) % 10 == 0:
        print(f"[SENDER] Sent: {i + 1} messages")