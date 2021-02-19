#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 14:13:10 2021

@author: antoine
"""

import numpy as np

def get_angle(vec):
    """
    

    Parameters
    ----------
    vec : TYPE
        DESCRIPTION.

    Returns
    -------
    angle_deg : TYPE
        DESCRIPTION.

    """
    angle_deg= np.arctan(vec[1]/vec[0])/np.pi*180
    if(vec[0] <0):
        angle_deg += 180
    elif(vec[1] < 0):
        angle_deg += 360
    return angle_deg


def xy_plane_is_clockwise(a,b):
    # axb > 0 = anticlockwisce
    return not ((a[0]*b[1]-a[1]*b[0]) > 0)

def inner_angle(a,b):
    diff_angle = b-a
    inner_angl = (diff_angle + 180) % 360 - 180
    return (abs(inner_angl),inner_angl < 0)

class VecAngle:
    def __init__(self,vec):
        self.vec = vec
        self.angle = get_angle(vec)
    def get_norme(self):
        return np.linalg.norm(self.vec)

class VecAngleDiff:
    def __init__(self,a,b):
        self.angle,self.is_clockwise = inner_angle(a.angle, b.angle)
        
        
if __name__ == '__main__':
    print(inner_angle(200.3, 100.2))
    print(inner_angle(100.3, 200.2))
    print(inner_angle(360, 0))
    print(inner_angle(0, 360))