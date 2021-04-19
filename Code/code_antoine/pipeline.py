# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 01:35:20 2021

@author: antoine
"""

import numpy as np
import time

import cv2

import tkinter as tk

from PIL import Image,ImageTk

import io

import matplotlib.pyplot as plt

from multiprocessing import Process,Queue

import vision
import decision
import copy
import publisher
import template_generator
import wrap

from system_classes import *

from pipedata import *

from config_loader import Configs




def stage_camera(q_in,q_out):
    """étage d'acquisition d'images et renvoie les images sans distortion

    Parameters
    ----------
    q_in : Queue
        queue pour recevoir un signal de kill en cas de besoins
    q_out : Queue
        queue pour renvoyer les images à la vision

    """

    vc = cv2.VideoCapture(Configs.get()['CAMERA']['ID'])
    vc.set(cv2.CAP_PROP_FPS,Configs.get()['CAMERA']['FPS'])
    w = Configs.get()['CAMERA']['WIDTH']
    h = Configs.get()['CAMERA']['HEIGHT']
    vc.set(cv2.CAP_PROP_FRAME_WIDTH,w)
    vc.set(cv2.CAP_PROP_FRAME_HEIGHT,h)

    distortion_remover= wrap.distortionRemover(w,h)
    warper = wrap.Warp.init_from_configs()
    while(True):
        t_start = time.perf_counter()
        time.sleep(Configs.get()['CAMERA']['SLEEP'])
        if(not q_in.empty()):
            if q_in.get().kill:
                q_out.put(PipeDataKill())
                return
        rval,img = vc.read()
        #print('camera ' + str(time.perf_counter() - t_start))
        q_out.put(PipeDataImg(warper(img,False)))

def stage_vision(q_in,q_out,q_display,to_detects):
    """étage d'analyse d'image

    Parameters
    ----------
    q_in : Queue
        Queue d'entrée contenant les images
    q_out : Queue
        queue de sortie envoyant les positions et angles
    q_display : Queue
        queue avec les rectangles de dessiné destiné à l'affichage
    to_detects : array of ToDetect
        tableau des éléments à détecter dans l'image

    """
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
    while(True):
        pipe_data_img = q_in.get()
        t_start = time.perf_counter()
        if pipe_data_img.kill :
            q_out.put(PipeDataKill())
            return
        vis_i = vision.get_info_vision(pipe_data_img.img,to_detects,template_robot,dot_template,template_balle,mask,robot_rayon_i)
        q_display.put(PipeDataImg(pipe_data_img.img))
        q_out.put(PipeDataVisionInfo(vis_i))

def stage_dec_and_pub(q_in,mqtt_client):
    """étage de décision et de publication

    Parameters
    ----------
    q_in : Queue
        Queue contenant les données de position et d'angle
    mqtt_client : MQTT.Client
        client MQTT


    """
    while(True):
        pipe_data_infovision = q_in.get()
        #t_start = time.perf_counter()
        if pipe_data_infovision.kill:
            return
        commands = decision.decision(pipe_data_infovision.vision_info)
        for command in commands:
            publisher.publish_CommandSkynet(mqtt_client,command)
        #print('dec_and_pub ' + str(time.perf_counter() - t_start))

class Pipeline:
    """pipeline de traitement, fait l'acquisition d'image, le traitement et la publiation

    Parameters
    ----------
    to_detects : array of ToDetect
        tableau des objets à détecter
    mqtt_client : MQTT.Client
        client MQTT

    Attributes
    ----------
    q_to_stage_camera : Queue
        queue se randant à la caméra
    q_to_display : Queue
        queue entre la vision et l'affichage
    q_to_stage_vision : Queue
        queue entre la caméra et la vision
    q_to_stage_decision : Queue
        queue entre la vision et la décision
    stage_camera : Process
        process de la caméra
    stage_vision : Process
        process de la vision
    stage_dec_and_pub : Process
        process de la décision et de la publication

    """
    def __init__(self,to_detects,mqtt_client):
        self.q_to_stage_camera = Queue()
        self.q_to_display = Queue()
        self.q_to_stage_vision = Queue()
        self.q_to_stage_decision = Queue()

        self.stage_camera = Process(target=stage_camera, args =(self.q_to_stage_camera,
                                                                self.q_to_stage_vision))
        self.stage_vision = Process(target=stage_vision, args=(self.q_to_stage_vision,
                                                               self.q_to_stage_decision,
                                                               self.q_to_display,
                                                               to_detects))
        self.stage_dec_and_pub = Process(target=stage_dec_and_pub, args=(self.q_to_stage_decision,
                                                                        mqtt_client))

    def start(self):
        self.stage_camera.start()
        self.stage_vision.start()
        self.stage_dec_and_pub.start()
        return self.q_to_display
    def kill(self):
        self.q_to_stage_camera.put(PipeDataKill())


class pipelineAndDisplay:
    """class contenant le pipeline et un affichage TKinter

    Parameters
    ----------
    parent : TK
        fenêtre parent
    to_detect : array of ToDetect
        objets à détecter
    mqtt_client : MQTT.Client
        client MQTT

    Attributes
    ----------
    on_closing : Func
        fonction de fermeture du système
    panel : Label
        panneau pour afficher la sortie de la vision
    pipeline : Pipeline
        pipeline de traitement
    queue_display : Queue
        queue contenant les images à afficher
    refresh_label : Func
        fonction de rafraichiment de l'image
    parent

    """
    def __init__(self, parent,to_detect,mqtt_client):
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.panel = tk.Label(self.parent)
        self.panel.pack(side = "top")
        self.pipeline = Pipeline(to_detect,mqtt_client)
        self.queue_display = self.pipeline.start()
        self.refresh_label()

    def refresh_label(self):
        new_val_img = self.queue_display.get()
        self.image = Image.fromarray(new_val_img.img[:,:,::-1])
        self.imgtk=ImageTk.PhotoImage(image=self.image)
        self.panel.configure(image=self.imgtk)
        self.parent.after(2, self.refresh_label)

    def on_closing(self):
        self.pipeline.kill()
        self.parent.destroy()

if __name__ == '__main__':

    robots = [ Robot(vision.color_by_name(robot_configs['COULEUR']),RobotIndex.init_from_dict(robot_configs)) for robot_configs in Configs.get()['ROBOTS']]


    ball = [Ball(vision.color_by_name(Configs.get()['BALLE']['COULEUR']))]




    client = publisher.start_skynet_client()
    root = tk.Tk()
    pipeline_and_display = pipelineAndDisplay(root,robots+ball,client)
    root.mainloop()
