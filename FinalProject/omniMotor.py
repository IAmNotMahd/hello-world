#Omni Motor Control
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

inA = 16
pwm = 20
inB = 21

GPIO.setup(inA, GPIO.OUT)
GPIO.setup(pwm, GPIO.OUT)
GPIO.setup(inB, GPIO.OUT)

p = GPIO.PWM(pwm, 100)
#q = GPIO.PWM(inA, 100)
p.start(50)
#q.start(50)
GPIO.output(inA, False)
GPIO.output(inB, True)

try:
    while(1):
        #GPIO.output(inB, False)
        #GPIO.output(inA, True)
        #p.ChangeDutyCycle(90)
        #q.ChangeDutyCycle(90)
        print("here")

finally:
    print("Cleaning Up")
    GPIO.cleanup()

    
'''from gpiozero import LED
from time import sleep
led = LED(26)
while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
    print("here")
'''
