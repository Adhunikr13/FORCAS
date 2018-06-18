import tensorflow as tf
import scipy.misc
import model
import cv2
from subprocess import call
import os
import cv2
import csv
import sys
import time

import numpy as np
import RPi.GPIO as GPIO
import time

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

Forward = 16
Backward = 17
Left = 13
Right = 12

sleeptime = 0.15
speed = 0.20

mode=GPIO.getmode()

GPIO.setmode(GPIO.BCM)
GPIO.setup(Forward, GPIO.OUT)
GPIO.setup(Backward, GPIO.OUT)
GPIO.setup(Left, GPIO.OUT)
GPIO.setup(Right, GPIO.OUT)

# Steer Funcitons
def forward(x):
    GPIO.output(Forward, GPIO.HIGH)
    print("Moving Forward")
    time.sleep(x)
    GPIO.output(Forward, GPIO.LOW)

def left(x):
    GPIO.output(Left, GPIO.HIGH)
    print("Moving Left")
    time.sleep(x)
    GPIO.output(Left, GPIO.LOW)

def right(x):
    GPIO.output(Right, GPIO.HIGH)
    print("Moving Right")
    time.sleep(x)
    GPIO.output(Right, GPIO.LOW)

sess = tf.InteractiveSession()
saver = tf.train.Saver()
saver.restore(sess, "save/model.ckpt")

cap = cv2.VideoCapture(0)
try:
    while(cv2.waitKey(10) != ord('q')):
        ret, frame = cap.read()
        image = scipy.misc.imresize(frame, [66, 200]) / 255.0
        predickt = model.y.eval(feed_dict={model.x: [image], model.keep_prob: 1.0})[0][0] * 180 / scipy.pi
        call("clear")
        if predickt > -14:
            a = "a"
        elif predickt < -28:
            a = "d"
        else:
            a = "w"
        if(a == 'w'):
            forward(sleeptime)
        elif(a == 'a'):
            forward(sleeptime)
            left(speed)
        elif(a == 'd'):
            forward(sleeptime)
            right(speed)
        print("Prediction" + str(a))
        cv2.imshow('frame', frame)

finally:
    print("closed")
    ##GPIO.output(16, 0)
    ##GPIO.output(13, 0)
    ##GPIO.output(12, 0)
    #GPIO.output(27, 0)
    #GPIO.input(6, 0)  
    GPIO.cleanup()
    cv2.destroyAllWindows()
    cap.release()
    del(cap)
