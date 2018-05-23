
# import required libraries
import socket
import numpy as np
import serial
import cv2
import time
import RPi.GPIO as GPIO
import sys
import math
def init_camera(cam):
	cap = cv2.VideoCapture(0)
	
	if not cap.isOpened():
        	print ("Error camera not available")
        	exit()
	return(cap)
def wifi():
	
	TCP_IP = '192.168.0.130'
	TCP_PORT = 5005
	BUFFER_SIZE = 1024
	MESSAGE = "verde"
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(MESSAGE.encode())
	data = s.recv(BUFFER_SIZE)
	s.close()

	print ("received data:", data)
	
	return(None)
def leer_sens():
	ser.flushInput()
	ser.flushOutput()
	prom0=[]
	prom1=[]
	us=[]
	sens=[]
	for i in range(1,11):
		ser.write(b's')
		while(len(sens)<3):
			state = ser.readline()
			state=state.decode("utf-8") 
			state=state[0:len(state)-3]
			sens= state.split(" ",3)
		try:	
			prom0.append(int(sens[0]))
		except:
			prom0.append(0)
		try:	
			prom1.append(int(sens[1]))
		except:
			prom1.append(0)
		try:	
			us.append(int(sens[2]))
		except:
			us.append(0)
	#print(prom1)
	#print(prom0)
	#print(us)
	prom0.sort()
	prom1.sort()
	us.sort()
	return (prom0[6], prom1[6], us[6])
	

def NAV():
	
	global lastmov
	global busca
	global sec
	global cont
	prom0, prom1, us= leer_sens()
	#print(prom1)
	#print(prom0)
	#print(us)
	#print("out while")
	if sec==1:
		time.sleep(.001)
		cont=cont+1
		print(cont)
	else:
		cont=0
	if cont >=1000:
		busca ='base'
		sec=3
		cont=0
	circ=False
	mov, pix=leer_img(busca)
	while(((prom0<310 and prom1<310) and us > 11) or disp):
		if sec==1:
			time.sleep(.001)
			cont=cont+1
			print(cont)
		else :
			cont=0
		if cont >=1000:
			busca ='base'
			sec=3
			cont=0
		print("\n\n----Sensores----")
		print(prom0,prom1,us)
		print("\n\n")
		print(busca)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break 
		mov,pix= leer_img(busca)
		delay = 1.5*pix+.1*(pix+pix_A)/2
		#print(delay,'DELAY')
		if delay > 5:
			delay = 5
		if mov == 'izq' :
			cont=0
			p.ChangeDutyCycle(delay)
			p2.ChangeDutyCycle(delay)	
			left()
			time.sleep(.015)
			#forward()
			stop()	
			print('\n\nIZQ\n\n')
		elif mov == 'der':
			cont=0
			p.ChangeDutyCycle(delay)
			p2.ChangeDutyCycle(delay)	
			right()
			time.sleep(.015)
			stop()
			print('\n\nDER\n\n')
		elif mov == 'cent':
			cont=0
			p.ChangeDutyCycle(15)
			p2.ChangeDutyCycle(15)
			forward()
			time.sleep(.015)
			stop()
			print(prom0, prom1 ,us)
			if (((us < 30 and (sec ==2 or sec==3)) or (us <=16 and sec == 1))):
				print("Sensores dentro de sec")
				print(prom0, prom1, us)
				if sec ==1: #and us <= 11:
					forward()
					time.sleep(.6)
					stop()
					print 'in sec1'
					ser.write(b'1')
					busca='descarga'
					sec=2
				elif sec == 2:
					ser.write(b'2')
					sec=1
					busca='pieza'
				elif sec == 3 :
					exit()
					
					
				print("secuencia")
				print(sec)
				time.sleep(10)
				#send=False
				leer_img(busca)
						
		else :
			p.ChangeDutyCycle(15)
			p2.ChangeDutyCycle(15)
			forward()
					
		print("DELAY")
		print(delay)		
		#time.sleep(delay)
		pix_A=pix
		prom0,prom1, us=leer_sens()
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break 
		lastmov = mov;
#	backward()
#	left()
	stop()
	
	if ((prom0>=310 or prom1>=310 or us<11) and not disp):
		p2.ChangeDutyCycle(10)
		p.ChangeDutyCycle(10)
		leer_img()
		prom0,prom1,us=leer_sens()
		if disp:
			if prom0>prom1:
				right()
			else:
				left()
		if lastmov == 'izq':
			right()
		elif lastmov == 'der':
			left()
		elif lastmov == 'cent':  
			forward()
		else: 
			left()
		time.sleep(.02)
		stop()
		
	return(None)
	
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
        #blue_object_img = cv2.bitwise_and(frame, frame, mask=mask)

       # visualise segmented blue object
#        cv2.imshow('blue object', blue_object_img)
        return(mask)

