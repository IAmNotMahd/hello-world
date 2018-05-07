#Omni Motor Control
'''import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
p = GPIO.PWM(26, 10000)
p.start(50)
while(1):
    p.ChangeDutyCycle(50)

'''
from gpiozero import LED
from time import sleep

led = LED(26)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
    print("here")
