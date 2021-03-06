from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk


def receive():  # handles receiving of messages

    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tk.END, msg)
        except OSError:  # possibly client has left
            break


def send(event=None):  # handles sending of messages
    msg = my_msg.get()
    my_msg.set("")  # clears input
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):  # function is called when window is closed
    my_msg.set("{quit}")
    send()


top = tk.Tk()
top.title("John's Chat App")

messages_frame = tk.Frame(top)
my_msg = tk.StringVar()  # for messages to be sent
my_msg.set("Type your messages here.")
scrollbar = tk.Scrollbar(messages_frame)  # to navigate through messages

msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()

messages_frame.pack()

entry_field = tk.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tk.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

HOST = input("Enter Host IP: ")

PORT = int(input("Enter Host Port: "))

BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tk.mainloop()
