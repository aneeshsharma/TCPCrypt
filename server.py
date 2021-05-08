from Connection import Connection

conn = Connection("0.0.0.0", 1234)

server = conn.get_server(10)

for client in server:
    print(client.recv())
    client.send("Hello")
    client.close()
