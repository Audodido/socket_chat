import socket 

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT' #when this msg is receieved we close the cnnction and disconnect client from the server
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

#to send a message you have to include a header first that communciates tyhe size of the message that's being sent
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT)) #this should actually follow same protocol of sending a header with size. Instead I put 2048 for now cuz its large enough that it will cover what's being sent. 

# send("Hey there")
send(input("enter your message:"))
send(DISCONNECT_MESSAGE)