def show_black(hsv):
	h_val_l = 0  #Red
	h_val_h = 0 #Red
	s_val_l = 0
	v_val_l = 0
	lower_red = np.array([h_val_l,s_val_l, v_val_l])
	upper_red = np.array([h_val_h, 255, 255])
        # threshold the hsv image so that only blue pixels are kept
	mask = cv2.inRange(hsv, lower_red, upper_red)
	 

        # AND-bitwise operation between the mask and input images
	#red_object_img = cv2.bitwise_and(frame, frame, mask=mask)
	
        # visualise segmented blue object
#	cv2.imshow('red object', red_object_img)
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
	#red_object_img = cv2.bitwise_and(frame, frame, mask=mask)
	
        # visualise segmented blue object
	#cv2.imshow('red object', mask)
	return(mask)

def show_yellow(hsv):
	h_val_l = 20  
	h_val_h = 40 
	s_val_l = 100
	v_val_l = 100
	lower_yellow = np.array([h_val_l,s_val_l, v_val_l])
	upper_yellow = np.array([h_val_h, 255, 255])
        # threshold the hsv image so that only blue pixels are kept
	mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # AND-bitwise operation between the mask and input images
	#yellow_object_img = cv2.bitwise_and(frame, frame, mask=mask)


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
#	cv2.imshow('violet', violet_object_img)
	return(mask)
def img_clear(mask,kernel):
	mask1 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	mask2 = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	mask = cv2.bitwise_and(mask1,mask1,mask = mask2)
	return(mask)
def boxing(frame,box):
	cv2.rectangle(frame,(115,85),(125,95),box,2)
	#cv2.circle(frame,(m.floor(x+w/2),m.floor(y+h/2)),5,(0,255,255),-1)
	return(frame)
def	ROI(framex,x,y,w,h):
	if x<5:
		x=5
	if y<5:
		y=5
	img_roi = framex[y-5:y+w+5,x-5:x+h+5]
	#show('ROI',img_roi)
	a,b,c=det_circ(img_roi,framex)
	#show("circulos",a)
	global disp
	disp= False
	if b>0 and c>0:
		disp = True
	else: 
		disp =False
	return(disp)	

def cnt(mask,framex):
	cX = 0
	cY = 0
	#ret, thresh = cv2.threshold(mask,127,255,0)
	framet, contours, hierarchy = cv2.findContours(mask,3,2)
	#cv2.imshow('framet', framet)
	num = len(contours)
	
	for cont in contours:
		
		rect = cv2.minAreaRect(cont)
		box = cv2.boxPoints(rect)
		#bo0x2 = box
		box = np.int0(box)
		(x, y, w, h) = cv2.boundingRect(cont)
		disp = ROI(mask,x,y,w,h)
		#print (disp)
		if disp:
			cv2.drawContours(framex, [box], 0, (0,255,200), 3)
			if h >10 and w >10:
			
			# compute the center of the contour
			#print(rect)
			#print(box2)	
			#print(x,y,w,h)
				M = cv2.moments(cont)
				if M["m00"]>0:
			
					cX = int(M["m10"] / M["m00"])
					cY = int(M["m01"] / M["m00"])
		
	# draw the contour and center of the shape on the image
		#cv2.drawContours(framex, [cont], -1, (0, 255, 0), 2)
					cv2.circle(framex, (cX, cY), 1, (255, 255, 255), -1)
					cv2.putText(framex, "center", (cX - 20, cY - 20),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
	
		
			
	if cX == 0 and cY == 0:
		return(framex, 0, 0)
	else:
		
		print("\n\n\n")
		print(cX,cY)
		print("\n\n\n")
		return(framex,cX,cY)

def leer_img(busca='pieza'):
	n=1
	while(n>0):
		#time1 = cv2.getTickCount()
		# grab current frame
		ret, frame = cap.read()
		frame = cv2.resize(frame, (240, 180)) 
		#cv2.circle(frame, (120,90), 1, (0, 255, 0), -1)
		# convert BGR to HSV
		#framex = cv2.medianBlur(frame,5)
		framex = frame
		#cv2.imshow('framex', framex)
		
		hsv = cv2.cvtColor(framex, cv2.COLOR_BGR2HSV)
		
	
			#----- Tune these parameters so that some colours ------ #
			# ----- objects can be detected                    ------ #
		if busca == 'base' :
			mask = show_blue(hsv)
			cap.set(11,.8)
			cap.set(10,1)
		elif busca== 'descarga':
			mask = show_yellow(hsv)
			cap.set(11,.5)
			cap.set(10,.3)
			cap.set(12,.5)	
		elif busca == 'pieza':
			mask = show_red(hsv)
			cap.set(11,.8)
			cap.set(10, 1)
			cap.set(12,1)
			#mask = mask + show_violet(hsv)
		# ------------------------------------------------------- #
		maskx = cv2.medianBlur(mask,7)
		kernel = np.ones((5,5),np.uint8)
		#frame = boxing(frame)
		#use morphology to improve the image
		#maskx = img_clear(mask,kernel)
		#use the mask to filter the image
		f_filter = cv2.bitwise_and(frame, frame, mask=maskx)
		#visualise current frame
	
		#visualise mask imagec
		cv2.imshow('mask', maskx)
		#Display the resulting frame
		#show('filter', f_filter)
		frame,cx,cy = cnt(maskx,frame)	
		#frame,cx,cy = det_circ(f_filter,frame)	
		mov='None'
		if cx>=115 and cx<=125 :
			box_color = (0,255,0)
			pix=0
			mov = 'cent'
		elif cx==0 and cy==0:
			box_color = (255,255,255)
			mov = 'None'
			pix=0
		else:
			if cx < 115:
				pix = 115-cx
				mov='der'
				#print('Izq')
			elif cx>125:
				pix = cx-125
				mov='izq'
				#print('Der')	
			else:
				mov = 'det'
				pix=0		
			box_color = (0,0,255)
		boxing(frame,box_color);
		#print(cx,cy)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break 
			
		cv2.imshow('frame',frame)
		n=n-1
	
		
	return(mov, pix)
		
def det_circ(cimg,frame):
	#cv2.imshow('prevcimg',cimg)
	cimg = cv2.GaussianBlur(cimg,(7	,7),0)
	#cimg = img_clear(cimg,kernel)
	#cimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	#cv2.imshow("cimg",cimg)
	kernel = np.ones((5,5),np.uint8)
	
	circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,1,10,param1=50,param2=25,minRadius=5,maxRadius=0)
	if circles is not None:
		circles = np.around(circles)
		circles = np.uint16(circles)

 	
		for i in circles[0,:]:
			# draw the outer circle
			cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
			# draw the center of the circle
			cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
			#print('\n circles')
			#print(circles)
			
		return(frame,i[0],i[1])
	else:
		return(frame,0,0) 		
	
