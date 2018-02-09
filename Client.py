import socket
from threading import Thread
from tkinter import *


class ClientGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("SeruChat@0.1v")
        self.thread = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.make_widgets()
        self.root.mainloop()

    def make_widgets(self):
        self.connection_block = Frame(self.root)
        self.connection_block.pack(pady=5, anchor="nw")
        Label(self.connection_block, text="Адрес сервера").pack(side=LEFT)
        self.server = Entry(self.connection_block, width=20, bd=2)
        self.server.pack(side=LEFT)
        Label(self.connection_block, text="Порт").pack(side=LEFT)
        self.port = Entry(self.connection_block, width=5, bd=2)
        self.port.pack(side=LEFT)
        Button(self.connection_block, text="Соединение", command=self.create_connection).pack(side=LEFT, anchor="nw",
                                                                                              pady=5)
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
        pass

    def create_connection(self):
        self.status.set("Устанавливаем соединение")
        try:
            self.sock = socket.create_connection(("127.0.0.1", 10001), 5)
            self.status.set("Соединение установленно")
            self.thread = Thread(target=self.resiver)
            self.thread.start()

        except ConnectionRefusedError as ex:
            self.status.set("Невозможно установить соединение, попробуйте позже")

    def resiver(self):
        while True:
            if not self.root:
                break
            try:
                data = self.sock.recv(1024)
                if not data:
                    continue
                else:
                    self.chat.insert(END, data.decode("utf-8"))
            except socket.error as ex:
                self.status.set(ex.strerror)

    def send_message(self):
        self.status.set("Отправка сообщения")
        try:
            self.sock.send(self.msq.get().encode("utf-8"))
            self.chat.insert(END, self.msq.get())
            self.msq.set("")
            self.status.set("Успешно отправленно")
        except socket.error as ex:
            self.status.set(ex.strerror)


if __name__ == "__main__":
    app = ClientGUI()
