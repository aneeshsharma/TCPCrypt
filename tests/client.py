from Connection import Connection

conn = Connection("localhost", 1234)

conn.connect()

message = input(">>> ")
conn.send(message)
print(conn.recv())
