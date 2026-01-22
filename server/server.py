# server/server.py
import socket
import threading
import sys
import os

# Ensure we can import from common/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server_config import HOST_IP, PORT
from common.constants import HEADER_SIZE, FORMAT, DISCONNECT_MESSAGE

clients = []
aliases = []

def broadcast(message, _source_client=None):
    """Sends a message to all connected clients except the sender (optional)"""
    for client in clients:
        try:
            client.send(message)
        except:
            # If sending fails, remove the client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            aliases.remove(alias)

def handle_client(client):
    """Thread function to handle a single client connection"""
    while True:
        try:
            message = client.recv(HEADER_SIZE)
            if not message:
                break
            
            # The server does NOT decrypt. It blindly forwards the ciphertext.
            broadcast(message)
        except:
            # Client disconnected or error
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                alias = aliases[index]
                print(f"[DISCONNECT] {alias} disconnected.")
                aliases.remove(alias)
                broadcast(f"System: {alias} has left the chat.".encode(FORMAT))
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST_IP, PORT))
        server.listen()
    except Exception as e:
        print(f"[ERROR] Could not bind server: {e}")
        return

    print(f"[STARTING] Server is listening on port {PORT}...")
    print(f"[INFO] Server IP Address: {socket.gethostbyname(socket.gethostname())}")

    while True:
        client, addr = server.accept()
        print(f"[CONNECTION] Connected with {str(addr)}")

        # First message is always the alias (username)
        # Note: In this simple version, alias is sent plain text or pre-encryption logic
        # For strict security, even alias should be encrypted, but we keep it simple here.
        client.send("ALIAS_REQ".encode(FORMAT))
        alias = client.recv(HEADER_SIZE).decode(FORMAT)
        
        aliases.append(alias)
        clients.append(client)

        print(f"[ACTIVE] Alias is {alias}")
        broadcast(f"System: {alias} has joined the chat!".encode(FORMAT))
        
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()