def forward():

#     time.sleep(1)

     GPIO.output(RIGHTF, GPIO.HIGH)

     GPIO.output(RIGHTB, GPIO.LOW)

     GPIO.output(LEFTF, GPIO.HIGH)
	
     GPIO.output(LEFTB, GPIO.LOW)

     print("FORWARD")

def backward():

     time.sleep(0)

     GPIO.output(RIGHTF, GPIO.LOW)

     GPIO.output(RIGHTB, GPIO.HIGH)

     GPIO.output(LEFTF, GPIO.LOW)

     GPIO.output(LEFTB, GPIO.HIGH)

     print("BACKWARD")


def stop():

  

     GPIO.output(RIGHTF, GPIO.LOW)

     GPIO.output(RIGHTB, GPIO.LOW)

     GPIO.output(LEFTF, GPIO.LOW)

     GPIO.output(LEFTB, GPIO.LOW)
     
     print("STOP")

 

def right():
	 
     
 
     GPIO.output(RIGHTF, GPIO.HIGH)

     GPIO.output(RIGHTB, GPIO.LOW)

     GPIO.output(LEFTF, GPIO.LOW)

     GPIO.output(LEFTB, GPIO.HIGH)

     print("RIGHT")
     
     

def left():

     #time.sleep(0.05)

     GPIO.output(RIGHTF, GPIO.LOW)

     GPIO.output(RIGHTB, GPIO.HIGH)

     GPIO.output(LEFTF, GPIO.HIGH)

     GPIO.output(LEFTB, GPIO.LOW)

     print("LEFT")
   
def def_global():
	global sec
	sec=1
	global cont
	cont=0
	global busca
	busca='pieza'
	global lastmov
	lastmov, nada = leer_img()
	global disp
	disp = False
	print lastmov
	global pix_A
	pix_A=0
	return None

# When everything done, release the capture
   
# initialise a video capture object
RIGHTF = 29 # pin de entrada

RIGHTB = 33 # pin de salida

LEFTB = 35 # pin de entrada

LEFTF = 37 # pin de salida


#GPIO se enumeran segun su posicion no su #de GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT) #in1
GPIO.setup(32, GPIO.OUT) #EN1
GPIO.setup(40, GPIO.OUT) #EN2
GPIO.setup(33, GPIO.OUT) #in2
GPIO.setup(35, GPIO.OUT) #in3
GPIO.setup(37, GPIO.OUT) #in4

cap = init_camera(0)
n=0


ser = serial.Serial('/dev/ttyACM0',115200,timeout=5)
time.sleep(1)
p = GPIO.PWM(32, 10000)
p2 = GPIO.PWM(40, 10000)
p.start(20)
p2.start(20)

def_global()
while(1):
	#Sleer_img()
	NAV()
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break 


stop()
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows() 
ser.close()
sys.exit()

