import socket
import threading
import uuid

def generate_unique_id():
    return str(uuid.uuid4())[:8]

chosen_name = input("Choose your name: ")

if chosen_name == 'admin' :
    password = input("Enter password for admin:")
     
unique_id = generate_unique_id()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

stop_thread = False

client.send(chosen_name.encode('ascii'))

received_id = client.recv(1024).decode('ascii')
print(f"Your unique ID is: {received_id}")

def receive():
    while True:
        if stop_thread :
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message =='NICK' :
                client.send(chosen_name.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASSCODE' :
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE' :
                        print("Connection was refused! Wrong Password!")
                        stop_thread = True
                elif next_message == 'BAN' :
                    print('Connection refused becuase of ban!')
                    client.close()
                    stop_thread =True
            else :
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        if stop_thread :
            break
        message = input('')
        full_message = f"{message}"
        if message[len(chosen_name)+2:].startswith('/'):
            if chosen_name == 'admin':
                if full_message[len(chosen_name)+2)].startswith('/kick'):
                    client.send(f'KICK {message[len(chosen_name)+2+6:]}'.encode('ascii'))
                elif full_message[len(chosen_name)+2)].startswith('/ban'):
                    client.send(f'BAN {message[len(chosen_name)+2+5:]}'.encode('ascii'))
                elif full_message[len(chosen_name)+2)].startswith('/mute'):
                    client.send(f'MUTE {message[len(chosen_name)+2+5:]}'.encode('ascii'))
            else:
                print("Commands can only be executed by the admin!")
        else :
            client.send(full_message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()