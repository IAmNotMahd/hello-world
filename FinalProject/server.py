import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Successfully Created")

port = 12347
s.bind(('', port))
print("Socket binded to {}".format(port))

s.listen(1)
print("Socket is listening")
try:
    while True:
        c, addr = s.accept()
        print("Got connection from {}".format(addr))
        while True:
            print(c.recv(1024).decode())
    c.close()
finally:
    c.close()
