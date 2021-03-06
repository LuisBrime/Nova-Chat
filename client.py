from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

import crypto
import LZW

### CLIENT HANDLERS ###
# https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)

            #dec_msg = crypto.decypher(msg, privateKey, publicKey)
            #print('Message has been decrypted... %s' % dec_msg)
            #dem_msg = LZW.decompress(dec_msg)
            #print('Message has been decompressed... %s' % dem_msg)
        except OSError:
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")

    com_msg = LZW.compress(msg)

    listToString = ""
    for i, item in enumerate(com_msg):
        if i:
            listToString = listToString + ','
        listToString = listToString + str(item)
    print('Message has been compressed... %s ' % listToString)

    enc_msg = crypto.cypher(listToString, publicKey, 1)
    print('Message has been encrypted... %s' % enc_msg)

    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    my_msg.set("{quit}")
    send()
### END CLIENT HANDLERS ###

### GUI ###
# https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
top = tkinter.Tk()
top.title("Nova Chat")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="        Send        ", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)
### END GUI ###

keypair = crypto.keygen(2 ** 64)
publicKey, privateKey = keypair.public, keypair.private

### CONNECT ###
# https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
HOST = input('Enter host: ')
PORT = input('Enter port: ')

if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()