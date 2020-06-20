import socket
import threading

# thread function
def receive_and_print(c):
    while True:
        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')
            break
        print('\nmessage received: ', str(data.decode('utf-8')))

    # connection closed
    c.close()


def Main():
    host = "0.0.0.0"
    port = 12345

    s = socket.socket()
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    try:
        while True:
            # establish connection with client
            c, addr = s.accept()

            # Start a new thread
            t = threading.Thread(target=receive_and_print, args=(c,))
            t.start()

            while True:
                text = input("\n")
                c.send(text.encode("utf-8"))
    except Exception as e:
        print(e)
    # close the connection
    s.close()


if __name__ == '__main__':
    Main()
