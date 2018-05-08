import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Successfully Created")

port = 12345
s.bind(('', port))
print("Socket binded to {}".format(port))

s.listen(1)
print("Socket is listening")

while True:
    c, addr = s.accept()
    print("Got connection from {}".format(addr))

    c.send("Thank you for connecting")

    c.close()
    
