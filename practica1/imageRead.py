# import required libraries
import numpy as np
import cv2 
import argparse

# parse command line arguments
#crea un nuevo objeto argumentparser 
parser = argparse.ArgumentParser('Read, visualise and write image into disk')
#define que es lo que espera en la linea de comandos espera a que en la 
#linea de comando este estrito "-i" o "--in_image_name" y lo relaciona a lo 
#que se escribe depues de esta
parser.add_argument('-i', '--in_image_name', help='input image name', required=True)
#separa la entrada de "-i" y espera a un "-o" y lo que hay despues de este lo
#lo relaciona a -o
parser.add_argument('-o', '--out_image_name', help='output image name', required=True)
#convierte en objetos los strings de entrada  
args = vars(parser.parse_args())

# retrieve name of input and output images given as arguments from command line
#Los argumentos de la linea de comando son leidos y ya que estan relacionados
#desde su lectura de consola se leen de la siguente manera
img_in_name = args['in_image_name']
img_out_name= args['out_image_name']

# read in image from file
#se lee la imagen en su formato original
img_in = cv2.imread(img_in_name, cv2.IMREAD_COLOR) # alternatively, you can use cv2.IMREAD_GRAYSCALE

# verify that image exists
if img_in is None:
    print('ERROR: image ', img_in_name, 'could not be read')
    exit()

# convert input image from colour to grayscale
img_out = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)

# create a new window for image purposes
#se despliegan las imagenes tanto de entrada como de salida(aqui se crea la ventana donde se desplegara)
cv2.namedWindow("input image", cv2.WINDOW_NORMAL)  # alternatively, you can use cv2.WINDOW_NORMAL
cv2.namedWindow("output image", cv2.WINDOW_NORMAL) # that option will allow you for window resizing
#aqui se despliega la ventana con la imagen que se cargo al inicio
# visualise input and output image
cv2.imshow("input image", img_in)
cv2.imshow("output image", img_out)

# wait for the user to press a key 
key = cv2.waitKey(0)

# if user pressed 's', the grayscale image is write to disk
if key == ord("s"):
    cv2.imwrite(img_out_name, img_out)
    print('output image has been saved in current working directory')

# destroy windows to free memory  
cv2.destroyAllWindows()
print('windows have been closed properly')
exit()
