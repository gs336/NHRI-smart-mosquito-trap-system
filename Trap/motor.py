import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
clk= 5
cw = 6
#GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(clk, GPIO.OUT)
GPIO.setup(cw, GPIO.OUT)
GPIO.output(clk, 0)
GPIO.output(cw, 0)

def rotate(steps, direction):
    GPIO.output(cw, direction)
    for dist in range(steps):
        GPIO.output(clk, 1)
        delay = max((dist - steps/2)/25, 0)
        time.sleep(delay/1000.0 + 0.001)
        GPIO.output(clk, 0)
        time.sleep(delay/1000.0 + 0.001)
    GPIO.output(cw, 0)
    GPIO.output(clk, 0)
    
while True:
        rotate(100, 0)
        time.sleep(3)
        rotate(100, 1)
        time.sleep(3)
