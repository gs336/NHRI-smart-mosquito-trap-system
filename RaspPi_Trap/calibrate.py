import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

pins = [23, 18]
#pin1 = 23
#pin2 = 18
clk= 5
cw = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(pins[0], GPIO.IN)
GPIO.setup(pins[1], GPIO.IN)
GPIO.setup(clk, GPIO.OUT)
GPIO.setup(cw, GPIO.OUT)
GPIO.output(clk, 0)
GPIO.output(cw, 0)

def calibrate(direction):
	GPIO.output(cw, direction)
	delay = 0.001
	#Step 1: First loop of rotation
	while GPIO.input(pins[0-direction])==0:
		GPIO.output(clk, 1)
		time.sleep(delay)
		GPIO.output(clk, 0)
		time.sleep(delay)
	#Step 2: go back
	GPIO.output(cw, 1-direction)
	time.sleep(0.25)
	for i in range(30):
		GPIO.output(clk, 1)
		time.sleep(delay)
		GPIO.output(clk, 0)
		time.sleep(delay)	
	#Step 3: Second loop with slower speed
	GPIO.output(cw, direction)
	time.sleep(0.25)
	delay = 0.003
	#Step 4: First loop of rotation
	while GPIO.input(pins[0-direction])==0:
		GPIO.output(clk, 1)
		time.sleep(delay)
		GPIO.output(clk, 0)
		time.sleep(delay)
	#Step 5: Count in between
	stepCount = 0
	while GPIO.input(pins[1-direction])==0:
		GPIO.output(clk, 1)
		time.sleep(delay)
		GPIO.output(clk, 0)
		time.sleep(delay)
		if GPIO.input(pins[0-direction])==0:
			stepCount+=1
	#Step 6: rotate back
	print(stepCount)
	time.sleep(0.25)
	GPIO.output(cw, 1-direction)
	for i in range(stepCount//2):
		GPIO.output(clk, 1)
		time.sleep(delay)
		GPIO.output(clk, 0)
		time.sleep(delay)

calibrate(1)
time.sleep(3)
calibrate(0)
