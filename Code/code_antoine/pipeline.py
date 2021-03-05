# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 01:35:20 2021

@author: antoine
"""

import numpy as np
import time

import cv2

import matplotlib.pyplot as plt

from multiprocessing import Process,Queue

import vision
import decision
import copy

from pipedata import *

from config_loader import Configs

class ToDetect:
    def __init__(self,color):
        self.color = color

class Ball(ToDetect):
    def __init__(self,color):
        super().__init__(color)


class Robot(ToDetect):
    def __init__(self,color,index):
        super().__init__(color)
        self.index = index



def stage_camera(q_in,q_out,cam_id):
    vc = cv2.VideoCapture(cam_id)
    vc.set(cv2.CAP_PROP_FPS,Configs.get()['CAMERA']['FPS'])
    vc.set(cv2.CAP_PROP_FRAME_WIDTH,Configs.get()['CAMERA']['WIDTH'])
    vc.set(cv2.CAP_PROP_FRAME_HEIGHT,Configs.get()['CAMERA']['HEIGHT'])

    while(True):
        t_start = time.perf_counter()
        if(not q_in.empty()):
            if q_in.get().kill:
                q_out.put(PipeDataKill())
                return
        rval,img = vc.read()
        print('camera' + str(time.perf_counter() - t_start))
        q_out.put(PipeDataImg(img))

def stage_vision(q_in,q_out,q_display,template_robot,template_balle,mask,to_detects):
    while(True):
        pipe_data_img = q_in.get()
        t_start = time.perf_counter()
        if pipe_data_img.kill :
            q_out.put(PipeDataKill())
            return
        vision_info = decision.InfoVision()
        for to_detect in to_detects:
            if type(to_detect) is Ball:
                position,img_rec = vision.get_position(pipe_data_img.img,
                                                                template_balle,
                                                                to_detect.color)
                vision_info.position_ball = position


            else:
                position,direction_vec,img_rec= vision.get_position_orientation(pipe_data_img.img,
                                                               template_robot,
                                                               mask,
                                                               to_detect.color)
                vision_info.robots_info.append(decision.RobotInfo(position,
                                                                  direction_vec,
                                                                  to_detect.index))
        print('vision' + str(time.perf_counter() - t_start))
        q_display.put(PipeDataImg(img_rec))
        q_out.put(PipeDataVisionInfo(vision_info))

class Pipeline:
    def __init__(self,cam_id,template_robot,template_balle,mask,to_detects):
        self.q_to_stage_camera = Queue()
        self.q_to_display = Queue()
        self.q_to_stage_vision = Queue()
        self.q_to_stage_decision = Queue()

        self.stage_camera = Process(target=stage_camera, args =(self.q_to_stage_camera,
                                                                self.q_to_stage_vision,
                                                                cam_id))
        self.stage_vision = Process(target=stage_vision, args=(self.q_to_stage_vision,
                                                               self.q_to_stage_decision,
                                                               self.q_to_display,
                                                               template_robot,
                                                               template_balle,
                                                               mask,
                                                               to_detects))

    def start(self):
        self.stage_camera.start()
        self.stage_vision.start()
        return self.q_to_display,self.q_to_stage_decision
    def kill(self):
        self.q_to_stage_camera.put(PipeDataKill())

if __name__ == '__main__':

    import tkinter as tk

    from PIL import Image,ImageTk
    import numpy as np

    import io


    class pipeline_and_display:
        def __init__(self, parent,to_detect):
            self.parent = parent
            self.panel = tk.Label(self.parent)
            self.panel.pack(side = "top")
            template = cv2.imread('images/symboleBlanc.png',cv2.IMREAD_GRAYSCALE)
            mask = cv2.imread('images/mask.png',cv2.IMREAD_GRAYSCALE)
            self.pipeline = Pipeline(Configs.get()['CAMERA']['ID'],template,template,mask,to_detect)
            self.queue_dis,self.queue_dec = self.pipeline.start()
            self.refresh_label()

        def refresh_label(self):
            new_val_img = self.queue_dis.get()
            self.image = Image.fromarray(new_val_img.img[:,:,::-1])
            #new_val_dec = self.queue_dec.get()
            #print(new_val_dec.vision_info.robots_info[0].vecangle_direction.vec)
            self.imgtk=ImageTk.PhotoImage(image=self.image)
            self.panel.configure(image=self.imgtk)
            self.parent.after(2, self.refresh_label)

    def on_closing():
        mouv_detect.pipeline.kill()
        root.destroy()

    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    mouv_detect = pipeline_and_display(root,[Robot(vision.color_by_name('bleu'),decision.RobotsIndex.HUMANITY_1),Robot(vision.color_by_name('magenta'),decision.RobotsIndex.HUMANITY_0)])
    root.mainloop()
