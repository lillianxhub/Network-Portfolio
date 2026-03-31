# receiver.py
import socket
from config import HOST, PORT, BUFFER_SIZE

received_ids = set()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    print(f"[RECEIVER] Received: {data.decode()} from {addr}")
    sock.sendto(b"ACK", addr)