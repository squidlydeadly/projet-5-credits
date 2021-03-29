#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 11:10:16 2021

@author: antoine
"""


from system_classes import *

from vecangle import *

from skynet_control import *

from config_loader import *

import numpy as np
#toute grandeur est en pixel on degre
robot_radius = Configs.get()['ROBOT_TEMPLATE']['RAYON_E']

ball_radius = Configs.get()['BALLE']['RAYON']

erreur_angle = Configs.get()['ERREUR']['ANGLE']
erreur_distance = Configs.get()['ERREUR']['DISTANCE']

terain_width = 640

terrain_height = 480

centre_but_skynet = [0,240]

centre_but_humanity = [640,240]

demi_largeur_buts = 100


def skynet_goal(robot_skynet):
    commande = None
    if(not robot_skynet.possession_balle):
        commande = CommandeSkynet(robot_skynet.robot_index)
    else:
        vecangle_robot_but = VecAngle(centre_but_humanity - robot_skynet.position)
        diff_vecangle_but_direction = VecAngleDiff(robot_skynet.vecangle_direction,vecangle_robot_but)
        if(diff_vecangle_but_direction.angle < erreur_angle):
            commande = CommandeSkynet(robot_skynet.robot_index,
                                      kick=True)
        else:
            commande = CommandeSkynet(robot_skynet.robot_index,
                                      angle=diff_vecangle_but_direction.angle,
                                      is_clockwise=diff_vecangle_but_direction.is_clockwise)
    return commande

def skynet_defence(robot_skynet):
    vecangle_robot_but = VecAngle(centre_but_skynet - robot_skynet.position)
    commande = None
    if(vecangle_robot_but.get_norme() > demi_largeur_buts):
        #se rendre dans la zone des buts a reculon
        vecangle_direction_inv = VecAngle(-1*robot_skynet.vecangle_direction.vec)
        diff_vecangle_but_direction_inv = VecAngleDiff(vecangle_direction_inv,vecangle_robot_but)

        commande = CommandeSkynet(robot_skynet.robot_index,
                                  angle=diff_vecangle_but_direction_inv.angle,
                                  is_clockwise=diff_vecangle_but_direction_inv.is_clockwise,
                                  grandeur=vecangle_robot_but.get_norme(),
                                  is_foward=False)
    else:
        #orienter vers la balle
        commande = CommandeSkynet(robot_skynet.robot_index,
                                  angle = robot_skynet.diff_vecangle.angle,
                                  is_clockwise=robot_skynet.diff_vecangle.is_clockwise)
    return commande
def skynet_fetch(robot_skynet):
    return CommandeSkynet(robot_skynet.robot_index,
                          angle=robot_skynet.diff_vecangle.angle,
                          is_clockwise=robot_skynet.diff_vecangle.is_clockwise,
                          grandeur=robot_skynet.get_distance_balle_robot())

StateMachineLike = {State.SKYNET_POSSESSION: skynet_goal, #L'Equipe Skynet a la balle, la balle doit se diriger vers le but
                    State.HUMANITY_POSSESSION: skynet_defence, #l'Equipe Humanity a la balle, mode defense
                    State.NO_ONE_POSSESSION: skynet_fetch} #personne n'a la balle, il faut donc aller la chercher





def decision(info_vision):
    #calcule de la situation actuelle
    info_vision.calculate_situation()

    #determination du state
    state = None
    if(any([rob.possession_balle for rob in info_vision.robots_info if rob.get_equ() == Equipe.SKYNET])):
        state = State.SKYNET_POSSESSION
    elif(any([rob.possession_balle for rob in info_vision.robots_info if rob.get_equ() == Equipe.HUMANITY])):
        state = State.HUMANITY_POSSESSION
    else:
        state = State.NO_ONE_POSSESSION
    print(state)
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
