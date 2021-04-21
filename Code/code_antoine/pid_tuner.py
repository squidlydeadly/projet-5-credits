from skynet_control import *
import vision
import cv2
from config_loader import Configs
from system_classes import *
import template_generator
import wrap
import publisher


def cmd_only_angle(robot_info):
    """génère des commandes pour robot skynet seulement avec un angle

    Parameters
    ----------
    robot_info : RobotInfo
        information du robot à commander

    Returns
    -------
    CommandeSkynet
        commande pour le robot skynet

    """
    return CommandeSkynet(robot_info.robot_index,
        angle=robot_info.diff_vecangle.angle,
        is_clockwise = robot_info.diff_vecangle.is_clockwise)

def cmd_only_grandeur(robot_info):
    """génère des commandes pour robot skynet seulement avec grandeur

    Parameters
    ----------
    robot_info : RobotInfo
        information du robot à commander

    Returns
    -------
    CommandeSkynet
        commande pour le robot skynet

    """
    return CommandeSkynet(robot_info.robot_index,
        grandeur=robot_info.vecangle_robot_balle.orth_projection_norme(robot_info.vecangle_direction),
        is_foward=robot_info.diff_vecangle.angle<90)

if __name__ == '__main__':
    vc = cv2.VideoCapture(Configs.get()['CAMERA']['ID'])
    vc.set(cv2.CAP_PROP_FPS,Configs.get()['CAMERA']['FPS'])
    w = Configs.get()['CAMERA']['WIDTH']
    h = Configs.get()['CAMERA']['HEIGHT']
    vc.set(cv2.CAP_PROP_FRAME_WIDTH,w)
    vc.set(cv2.CAP_PROP_FRAME_HEIGHT,h)

    robot_rayon_e = Configs.get()['ROBOT_TEMPLATE']['RAYON_E']
    robot_rayon_i = Configs.get()['ROBOT_TEMPLATE']['RAYON_I']

    template_robot = template_generator.ring(robot_rayon_e,robot_rayon_i).astype(np.uint8)
    mask = template_generator.circle(robot_rayon_e,robot_rayon_i).astype(np.uint8)

    ret,mask = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)
    #cv2.imwrite('testi.jpg',mask)
    ball_rayon = Configs.get()['BALLE']['RAYON']
    template_balle = template_generator.circle(ball_rayon,ball_rayon).astype(np.uint8)

    dot_rayon = Configs.get()['ROBOT_TEMPLATE']['RAYON_DOT']

    dot_template = template_generator.circle(dot_rayon,dot_rayon).astype(np.uint8)

    warper = wrap.Warp.init_from_configs()
    to_detects = [Robot( vision.color_by_name('azur'),RobotIndex(Equipe.SKYNET,0)),Ball(vision.color_by_name('blanc'))]
    mqtt_client = publisher.start_skynet_client()
    while(1):
        retv,img = vc.read()
        i_vis = vision.get_info_vision(warper(img),to_detects,template_robot,dot_template,template_balle,mask,robot_rayon_i)
        i_vis.calculate_situation()
        cmd = cmd_only_grandeur(i_vis.robots_info[0])
        publisher.publish_CommandSkynet(mqtt_client,cmd)
