"""
	image_edge_detection_using_operators.py

	author: andres.hernandezg@udem.edu
	universidad de monterrey
"""

# import required libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2


# compute Sobel gradient
def compute_absolute_sobel_gradient(img, ax='x', ksize=3, threshold=(40,140)):

	# 1) check whether img is a colour or greyscale image
	if len(img.shape)>2:

		# convert from colour to greyscale image
		grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	else:
		# if greyscale grey=img
		grey = img

	# 2) take the derivate in 'ax' axis
	if ax.lower()=='x':

		# apply the Sobel operator along the x axis
		sobel_derivative = cv2.Sobel(grey, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=ksize, scale=1)

	if ax.lower()=='y':

		# apply the Sobel operator along the y axis
		sobel_derivative = cv2.Sobel(grey, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=ksize, scale=1)

	# 3) take the absolute value of the derivative
	sobel_absolute = np.absolute(sobel_derivative)

	# 4) scale to 8-bit (0-255), then convert to type = np.uint8
	sobel_scaled = np.uint8(255 * sobel_absolute / np.max(sobel_absolute))

	# 5) create a mask of 1's where threshold[0] < sobel_scaled < threshold[1]
	binary_output = np.zeros_like(sobel_scaled)
	threshold_min = threshold[0]
	threshold_max = threshold[1]
	binary_output[(sobel_scaled >= threshold_min) & (sobel_scaled <= threshold_max)] = 1

    # return binary_image with gradient being detected along 'ax' axis
	return sobel_derivative, binary_output


# combine x and y derivatives using AND operation
def combine_x_and_y_binary_derivatives(img_derivative_x, img_derivative_y, threshold=(40,120)):

	# verify that both image derivatives are the same size
	if img_derivative_x.shape != img_derivative_y.shape:
		print('ERROR [combine_x_and_y_binary_derivatives]: img_binary_x and img_binary_y images should be of same size')
		exit()

	# 1) take the absolute value of the derivative
	absolute_x = np.absolute(img_derivative_x)
	absolute_y = np.absolute(img_derivative_y)

	# 2) scale to 8-bit (0-255), then convert to type = np.uint8
	absolute_scaled_x = np.uint8(255 * absolute_x / np.max(absolute_x))
	absolute_scaled_y = np.uint8(255 * absolute_y / np.max(absolute_y))

	# 3) create a mask of 1's where threshold[0] < sobel_scaled < threshold[1]
	binary_combined_gradients = np.zeros_like(absolute_scaled_x)
	indx_x = (absolute_scaled_x >= threshold[0]) & (absolute_scaled_x <= threshold[1])
	indx_y = (absolute_scaled_y >= threshold[0]) & (absolute_scaled_y <= threshold[1])
	binary_combined_gradients[indx_x|indx_y] = 1

	# return combined binary x-and-y derivatives
	return binary_combined_gradients


# compute magnitude of x and y derivatives
def compute_magnitude_of_derivatives(img_derivative_x, img_derivative_y, ksize=3, threshold=(40,120)):

	# 1) calculate the magnitude
    gradient_magnitude = np.sqrt(np.power(img_derivative_x, 2) + np.power(img_derivative_y, 2))

    # 2) scale to 8-bit (0 - 255) and convert to type = np.uint8
    gradient_scaled = np.uint8(255 * gradient_magnitude / np.max(gradient_magnitude))

    # 3) create a binary mask where mag thresholds are met
    binary_magnitude = np.zeros_like(gradient_scaled)
    binary_magnitude[(gradient_scaled >= threshold[0]) & (gradient_scaled <= threshold[1])] = 1

    return binary_magnitude


# compute orientation of magnitude of x and y derivatives
def compute_direction(img_derivative_x, img_derivative_y, threshold=(0, np.pi/2)):

	# 1) take the absolute value of the x and y gradients
    gradient_magnitude_x = np.absolute(img_derivative_x)
    gradient_magnitude_y = np.absolute(img_derivative_y)

    # 2) calculate the gradient magnitude direction
    #gradient_direction = np.arctan2(gradient_magnitude_y, gradient_magnitude_x)
    gradient_direction = np.arctan2(img_derivative_y, img_derivative_x)

    # 3) reate a binary mask where direction thresholds are met
    binary_direction = np.zeros_like(gradient_direction)
    binary_direction[(gradient_direction >= threshold[0]) & (gradient_direction <= threshold[1])] = 1

    return binary_direction
