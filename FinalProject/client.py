import RPi.GPIO as GPIO
import socket
import smbus
import time

GPIO.setmode(GPIO.BCM)

lt = 5
li = 6
lm = 13
rt = 19
ri = 26
rm = 21

GPIO.setup(lt, GPIO.IN)
GPIO.setup(li, GPIO.IN)
GPIO.setup(lm, GPIO.IN)
GPIO.setup(rt, GPIO.IN)
GPIO.setup(ri, GPIO.IN)
GPIO.setup(rm, GPIO.IN)

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
        
        lt = GPIO.input(lt)
        li = GPIO.input(li)
        lm = GPIO.input(lm)
        rt = GPIO.input(rt)
        ri = GPIO.input(rI)
        rm = GPIO.input(rM)
        
        stringToSend = str(xAccl) + "," + str(yAccl) + "," + str(zAccl) +
                       str(lt) + "," + str(li) + "," + str(lm) + "," +
                       str(rt) + "," + str(ri) + "," + str(rm) + "," + "#"
        s.send(stringToSend.encode())
        print("sent all")
        time.sleep(0.05)
        
finally:
    print("Cleaning up")
    s.close()
    GPIO.cleanup()
