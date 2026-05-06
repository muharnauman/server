import socket
import threading
import os
host = "0.0.0.0"
port = 5000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()
clients = []
names = []
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

def handle(client):
    while True:
        try:
            # Receive message header (TEXT only)
            header = client.recv(1024).decode()
            if header.startswith("TEXT"):
                broadcast(header.encode())
        
        except:
            try:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                name = names[index]
                broadcast(f"TEXT|System|{name} left the chat".encode())
                names.remove(name)
            except:
                pass
            break

def receive():
    print(f"Server running on {host}:{port}...")
    while True:
        try:
            client, addr = server.accept()
            print(f"Connection from {addr}")

            client.send("NAME".encode())
            name = client.recv(1024).decode()

            names.append(name)
            clients.append(client)

            print(f"{name} joined the chat")
            broadcast(f"TEXT|System|{name} joined the chat".encode())

            thread = threading.Thread(target=handle, args=(client,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"Error accepting connection: {e}")

try:
    receive()
except KeyboardInterrupt:
    print("Server shutting down...")
    server.close()