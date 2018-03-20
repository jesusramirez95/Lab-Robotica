"""
	convolve_image_with_kernel.py
	
	add a description of your code here

	author: add your fullname 
	date created: add this info
	universidad de monterrey
"""

# import required libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2

# read image
img_name = 'cavalo_motorizado.jpg'
img = cv2.imread(img_name)

# verify that image `img` exist
if img is None:
	print('ERROR: image ', img_name, 'could not be read')
	exit()

# define a kernel
#kernel = np.ones((5,5), np.float32)/25
#kernel = np.ones((13,13), np.float32)/169
#kernel = np.ones((21,21), np.float32)/441
kernel = np.ones((31,31), np.float32)/961
dst_correlation = cv2.filter2D(img, -1, kernel)

# rotate kernel
kernel_rotated = cv2.flip(kernel, -1)
dst_convolution = cv2.filter2D(img, -1, kernel_rotated)

# plot input and convolved images
plt.figure(1)
plt.imshow(img)
plt.title('Input image')
plt.xticks([]) 
plt.yticks([])

plt.figure(2)
plt.imshow(dst_correlation)
plt.title('Output image using a 5x5 averaging filter (correlation)')
plt.xticks([]) 
plt.yticks([])

plt.figure(3)
plt.imshow(dst_convolution)
plt.title('Output image using a 5x5 averaging filter (convolution)')
plt.xticks([]) 
plt.yticks([])

plt.show()
