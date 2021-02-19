#!/usr/bin/env python3
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

class PipeData:
    def __init__(self,kill=False):
        self.kill = kill
        
class PipeDataKill(PipeData):
    def __init__(self):
        super().__init__(True)
            

class PipeDataImg(PipeData):
    def __init__(self,img=[]):
        super().__init__()
        self.img = img

class PipeDataVisionInfo(PipeData):
    def __init__(self,vision_info):
        super().__init__()
        self.vision_info = vision_info
        
def stage_camera(q_in,q_out,cam_id):
    vc = cv2.VideoCapture(cam_id)
    while(True):
        if(not q_in.empty()):
            if q_in.get().kill:
                q_out.put(PipeDataKill())
                return
        rval,img = vc.read()
        q_out.put(PipeDataImg(img))

def stage_vision(q_in,q_out,q_display,template_robot,template_balle,to_detects):
    while(True):
        pipe_data_img = q_in.get()
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
                
                q_display.put(PipeDataImg(img_rec))
            else:
                position,direction_vec = vision.get_position_orientation(pipe_data_img.img,
                                                               template_robot,
                                                               to_detect.color)
                vision_info.robots_info.append(decision.RobotInfo(position,
                                                                  direction_vec,
                                                                  to_detect.index))
        q_out.put(PipeDataVisionInfo(vision_info))

class Pipeline:
    def __init__(self,cam_id,template_robot,template_balle,to_detects):
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
    
    
    class movement_detector:
        def __init__(self, parent):
            self.parent = parent
            self.panel = tk.Label(self.parent)
            self.panel.pack(side = "top")
            template = cv2.imread('symboleBlanc.png',cv2.IMREAD_GRAYSCALE)
            self.pipeline = Pipeline(0,template,template,[Ball(vision.color_by_name('bleu'))])
            self.queue_dis,self.queue_dec = self.pipeline.start()
            self.refresh_label()
    
        def refresh_label(self):
            new_val_img = self.queue_dis.get()
            self.image = Image.fromarray(new_val_img.img[:,:,::-1])
            new_val_dec = self.queue_dec.get()
            print(new_val_dec.vision_info.position_ball)
            self.imgtk=ImageTk.PhotoImage(image=self.image)
            self.panel.configure(image=self.imgtk)
            self.parent.after(2, self.refresh_label)

    def on_closing():
        mouv_detect.pipeline.kill()
        root.destroy()
    
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    mouv_detect = movement_detector(root)
    root.mainloop()