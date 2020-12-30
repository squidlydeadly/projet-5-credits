#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 12:38:54 2020

@author: antoine
"""

import cv2

import time 
import matplotlib.pyplot as plt

def get_image():
    return cv2.imread("terrain_test.png")



if __name__ == "__main__":
    n = 100
    t_start = time.perf_counter()
    template = cv2.imread('symbole1.png')
    w, h = template.shape[:2]

    for i in range(n):
        image = get_image()
        res = cv2.matchTemplate(image,template,cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(image,top_left, bottom_right, 255, 2)
        #plt.imshow(res)
        #plt.show()
        #plt.imshow(image)
        #plt.show()
    t_stop = time.perf_counter()
    
    t_delta = t_stop - t_start
    print("temps par iteration= " + str(t_delta/n))