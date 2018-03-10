"""
	change_colour_space.py
	
	add a description of your code here

	author: add your fullname 
	date created: add this info
	universidad de monterrey
"""

# import required libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2

# initialise a video capture object
cap = cv2.VideoCapture(0)

while(True):

	# grab current frame
	cf, frame = cap.read()

	# convert BGR to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


	# ----- Tune these parameters so that blue-colour  ------ #
	# ----- objects can be detected                    ------ #
	h_val_l = 80
	h_val_h = 120
	s_val_l = 100
	v_val_l = 100
	lower_blue = np.array([h_val_l,s_val_l, v_val_l])
	upper_blue = np.array([h_val_h, 255, 255])
	# ------------------------------------------------------- #


	# threshold the hsv image so that only blue pixels are kept
	mask = cv2.inRange(hsv, lower_blue, upper_blue)

	# AND-bitwise operation between the mask and input images
	blue_object_img = cv2.bitwise_and(frame, frame, mask=mask)

	# visualise current frame
	cv2.imshow('frame',frame)

	# visualise mask image
	cv2.imshow('mask', mask)

	# visualise segmented blue object
	cv2.imshow('blue object', blue_object_img)

	# Display the resulting frame
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()    
