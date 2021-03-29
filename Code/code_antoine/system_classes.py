
from enum import Enum
from vecangle import *
from config_loader import *

ball_radius = Configs.get()['BALLE']['RAYON']


erreur_angle = Configs.get()['ERREUR']['ANGLE']
erreur_distance = Configs.get()['ERREUR']['DISTANCE']

robot_radius = Configs.get()['ROBOT_TEMPLATE']['RAYON_E']


class Equipe(Enum):
    HUMANITY = 0
    SKYNET = 1


class State(Enum):
    SKYNET_POSSESSION = 0
    HUMANITY_POSSESSION = 1
    NO_ONE_POSSESSION = 2

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
        return self.vecangle_robot_balle.get_norme() - robot_radius - ball_radius

    def get_num(self):
        return self.robot_index.num
    def get_equ(self):
        return self.robot_index.equipe
    def get_name(self):
        return self.robot_index.to_string()

    def print(self):
        print(str(self.get_name()) + ' pos: ' + str(self.position) + ' angle: ' + str(self.vecangle_direction.angle))


class InfoVision:
    def __init__(self):
        self.robots_info = []
        self.position_balle = None
    def calculate_situation(self):
        for robot in self.robots_info:
            robot.calculate_situation(self.position_balle)
    def print(self):
        print('balle position: ' + str(self.position_balle)  )
        for robot in self.robots_info:
            robot.print()

class ToDetect:

    def __init__(self,color):
        self.color = color

class Ball(ToDetect):
    def __init__(self,color):
        super().__init__(color)


class Robot(ToDetect):
    def __init__(self,color,robot_index):
        super().__init__(color)
        self.robot_index = robot_index

class RobotIndex:
    @staticmethod
    def init_from_dict(dict):
        return RobotIndex( Equipe[dict['EQUIPE']],dict['NUM'])

    def __init__(self,equipe,num):
        self.equipe = equipe
        self.num = num

    def to_string(self):
        return self.equipe.name + '_' + str(self.num)
