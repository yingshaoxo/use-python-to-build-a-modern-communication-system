from multiprocessing import Process
import socket


def receive_and_print(c):
    while True:
        data = c.recv(1024)
        if not data:
            print('Bye')
            break
        print('\nmessage received: ', str(data.decode('utf-8')))

    c.close()


host = "0.0.0.0"
port = 12345

s = socket.socket()
s.bind((host, port))

s.listen(5)

try:
    while True:
        c, addr = s.accept()

        p = Process(target=receive_and_print, args=(c,))
        p.start()

        while True:
            text = input("\n")
            c.send(text.encode("utf-8"))
except Exception as e:
    print(e)

s.close()
