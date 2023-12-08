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
            msg = message = client_socket.recv(1024)
            if msg.decode('ascii').startswith('KICK') :
                if nicknames[clients.index(client_socket)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else :
                    client_socket.send('Command was refused'.encode('ascii'))
            elif msg.decode('ascii'.startswith('BAN'):
                if nicknames[clients.index(client_socket)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt','a') as f:
                        f.write(f'{name_to_ban}\n')
                    print(f'{name_to_ban} was Banned!')
                else :
                    client_socket.send('Command was refused'.encode('ascii'))
            elif msg.decode('ascii').startswith('MUTE'):
                if nicknames[clients.index(client_socket)] == 'admin':
                    name_to_mute = msg.decode('ascii')[3:]
                else:
                     client_socket.send('Command was refused'.encode('ascii'))
            else:
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
        client, address = server.accept()
        print(f"Connected with {address}")

        chosen_name = client.recv(1024).decode('ascii')

        with open('bans.txt','r') as f:
            bans = f.readlines()

        if chosen_name+'\n' in bans:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        if chosen_name == 'admin' :
            client.send('PASSCODE'.encode('ascii'))
            password = client.recv(1024).decode('ascii')

            if password != 'codingyogi' :
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        unique_id = generate_unique_id()
        clients[client] = unique_id
        nicknames[client] = chosen_name

        print(f"{chosen_name} ({unique_id}) joined the chat.")
        broadcast(f"{chosen_name} joined the chat.".encode('ascii'), client_socket)

        client.send(unique_id.encode('ascii'))

        threading.Thread(target=handle, args=(client,)).start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You Were Kicked By Admin!')
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked by an Admin!'.encode('ascii'))



print("Server is listening...")
receive()