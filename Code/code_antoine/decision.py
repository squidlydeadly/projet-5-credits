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
    
class State(Enum):
    SKYNET_POSSESSION = 0
    HUMANITY_POSSESSION = 1
    NO_ONE_POSSESSION = 2
    
def skynet_goal(robot_skynet):
    command = None
    if(not robot_skynet.possession_balle):
        command = CommandeSkynet(robot_skynet.get_num())
    else:
        vecangle_robot_but = VecAngle(centre_but_humanity - robot_skynet.position)
        diff_vecangle_but_direction = VecAngleDiff(robot_skynet.vecangle_direction,vecangle_robot_but)
        if(diff_vecangle_but_direction.angle < erreur_angle):
            commande = CommandeSkynet(robot_skynet.get_num(),
                                      kick=True)
        else:
            commande = CommandeSkynet(robot_skynet.get_num(),
                                      angle=diff_vecangle_but_direction.angle,
                                      is_clockwise=diff_vecangle_but_direction.is_clockwise)
        return command

def skynet_defence(robot_skynet):
    vecangle_robot_but = VecAngle(centre_but_skynet - robot_skynet.position)
    command = None
    if(vecangle_robot_but.get_norme() > demi_largeur_buts):
        #se rendre dans la zone des buts a reculon
        vecangle_direction_inv = VecAngle(-1*robot_skynet.direction.vec)
        diff_vecangle_but_direction_inv = VecAngleDiff(vecangle_direction_inv.angle,vecangle_robot_but)
        
        commande = CommandeSkynet(robot_skynet.get_num(),
                                  angle=diff_vecangle_but_direction_inv.angle,
                                  is_clockwise=diff_vecangle_but_direction_inv.is_clockwise,
                                  grandeur=vecangle_robot_but.get_norme(),
                                  is_foward=False)
    else:
        #orienter vers la balle
        commande = CommandeSkynet(robot_skynet.get_num(),
                                  angle = robot_skynet.diff_vecangle.angle,
                                  is_clockwise=robot_skynet.diff_vecangle.is_clockwise)
    return command
def skynet_fetch(robot_skynet):
    
    return CommandeSkynet(robot_skynet.get_num(),
                          angle=robot_skynet.diff_vecangle.angle,
                          is_clockwise=robot_skynet.diff_vecangle.is_clockwise,
                          grandeur=robot_skynet.get_distance_balle_robot())

StateMachineLike = {State.SKYNET_POSSESSION: skynet_goal, #L'Equipe Skynet a la balle, la balle doit se diriger vers le but
                    State.HUMANITY_POSSESSION: skynet_defence, #l'Equipe Humanity a la balle, mode defense
                    State.NO_ONE_POSSESSION: skynet_fetch} #personne n'a la balle, il faut donc aller la chercher


class RobotInfo:
    def __init__(self,position,direction_vec,robot_index):
        self.vecangle_direction = VecAngle(direction_vec)
        self.robot_index = robot_index
        self.position = position
        self.possession_balle = None
        self.vecangle_robot_balle = None
        self.diff_vecangle = None
        
    def calculate_situation(self,position_balle):
        self.vecangle_robot_balle = VecAngle(position_balle - self.position)
        self.diff_vecangle = VecAngleDiff(self.vecangle_direction,self.vecangle_robot_balle)
        self.possession_balle = self.diff_vecangle.angle < erreur_angle and \
            self.get_distance_balle_robot() < erreur_distance
    def get_distance_balle_robot(self):
        return self.vecangle_robot_balle.get_norme() - robot_radius
        
    def get_num(self):
        return self.robot_index.value%robots_par_equipe
    def get_equ(self):
        return Equipe(int(self.robot_index.value/robots_par_equipe))
    
class CommandIntensity:
    def __init__(self,clockwise_intensity=0,foward_intensity=0):
        self.clockwise_intensity = clockwise_intensity
        self.foward_intensity = foward_intensity
    
class CommandeSkynet:

    
    def __init__(self,numero,angle=0,is_clockwise=True,grandeur=0,is_foward=True,kick=False):
        self.num = numero
        self.angle = angle
        self.is_clockwise = is_clockwise
        self.grandeur = grandeur
        self.is_foward = is_foward
        self.kick = kick
    def get_command_intesity(self):
        angle_max = 90
        grandeur_max = 10
        intensity_max = 512
        angle_intensity = np.round((min(angle_max,self.angle)*intensity_max)/angle_max)
        grandeur_intensity = np.round((min(grandeur_max,self.grandeur)*intensity_max)/grandeur_max)
        return CommandIntensity(angle_intensity if self.is_clockwise else -angle_intensity,
                                grandeur_intensity if self.is_foward else -grandeur_intensity )

class InfoVision:
    def __init__(self):
        self.robots_info = []
        self.position_balle = None
    def calculate_situation(self):
        for robot in self.robots_info:
            robot.calculate_situation(self.position_balle)


def decision(info_vision):
    #calcule de la situation actuelle
    info_vision.calculate_situation()
    
    #determinaison du state
    state = None
    if(any([rob.possession_balle for rob in info_vision.robots_info if rob.get_equ() == Equipe.SKYNET])):
        state = State.SKYNET_POSSESSION
    elif(any([rob.possession_balle for rob in info_vision.robots_info if rob.get_equ() == Equipe.HUMANITY])):
        state = State.HUMANITY_POSSESSION
    else:
        state = State.NO_ONE_POSSESSION
        
    #comme une state machine mais modifié
    commandes = []
    for robot_skynet in [rob for rob in info_vision.robots_info if rob.get_equ() == Equipe.SKYNET]:
        commandes.append(StateMachineLike[state](robot_skynet))
    return commandes
    



if __name__ == "__main__":
    new_info = InfoVision()
    new_info.position_balle = [0,122]
    new_info.robots_info.append(RobotInfo(np.array([61,0]), np.array([-1,1]), RobotsIndex.SKYNET_0))
    new_info.robots_info.append(RobotInfo(np.array([61,0]), np.array([-1,1]), RobotsIndex.SKYNET_1))
    new_info.robots_info.append(RobotInfo(np.array([61,0]), np.array([1,1]), RobotsIndex.HUMANITY_0))
    new_info.robots_info.append(RobotInfo(np.array([61,0]), np.array([1,1]), RobotsIndex.HUMANITY_1))
    commands = decision(new_info)
    
    commands_intensity = [command.get_command_intesity() for command in commands]
    