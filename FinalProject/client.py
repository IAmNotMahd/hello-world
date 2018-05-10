import RPi.GPIO as GPIO
import socket
import smbus
import time

GPIO.setmode(GPIO.BCM)

leftTh = 5
leftIn = 6
leftMi = 13
rightTh = 19
rightIn = 26
rightMi = 21

GPIO.setup(leftTh, GPIO.IN)
GPIO.setup(leftIn, GPIO.IN)
GPIO.setup(leftMi, GPIO.IN)
GPIO.setup(rightTh, GPIO.IN)
GPIO.setup(rightIn, GPIO.IN)
GPIO.setup(rightMi, GPIO.IN)

#SOCKET + I2C STUFF
bus = smbus.SMBus(1)
s = socket.socket()
port = 12345
s.connect(('127.0.0.1', port))

try:
    while True:
        bus.write_byte_data(0x1D, 0x2A, 0x00)
        bus.write_byte_data(0x1D, 0x2A, 0x01)
        bus.write_byte_data(0x1D, 0x0E, 0x00)
        data = bus.read_i2c_block_data(0x1D, 0x00, 7)

        xAccl = (data[1] * 256 + data[2]) / 16
        if xAccl > 2047:
            xAccl -= 4096

        yAccl = (data[3] * 256 + data[4]) / 16
        if yAccl > 2047:
            yAccl -= 4096

        zAccl = (data[5] * 256 + data[6]) / 16
        if zAccl > 2047:
            zAccl -= 4096
        
        s.sendall(str(xAccl).encode())
        print("sent x")
        time.sleep(0.01)
        s.sendall(str(yAccl).encode())
        print("sent y")
        time.sleep(0.01)
        s.sendall(str(zAccl).encode())
        print("sent z")
        time.sleep(0.01)
        
        time.sleep(0.05)
        
finally:
    s.close()
