import socket
import keyboard

from threading import Thread


class LiteNetClient:
    def __init__(self, ip, port=5050, header=64, encoding="utf-8"):
        self.ip, self.port = ip, port

        self.header, self.encoding = header, encoding

        self._close_msg = "[CLOSE]"

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        socket.setdefaulttimeout(5)

        keyboard.add_hotkey("t", self.message)

        self._temp = None

    def start(self):
        Thread(target=self._start).start()

    def message(self):
        message = input("You >> ")
        self.send(message)

    def get_server_msg(self):
        try:
            msg_length = self.socket.recv(self.header).decode(self.encoding)

            if msg_length:
                msg = self.socket.recv(int(msg_length)).decode(self.encoding)

                return msg

            else:
                return None

        except socket.timeout:
            return None

        except socket.error:
            print("Server has closed connection with server.")
            return None

    def send(self, msg):
        msg = msg.encode(self.encoding)
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.encoding) + b' ' * (self.header - len(str(msg_length).encode(self.encoding)))
        self.socket.send(send_length)
        self.socket.send(msg)

    def _start(self):
        self.socket.connect((self.ip, self.port))
        print(f"Connected to {self.ip}:{self.port}")

        while True:
            server_msg = self.get_server_msg()

            if server_msg:
                print(server_msg)

    def disconnect(self):
        self.send(self._close_msg)
        self.socket.close()