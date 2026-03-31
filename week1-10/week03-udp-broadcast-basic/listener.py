# listener.py with reply
import socket
from config import PORT, BUFFER_SIZE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    print(f"[LISTENER] Received From {addr}: {data.decode()}")
    
    # Send unicast reply back to sender
    reply = f"Hello from listener at {socket.gethostname()}!"
    sock.sendto(reply.encode(), addr)