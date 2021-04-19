#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 19:42:10 2021

@author: antoine
"""

import matplotlib.pyplot as plt
import cv2
import numpy as np

from config_loader import Configs

class Warp:
    """retire la distortion d'une image et ajuste l'angle"""
    @staticmethod
    def init_from_configs():
        return Warp(
        Configs.get()['CAMERA']['WIDTH'],
        Configs.get()['CAMERA']['HEIGHT'],
        Configs.get()['CALIBRATION']['K1'],
        Configs.get()['CALIBRATION']['K2'],
        Configs.get()['CALIBRATION']['P1'],
        Configs.get()['CALIBRATION']['P2'],
        int(Configs.get()['CALIBRATION']['CROP_TOP']),
        int(Configs.get()['CALIBRATION']['CROP_BOTTOM']),
        int(Configs.get()['CALIBRATION']['CROP_LEFT']),
        int(Configs.get()['CALIBRATION']['CROP_RIGHT']),
        Configs.get()['CALIBRATION']['THETA'])
    def __init__(self,w,h,k1,k2,p1,p2,crop_top,crop_bottom,crop_left,crop_right,theta):
        self.distortion_remover = distortionRemover(w,h,k1,k2,p1,p2)
        self.w = w
        self.h = h
        self.crop_top = crop_top
        self.crop_bottom = crop_bottom
        self.crop_left = crop_left
        self.crop_right = crop_right
        self.theta = theta
        self.M_rot = cv2.getRotationMatrix2D((self.w//2,self.h//2),self.theta,1.0)
    def __call__(self,img,draw=False):
        img = self.distortion_remover(img)
        img = cv2.warpAffine(img,self.M_rot,(self.w,self.h))
        new_h,new_w = img.shape[:2]
        if draw:
            cv2.rectangle(img,
            tuple([self.crop_left,self.crop_top]),
            tuple([new_w-self.crop_right,new_h-self.crop_bottom]),
            [255,255,255],
            1)
        else:
            img = img[self.crop_top:new_h-self.crop_bottom , self.crop_left:new_w-self.crop_right]
        return img

class distortionRemover:
    """retire la distortion d'une image"""
    def __init__(self,width,height,k1=-8.2e-6,k2=0,p1=0.0,p2=0.0):
        self.distCoeff = np.zeros((4,1),np.float64)
        self.distCoeff[0,0] = k1;
        self.distCoeff[1,0] = k2;
        self.distCoeff[2,0] = p1;
        self.distCoeff[3,0] = p2;

        self.cam = np.eye(3,dtype=np.float32)

        self.cam[0,2] = (width-1)/2.0  # define center x
        self.cam[1,2] = (height-1)/2.0 # define center y
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
