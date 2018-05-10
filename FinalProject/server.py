import RPi.GPIO as GPIO
import socket
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

GPIO.setup(inA1, GPIO.OUT)
GPIO.setup(pwm1, GPIO.OUT)
GPIO.setup(inB1, GPIO.OUT)
GPIO.setup(inA2, GPIO.OUT)
GPIO.setup(pwm2, GPIO.OUT)
GPIO.setup(inB2, GPIO.OUT)
GPIO.setup(inA3, GPIO.OUT)
GPIO.setup(pwm3, GPIO.OUT)
GPIO.setup(inB3, GPIO.OUT)

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
    GPIO.output(inA1, False)
    GPIO.output(inB1, True)
def cw2():
    GPIO.output(inA2, False)
    GPIO.output(inB2, True)
def cw3():
    GPIO.output(inA3, False)
    GPIO.output(inB3, True)

# ANTICLOCKWISE FUNCTION FOR ALL MOTORS
def acw1():
    GPIO.output(inA1, True)
    GPIO.output(inB1, False)
def acw2():
    GPIO.output(inA2, True)
    GPIO.output(inB2, False)
def acw3():
    GPIO.output(inA3, True)
    GPIO.output(inB3, False)

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

# ROTATION ANTICLOCKWISE
def anticlock():
    acw1()
    acw2()
    acw3()
    
# FORWARD ALL DIRECTIONS
def forward1():
    stop1()
    acw2()
    cw3()
def forward2():
    stop2()
    cw1()
    acw3()
def forward3():
    stop3()
    acw1()
    cw2()

# BACKWARD ALL DIRECTIONS
def backward1():
    stop1()
    cw2()
    acw3()
def backward2():
    stop2()
    acw1()
    cw3()
def backward3():
    stop3()
    cw1()
    acw2()

    
# ------------------------#
#-------------------------#
try:
    c, addr = s.accept()
    print("Got connection from {}".format(addr))
        
    while True:
        x = c.recv(1024).decode()
        print("X Accl = {}".format(x))
        time.sleep(0.01)
        y = c.recv(1024).decode()
        print("Y Accl = {}".format(y))
        time.sleep(0.01)
        z = c.recv(1024).decode()
        print("Z Accl = {}".format(z))
        time.sleep(0.01)
        print("*********************")
        
        time.sleep(0.05)

finally:
    print("Cleaning up")
    c.close()
    GPIO.cleanup()
