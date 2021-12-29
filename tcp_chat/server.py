## https://www.youtube.com/watch?v=3UOyky9sEQY
import threading
import socket

# check out neuralNine's port scanner project

host = '127.0.0.1' #local host 
port = 5050

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()

clients = [] #new clients go here
screennames = [] #clients chat aliases/screennames


# method that will broadcast messages to everyone connected to the server
def broadcast(message):
    for client in clients:
        client.send(message)

# method that will handle/deal with messages if they come in
def handle(client):
    while True:
        try:
            message = client.recv(1024) # while connection is running try and receieve a message if there is one
            broadcast(message) # then send the message out to everyone in the chat
        except: # if there's an error receiving or brdcasting a message, cut the connection to this client, remove them from lists.   
            index = clients.index(clients) #gets index of the client that caused the error
            client.remove(client) # remove them from the clients list
            client.close() #close their connection
            screenname = screennames[index]
            screennames.remove(screenname)

            broadcast(f'{screenname} has left the chat.'.encode('utf-8'))
            break

#create a function for receieving messages
def receive():
    while True: #running the accept() method constantly
        client, address = server.accept() #accept() function returns client and address of the sender
        print(f'Connected with {str(address)}') #prints to console — not chatroom

        client.send('SCREENNAME'.encode('utf=8')) # this message is like a codeword sent to client — not chatroom — in order to trigger something in the client that will prompt them for a username. 
        screenname = client.recv(1024).decode('utf-8')
        screennames.append(screenname) #add sender to the lists
        clients.append(client)

        print(f'Clients screenname is {screenname}') # print to console
        broadcast(f'{screenname} has joined the chat.'.encode('utf-8'))
        client.send('You\'ve connected to the server.'.encode('utf-8')) #send sender confirmation that they've connected

        #set up threads/multithreading
        thread = threading.Thread(target=handle, args=(client,))
        thread.start() #start up a thread for user  

print('Server is listening...')
receive()
