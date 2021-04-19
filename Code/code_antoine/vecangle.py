#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 14:13:10 2021

@author: antoine
"""

import numpy as np

def get_angle(vec):
    """renvoie l'angle d'un vecteur par rapport aux abscisses"""
    angle_deg= np.arctan(vec[1]/vec[0])/np.pi*180
    if(vec[0] <0):
        angle_deg += 180
    elif(vec[1] < 0):
        angle_deg += 360
    return angle_deg


def xy_plane_is_clockwise(a,b):
    """détermine si le vecteur a vers le vecteur b est horaire"""
    # axb > 0 = anticlockwisce
    return not ((a[0]*b[1]-a[1]*b[0]) > 0)

def inner_angle(a,b):
    """angle entre les vecteurs a et b"""
    diff_angle = b-a
    inner_angl = (diff_angle + 180) % 360 - 180
    return (abs(inner_angl),inner_angl < 0)

class VecAngle:
    """Short summary.

    Parameters
    ----------
    vec : array of float
        vecteur

    Attributes
    ----------
    angle : int
        angle du vecteur
    vec

    """
    def __init__(self,vec):
        self.vec = vec
        self.angle = get_angle(vec)
    def get_norme(self):
        return np.linalg.norm(self.vec)
    def orth_projection_norme(self,vecangle):
        return abs(np.dot(self.vec,vecangle.vec))/vecangle.get_norme()

class VecAngleDiff:
    """difference entre deux VecAngle

    Parameters
    ----------
    a : VecAngle
        vecteur a
    b : VecAngle
        vecteur b

    Attributes
    ----------
    angle : int
        angle entre les deux vecteurs
    is_clockwise : bool
        si le sens de a à b est horaire

    """
    def __init__(self,a,b):
        self.angle,self.is_clockwise = inner_angle(a.angle, b.angle)


if __name__ == '__main__':
    print(inner_angle(200.3, 100.2))
    print(inner_angle(100.3, 200.2))
    print(inner_angle(360, 0))
    print(inner_angle(0, 360))
