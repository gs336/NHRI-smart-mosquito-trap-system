#NOTES: To work on opencv virtual environment, type:
#source ~/.profile
#workon cv

import numpy as np
import argparse
import imutils
import time
import cv2

#import keras related libraries
from keras.models import Sequential, Model
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.optimizers import SGD,RMSprop,Adam
from keras.utils import np_utils
from keras.preprocessing.image import img_to_array
from keras.models import load_model, model_from_json


#load trained network
json_file = open('Net/model.json','r')
loaded_model_json = json_file.read()
json_file.close()

#for testing purpose
from PIL import Image

model = model_from_json(loaded_model_json)
model.load_weights('Net/model.h5')
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#initialize variable for video recording
fileNames = ['Vids/Aedes/Test_Aedes_1']

#Categories
categories = ['Aedes', 'Culex', 'Empty']
expand_size = 25

for filename in fileNames:
    output = filename + '.avi'
    cap = cv2.VideoCapture(output)
    imagepath = 'Aedes/'
    imageCount = 0

    if (cap.isOpened()):
        print("Error opening video stream or file")

    #ap = argparse.ArgumentParser()
    #ap.add_argument("-p","--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
    #ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
    #ap.add_argument("-C", "--confidence", type=float, default=0.2, help="minimum probability to filter weak detections")
    #args = vars(ap.parse_ags())

    print("[INFO] starting video stream...")
    #camera = PiCamera()
    #camera.resolution = tuple([640, 480])
    #camera.framerate = 16
    #rawCapture = PiRGBArray(camera, size=tuple([640, 480]))

    #Camera warm up time
    #time.sleep(5)

    avg = None

    #loop over the frames from the video stream
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            #cv2.imshow('Frame', frame)
            #Write to Video file
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
            #threshold the delta image
            #Orignial Values:
            #thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)[1]
            #thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        
            for c in cnts:
                if 300 < cv2.contourArea(c) < 5000:
                    (x,y,w,h)=cv2.boundingRect(c)
                    x = max(0, x-expand_size)
                    y = max(0, y-expand_size)
                    x1 = min(499, x+w+expand_size)
                    y1 = min(499, y+h+expand_size)
                    detected = frame[y:y1, x:x1]
                    im = cv2.resize(detected, (227, 227))
                    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                    img = im.astype("float") / 255.0
                    #img = img_to_array(img)
                    img = np.expand_dims(img, axis = 0)
                    #print(model.predict(img))
                    if np.argmax(model.predict(img)) != 2:
                        prob = model.predict(img)
                        index = np.argmax(prob)
                        proba = prob[0][index]*100
                        #print(type(proba))
                        label = "{}: {:.2f}%".format(categories[index], proba)
                        cv2.putText(frame, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2) 
                        cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

                #if 400 < cv2.contourArea(c) < 5000:
                #    continue
                #(x,y,w,h)=cv2.boundingRect(c)
                #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow("Video stream", frame)
            key = cv2.waitKey(1) & 0xFF
            time.sleep(0.05)
            if key == ord("q"):
                break
            #rawCapture.truncate(0)
        else:
            break

#Release once job is finished
#out.release()
