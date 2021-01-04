#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 11:10:16 2021

@author: antoine
"""

from enum import Enum

from vecangle import *


import numpy as np
#toute grandeur est en centimetre
robot_radius = 5

erreur_angle = 5
erreur_distance = 2       

terain_width = 61

terrain_height = 122

centre_but_skynet = [31,122]

centre_but_humanity = [31,0]

demi_largeur_buts = 10

robots_par_equipe = 2

class Equipe(Enum):
    HUMANITY = 0
    SKYNET = 1

class RobotsIndex(Enum):
    HUMANITY_0 = 0
    HUMANITY_1 = 1
    SKYNET_0 = 2
    SKYNET_1 = 3
    
def xy_plane_vec_product(a,b):
    return a[0]*b[1]-a[1]*b[0]

def inner_angle(a,b):
    diff_angle = a - b
    return (diff_angle + 180) % 360 - 180

class RobotInfo:
    def __init__(self,position,direction_vec,robot_index):
        self.direction_vec = direction_vec
        self.robot_index = robot_index
        self.position = position
        self.direction = 0
        self.possession_balle = None
        self.vec_robot_balle = None
        self.angle_robot_balle = 0
        self.diff_angle = 0
        self.distance_balle = 0
        self.diff_distance_balle_robot = 0
        self.is_diff_angle_clockwise = None
        
    def calculate_situation(position_balle):
        self.direction = vecangle(direction_vec)
        self.vec_robot_balle = position_balle - self.position
        self.angle_robot_balle = get_angle(self.vec_robot_balle)
        self.diff_angle = inner_angle(angle_robot_balle,self.direction)
        self.distance_balle = np.linalg.norm(vec_robot_balle)
        self.diff_distance_balle_robot = abs( distance_balle - robot_radius)
        self.is_diff_angle_anticlockwise = \
            0 < xy_plane_vec_product(self.direction_vec, self.vec_robot_balle)
        self.possession_balle = self.diff_angle < erreur_angle and \
            self.diff_distance < erreur_distance
        
    def get_num(self):
        return self.robot_index%robots_par_equipe
    def get_equ(self):
        return Equipe(self.robot_index/robots_par_equipe)
    
class CommandeSkynet:
    def __init__(self,numero,angle,grandeur,kick):
        self.num = numero
        self.angle = angle
        self.grandeur = grandeur
        self.kick = kick
    def get_commande(self):
        return 0

class InfoVision:
    def __init__(self):
        self.robots_info = [None]*2*robots_par_equipe
        self.position_balle = None
    def calculate_situation():
        for robot in self.robots_info:
            robot.calculate_situation(self.position_balle)


def decision(info_vision):
    info_vision.calculate_situation()
    #debut de la prise de décision
    commandes = [None]*robots_par_equipe
    if(not [ rob.possession_balle for rob in info_vision.robots_info].any()):
        #personne n'a la balle, il faut donc aller la chercher
        for robot_skynet in [rob for rob in info_vision.robots_info if rob.get_equ() == Equipe.SKYNET]:
            angle = robot_skynet.diff_angle
            if(not robot_skynet.is_diff_angle_anticlockwise):
                angle = angle*(-1)
            commandes[robot_skynet.get_num()] = CommandeSkynet(robot_skynet.get_num(),
                                                               angle,
                                                               robot_skynet.diff_distance_balle_robot,
                                                               False )
        
        
    elif([rob.possession_balle for rob in info_vision.robots_info if rob.get_equ() == Equipe.SKYNET].any()):
        #L'Equipe Skynet a la balle, la balle doit se diriger vers le but
        for robot_skynet in [rob for rob in info_vision.robots_info if rob.get_equ() == Equipe.SKYNET]:
            if(not robot_skynet.possession_balle):
                commandes[robot_skynet.get_num()] = CommandeSkynet(robot_skynet.get_num(),
                                                               0,
                                                               0,
                                                               False )
            else:
                vec_robot_but = centre_but_humanity - robot_skynet.position
                
                
    else:
        #l'Equipe Humanity a la balle, mode defense
    return commandes
def get_info_vision():
    return InfoVision()




if __name__ == "__main__":
    new_info = get_info_vision()
    