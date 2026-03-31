import socket
import time
from config import HOST, PORT, BUFFER_SIZE

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)


print(f"[ADVANCED SERVER] Listening on {HOST}:{PORT}")


while True:
    conn, addr = server_socket.accept()
    print(f"[ADVANCED SERVER] @{time.strftime('%H:%M:%S')} - Connection from {addr}")

    try:
        while True:    
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break

            msg= data.decode()
            timestamp = time.strftime('%H:%M:%S')
            print(f"[ADVANCED SERVER] @{timestamp} - Received Client: {msg}")
            
            reply = f"ACK: {msg} (Advanced Server at {timestamp})"
            conn.sendall(reply.encode())
    
    finally:
        conn.close()
        print(f"[ADVANCED SERVER] @{time.strftime('%H:%M:%S')} - Connection closed")