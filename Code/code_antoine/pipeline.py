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
import publisher

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
        time.sleep(Configs.get()['CAMERA']['SLEEP'])
        if(not q_in.empty()):
            if q_in.get().kill:
                q_out.put(PipeDataKill())
                return
        rval,img = vc.read()
        #print('camera ' + str(time.perf_counter() - t_start))
        q_out.put(PipeDataImg(img))

def stage_vision(q_in,q_out,q_display,template_robot,template_balle,mask,to_detects):
    while(True):
        pipe_data_img = q_in.get()
        t_start = time.perf_counter()
        if pipe_data_img.kill :
            q_out.put(PipeDataKill())
            return
        vision_info = decision.InfoVision()
        rectangles =[]
        lines = []
        for to_detect in to_detects:
            if type(to_detect) is Ball:
                #print('Ball')
                position,rect_dict = vision.get_position(pipe_data_img.img,
                                                                template_balle,
                                                                to_detect.color)
                #print(position)
                vision_info.position_balle = position
                rectangles.append(rect_dict)


            else:
                position,direction_vec,rect_dict,line_dict= vision.get_position_orientation(pipe_data_img.img,
                                                               template_robot,
                                                               mask,
                                                               to_detect.color)
                vision_info.robots_info.append(decision.RobotInfo(position,
                                                                  direction_vec,
                                                                  to_detect.index))
                lines.append(line_dict)
                rectangles.append(rect_dict)
        #print('vision ' + str(time.perf_counter() - t_start))
        for rect in rectangles:
            cv2.rectangle(pipe_data_img.img, rect['top_left'],rect['bottom_right'] ,rect['bgr'] ,2)
        for line in lines:
            cv2.line(pipe_data_img.img, line['start'],line['end'] ,line['bgr'] ,2)
        q_display.put(PipeDataImg(pipe_data_img.img))
        q_out.put(PipeDataVisionInfo(vision_info))

def stage_dec_and_pub(q_in,mqtt_client):
    while(True):
        pipe_data_infovision = q_in.get()
        t_start = time.perf_counter()
        if pipe_data_infovision.kill:
            return
        commands = decision.decision(pipe_data_infovision.vision_info)
        for command in commands:
            publisher.publish_CommandSkynet(mqtt_client,command)
        #print('dec_and_pub ' + str(time.perf_counter() - t_start))

class Pipeline:
    def __init__(self,cam_id,template_robot,template_balle,mask,to_detects,mqtt_client):
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
        self.stage_dec_and_pub = Process(target=stage_dec_and_pub, args=(self.q_to_stage_decision,
                                                                        mqtt_client))

    def start(self):
        self.stage_camera.start()
        self.stage_vision.start()
        self.stage_dec_and_pub.start()
        return self.q_to_display
    def kill(self):
        self.q_to_stage_camera.put(PipeDataKill())

if __name__ == '__main__':

    import tkinter as tk

    from PIL import Image,ImageTk
    import numpy as np

    import io


    class pipeline_and_display:
        def __init__(self, parent,to_detect,robot_template,ball_template,robot_mask,mqtt_client):
            self.parent = parent
            self.panel = tk.Label(self.parent)
            self.panel.pack(side = "top")
            self.pipeline = Pipeline(Configs.get()['CAMERA']['ID'],robot_template,ball_template,robot_mask,to_detect,mqtt_client)
            self.queue_display = self.pipeline.start()
            self.refresh_label()

        def refresh_label(self):
            new_val_img = self.queue_display.get()
            self.image = Image.fromarray(new_val_img.img[:,:,::-1])
            self.imgtk=ImageTk.PhotoImage(image=self.image)
            self.panel.configure(image=self.imgtk)
            self.parent.after(2, self.refresh_label)

    def on_closing():
        mouv_detect.pipeline.kill()
        root.destroy()

    client = publisher.start_skynet_client()
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    mouv_detect = pipeline_and_display(root,[Robot(vision.color_by_name('orange'),decision.RobotsIndex.HUMANITY_1),
                                            Robot(vision.color_by_name('magenta'),decision.RobotsIndex.SKYNET_0),
                                            Ball(vision.color_by_name('vert'))],client)
    root.mainloop()
