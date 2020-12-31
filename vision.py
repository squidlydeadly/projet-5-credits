#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 12:38:54 2020

@author: antoine
"""

import cv2

import time 
import matplotlib.pyplot as plt
import numpy as np

def get_image():
    return cv2.imread("terrain_test.png")


def template_pos(img, template):
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_loc

magenta_BGR = [230,0,255]

if __name__ == "__main__":
    n = 1
    t_start = time.perf_counter()
    template = cv2.imread('symboleBlanc.png',cv2.IMREAD_GRAYSCALE)
    w, h = template.shape[:2]

    for i in range(n):
        image = get_image()
        color_image= np.full_like(image,fill_value=magenta_BGR,dtype= np.uint8)
        
        diff_image= cv2.absdiff(image, color_image)
        gray_scale = cv2.cvtColor(diff_image, cv2.COLOR_BGR2GRAY)
        inv_gray_scale = cv2.bitwise_not(gray_scale)
        res = cv2.matchTemplate(inv_gray_scale,template,cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        sliced_image = inv_gray_scale[top_left[1]:bottom_right[1]+1,top_left[0]:bottom_right[0]+1]
        M = cv2.moments(sliced_image)
        cx = M['m10']/M['m00']
        cy = M['m01']/M['m00']
        vec = [cx-(w+1)/2,(h+1)/2-cy] #inversion en y du au formatage des images en python
        angle_deg= np.arctan(vec[1]/vec[0])/np.pi*180
        if(vec[0] <0):
            angle_deg += 180
        elif(vec[1] < 0):
            angle_deg += 360
        print('centroid: ' + str(cx) + ', ' + str(cy))
        print('angle(deg): '+ str(angle_deg))
        cv2.rectangle(image,top_left, bottom_right, 255, 2)
        plt.imshow(image)
        plt.show()
        plt.imshow(inv_gray_scale)
        plt.show()
        plt.imshow(res)
        plt.show()
        plt.imshow(sliced_image)
        plt.show()
    t_stop = time.perf_counter()
    
    t_delta = t_stop - t_start
    print("temps par iteration= " + str(t_delta/n))