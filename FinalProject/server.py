import RPi.GPIO as GPIO
import socket
import smbus
import sys
import time

GPIO.setmode(GPIO.BCM)

inA1 = 16
pwm1 = 20
inB1 = 21
inA2 = 13
pwm2 = 19
inB2 = 26
inA3 = 17
pwm3 = 27
inB3 = 22
led1 = 18
led2 = 15
led3 = 14

GPIO.setup(inA1, GPIO.OUT)
GPIO.setup(pwm1, GPIO.OUT)
GPIO.setup(inB1, GPIO.OUT)
GPIO.setup(inA2, GPIO.OUT)
GPIO.setup(pwm2, GPIO.OUT)
GPIO.setup(inB2, GPIO.OUT)
GPIO.setup(inA3, GPIO.OUT)
GPIO.setup(pwm3, GPIO.OUT)
GPIO.setup(inB3, GPIO.OUT)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)

p1 = GPIO.PWM(pwm1, 100)
p2 = GPIO.PWM(pwm2, 100)
p3 = GPIO.PWM(pwm3, 100)
p1.start(50)
p2.start(50)
p3.start(50)

GPIO.output(inA1, False)
GPIO.output(inB1, False)
GPIO.output(inA2, False)
GPIO.output(inB2, False)
GPIO.output(inA3, False)
GPIO.output(inB3, False)
GPIO.output(led1, False)
GPIO.output(led2, False)
GPIO.output(led3, False)


bus = smbus.SMBus(1)

# SOCKET STUFF
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Successfully Created")

port = 12345
s.bind(('', port))
print("Socket binded to {}".format(port))

s.listen(1)
print("Socket is listening")

# STOP FUNCTION FOR ALL MOTORS
def stop1():
    GPIO.output(inA1, False)
    GPIO.output(inB1, False)
def stop2():
    GPIO.output(inA2, False)
    GPIO.output(inB2, False)
def stop3():
    GPIO.output(inA3, False)
    GPIO.output(inB3, False)

# CLOCKWISE FUNCTION FOR ALL MOTORS
def cw1():
    GPIO.output(inA1, True)
    GPIO.output(inB1, False)
def cw2():
    GPIO.output(inA2, True)
    GPIO.output(inB2, False)
def cw3():
    GPIO.output(inA3, True)
    GPIO.output(inB3, False)

# ANTICLOCKWISE FUNCTION FOR ALL MOTORS
def acw1():
    GPIO.output(inA1, False)
    GPIO.output(inB1, True)
def acw2():
    GPIO.output(inA2, False)
    GPIO.output(inB2, True)
def acw3():
    GPIO.output(inA3, False)
    GPIO.output(inB3, True)

# STOP 
def allStop():
    stop1()
    stop2()
    stop3()

# ROTATION CLOCKWISE
def clock():
    cw1()
    cw2()
    cw3()
    p2.ChangeDutyCycle(50)
    p3.ChangeDutyCycle(50)
    

# ROTATION ANTICLOCKWISE
def anticlock():
    acw1()
    acw2()
    acw3()
    p2.ChangeDutyCycle(50)
    p3.ChangeDutyCycle(50)
    
# FORWARD ALL DIRECTIONS
def forward():
    stop1()
    cw2()
    acw3()
    p2.ChangeDutyCycle(50)
    p3.ChangeDutyCycle(50)

# BACKWARD ALL DIRECTIONS
def backward():
    stop1()
    acw2()
    cw3()
    p2.ChangeDutyCycle(50)
    p3.ChangeDutyCycle(50)
    
# FOUR DIRECTION NOW BECAUSE PARKER
def right():
    cw1()
    acw2()
    acw3()
    p2.ChangeDutyCycle(17)
    p3.ChangeDutyCycle(17)
    
def left():
    acw1()
    cw2()
    cw3()
    p2.ChangeDutyCycle(17)
    p3.ChangeDutyCycle(17)


    
# ------------------------#
# MAIN LOOP #
#-------------------------#
try:
    c, addr = s.accept()
    print("Got connection from {}".format(addr))
        
    while True:
        '''bus.write_byte_data(0x69, 0x3E, 0x01)
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
        '''
        stringToSplit = c.recv(1024).decode()
        print("String received is {}".format(stringToSplit))
        split = stringToSplit.split("#")
        if (len(split) > 2):
          time.sleep(0.05)
          continue
        coords = split[0].split(",")
        xAccl = int(coords[0])
        yAccl = int(coords[1])
        zAccl = int(coords[2])
        lt = int(coords[3])
        li = int(coords[4])
        lm = int(coords[5])
        rt = int(coords[6])
        ri = int(coords[7])
        rm = int(coords[8])
        
        print("X Accl = {}".format(xAccl))
        print("Y Accl = {}".format(yAccl))
        print("Z Accl = {}".format(zAccl))
        print("Left Thumb = {}".format(lt))
        print("Left Index = {}".format(li))
        print("Left Middle = {}".format(lm))
        print("Right Thumb = {}".format(rt))
        print("Right Index = {}".format(ri))
        print("Right Middle = {}".format(rm))

        #--------------------#
        # CONTROL ALGORITHM  #
        #--------------------#
        if (lt == 1):
            GPIO.output(led1, True)
            GPIO.output(led2, False)
            GPIO.output(led3, False)
            # motor 1
            if (xAccl < -500):
                forward()
                if (rm == 1):
                    cw1()
                    p3.ChangeDutyCycle(30)
                elif (lm == 1):
                    acw1()
                    p2.ChangeDutyCycle(30)
            elif (xAccl > 475):
                backward()
                if (rm == 1):
                    acw1()
                    p3.ChangeDutyCycle(30)
                elif (lm == 1):
                    cw1()
                    p2.ChangeDutyCycle(30)
            elif (yAccl > 900):
                right()
            elif (yAccl < 500):
                left()
            elif (xAccl > -500) and (xAccl < 475) and (yAccl < 900) and (yAccl > 500):
                allStop()
            
        elif (rt == 1):
            GPIO.output(led1, False)
            GPIO.output(led2, True)
            GPIO.output(led3, False)
            if (li == 1):
                forward()
                if (rm == 1):
                    p3.ChangeDutyCycle(30)
                    cw1()
                elif (lm == 1):
                    acw1()
                    p2.ChangeDutyCycle(30)
            elif (ri == 1):
                backward()
                if (rm == 1):
                    acw1()
                    p3.ChangeDutyCycle(30)
                elif (lm == 1):
                    cw1()
                    p2.ChangeDutyCycle(30)
            elif (lm == 1):
                left()
            elif (rm == 1):
                right()
            else:
                allStop()
        
        elif (lt == 0):
            GPIO.output(led3, True)
            GPIO.output(led2, False)
            GPIO.output(led1, False)
            if (ri == 1):
                clock()
            elif (li == 1):
                anticlock()
            else:
                allStop()
                
        time.sleep(0.05)
        

finally:
    print("Cleaning up")
    c.close()
    GPIO.cleanup()
