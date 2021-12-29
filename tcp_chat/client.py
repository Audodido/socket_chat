## https://youtu.be/3UOyky9sEQY
import threading
import socket 

screenname = input('Choose a screenname: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('127.0.0.1', 5050))

# create a function that will run constantly and receieve incoming messages
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "SCREENNAME": # SCREENNAME is codeword sent from server receieve() function
                client.send(screenname.encode('utf-8'))
            else:
                print(message)

        except:
            print('An error occurred')
            client.close()
            break

def write():
    while True:
        message = f'{screenname}: {input("")}'
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()