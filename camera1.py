import cv2
import numpy as np
import time
import datetime
import os
from time import gmtime, strftime
newdir = strftime("%Y-%m-%d", gmtime())

camera_port = 0
ramp_frames = 30

if not os.path.exists(newdir):
    os.makedirs(newdir)

camera = cv2.VideoCapture(camera_port)
i = 1
def get_image():
 retval, im = camera.read()
 return im
while (cv2.waitKey(1) != 27):
    for j in xrange(ramp_frames):
         temp = get_image()
    print("Taking image...")
    camera_capture = get_image()
    file = str(i) + ".jpg"
    file = newdir + "/" + file
    i =i+1
    cv2.imwrite(file, camera_capture)
    time.sleep(1.5)
    #if cv2.waitkey(1)  & OxFF == ord('q'):
     #   break

del(camera)
cv2.destroyAllWindows()
