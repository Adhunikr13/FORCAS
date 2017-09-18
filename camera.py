import cv2
import numpy as np
import time

camera_port = 0
ramp_frames = 30

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
    i =i+1
    cv2.imwrite(file, camera_capture)
    time.sleep(1.5)
    #if cv2.waitkey(1)  & OxFF == ord('q'):
     #   break

del(camera)
cv2.destroyAllWindows()