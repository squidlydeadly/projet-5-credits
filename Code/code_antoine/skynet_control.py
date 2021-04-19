from simple_pid import PID
import time
import numpy as np

class pidList:
    """presque Singleton contenant une liste de PID

    Attributes
    ----------
    pids : dictionary of tuple of simple_pid.PID
        PID pour chaque robot de skynet en position et angle

    """
    pids = {}

    @staticmethod
    def get(num):
        """
        renvoie les PID de num

        Parameters
        ----------
        num : int
            indice des PID

        Returns
        -------
        tuple of PID
            PID en angle et position

        """
        if num not in pidList.pids:
            pidList.pids[num] = (PID(10,0,0,setpoint=0),PID(20,0,0,setpoint=0))
        return pidList.pids[num]

def clamp_intensity(val):
    """clamp val avec les valeurs extrêmes d'intensité

    Parameters
    ----------
    val : int
        valeur à clamp

    Returns
    -------
    int
        valeur clampé

    """
    max_intensity = 500
    min_intensity = -500
    return max(min(val,max_intensity),min_intensity)

class CommandIntensity:
    """ objet pour contenir les commandes en intensité

    Parameters
    ----------
    clockwise_intensity : int
        intensité dans le sens horaire
    foward_intensity : int
        intensité vers l'avant

    Attributes
    ----------
    clockwise_intensity
    foward_intensity

    """
    def __init__(self,clockwise_intensity=0,foward_intensity=0):
        self.clockwise_intensity = clockwise_intensity
        self.foward_intensity = foward_intensity


class CommandeSkynet:
    """commandes créés par la décision pour chaque robot

    Parameters
    ----------
    robot_index : RobotIndex
        identifiant du robot
    angle : float
        erreur sur l'angle à combler
    is_clockwise : bool
        le sens de l'angle (référentiel de l'image)
    grandeur : float
        erreur sur la grandeur à combler
    is_foward : bool
        sens de la grandeur
    kick : bool
        est-ce que le robot doit frapper la balle

    Attributes
    ----------
    robot_index
    angle
    is_clockwise
    grandeur
    is_foward
    kick

    """
    def __init__(self,robot_index,angle=0,is_clockwise=True,grandeur=0,is_foward=True,kick=False):
        self.robot_index = robot_index
        self.angle = 0.0 if np.isnan(angle) else angle
        self.is_clockwise = is_clockwise
        self.grandeur = 0.0 if np.isnan(grandeur) else grandeur
        self.is_foward = is_foward
        self.kick = kick
        print(robot_index.to_string() + ' grandeur: ' + str(self.grandeur) + str(self.is_foward))
        print(robot_index.to_string() + ' angle: ' + str(self.angle) + str(self.is_clockwise))

    def get_command_intensity(self):
        """applique les PID aux commandes pour générer les données à envoyer aux robots

        Returns
        -------
        CommandIntensity
            commande en intensité pour les robots

        """
        pid_angle,pid_grandeur = pidList.get(self.robot_index.num)

        #double inversion de la commande puisque la différence est envoyé au lieu du retour et que les référentiels sont différents
        intensity_angle = pid_angle(self.angle if self.is_clockwise else -self.angle)
        intensity_angle = clamp_intensity(intensity_angle)

        #inversion de la commande puisque la différence est envoyé au lieu du retour
        intensity_grandeur = pid_grandeur(-self.grandeur if self.is_foward == (self.angle < 90) else self.grandeur)
        intensity_grandeur = clamp_intensity(intensity_grandeur)
        return CommandIntensity(int(intensity_angle),int(intensity_grandeur))

if __name__ == "__main__":
    x = 89
    y = 100
    while(True):
        cmd = CommandeSkynet(0,angle=x,grandeur=y)
        intensity = cmd.get_command_intensity()
        print(str(intensity.clockwise_intensity) + ' ' + str(intensity.foward_intensity) )
        x-=1
        y-=1
        time.sleep(0.5)
