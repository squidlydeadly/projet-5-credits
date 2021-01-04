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


from vecangle import *

def get_image():
    return cv2.imread("terrain_test.png")


def template_pos(img, template):
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_loc

class Color:
    def __init__(self,name,BGR):
        self.name = name
        self.BGR = BGR
        
colors = [Color('magenta', [255,0,255]),
          Color('vert', [0,255,0]),
          Color('bleu', [255,0,0]),
          Color('azur', [255,255,0]),
          Color('jaune', [0,255,255])]
def inv_gray_scale_color(image,color):
    color_image= np.full_like(image,fill_value=color.BGR,dtype= np.uint8)
            
    diff_image= cv2.absdiff(image, color_image)
    gray_scale = cv2.cvtColor(diff_image, cv2.COLOR_BGR2GRAY)
    inv_gray_scale = cv2.bitwise_not(gray_scale)
    return inv_gray_scale

def get_position_top_left(inv_gray_scale,template):
    
    res = cv2.matchTemplate(inv_gray_scale,template,cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return np.array(max_loc)

def get_position(image,template,color):
    w, h = template.shape[:2]
    inv_gray_scale = inv_gray_scale_color(image,color)
    top_left = get_position_top_left(inv_gray_scale,template)
    centre_template = get_template_center(w,h)
    return top_left + centre_template

def get_template_center(w,h):
    return np.array([(w-1)/2,(h-1)/2])

def get_position_orientation(image, template, color):
    w, h = template.shape[:2]
    centre_template = get_template_center(w,h)
    
    inv_gray_scale = inv_gray_scale_color(image, color)
    
    top_left = get_position_top_left(inv_gray_scale,template)
    
    position = top_left + centre_template 
    
    bottom_right = top_left + [w,h]
    sliced_image = inv_gray_scale[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0]]
    M = cv2.moments(sliced_image)
    cx = M['m10']/M['m00']
    cy = M['m01']/M['m00']
    vec = centre_template - [cx,cy]   #inversion en y du au formatage des images en python
    angle_deg= get_angle(vec)
    return (position,angle_deg)
    

if __name__ == "__main__":
    n = 1
    t_start = time.perf_counter()
    template = cv2.imread('symboleBlanc.png',cv2.IMREAD_GRAYSCALE)

    for i in range(n):
        image = get_image()
        for color in colors:
            position,orientation =  get_position_orientation(image, template, color)
            print(color.name + str(position) + ' ' + str(orientation))
    t_stop = time.perf_counter()
    b,g,r = cv2.split(image)       # get b,g,r
    rgb_img = cv2.merge([r,g,b])     # switch it to rgb
    plt.imshow(rgb_img)
    t_delta = t_stop - t_start
    print("temps par iteration= " + str(t_delta/(n*len(colors))))