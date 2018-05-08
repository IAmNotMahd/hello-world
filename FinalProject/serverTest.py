import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket Successfully Created")
except socket.error as err:
    print("Socket Creation Failure with error {}".format(err))

port = 80

try:
    host_ip = socket.gethostbyname("www.google.com")
except socket.gaierror:
    print("there was an error resolving the host")
    sys.exit()

s.connect((host_ip, port))

print("Socket connected to google on port {}".format(host_ip))
