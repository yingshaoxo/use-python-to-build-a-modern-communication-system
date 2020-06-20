# first of all import the socket library
import socket

# next create a socket object
s = socket.socket()
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything in a range of 0 to 65535
port = 12345

# bind the listener to Local Area Network
s.bind(('0.0.0.0', port))
print(f"socket binded to {port}")

# put the socket into listening mode
s.listen(5)
print("socket is listening")

# we run this server forever until we interrupt it or any error occurs
try:
    while True:
        # Establish connection with client.
        c, addr = s.accept()
        print('Got connection from', addr)

        # send a thank you message to the client.
        c.send(b'Thank you for connecting')
except Exception as e:
    print(e)
    # Close the connection with the client
    c.close()