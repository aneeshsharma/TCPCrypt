import socket

class Connection:
    def __init__(self, hostname="localhost", port=8000):
        self.hostname = str(hostname)
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_socket(self, socket):
        self.socket = socket

    def connect(self):
        self.socket.connect((self.hostname, self.port))

    def bind(self):
        self.socket.bind((self.hostname, self.port))

    def listen(self, connection_count):
        self.socket.listen(connection_count)

    def get_server(self, connection_count):
        self.bind()
        self.listen(connection_count)
        while True:
            (client, address) = self.socket.accept()
            client_connection = Connection()
            client_connection.set_socket(client)
            yield client_connection

    def send(self, message):
        data = '{:<256}'.format(message).encode('utf-8')
        return self.socket.send(data)

    def recv(self):
        return self.socket.recv(256)

    def close(self):
        self.socket.close()

