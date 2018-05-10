import socket
import smbus
import time

bus = smbus.SMBus(1)
s = socket.socket()
port = 12347
s.connect(('127.0.0.1', port))

try:
    while True:
        bus.write_byte_data(0x69, 0x3E, 0x01)
        bus.write_byte_data(0x69, 0x16, 0x18)
        data = bus.read_i2c_block_data(0x69, 0x1D, 6)

        xGyro = data[0] * 256 + data[1]
        if xGyro > 32767 :
                xGyro -= 65536

        yGyro = data[2] * 256 + data[3]
        if yGyro > 32767 :
                yGyro -= 65536

        zGyro = data[4] * 256 + data[5]
        if zGyro > 32767 :
                zGyro -= 65536
        
        s.sendall(str(xGyro).encode())
        print("sent x")
        time.sleep(1)
        
finally:
    s.close()
