#NOTES: To work on opencv virtual environment, type:
#source ~/.profile
#workon cv
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import argparse
import imutils
import time
import cv2
#import ParaSaver

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
'''
#import from keras
#import keras related libraries
from keras.models import Sequential, Model
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.optimizers import SGD,RMSprop,Adam
from keras.utils import np_utils
from keras.preprocessing.image import img_to_array
from keras.models import load_model, model_from_json
'''
'''
#load trained network
json_file = open('RaspiNet/11_nonrand/model.json','r')
loaded_model_json = json_file.read()
json_file.close()
'''
#for testing purpose
from PIL import Image

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

def capture(type):
    rotate(80,1-type)
    time.sleep(3)
    rotate(80 , type)
    time.sleep(3)
'''
model = model_from_json(loaded_model_json)
model.load_weights('RaspiNet/11_nonrand/model.h5')
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#Categories
categories = ['Aedes', 'Culex', 'Empty']
expand_size = 25

'''

#initialize variable for video recording
#path = ('/demoVid.avi')
#fourcc = cv2.VideoWriter_fourcc(*'XVID')#cv.CV_FOURCC(*'XVID')
#out = cv2.VideoWriter(path, fourcc, 20.0, (640,480))

#ap = argparse.ArgumentParser()
#ap.add_argument("-p","--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
#ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
#ap.add_argument("-C", "--confidence", type=float, default=0.2, help="minimum probability to filter weak detections")
#args = vars(ap.parse_ags())

print("[INFO] starting video stream...")
camera = PiCamera()
camera.resolution = tuple([640, 480])
camera.framerate = 20
rawCapture = PiRGBArray(camera, size=tuple([640, 480]))

#Camera warm up time
time.sleep(5)


avg = None

imgcount = 0

#loop over the frames from the video stream
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = f.array
    #Write to Video file
    #out.write(frame)
    frame = imutils.resize(frame, width=500)
    
    #threshold the delta image
    #Orignial Values:
    #Area for recognizing
    x = 0
    y = 100
    w = 480
    h = 300
    frame = frame[y:y+h, x:x+w]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if avg is None:
        print("[INFO] starting background model...")
        avg = gray.copy().astype("float")
        rawCapture.truncate(0)
        continue
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)        

    cv2.imshow('thresh', thresh)
        
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        

    #turn stepper motor
    #backwards(delay, 50)
    #time.sleep(1)
    '''   
    for c in cnts:
        if cv2.contourArea(c) < 5000:
            (x,y,w,h)=cv2.boundingRect(c)
            x = max(0, x-expand_size)
            y = max(0, y-expand_size)
            x1 = min(499, x+w+expand_size)
            y1 = min(499, y+h+expand_size)
            cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
            detected = frame[y:y1, x:x1]
            im = cv2.resize(detected, (227,227))
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            img = im.astype("float") / 255.0
            #img = img_to_array(img)
            img = np.expand_dims(img, axis = 0)
            
            #if np.argmax(model.predict(img)) != 2:
            prob = model.predict(img)
            prob = prob[0][0:2]
            print(prob)
            index = np.argmax(prob)
            proba = prob[index]*100
            if proba > 10:
                if index == 0:
                    capture(1)
                    cv2.imwrite('img/A'+str(imgcount)+'.png', detected)
                    cv2.imwrite('img/A'+str(imgcount)+'_full.png', frame)
                    ParaSaver.SaveParameter('Aedes')
                else:
                    capture(0)
                    cv2.imwrite('img/C'+str(imgcount)+'.png', detected)
                    cv2.imwrite('img/C'+str(imgcount)+'_full.png', frame)
                    ParaSaver.SaveParameter('Culex')
                imgcount += 1
                break
   '''
    cv2.imshow("Video stream", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    rawCapture.truncate(0)


