from Connection import Connection

conn = Connection("localhost", 1234)

conn.connect()

print(conn.recv())

