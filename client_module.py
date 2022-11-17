"""
The GUI side of the chat system. Work in conjunction with the server.py file, creating a live chat system.
"""

from socket import *
from threading import *
import tkinter as tk
from tkinter import END
import pyodbc

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'Server=RORYS-PC;'
                      'Database=Users;'
                      'UID=remote_connection;'
                      'PWD=123;')

def chat_room_window():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    hostIp = "127.0.0.1"
    portNumber = 7500

    clientSocket.connect((hostIp, portNumber))

    window = tk.Toplevel()
    window.title("Connected To: "+ hostIp+ ":"+str(portNumber))

    txtMessages = tk.Text(window, width=50)
    txtMessages.grid(row=0, column=0, padx=10, pady=10)

    txtYourMessage = tk.Entry(window, width=50)
    txtYourMessage.grid(row=1, column=0, padx=10, pady=10)

    def sendMessage():
        clientMessage = txtYourMessage.get()
        if clientMessage == '/users':
            cursor = conn.execute('SELECT * FROM Users WHERE is_online = 1')
            results = cursor.fetchall()
            current_users = []
            for name in results:
                users = name[0]
                current_users.append(users)
            users_list = f"The currently online users are: {current_users}"
            txtMessages.insert('1.0', users_list)
            txtYourMessage.delete(0, END)
        if clientMessage == '/clear':
            txtMessages.delete('1.0', END)
            txtYourMessage.delete(0, END)
        else:
            txtMessages.insert(END, "\n" + "You: "+ clientMessage)
            clientSocket.send(clientMessage.encode("utf-8"))
            txtYourMessage.delete(0, END)

    btnSendMessage = tk.Button(window, text="Send", width=20, command=sendMessage)
    btnSendMessage.grid(row=2, column=0, padx=10, pady=10)

    def recvMessage():
        while True:
            serverMessage = clientSocket.recv(1024).decode("utf-8")
            print(serverMessage)
            txtMessages.insert(END, "\n"+serverMessage)

    recvThread = Thread(target=recvMessage)
    recvThread.daemon = True
    recvThread.start()