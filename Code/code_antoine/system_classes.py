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
    """informations relatives à un robot

    Parameters
    ----------
    position : array of float
        position du robot
    direction_vec : array of float
        vecteur de direction du robot
    robot_index : RobotIndex
        identifiant du robot

    Attributes
    ----------
    vecangle_direction : VecAngle
        direction du robot
    possession_balle : bool
        si le robot possède la balle
    vecangle_robot_balle : VecAngle
        direction entre le robot et la balle
    diff_vecangle : VecAngleDiff
        difference entre la diretion du robot et de la balle
    robot_index
    position

    """
    def __init__(self,position,direction_vec,robot_index):
        self.vecangle_direction = VecAngle(direction_vec)
        self.robot_index = robot_index
        self.position = position
        self.possession_balle = None
        self.vecangle_robot_balle = None
        self.diff_vecangle = None

    def calculate_situation(self,position_balle):
        """remplie les informations manquante relative à la balle

        Parameters
        ----------
        position_balle : array of float
            position de la balle


        """
        self.vecangle_robot_balle = VecAngle(position_balle - self.position)
        self.diff_vecangle = VecAngleDiff(self.vecangle_direction,self.vecangle_robot_balle)
        self.possession_balle = self.diff_vecangle.angle < erreur_angle and \
            self.get_distance_balle_robot() < erreur_distance
    def get_distance_balle_robot(self):
        return self.vecangle_robot_balle.get_norme() - robot_radius - ball_radius

    def get_num(self):
        """renvoie le numéro de l'identifiant"""
        return self.robot_index.num
    def get_equ(self):
        """renvoie léquipe de l'identifiant"""
        return self.robot_index.equipe
    def get_name(self):
        """renvoie l'identifiant en string"""
        return self.robot_index.to_string()

    def print(self):
        """print les commandes et l'identifiant"""
        print(str(self.get_name()) + ' pos: ' + str(self.position) + ' angle: ' + str(self.vecangle_direction.angle))


class InfoVision:
    """informations provenant de la vision

    Attributes
    ----------
    robots_info : array of RobotInfo
        tableau des informations des robots
    position_balle : array of float
        position de la balle

    """
    def __init__(self):
        self.robots_info = []
        self.position_balle = None
    def calculate_situation(self):
        """calcule la situation de chaque robot"""
        for robot in self.robots_info:
            robot.calculate_situation(self.position_balle)
    def print(self):
        """print les informations de la vision"""
        print('balle position: ' + str(self.position_balle)  )
        for robot in self.robots_info:
            robot.print()

class ToDetect:
    """objet à détecter par la vision

    Parameters
    ----------
    color : Color
        couleur de l'objet à détecter

    Attributes
    ----------
    color

    """

    def __init__(self,color):
        self.color = color

class Ball(ToDetect):
    """balle à détecter"""
    def __init__(self,color):
        super().__init__(color)


class Robot(ToDetect):
    """robot à détecter

    Parameters
    ----------
    color : Color
        couleur du robot à détecter
    robot_index : RobotIndex
        identifiant du robot

    Attributes
    ----------
    robot_index

    """
    def __init__(self,color,robot_index):
        super().__init__(color)
        self.robot_index = robot_index

class RobotIndex:
    """identifiant d'un robot

    Parameters
    ----------
    equipe : Equipe
        équipe du robot
    num : int
        numéro du robot

    Attributes
    ----------
    equipe
    num
    """
    @staticmethod
    def init_from_dict(dict):
        return RobotIndex( Equipe[dict['EQUIPE']],dict['NUM'])

    def __init__(self,equipe,num):
        self.equipe = equipe
        self.num = num

    def to_string(self):
        """renvoie l'identifiant en string"""
        return self.equipe.name + '_' + str(self.num)
