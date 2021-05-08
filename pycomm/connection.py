import socket
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet

HEADER_SIZE = 32
def make_header(length):
    header_format = '{:<' + str(HEADER_SIZE) + '}'
    return header_format.format(length).encode('utf-8')

def get_length(header):
    return int(header.strip())


class Connection:
    def __init__(self, hostname="localhost", port=8000):
        self.hostname = str(hostname)
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fernet = None

    def set_socket(self, socket):
        self.socket = socket

    def connect(self):
        self.socket.connect((self.hostname, self.port))
        self.key_exchange_client()

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
            try:
                client_connection.key_exchange_server()
                yield client_connection
            except Exception as e:
                print('Error in key exchange:', e)

    def key_exchange_client(self):
        public_raw = self.recv_bytes()
        public_key = serialization.load_pem_public_key(public_raw)

        enc_key = Fernet.generate_key()

        cipher_key = public_key.encrypt(
                enc_key,
                padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                )
        )

        self.send_bytes(cipher_key)

        self.enc_key = enc_key
        self.fernet = Fernet(enc_key)


    def key_exchange_server(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        public_raw = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.PKCS1,
        )

        self.send_bytes(public_raw)

        cipher_raw = self.recv_bytes()

        enc_key = private_key.decrypt(
                cipher_raw,
                padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                )
        )

        self.enc_key = enc_key
        self.fernet = Fernet(enc_key)

    def send_bytes(self, message):
        if self.fernet:
            message = self.fernet.encrypt(message)
        length = len(message)
        header = make_header(length)
        self.socket.send(header)
        self.socket.send(message)
        return length

    def recv_bytes(self):
        header = self.socket.recv(HEADER_SIZE)
        length = get_length(header)
        message = self.socket.recv(length)
        if self.fernet:
            return self.fernet.decrypt(message)
        else:
            return message

    def send(self, message):
        return self.send_bytes(message.encode('utf-8'))

    def recv(self):
        return self.recv_bytes().decode('utf-8')

    def close(self):
        self.socket.close()

