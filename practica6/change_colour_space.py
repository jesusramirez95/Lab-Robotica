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

def init_camera(cam):
	cap = cv2.VideoCapture(cam)

	if not cap.isOpened():
        	print ("Error camera not available")
        	exit()
	return(cap)

def show_blue(hsv):
        h_val_l = 80  #Blue
        h_val_h = 120 #Blue      
        s_val_l = 100
        v_val_l = 100
        lower_blue = np.array([h_val_l,s_val_l, v_val_l])
        upper_blue = np.array([h_val_h, 255, 255])
        # threshold the hsv image so that only blue pixels are kept
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # AND-bitwise operation between the mask and input images
        blue_object_img = cv2.bitwise_and(frame, frame, mask=mask)

       # visualise segmented blue object
#        cv2.imshow('blue object', blue_object_img)
        return(mask)

def show_red(hsv):
	h_val_l = 160  #Red
	h_val_h = 200 #Red
	s_val_l = 100
	v_val_l = 100
	lower_red = np.array([h_val_l,s_val_l, v_val_l])
	upper_red = np.array([h_val_h, 255, 255])
        # threshold the hsv image so that only blue pixels are kept
	mask = cv2.inRange(hsv, lower_red, upper_red)

        # AND-bitwise operation between the mask and input images
	red_object_img = cv2.bitwise_and(frame, frame, mask=mask)

        # visualise segmented blue object
#	cv2.imshow('red object', red_object_img)
	return(mask)

def show_yellow(hsv):
	h_val_l = 10  
	h_val_h = 50 
	s_val_l = 100
	v_val_l = 100
	lower_yellow = np.array([h_val_l,s_val_l, v_val_l])
	upper_yellow = np.array([h_val_h, 255, 255])
        # threshold the hsv image so that only blue pixels are kept
	mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # AND-bitwise operation between the mask and input images
	yellow_object_img = cv2.bitwise_and(frame, frame, mask=mask)


        # visualise segmented blue object
#	cv2.imshow('yellow object', yellow_object_img)
	return(mask)

def show_violet(hsv):
	h_val_l = 130  
	h_val_h = 170 
	s_val_l = 50
	v_val_l = 50
	lower_violet = np.array([h_val_l,s_val_l, v_val_l])
	upper_violet = np.array([h_val_h, 255, 255])
        # threshold the hsv image so that only blue pixels are kept
	mask = cv2.inRange(hsv, lower_violet, upper_violet)

        # AND-bitwise operation between the mask and input images
	violet_object_img = cv2.bitwise_and(frame, frame, mask=mask)

        # visualise segmented violet object
#	cv2.imshow('violet object', violet_object_img)
	return(mask)

# initialise a video capture object
cap = init_camera(0)


while(True):

	# grab current frame
	cf, frame = cap.read()

	# convert BGR to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	

	# ----- Tune these parameters so that blue-colour  ------ #
	# ----- objects can be detected                    ------ #
	mask = show_red(hsv)
	mask = mask + show_blue(hsv)
	mask = mask + show_yellow(hsv)
	mask = mask + show_violet(hsv)
	# ------------------------------------------------------- #
	frame2 = cv2.bitwise_and(frame, frame, mask=mask)

	cv2.imshow('filter', frame2)
        # visualise current frame
	cv2.imshow('frame',frame)
	# visualise mask imagec
	cv2.imshow('mask', mask)
	# Display the resulting frame
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()    
