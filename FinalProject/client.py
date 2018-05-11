import RPi.GPIO as GPIO
import socket
import smbus
import time

GPIO.setmode(GPIO.BCM)

prm = 5
plm = 6
pri = 13
pli = 19
plt = 26
prt = 21

GPIO.setup(plt, GPIO.IN)
GPIO.setup(pli, GPIO.IN)
GPIO.setup(plm, GPIO.IN)
GPIO.setup(prt, GPIO.IN)
GPIO.setup(pri, GPIO.IN)
GPIO.setup(prm, GPIO.IN)

#SOCKET + I2C STUFF
bus = smbus.SMBus(1)
s = socket.socket()
port = 12345
s.connect(('10.9.221.184', port))

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
            
        lt = GPIO.input(plt)
        li = GPIO.input(pli)
        lm = GPIO.input(plm)
        rt = GPIO.input(prt)
        ri = GPIO.input(pri)
        rm = GPIO.input(prm)

        print("X Accl = {}".format(xAccl))
        print("Y Accl = {}".format(yAccl))
        print("Z Accl = {}".format(zAccl))
        print("Left Thumb = {}".format(lt))
        print("Left Index = {}".format(li))
        print("Left Middle = {}".format(lm))
        print("Right Thumb = {}".format(rt))
        print("Right Index = {}".format(ri))
        print("Right Middle = {}".format(rm))
        stringToSend = str(xAccl) + "," + str(yAccl) + "," + str(zAccl) + "," + \
                       str(lt) + "," + str(li) + "," + str(lm) + "," + \
                       str(rt) + "," + str(ri) + "," + str(rm) + "#"
        print("String Sent is: {}".format(stringToSend))
        s.send(stringToSend.encode())
        print("sent all")
        time.sleep(0.05)
        
finally:
    print("Cleaning up")
    s.close()
    GPIO.cleanup()
