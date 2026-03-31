# broadcaster.py with periodic sending
import socket
import time
from config import BROADCAST_IP, PORT, BUFFER_SIZE

time.sleep(2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.bind(("", 0))

message = b"DISCOVERY: "+socket.gethostname().encode()+b" is online"
sock.sendto(message, (BROADCAST_IP, PORT))
print(f"[BROADCASTER] Sent broadcast to {BROADCAST_IP}:{PORT}")

sock.settimeout(5)
responses = []

try:
    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        if data != message: # Loopback prevention
            responses.append((data, addr))
            print(f"[BROADCASTER] Received response from {addr}: {data.decode()}")
except socket.timeout:
    print("[BROADCASTER] No more responses received.")
finally:
    sock.close()