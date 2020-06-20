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


host = '127.0.0.1'
port = 12345

s = socket.socket()
s.connect((host, port))

p = Process(target=receive_and_print, args=(s,))
p.start()

message = "yingshaoxo is awesome"
s.send(message.encode('utf-8'))

try:
    while True:
        text = input("\n")
        s.send(text.encode('utf-8'))
except Exception as e:
    print(e)

s.close()
