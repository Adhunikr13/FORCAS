import time
import RPi.GPIO as GPIO
import sys

mode=GPIO.getmode()

GPIO.cleanup()

Forward=7
Backward=8
sleeptime=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(Forward, GPIO.OUT)
GPIO.setup(Backward, GPIO.OUT)

def forward(x):
    GPIO.output(Forward, GPIO.HIGH)
    print("Moving Forward")
    time.sleep(x)
    GPIO.output(Forward, GPIO.LOW)

def reverse(x):
    GPIO.output(Backward, GPIO.HIGH)
    print("Moving Backward")
    time.sleep(x)
    GPIO.output(Backward, GPIO.LOW)
try:
    while(1):
        forward(2)
        reverse(2)

except KeyboardInterrupt:
    print("nothing exception")

finally:
    GPIO.cleanup()
    sys.exit(1)