"""
	get_image_stats.py
	
	add a description of your code here

	author: add your fullname 
	date created: add this info
	universidad de monterrey
"""

# import required libraries
import numpy as numpy
import matplotlib.pyplot as plt
import cv2

# print image statistics
def print_image_statistics(img, head_string, iscolour):

	"""
		include docstring here
	"""
	# add your code below this line
	# get image size
	img_size = img.shape

# print image size
	print(head_string)
	print('colour image size: ', img_size)
	
# retrieve image width resolution
	print('image width resolution: ', img_size[0])
	
# retrieve image height resolution
	print('image height resolution: ', img_size[1])
# retrieve number of channels
	if iscolour:
		print('number of channels: ', img_size[2])

# minimum pixel value in image
	print('minimum intensity value: ', img.min())

# minimum pixel value in image
	print('max intensity value: ', img.max())

# maximum intensity value in image
	print('meam intensity value: ', img_colour.mean())

# print type of image
	print('type of image: ', img_colour.dtype)

	return None


# visualise image
def visualise_image(img, fig_number, fig_title, iscolour):

	"""
		include docstring here
	"""
	# add your code below this line
	# visualise colour image
	plt.figure(fig_number)
	if iscolour:
		plt.imshow(img)
	else:
		plt.imshow(img, cmap='gray')
	plt.title(fig_title)
	plt.xlabel('x-resolution')
	plt.ylabel('y-resolution')

	return None
# read image
image_name = 'vehicular_traffic.jpg'
img_colour = cv2.imread(image_name, cv2.IMREAD_COLOR)

# verify that image exists
if img_colour is None:
	print('ERROR: image ', image_name, 'could not be read')
	exit()

# convert the input colour image into a grayscale image
img_greyscale = cv2.cvtColor(img_colour, cv2.COLOR_BGR2GRAY)
#convert to RGB
img_colour = cv2.cvtColor(img_colour, cv2.COLOR_BGR2RGB)
# print colour image stats and visualise it
print_image_statistics(img_colour, 'COLOUR IMAGE STATS:',1)
visualise_image(img_colour, 1, 'INPUT IMAGE: COLOUR', 1)

# print greyscale image stats and visualise it
print_image_statistics(img_greyscale, 'GREYSCALE IMAGE STATS:',0)
visualise_image(img_greyscale, 2, 'OUTPUT IMAGE: GREYSCALE', 0)

# visualise figures
plt.show()
