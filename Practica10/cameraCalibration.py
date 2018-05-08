# -*- coding: utf-8 -*-
"""
Created on Sun May  6 20:48:47 2018

@author: Alberto Herrera, Jesús Ramírez y Kassandra Ibarra
"""

import numpy as np
import cv2
import glob

def GetPoints(images):
    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*8,3), np.float32)
    objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    i = 0
    j = 0
    for fname in images:
        img = cv2.imread(fname)
        img = cv2.resize(img, None, fx=0.6, fy=0.6)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        i=i+1
        print(fname)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (8,6),None)
        
        # If found, add object points, image points (after refining them)
        if ret == True:
            j=j+1
            print(fname+" Impreso")
            objpoints.append(objp)
            
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)
            
            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (8,6), corners2,ret)
            cv2.imwrite('evidencia'+str(j)+'.jpg', img)
            #cv2.namedWindow('img', cv2.WINDOW_AUTOSIZE)
            #cv2.imshow('img',img)
            #cv2.waitKey(100)
    print("Se encontro el tablero en "+str(j)+" de "+str(i)+" imagenes")
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    return objpoints, imgpoints, ret, mtx, dist, rvecs, tvecs

def undistort(image, mtx, dist, no):
    img = cv2.imread(image)
    img = cv2.resize(img, None, fx=0.6, fy=0.6)
    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
 
    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite('calibresult '+str(no)+'.png',dst)
    return None

def Merror(objpoints, imgpoints, rvecs, tvecs, mtx, dist):
    tot_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        tot_error += error
    mean_error=tot_error/len(objpoints)    
    print ("total error: ", mean_error)
    return None

def pipeline():
    images = glob.glob('*.jpg')
    objpoints , imgpoints , ret, mtx, dist, rvecs, tvecs= GetPoints(images)
    cont=0
    for fname in images:
        cont=cont+1
        undistort(fname, mtx, dist, cont)
    Merror(objpoints, imgpoints, rvecs, tvecs, mtx, dist)
    return None

pipeline()
cv2.destroyAllWindows()
