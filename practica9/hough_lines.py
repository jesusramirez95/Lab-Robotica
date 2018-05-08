"""
	line_detection_using_hough_transform.py

	author: andres.hernandezg@udem.edu
	universidad de monterrey
"""

# import required libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import math
# select a region of interest
def draw_lines(img,lines):
    # In case of error, don't draw the line
	draw_right = True
	draw_left = True
    
    # Find slopes of all lines
    # But only care about lines where abs(slope) > slope_threshold
	slope_threshold = 0.1
	slopes = []
	new_lines = []
	for line in lines:
		x1, y1, x2, y2 = line[0]  # line = [[x1, y1, x2, y2]]
        
        # Calculate slope
		if x2 - x1 == 0.:  # corner case, avoiding division by 0
			slope = 999.  # practically infinite slope
		else:
			slope = (y2 - y1) / (x2 - x1)
            
        # Filter lines based on slope
		if abs(slope) > slope_threshold:
			slopes.append(slope)
			new_lines.append(line)
        
	lines = new_lines
    
    # Split lines into right_lines and left_lines, representing the right and left lane lines
    # Right/left lane lines must have positive/negative slope, and be on the right/left half of the image
	right_lines = []
	left_lines = []
	for i, line in enumerate(lines):
		x1, y1, x2, y2 = line[0]
		img_x_center = img.shape[1] / 2  # x coordinate of center of image
		if slopes[i] > 0 and x1 > img_x_center and x2 > img_x_center:
			right_lines.append(line)
		elif slopes[i] < 0 and x1 < img_x_center and x2 < img_x_center:
			left_lines.append(line)
            
    # Run linear regression to find best fit line for right and left lane lines
    # Right lane lines
	right_lines_x = []
	right_lines_y = []
    
	for line in right_lines:
		x1, y1, x2, y2 = line[0]
        
		right_lines_x.append(x1)
		right_lines_x.append(x2)
        
		right_lines_y.append(y1)
		right_lines_y.append(y2)
        
	if len(right_lines_x) > 0:
		right_m, right_b = np.polyfit(right_lines_x, right_lines_y, 1)  # y = m*x + b
	else:
		right_m, right_b = 1, 1
		draw_right = False

    # Left lane lines
	left_lines_x = []
	left_lines_y = []
    
	for line in left_lines:
		x1, y1, x2, y2 = line[0]
        
		left_lines_x.append(x1)
		left_lines_x.append(x2)
        
		left_lines_y.append(y1)
		left_lines_y.append(y2)
        
	if len(left_lines_x) > 0:
		left_m, left_b = np.polyfit(left_lines_x, left_lines_y, 1)  # y = m*x + b
		global mAnt
		global bAnt
		mAnt,bAnt  = left_m,left_b
		
	else:
		left_m, left_b = mAnt,bAnt
		draw_left = True
    
    # Find 2 end points for right and left lines, used for drawing the line
    # y = m*x + b --> x = (y - b)/m
	y1 = 850
	y2 = 610
    
	right_x1 = (y1 - right_b) / right_m
	right_x2 = (y2 - right_b) / right_m
    
	left_x1 = (y1 - left_b) / left_m
	left_x2 = (y2 - left_b) / left_m
    
    # Convert calculated end points from float to int
	y1 = int(y1)
	y2 = int(y2)
	right_x1 = int(right_x1)
	right_x2 = int(right_x2)
	left_x1 = int(left_x1)
	left_x2 = int(left_x2)
    
    # Draw the right and left lines on image
	if draw_right:
		cv2.line(img, (right_x1, y1), (right_x2, y2), (0,0,255), 5)
	if draw_left:
		cv2.line(img, (left_x1, y1), (left_x2, y2), (0,0,255), 5)
	if draw_right and draw_left:
		overlay=img.copy()
		pts=np.array([[right_x1, y1],[right_x2, y2],[left_x2, y2],[left_x1, y1]],np.int32)
		pts=pts.reshape((-1,1,2))
		cv2.fillPoly(overlay,[pts],(0,255,0))
		opacity=.2
		cv2.addWeighted(overlay, opacity, img, 1 - opacity, 0, img)
		
		
	
	return(img)

