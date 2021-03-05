#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 12:19:17 2021

@author: antoine
"""
import cv2
import matplotlib.pyplot as plt
from multiprocessing import Process,Queue
from pipedata import *

def stage_grab(q_in,q_out,vc):
    while(True):
        if(not q_in.empty()):
            if q_in.get().kill:
                q_out.put(PipeDataKill())
                return
        print('grab' + str(vc.grab()))
        #print('wooting')
def stage_retrieve(q_in,q_out,vc):
    while(True):
        if(not q_in.empty()):
            if q_in.get().kill:
                q_out.put(PipeDataKill())
                return
        r,img = vc.retrieve()
        print('grab' + str(vc.grab()))
        q_out.put(PipeDataImg(img))
        #print('woot')
class PipelineCamera:
    def __init__(self,vc,q_in,q_out):
        self.q_in = q_in
        self.q_out = q_out
        self.q_to_retrieve = Queue()
        self.stage_grab = Process(target=stage_grab,
                                    args=(self.q_in,self.q_to_retrieve,vc))
        self.stage_retrieve = Process(target=stage_retrieve,
                                        args =(self.q_to_retrieve,self.q_out,vc))
    def start(self):
        self.stage_grab.start()
        self.stage_retrieve.start()


if __name__ == "__main__":
    import time
    from config_loader import Configs
    import tkinter as tk

    from PIL import Image,ImageTk
    import numpy as np

    import io

    class pipeline_and_display:
        def __init__(self, parent,vc):
            self.parent = parent
            self.panel = tk.Label(self.parent)
            self.panel.pack(side = "top")
            self.q_in = Queue()
            self.q_out = Queue()
            self.pipeline = PipelineCamera(vc,self.q_in,self.q_out)
            self.pipeline.start()
            self.refresh_label()
        def kill(self):
            self.q_in.put(PipeDataKill())

        def refresh_label(self):
            new_val_img = self.q_out.get()
            self.image = Image.fromarray(new_val_img.img[:,:,::-1])
            #new_val_dec = self.queue_dec.get()
            #print(new_val_dec.vision_info.robots_info[0].vecangle_direction.vec)
            self.imgtk=ImageTk.PhotoImage(image=self.image)
            self.panel.configure(image=self.imgtk)
            self.parent.after(2, self.refresh_label)

    def on_closing():
        mouv_detect.kill()
        root.destroy()


    vc = cv2.VideoCapture(Configs.get()['CAMERA']['ID'])

    if vc.isOpened(): # try to get the first frame
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", on_closing)
        mouv_detect = pipeline_and_display(root,vc)
        root.mainloop()
