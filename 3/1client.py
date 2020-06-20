# Import socket module
import socket

# Create a socket object
s = socket.socket()

# Define the port on which you want to connect, it should be the same as server's bound port
port = 12345

try:
    # connect to the server
    s.connect(('127.0.0.1', port))

    # receive data from the server
    print(s.recv(1024))
except Exception as e:
    print(e)
    # close the connection
    s.close()