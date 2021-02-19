#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 12:19:17 2021

@author: antoine
"""
import cv2
import matplotlib.pyplot as plt



if __name__ == "__main__":
    import time
    vc = cv2.VideoCapture(2)
    n = 100

    if vc.isOpened(): # try to get the first frame
        t_start = time.perf_counter()

        for i in range(n):
            rval, frame = vc.read()
        t_end = time.perf_counter()
        plt.imshow(frame[:,:,::-1])
        vc.release()


        t_total = t_end - t_start
        fps = n/t_total
        print(fps)
