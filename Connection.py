import socket

HEADER_SIZE = 32
def make_header(length):
    header_format = '{:<' + str(HEADER_SIZE) + '}'
    return header_format.format(length)

def get_length(header):
    return int(header.strip())


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
        length = len(message)
        header = make_header(length)
        self.socket.send(header.encode('utf-8'))
        self.socket.send(message.encode('utf-8'))

    def recv(self):
        header = self.socket.recv(HEADER_SIZE)
        length = get_length(header)
        return self.socket.recv(length).decode('utf-8')

    def close(self):
        self.socket.close()

