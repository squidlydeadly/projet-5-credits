#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 14:13:10 2021

@author: antoine
"""

import numpy as np

def get_angle(vec):
    angle_deg= np.arctan(vec[1]/vec[0])/np.pi*180
    if(vec[0] <0):
        angle_deg += 180
    elif(vec[1] < 0):
        angle_deg += 360
    return angle_deg
