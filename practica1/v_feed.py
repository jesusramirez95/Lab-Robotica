# import required libraries
import numpy as np
import cv2 as cv

# create a VideoCapture object
#cap = cv.VideoCapture(0)
cap2 = cv.VideoCapture(1)
# main loop
while(True):

    # capture new frame
    #ret, frame = cap.read()
    ret1,framex= cap2.read()
    #cap2.set(15,-8.0)
    cap2.set(11,.0)
    #cap2.set(12,-.15)
    #cap2.set(13,-.1)
    # convert from colour to grayscale image
 #   gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # visualise image
   # cv.imshow('frame', frame)
    cv.imshow('frame2', framex)
    # wait for the user to press 'q' to close the window
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# release VideoCapture object
#cap.release()
cap2.release()
# destroy windows to free memory
cv.destroyAllWindows()
