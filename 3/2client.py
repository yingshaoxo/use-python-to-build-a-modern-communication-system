import socket
import threading


def receive_and_print(c):
    while True:
        # data received from server
        data = c.recv(1024)
        if not data:
            print('Bye')
            break
        print('\nmessage received: ', str(data.decode('utf-8')))
        print("\n")

    # connection closed
    c.close()


def Main():
    host = '127.0.0.1'
    port = 12345

    s = socket.socket()
    s.connect((host, port))

    t = threading.Thread(target=receive_and_print, args=(s,))
    t.start()

    # greeting
    message = "yingshaoxo is awesome"
    s.send(message.encode('utf-8'))

    try:
        while True:
            # message sent to server
            text = input("\n")
            s.send(text.encode('utf-8'))
    except Exception as e:
        print(e)

    # close the connection
    s.close()


if __name__ == '__main__':
    Main()
