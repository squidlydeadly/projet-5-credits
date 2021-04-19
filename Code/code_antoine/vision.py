#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 12:38:54 2020

@author: antoine
"""

import cv2

from system_classes import *

import time
import matplotlib.pyplot as plt
import numpy as np


from vecangle import *

def get_image():
    """renvoie l'image test"""
    return cv2.imread("parcour_test.png")


class Color:
    """couleur

    Parameters
    ----------
    name : string
        nom de la couleur
    BGR : type
        code en BGR de la couleur

    Attributes
    ----------
    name
    BGR

    """
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
    """renvoie la couleur par nom"""
    color_filtered = [color for color in colors if color.name==name]
    if len(color_filtered) == 1:
        return color_filtered[0]
    else:
        return None

class Square:
    """un carré à dessiner sur une image

    Parameters
    ----------
    top_left : array of float
        coin haut gauche du carré
    side_length : int
        longueur des coté du carré
    color : Color
        couleur du carré à dessiner
    line_width : int
        épaisseur de la ligne

    Attributes
    ----------
    bottom_right : array of float
        position du coin bas droit du carré
    color
    top_left
    line_width

    """
    def __init__(self,top_left,side_length,color,line_width=1):
        self.color = color
        self.top_left = tuple(top_left)
        self.bottom_right = tuple(top_left + np.array([side_length,side_length]))
        self.line_width = line_width
    def draw(self,img):
        """dessine le carré sur img"""
        cv2.rectangle(img,self.top_left,self.bottom_right,self.color.BGR,self.line_width)


def inv_gray_scale_color(image,color):
    """renvoie l'image en nuances de gris par rapport à color"""
    color_image= np.full_like(image,fill_value=color.BGR,dtype= np.uint8)
    #plt.imsave('color_image.jpg' ,color_image[:,:,::-1])
    diff_image= cv2.absdiff(image, color_image)
    #cv2.imwrite('diff_image.jpg', diff_image)
    gray_scale = cv2.cvtColor(diff_image, cv2.COLOR_BGR2GRAY)
    #plt.imsave('gray_scale.jpg',gray_scale,cmap='gray')
    inv_gray_scale = cv2.bitwise_not(gray_scale)
    return inv_gray_scale

from scipy.interpolate import interp1d

def get_position_top_left(inv_gray_scale,template,img_name= ''):
    """renvoie la position du coin haut gauche du template par convolution"""
    #res = cv2.matchTemplate(inv_gray_scale,template,cv2.TM_CCOEFF)
    res = cv2.filter2D(inv_gray_scale,cv2.CV_64F,template,anchor=(0,0),borderType=cv2.BORDER_CONSTANT)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    m = interp1d([min_val,max_val],[0,255])
    #cv2.imwrite(img_name,m(res))

    return np.array(max_loc)

def get_position(image,template,color):
    """renvoie la position du template de couleur color dans image """
    w, h = template.shape[:2]
    inv_gray_scale = inv_gray_scale_color(image,color)
    top_left = get_position_top_left(inv_gray_scale,template)
    centre_template = get_template_center(w,h)
    bottom_right = top_left + [w,h]
    square = Square(top_left,w,color)
    return top_left + centre_template,square

def get_template_center(w,h):
    """renvoie le centre du template"""
    return np.array([(w-1)/2,(h-1)/2])

def get_position_orientation(image, template,template_dot,mask,inner_radius,color):
    """renvoie la position et l'angle d'un robot"""
    w, h = template.shape[:2]
    centre_template = get_template_center(w,h)

    inv_gray_scale = inv_gray_scale_color(image, color)
    #plt.imsave('inv_gray_scale.jpg',inv_gray_scale,cmap='gray')

    top_left = get_position_top_left(inv_gray_scale,template,'convolve.jpg')
    position = top_left + centre_template

    bottom_right = top_left + [w,h]
    sliced_image = inv_gray_scale[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0]]
    #plt.imsave('sliced_image.jpg',sliced_image,cmap='gray')
    if(sliced_image.shape[:2] == (w,h)):
        masked_image = cv2.bitwise_and(sliced_image, sliced_image,mask=mask)
    else:
        masked_image = sliced_image
    #plt.imsave('masked_image.jpg',masked_image,cmap='gray')





    w_dot, h_dot = template_dot.shape[:2]
    centre_template_dot = get_template_center(w_dot,h_dot)

    top_left_rel_dot = get_position_top_left(masked_image,template_dot,'convolve_dot.jpg')
    top_left_dot = top_left_rel_dot + top_left

    bottom_right_dot = top_left_dot + [w_dot,h_dot]
    position_rel_dot = top_left_rel_dot + centre_template_dot
    vec =centre_template - position_rel_dot


    #M = cv2.moments(masked_image)
    #cx = M['m10']/M['m00']
    #cy = M['m01']/M['m00']
    #vec = centre_template - [cx,cy]
    #centre_masse = [cx,cy] + top_left
    squares = []
    squares.append(Square(top_left,w,color))
    ring_thickness = int(w/2 - inner_radius - 0.5)
    squares.append(Square(top_left + [ring_thickness,ring_thickness],inner_radius*2 +1,color))
    squares.append(Square(top_left_dot.astype(int),w_dot,color))

    return (position,vec,squares)

def get_info_vision(img,to_detects,template_robot,dot_template,ball_template,mask,inner_radius):
    """renvoie les positions et orientations des objets de to_detects"""
    vision_info = InfoVision()
    rectangles =[]
    for to_detect in to_detects:
        if type(to_detect) is Ball:
            #print('Ball')
            position,rect = get_position(img,
                                                ball_template,
                                                to_detect.color)
            #print(position)
            vision_info.position_balle = position
            rectangles.append(rect)


        else:
            position,direction_vec,rects= get_position_orientation(img,
                                                           template_robot,
                                                           dot_template,
                                                           mask,
                                                           inner_radius,
                                                           to_detect.color)
            vision_info.robots_info.append(RobotInfo(position,
                                                              direction_vec,
                                                              to_detect.robot_index))
            rectangles.extend(rects)
    #print('vision ' + str(time.perf_counter() - t_start))
    for rect in rectangles:
        rect.draw(img)
    return vision_info


if __name__ == "__main__":
    import template_generator
    from config_loader import *

    import wrap
    robot_rayon_e = 24
    robot_rayon_i = 16


    template_robot = template_generator.ring(robot_rayon_e,robot_rayon_i).astype(np.uint8)
    mask = template_generator.circle(robot_rayon_e,robot_rayon_i).astype(np.uint8)
    cv2.imwrite('template_robots.jpg',template_robot)

    ret,mask = cv2.threshold(mask,254,255,cv2.THRESH_BINARY)
    cv2.imwrite('mask.jpg',mask)


    dot_rayon = 4

    dot_template = template_generator.circle(dot_rayon,dot_rayon).astype(np.uint8)

    cv2.imwrite('template_dot.jpg',dot_template)

    to_detects = [Robot(color_by_name('magenta'),RobotIndex(Equipe.SKYNET,0))]#,Robot(color_by_name('vert'),RobotsIndex.HUMANITY_0)]
    vc = cv2.VideoCapture(0)

    woot,img = vc.read()

    cv2.imwrite('from_camera.jpg',img)
    warper = wrap.Warp.init_from_configs()

    img_input = warper(img)

    cv2.imwrite('img_input.jpg',img_input)


    vis_i = get_info_vision(img_input,to_detects,template_robot,dot_template,dot_template,mask,robot_rayon_i)
    vis_i.print()
    cv2.imwrite('output.jpg',img_input)
