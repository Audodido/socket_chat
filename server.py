#https://youtu.be/3QiPPX-KeSc

import socket
import threading # lets you run multiple python 'threads' in a single program

HEADER = 64
PORT = 5050
# SERVER = '192.168.1.162'
SERVER = socket.gethostbyname(socket.gethostname()) #gets my IP addy for me
ADDR = (SERVER, PORT) #when we bind a socket to an address it needs to be in a tuple
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT' #when this msg is receieved we close the cnnction and disconnect client from the server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # INET refers to the type of address we're looking for for connections. 
#So INET because we're using IP addy. Sock_stream means we'll be streaming data through thtat connection. 

server.bind(ADDR) # now we've bound our socket to the address

#this fn handles individual conn and exchange between client and server 
def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length: # make sure you're getting a message upon connection
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                conn.send('Connection ended'.encode(FORMAT))

            print(f'[{addr}] {msg}')
            return_msg = input('return msg:')
            conn.send(return_msg.encode(FORMAT)) #dynamic/custom return msg
            # conn.send('Msg received'.encode(FORMAT)) #static/automated return msg
    
    conn.close()


#this fn handles initial connection tasks when a new conn is made
def start(): #start socket server
    server.listen() # tells server to listen for new connections
    print(f'[LISTENING] Server is listening on {SERVER}')
    while True:
        conn, addr = server.accept() # when a connection comes in we'll store the port and address it came from in these 2 vars
        thread = threading.Thread(target=handle_client, args=(conn,addr)) #pass new conn up to a new thread via handle_client fn 
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')

print('[STARTING] SERVER IS STARTING ... ')
start()
