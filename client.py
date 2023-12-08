import socket
import threading
import uuid

def generate_unique_id():
    return str(uuid.uuid4())[:8]

chosen_name = input("Choose your name: ")

unique_id = generate_unique_id()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))


client.send(chosen_name.encode('ascii'))

received_id = client.recv(1024).decode('ascii')
print(f"Your unique ID is: {received_id}")

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = input('')
        full_message = f"{message}"
        client.send(full_message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()