import RPi.GPIO as GPIO
import time

pin1 = 23
pin2 = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin1, GPIO.IN)
GPIO.setup(pin2, GPIO.IN)
while True:
    left = GPIO.input(pin1)
    right = GPIO.input(pin2)
    print('left: {} right: {}'.format(left, right))
    time.sleep(0.1)