def region_of_interest(img, vertices):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)

    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

# run line detection pipeline
def leer_vid():
	#1.- get frame from the video 
	cap = cv2.VideoCapture('highway_right_solid_white_line_short.mp4')
	while cap.isOpened():
		ret, frame = cap.read()
		if ret:
			lec  = run_pipeline(frame)
		else:
			if not lec: 
				print("No frame available")
				break
			elif lec:
				print("Video Finished")
				break
			
		# wait for the user to press 'q' to exit 
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
			
	cap.release()

# destroy windows to free memory
	cv2.destroyAllWindows()
	return(None)
def run_pipeline(img_colour):
      
    
	# 2. Convert from BGR to RGB then from RGB to greyscale
    img_colour_rgb = cv2.cvtColor(img_colour, cv2.COLOR_BGR2RGB)
    grey = cv2.cvtColor(img_colour_rgb, cv2.COLOR_RGB2GRAY)

	# 3.- Apply Gaussuan smoothing
    kernel_size = (7,7)
    blur_grey = cv2.GaussianBlur(grey, kernel_size, sigmaX=0, sigmaY=0)

	# 4.- Apply Canny edge detector
    low_threshold = 10
    high_threshold = 70
    edges = cv2.Canny(blur_grey, low_threshold, high_threshold, apertureSize=3)

	# 5.- Define a polygon-shape like region of interest
    img_shape = grey.shape

    # uncomment the following lines when extracting lines around the whole image
    '''
    img_size = img_shape
    bottom_left = (0, img_size[0])
    top_left = (0, 0)
    top_right = (img_size[1], 0)
    bottom_right = (img_size[1], img_size[0])
    '''

	# comment the following lines when extracting  lines around the whole image
    bottom_left = (410, 850)
    top_left = (820, 600)
    top_right = (1070, 600)
    bottom_right = (1530, 850)

    # create a vertices array that will be used for the roi
    vertices = np.array([[bottom_left,top_left, top_right, bottom_right]], dtype=np.int32)

	# 6.- Get a region of interest using the just created polygon. This will be
	#     used together with the Hough transform to obtain the estimated Hough lines
    masked_edges = region_of_interest(edges, vertices)

	# 7.- Apply Hough transform for lane lines detection
    rho = 1                       # distance resolution in pixels of the Hough grid
    theta = np.pi/180             # angular resolution in radians of the Hough grid
    threshold = 40                # minimum number of votes (intersections in Hough grid cell)
    min_line_len = 5              # minimum number of pixels making up a line
    max_line_gap = 450             # maximum gap in pixels between connectable line segments
    line_image = np.copy(img_colour)*0   # creating a blank to draw lines on
    hough_lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
##################3
    
    img_w_lines2 = draw_lines(img_colour_rgb.copy(),hough_lines)

##########33
	# 8.- Visualise input and output images
    img_colour_with_lines = img_colour_rgb.copy()
    if hough_lines is not None: 
        for line in hough_lines:
            for x1, y1, x2, y2 in line:
                cv2.line(img_colour_with_lines, (x1, y1), (x2, y2), (0,255,0), 3)

	# visualise input and output images
    #cv2.imshow("img colour rgb",img_colour_rgb)
    #cv2.imshow("blur grey",blur_grey)
    cv2.imshow("practica9",img_w_lines2)
    cv2.imshow("edges",edges)
    #cv2.imshow("img color w/lines", img_colour_with_lines)
    
    return True
def plt_vis():
    plt.figure(1)
    plt.imshow(img_colour_rgb)
    plt.axis('off')

    plt.figure(2)
    plt.imshow(blur_grey, cmap='gray')
    plt.axis('off')

    plt.figure(3)
    plt.imshow(edges, cmap='gray')
    plt.axis('off')

    plt.figure(4)
    plt.imshow(img_colour_with_lines)
    plt.axis('off')

    plt.show()
# fun pipeline
#img_name = 'highway_frame_0001.png'
#run_pipeline(img_name)
global lec 
lec = False
global mAnt
global bAnt
leer_vid()

