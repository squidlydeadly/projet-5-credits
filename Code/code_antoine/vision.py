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
    return cv2.imread("images/terrain_test.png")


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
          Color('jaune', [0,255,255]),
          Color('rouge', [0,0,255]),
          Color('orange',[0,165,255]),
          Color('blanc',[255,255,255]),
          Color('noir',[0,0,0])]
def color_by_name(name):
    color_filtered = [color for color in colors if color.name==name]
    if len(color_filtered) == 1:
        return color_filtered[0]
    else:
        return None


def inv_gray_scale_color(image,color):
    color_image= np.full_like(image,fill_value=color.BGR,dtype= np.uint8)
    #plt.imsave('color_image.jpg' ,color_image[:,:,::-1])
    diff_image= cv2.absdiff(image, color_image)
    #plt.imsave('diff_image.jpg', diff_image[:,:,::-1])
    gray_scale = cv2.cvtColor(diff_image, cv2.COLOR_BGR2GRAY)
    #plt.imsave('gray_scale.jpg',gray_scale,cmap='gray')
    inv_gray_scale = cv2.bitwise_not(gray_scale)
    return inv_gray_scale

def get_position_top_left(inv_gray_scale,template):

    res = cv2.matchTemplate(inv_gray_scale,template,cv2.TM_CCOEFF)
    #plt.imsave('convolve.jpg',res,cmap='gray')
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return np.array(max_loc)

def get_position(image,template,color):
    w, h = template.shape[:2]
    inv_gray_scale = inv_gray_scale_color(image,color)
    top_left = get_position_top_left(inv_gray_scale,template)
    centre_template = get_template_center(w,h)
    bottom_right = top_left + [w,h]
    rect_dict = {'top_left':tuple(top_left),'bottom_right':tuple(bottom_right),'bgr':color.BGR}
    return top_left + centre_template,rect_dict

def get_template_center(w,h):
    return np.array([(w-1)/2,(h-1)/2])

def get_position_orientation(image, template,mask, color):
    w, h = template.shape[:2]
    centre_template = get_template_center(w,h)

    inv_gray_scale = inv_gray_scale_color(image, color)
    #plt.imsave('inv_gray_scale.jpg',inv_gray_scale,cmap='gray')

    top_left = get_position_top_left(inv_gray_scale,template)

    position = top_left + centre_template

    bottom_right = top_left + [w,h]
    sliced_image = inv_gray_scale[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0]]
    #plt.imsave('sliced_image.jpg',sliced_image,cmap='gray')
    masked_image = cv2.bitwise_and(sliced_image, sliced_image,mask=mask)
    #plt.imsave('masked_image.jpg',masked_image,cmap='gray')
    M = cv2.moments(masked_image)
    cx = M['m10']/M['m00']
    cy = M['m01']/M['m00']
    vec = centre_template - [cx,cy]
    mass_center = position + vec
    rect_dict = {'top_left':tuple(top_left),'bottom_right':tuple(bottom_right),'bgr':color.BGR}
    line_dict = {'start':tuple(position.astype(int)),'end':tuple(mass_center.astype(int)),'bgr':color.BGR}

    return (position,vec,rect_dict,line_dict)


if __name__ == "__main__":
    n = 1
    t_start = time.perf_counter()
    template = cv2.imread('images/symboleBlanc.png',cv2.IMREAD_GRAYSCALE)
    mask = cv2.imread('images/mask.png',0)

    for i in range(n):
        image = get_image()
        for color in colors[0:1]:
            position,orientation,img_out =  get_position_orientation(image, template,mask, color)
            print(color.name + str(position) + ' ' + str(orientation))
    t_stop = time.perf_counter()
    b,g,r = cv2.split(image)       # get b,g,r
    plt.imshow(img_out[:,:,::-1])
    plt.imsave('img_out.jpg',img_out)
    t_delta = t_stop - t_start
    print("temps par iteration= " + str(t_delta/(n*len(colors))))
