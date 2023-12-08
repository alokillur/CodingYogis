import socket
import threading
import uuid

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = {}
nicknames = {}

def generate_unique_id():
    return str(uuid.uuid4())[:8]

def broadcast(message, sender):
    sender_id = clients[sender]
    for client_socket, client_id in clients.items():
        if client_socket != sender:
            try:
                client_socket.send(f"{sender_id}: {message}".encode('ascii'))
            except:
                remove(client_socket)



def remove(client_socket):
    if client_socket in clients:
        unique_id = clients[client_socket]
        nickname = nicknames[client_socket]
        clients.pop(client_socket)
        nicknames.pop(client_socket)
        broadcast(f"{nickname} left the chat.".encode('ascii'), None)

def handle(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('ascii')
            if message == 'NICK':
                unique_id = generate_unique_id()
                clients[client_socket] = unique_id
                client_socket.send(unique_id.encode('ascii'))
            else:
                broadcast(message, client_socket)
        except:
            remove(client_socket)
            break


def receive():
    while True:
        client_socket, address = server.accept()
        print(f"Connected with {address}")

        chosen_name = client_socket.recv(1024).decode('ascii')

        unique_id = generate_unique_id()
        clients[client_socket] = unique_id
        nicknames[client_socket] = chosen_name

        print(f"{chosen_name} ({unique_id}) joined the chat.")
        broadcast(f"{chosen_name} joined the chat.".encode('ascii'), client_socket)

        client_socket.send(unique_id.encode('ascii'))

        threading.Thread(target=handle, args=(client_socket,)).start()

print("Server is listening...")
receive()