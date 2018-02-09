import socket
from threading import Thread
from tkinter import *


class ServerGUI:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(("127.0.0.1", 10001))
        self.root = Tk()
        self.root.title("SeruChat@0.1v")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.make_widgets()
        self.thread = Thread(target=self.start_server).start()
        self.root.mainloop()

    def start_server(self):
        self.sock.listen()
        while True:
            if not self.root:
                break
            self.conn, adress = self.sock.accept()
            self.status.set(f"Соеденино")
            with self.conn:
                while True:
                    try:
                        data = self.conn.recv(1024)
                        if not data:
                            self.status.set("Клиент отрубился")
                            break
                        self.chat.insert(END, data.decode("utf-8"))
                    except ConnectionResetError as ex:
                        self.status.set("Слава богу, клиент отрубился")
                        break
            self.status.set("Ищу нового клиента")

    def make_widgets(self):
        self.status = StringVar()
        self.status_label = Label(self.root, bg="#cccccc", textvariable=self.status, width=49, height=2)
        self.status_label.pack(padx=10)
        self.chat = Listbox(self.root, width=58, bg="#ffffff")
        self.chat.pack()
        self.message_block = Frame(self.root)
        self.message_block.pack(pady=10)
        Label(self.message_block, text="Ваше сообщение").pack(anchor="nw")
        self.msq = StringVar()
        self.message = Entry(self.message_block, textvariable=self.msq, width=45)
        self.message.pack(side=LEFT, padx=5)
        Button(self.message_block, text="Отправить", command=self.send_message).pack(side=LEFT)

    def on_closing(self):
        self.root.destroy()
        self.root = None

    def send_message(self):
        self.status.set("Отправка сообщения")
        try:
            self.conn.send(self.msq.get().encode("utf-8"))
            self.chat.insert(END, self.msq.get())
            self.msq.set("")
            self.status.set("Успешно отправленно")
        except socket.error as ex:
            self.status.set(ex.strerror)


if __name__ == "__main__":
    app = ServerGUI()