def visualise_image(img, fig_number, title, flag_colour_conversion, conversion_colour, cmap):
	
	plt.figure(fig_number)
	if flag_colour_conversion:
		img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	if cmap == '':
		cmap = 'gray'
	plt.imshow(img,cmap)
	plt.title(title)
	plt.xticks([])
	plt.yticks([])
	#plt.show()	
	return None
def edge_detection(image,kernel1,kernel2,fig_number, title, flag_colour_conversion, conversion_colour, cmap):
	x_ima = cv2.filter2D(image,-1,kernel1)
	y_ima = cv2.filter2D(image,-1,kernel2)
	n_img = x_ima+y_ima
	visualise_image(x_ima,fig_number, title+' x', flag_colour_conversion, conversion_colour, cmap)
	visualise_image(y_ima,fig_number+1, title+' y', flag_colour_conversion, conversion_colour, cmap)
	visualise_image(n_img,fig_number+2, title+' combinado', flag_colour_conversion, conversion_colour, cmap)
	return None
# pipeline
def run_pipeline(img_name):

	# read image
	img = cv2.imread(img_name)

	# verify that image `img` exist
	if img is None:
		print('ERROR: image ', img_name, 'could not be read')
		exit()



	# compute sobel derivative along x axis
	img_derivative_x, img_binary_x = compute_absolute_sobel_gradient(img, ax='x', ksize=3, threshold=(40,140))

	# compute sobel derivative along y axis
	img_derivative_y, img_binary_y = compute_absolute_sobel_gradient(img, ax='y', ksize=3, threshold=(40,140))

	# combine x and y derivatives
	img_combined_derivatives = combine_x_and_y_binary_derivatives(img_derivative_x, img_derivative_y, threshold=(50,140))

	# compute magnitude of gradient
	img_magnitude_gradient = compute_magnitude_of_derivatives(img_derivative_x, img_derivative_y, ksize=3, threshold=(40,140))

	# compute direction of gradient
	thresh_min = 0
	thresh_max = 2
	img_direction_gradient = compute_direction(img_derivative_x, img_derivative_y, threshold=(np.radians(thresh_min), np.radians(thresh_max)))
	#Kernel Roberts
	roberts1 = np.array([[0,1],[-1,0]])
	roberts2 = np.array([[1,0],[0,-1]])
	#Kernel	prewwit
	Gx = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
	Gy = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
	#kernel Scharr
	scharrx = np.array([[3,0,-3],[10,0,-10],[3,0,-3]])
	scharry = np.array([[-3,-10,-3],[0,0,0],[3,10,3]])
	
	"""
	visualise_image(img, 1, 'Colour input image', True, 'BGR2RGB', '')
	visualise_image(img_derivative_x, 2, 'x derivative', False, '', 'gray')
	visualise_image(img_binary_x, 3, 'binary x derivative', False, '', 'gray')
	visualise_image(img_derivative_y, 4, 'y derivative', False, '', 'gray')
	visualise_image(img_binary_y, 5, 'binary y derivative', False, '', 'gray')
	visualise_image(img_combined_derivatives, 6, 'combined x and y derivative', False, '', 'gray')
	visualise_image(img_magnitude_gradient,7,'gradient magnitude',False,'','gray')
	"""
	edge_detection(img,roberts1,roberts2,8,'Roberts Kernel',False,'','gray')
	edge_detection(img,Gx,Gy,11,'Prewitt Kernel',False,'','gray')
	edge_detection(img,scharrx,scharry,14,'Scharr Kernel',False,'','gray')
	plt.show()



# uncomment the corresponding line to try a particular image
#img_name = 'opera_house_vivid_sydney.jpg'
img_name = 'sydney_harbour.jpg'
#img_name = 'vehicular_traffic.jpg'

# run pipeline
run_pipeline(img_name)
