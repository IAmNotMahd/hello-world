import socket

s = socket.socket()
port = 12345
s.connect(('10.8.79.79', port))
print(s.recv(1024))
s.close()
