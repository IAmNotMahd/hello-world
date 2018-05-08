#Omni Motor Control
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

inA = 13
pwm = 19
inB = 26

GPIO.setup(inA, GPIO.OUT)
GPIO.setup(pwm, GPIO.OUT)
GPIO.setup(inB, GPIO.OUT)

p = GPIO.PWM(pwm, 300)
q = GPIO.PWM(inB, 300)
p.start(50)
q.start(50)
GPIO.output(inA, False)
#GPIO.output(inB, False)
try:
    while(1):
        p.ChangeDutyCycle(50)
        q.ChangeDutyCycle(50)

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
