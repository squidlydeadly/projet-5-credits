#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 19:42:10 2021

@author: antoine
"""

import matplotlib.pyplot as plt
import cv2
import numpy as np

class distortionRemover:
    def __init__(self,width,height,k1=-0.4e-5,k2=0,p1=0.0,p2=0.0):
        self.distCoeff = np.zeros((4,1),np.float64)
        self.distCoeff[0,0] = k1;
        self.distCoeff[1,0] = k2;
        self.distCoeff[2,0] = p1;
        self.distCoeff[3,0] = p2;

        self.cam = np.eye(3,dtype=np.float32)

        self.cam[0,2] = (width+1)/2.0  # define center x
        self.cam[1,2] = (height+1)/2.0 # define center y
        self.cam[0,0] = 2.8        # define focal length x
        self.cam[1,1] = 2.8        # define focal length y

    def __call__(self,img):
        return cv2.undistort(img,self.cam,self.distCoeff)

if __name__ == "__main__":
    src = cv2.imread('parcour_test.png')
    plt.imshow(src)

    width  = src.shape[1]
    height = src.shape[0]

    distortion_remover = distortionRemover(width,height)

    plt.imshow(distortion_remover.apply(src))
