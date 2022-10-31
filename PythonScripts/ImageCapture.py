#################################################################
#####     IMAGE CAPTURE | CAPTURE DATA FOR TIMELAPSE        #####
#####     AUTHOR: GARRETT PETER BARDINI (GPB)               #####
#####     CREATE_DATE: 2022/10/14                           #####
#####     LAST_MODIFIED: 2022/10/27                         #####
#################################################################
import os
import time
import cv2
import datetime
workingdir = (r"/mnt/usb0/TimelapseImages")

def capture_image():
    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    filename = timestamp + 'ImageCapture.jpg'
    cam = cv2.VideoCapture(0)
    ret, image = cam.read()
    # image = cv2.resize(image, (720, 720))
    cv2.imwrite(os.path.join(workingdir,filename), image)
    cam.release()
    cv2.destroyAllWindows()

dt = datetime.datetime.now()
secondsToMidnight = (((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second))
time.sleep(secondsToMidnight)
while True:
    capture_image() # Do I Need Retrys? 
    time.sleep(24*60*60)# Wait till tomorrow 