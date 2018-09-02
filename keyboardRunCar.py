import time
import RPi.GPIO as GPIO
import sys
from pynput import keyboard
import csv
##from termios import tcflush, TCIOFLUSH, TCIFLUSH
from multiprocessing import Process
from datetime import datetime

GPIO.cleanup()

Forward = 17
Backward = 27
Left = 23
Right = 24
sleeptime = 0.25
speed = 0.5

mode=GPIO.getmode()

GPIO.setmode(GPIO.BCM)
GPIO.setup(Forward, GPIO.OUT)
GPIO.setup(Backward, GPIO.OUT)
GPIO.setup(Left, GPIO.OUT)
GPIO.setup(Right, GPIO.OUT)

def forward(x):
    GPIO.output(Forward, GPIO.HIGH)
    print("Moving Forward")
    time.sleep(x)
##    sys.stdout.flush();
##    tcflush(sys.stdin, TCIFLUSH)
    GPIO.output(Forward, GPIO.LOW)

def left(x):
    GPIO.output(Left, GPIO.HIGH)
    print("Moving Left")
    time.sleep(x)
##    sys.stdout.flush();
##    tcflush(sys.stdin, TCIFLUSH)
    GPIO.output(Left, GPIO.LOW)

def right(x):
    GPIO.output(Right, GPIO.HIGH)
    print("Moving Right")
    time.sleep(x)
##    sys.stdout.flush();
##    tcflush(sys.stdin, TCIFLUSH)
    GPIO.output(Right, GPIO.LOW)

def reverse(x):
    GPIO.output(Backward, GPIO.HIGH)
    print("Moving Backward")
    time.sleep(x)
##    sys.stdout.flush();
##    tcflush(sys.stdin, TCIFLUSH)
    GPIO.output(Backward, GPIO.LOW)
'''
def runInParallel(*fns):
    proc = []
    for fn in fns:
        global p
        p = Process(target=fn, args=(speed,))
        p.start()
        proc.append(p)
    #for p in proc:
     #   p.join()
    while not p.empty():
            p.get()
'''
def on_press(key):
    try:
        with open("controls.csv","a") as filename:
            fieldnames = ['images','controls']
            writer = csv.DictWriter(filename, fieldnames=fieldnames)
            if (key.char == 's'):
                print("speed")
                reverse(sleeptime)
            elif(key.char == 'w'):
                forward(sleeptime)
            elif(key.char == 'a'):
                left(sleeptime)
            elif(key.char == 'd'):
                right(sleeptime)
            elif(key.char == 'q'):
                '''runInParallel(forward,left)
                p.terminate()'''
                forward(sleeptime)
                left(sleeptime+0.10)
                '''p1 = Process(target=forward, args=(speed,))
                p1.start()
                p2 = Process(target=left, args=(speed,))
                p2.start()
                #p1.join()
                #p2.join()
                p1.get()
                p2.get()
                #p1.terminate()'''
            elif(key.char == 'e'):
                forward(sleeptime)
                right(sleeptime+0.10)
            timestamp = datetime.now()
            writer.writerows([{'images': str(timestamp), 'controls': key.char}])
            
    except AttributeError: \
        print('special key {0} pressed'.format(
                key))

def on_release(key):
    if (key == keyboard.Key.esc):
        return False

if __name__ =='__main__':
    try:
        with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
            listener.join()
    finally:
        print("closed")
        GPIO.cleanup()
