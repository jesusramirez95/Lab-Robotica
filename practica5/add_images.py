"""

	add_images.py

	En este código hacemos la unión de dos imagenes, esta se da a nivel pixel, por lo que lo que hacemos es sumar los valores de las propiedades de los pixeles de dos imagenes.
	Probaremos dos métodos, el primero numpy hace la suma y el resultado puede ser el residuo de 255, mientras que opencv no entrega un resultado despues  valor maximo
	author: add your fullname 
	date created: add this info
	universidad de monterrey

"""

# import required libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2

# specify names of image files
image_name_1 = 'salinas_beach_quijo_asado.jpg'
image_name_2 = 'salinas_beach_bird.jpg'

# load image 1
img_1 = cv2.imread(image_name_1, cv2.IMREAD_COLOR)

# verify that img_1 exists
if img_1 is None:
	print('ERROR: image ', image_name_1, 'could not be read')
	exit()

# convert BGR to RGB
img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB)

# load image 2
img_2 = cv2.imread(image_name_2, cv2.IMREAD_COLOR)

# verify that img_1 exists
if img_2 is None:
	print('ERROR: image ', image_name_2, 'could not be read')
	exit()

# convert BGR to RGB
img_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2RGB)

# add images using cv2.add()
img_cv2 = cv2.add(img_1, img_2)

# add images using numpy library
img_np = np.uint8(img_1) + np.uint8(img_2)

# visualise images
plt.figure(1)
plt.imshow(img_1)
plt.title('Image 1')

plt.figure(2)
plt.imshow(img_2)
plt.title('Image 2')

plt.figure(3)
plt.imshow(img_cv2)
plt.title('Sum of Image 1 and Image 2 using cv2.add()')

plt.figure(4)
plt.imshow(img_np)
plt.title('Sum of Image 1 and Image 2 using numpy')

# display figures
plt.show()
