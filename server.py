from Connection import Connection

conn = Connection("localhost", 1234)

server = conn.get_server(10)

for client in server:
    print(client.recv())
    client.send("Hello")
    client.close()
