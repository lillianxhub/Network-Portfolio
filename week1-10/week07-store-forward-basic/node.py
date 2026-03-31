#  Step 2: Node Detects Link Availability and Stores Messages
# node.py

# node.py
import socket
import threading
import time
import sys
from config import HOST, PEER_PORTS, BUFFER_SIZE, RETRY_INTERVAL
from message_queue import MessageQueue

# รับ BASE_PORT จาก argument
if len(sys.argv) < 2:
    print("Usage: python node.py <BASE_PORT>")
    sys.exit(1)
BASE_PORT = int(sys.argv[1])


queue = MessageQueue()


# ================================
# SEND MESSAGE
# ================================
def send_message(peer_port, message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((HOST, peer_port))
        s.sendall(message.encode())
        s.close()
        return True
    except Exception:
        return False

# ================================
# RETRY LOOP
# ================================
def retry_loop():
    while True:
        time.sleep(RETRY_INTERVAL)
        for msg_entry in queue.get_messages():
            peer = msg_entry["peer"]
            message = msg_entry["message"]
            print(f"[NODE {BASE_PORT}] Retrying to {peer}... (attempt {msg_entry.get('attempts', 0) + 1})")
            if send_message(peer, message):
                print(f"[NODE {BASE_PORT}] Sent stored message to {peer}")
                queue.remove_message(msg_entry)
            else:
                queue.inc_attempts(msg_entry)
# Step 3: Node Receives Messages and Stores Undeliverable Messages
# ================================
# SERVER
# ================================
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, BASE_PORT))
    server.listen()
    print(f"[NODE {BASE_PORT}] Listening for messages...")
    while True:
        conn, addr = server.accept()
        data = conn.recv(BUFFER_SIZE).decode()
        print(f"[NODE {BASE_PORT}] Received: {data} from {addr}")
        conn.close()
# ================================
# MAIN
# ================================
if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    threading.Thread(target=retry_loop, daemon=True).start()

    for peer in PEER_PORTS:
        msg = f"hello from node {BASE_PORT}"
        if send_message(peer, msg):
            print(f"[NODE {BASE_PORT}] Sent to {peer}")
        else:
            print(f"[NODE {BASE_PORT}] Peer {peer} unavailable, storing message")
            queue.add_message(msg, peer)

    print(f"[NODE {BASE_PORT}] Queue size: {len(queue.get_messages())}")

    while True:
        time.sleep(1)
