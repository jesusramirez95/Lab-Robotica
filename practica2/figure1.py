""" draw_shapes_on_image.py

    example:
    
    python3.5 draw_shapes_on_image.py -i vehicular_traffic.jpg -s rectangle -lp1 610 530 -lp2 780 700
    
    python3.5 draw_shapes_on_image.py -i vehicular_traffic.jpg --shape line --line_p1 100 100 --line_p2 900 100


    This script draws different geometric shapes on an image.
    
    This includes: 
        - lines
        - rectangles
        - circles
        - ellipses
        - polygons
        - text

    author: include your full name here
    date created: include that info here
    universidad de monterrey.
"""

# import required libraries
import numpy as np
import cv2 
import argparse


# ------------------------------------- #
# -------- UTILITY FUNCTIONS ---------- #
# ------------------------------------- #

# define function to draw a line
def draw_a_line(img, p1, p2, colour=(255,0,0), thickness=2, linetype=cv2.LINE_8):

    # draw a line on image
    cv2.line(img, p1, p2, colour, thickness, linetype)

    # return img 
    return img


# define function to draw a rectangle
def draw_a_rectangle(img, p1, p2, colour=(255,0,0), thickness=2, linetype=cv2.LINE_8):

    # draw a line on image
    cv2.rectangle(img, p1, p2, colour, thickness, linetype)

    # return img 
    return img

#define function to draw an ellipse
def draw_an_ellipse(img, p1, p2,angle = 0,start_ang=0,end_ang=360,color=(0,0,0),thickness=2):
	cv2.ellipse(img,p1,p2,angle,start_ang,end_ang,color,thickness)

	return img

#define function to draw a circle
def draw_a_circle(img, p1,radius,colour=(255,0,0),thickness=2):
	#draw a circle un image
	cv2.circle(img, p1,radius,colour,thickness)


	#return image with circle
	return img


#define polygon function
def draw_a_polygon(img, pts):
	cv2.polylines(img,[pts],True,(0,255,255))

	return img

#define textfunction
def display_text(img, ttext, p1, ttext_type=cv2.FONT_HERSHEY_SIMPLEX):
	cv2.putText(img, ttext,p1, ttext_type,1.5,(0,0,0) , 2, cv2.LINE_8)
	
	return img
# ------------------------------------- #
# ------------- MAIN CODE ------------- #
# ------------------------------------- #

# parse command line arguments
parser = argparse.ArgumentParser('Draw geometric shapes on an image')
parser.add_argument('-i', '--image', 
                    help='name of input image', type=str, required=True)
parser.add_argument('-s', '--shape', 
                    help='geometric shape to be drawn on the input image', type=str, required=True)
parser.add_argument('-lp1', '--line_p1', nargs='*', 
                    help='x,y coordinate of point 1', required=False)
parser.add_argument('-lp2', '--line_p2', nargs='*', 
                    help='x,y coordinate of point 2', required=False)
parser.add_argument('-rad', '--radius', type=int, nargs='+',
                    help='circle radius',required=False)
parser.add_argument('-cp', '--centerpoint', type=int, nargs='+',
                    help='centerpoint of the ellipse or circle',required=False)
parser.add_argument('-ax', '--axis', type=int, nargs='+',
                    help='size of the axis of the ellipse',required=False)
parser.add_argument('-lec','--lectura',nargs='*',
                    help='text you want to display',required= False)

parser.add_argument('-v', '--vertice', nargs='*',
                    help='vertices del poligono', required=False)

args = vars(parser.parse_args())


# retrieve name of input image given as argument from command line
img_in_name = args['image']

# read in image from disk
img_in = cv2.imread(img_in_name, cv2.IMREAD_COLOR) # alternatively, you can use cv2.IMREAD_GRAYSCALE

# verify that image exists
if img_in is None:
    print('ERROR: image ', img_in_name, 'could not be read')
    exit()

# retrieve geometric shape name
geometric_shape = args['shape']

# if geometric shape is a line
if (geometric_shape == 'line') or (geometric_shape == 'rectangle'):

    # retrieve line features
    line_p1 = args['line_p1']
    line_p2 = args['line_p2']

    # if '--line' is specified, but either '--line_p1' or 
    # '--line_p2' is missing, ask the user to enter 
    # the corresponding coordinate
    if (line_p1 is None) or (line_p2 is None):

        # ask user enter line coordinates
        print('ERROR: line coordinate missing')
        exit()            

    # otherwise
    else:

        # retrieve line coordinates
        line_p1 = tuple(list(map(int, line_p1)))
        line_p2 = tuple(list(map(int, line_p2)))
        # check that each coordinate is of length 2
        if len(line_p1) == 2 and len(line_p2)==2:        

            # if drawing a line
            if geometric_shape == 'line':
                      
                # call 'draw_a_line' 
                img_in = draw_a_line(img_in, line_p1, line_p2, (255,0,0), 2)
         
            # if drawing a rectangle
            elif geometric_shape == 'rectangle':
          
                # call 'draw_a_rectangle'
                img_in = draw_a_rectangle(img_in, line_p1, line_p2, (255, 0, 0), 2)
        # otherwise    
        else:
          
            # ask the user enter a valid line coordinate
            print('ERROR: both p1 and p2 coordinates must be of length 2')
            exit()            
###
if geometric_shape == 'circle': 
	radiusx = args['radius']
	cp = args['centerpoint']
	if (radiusx is None) or (cp is None):

        # ask user enter line coordinates
		print('ERROR one is missing')
		exit
 
	else:
		cp = tuple(list(map(int, cp)))
		radiusx = tuple(list(map(int, radiusx)))
		radius = radiusx[0]
		img_in = draw_a_circle(img_in, cp, radius, (255, 0, 0), 2)


if geometric_shape == 'ellipse':
	cp  = args['centerpoint']
	ax = args['axis']
	if (ax is None) or (cp is None):

		# ask user enter line coordinates
                print('ERROR one is missing')
                exit()
	else:
                cp  = tuple(list(map(int, cp)))
                ax = tuple(list(map(int, ax)))
                img_in = draw_an_ellipse(img_in, cp, ax, 0, 0, 360, (255, 0, 0), 2)

if geometric_shape == 'polygon':
	vertex=args['vertice']
	vertex_a=np.asarray(vertex)
	pts = np.array(vertex_a,np.int32)
	pts = pts.reshape(-1,1,2)
	img_in=draw_a_polygon(img_in,pts)
if geometric_shape == 'text':
	xlec = ""
	p1 = args['line_p1']
	p1 = tuple(list(map(int, p1)))
	lec = args['lectura']
	if(p1 is None) or  (lec is None):
		# ask user enter line coordinates
                                print('ERROR one is missing')
                                exit()
	else:
		for i in lec:
			xlec+=(i+" ")

		img_in = display_text(img_in,xlec, p1, ttext_type=cv2.FONT_HERSHEY_SIMPLEX)
	#print(xlec)

# create a new window for image purposes
cv2.namedWindow("input image", cv2.WINDOW_NORMAL)  # alternatively, you can use cv2.WINDOW_NORMAL

# visualise input and output image
cv2.imshow("input image", img_in)

# wait for the user to press a key 
key = cv2.waitKey(0)

# destroy windows to free memory  
cv2.destroyAllWindows()
print('windows have been closed properly')
exit()
