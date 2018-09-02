from __future__ import print_function
import time
import RPi.GPIO as GPIO
import csv
from datetime import datetime
# -----------------------
# Define some functions
# -----------------------
def measure():
  # This function measures a distance
  GPIO.output(GPIO_TRIGGER, True)
  # Wait 10us
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()
  
  while GPIO.input(GPIO_ECHO)==0:
    start = time.time()

  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * speedSound)/2

  return distance

def measure_average():
  # This function takes 3 measurements and
  # returns the average.

  distance1=measure()
  time.sleep(0.05)
  distance2=measure()
  time.sleep(0.05)
  distance3=measure()
  distance = distance1 + distance2 + distance3
  distance = distance / 3
  return distance

# -----------------------
# Main Script
# -----------------------
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 25
GPIO_ECHO    = 18

#Speed of sound in cm/s at temperature
temperature = 40
speedSound = 34300 + (0.6*temperature)

print("Ultrasonic Measurement")
print("Speed of sound is",speedSound/100,"m/s at ",temperature,"deg")

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# Allow module to settle
time.sleep(0.5)

try:
  while True:
      with open("distance.csv","a") as filename:
          fieldnames = ['timestamp','distance']
          writer = csv.DictWriter(filename, fieldnames=fieldnames)
          distance = measure_average()
          print("Distance : {0:5.1f}".format(distance))
          distance = round(distance,2)#print(distance)
          timestamp = datetime.now()
          writer.writerows([{'timestamp': str(timestamp), 'distance': distance}])
          time.sleep(0.1)

except KeyboardInterrupt:
  # User pressed CTRL-C
  # Reset GPIO settings
  GPIO.cleanup()
