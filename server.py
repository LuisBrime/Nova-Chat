from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

### SERVER HANDLERS ###
# https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to Nova Chat! Type your name and press enter, please.", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome to Nova Chat %s! If you want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))

    msg = "%s has joined the Nova Chat." % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left Nova Chat." % name, "utf8"))
            break

def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)
### END SERVER HANDLERS ###

### CONSTANTS ###
# https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()