import cv2

import numpy as np

import wrap

from config_loader import Configs

import tkinter as tk

from PIL import Image,ImageTk

import io


class TunableParam:
    """paramètre pouvant être modifié par le configurateur
    Parameters
    ----------
    parent : Tk
        conteneur tkinter du paramètre
    name : string
        nom du paramètre dans le fichier de configuration
    default_delta : float
        variation par défault du paramètre

    Attributes
    ----------
    value : float
        valeur du paramètre
    plus : func
        fonction d'incrémentation
    minus : type
        function de décrémentation
    entry_delta : Entry
        champ modifiable de la valeur du delta
    name

    """
    def __init__(self,parent,name,default_delta):
        self.name = name
        self.value = Configs.get()['CALIBRATION'][self.name]
        frame = tk.Frame(parent)
        frame.pack(side='top')
        button_plus = tk.Button(frame,text=self.name+'+',command = self.plus)
        button_plus.pack(side="left")
        button_minus = tk.Button(frame,text=self.name+'-',command = self.minus)
        button_minus.pack(side="left")
        self.entry_delta = tk.Entry(frame)
        self.entry_delta.insert(0,default_delta)
        self.entry_delta.pack(side='left')
        self.print()
    def plus(self):
        """fonction d'incrémentation de la valeur


        """
        self.value = self.value + float(self.entry_delta.get())
        self.print()
    def minus(self):
        """fonction de décrémentation de la valeur

        """
        self.value = self.value - float(self.entry_delta.get())
        self.print()
    def print(self):
        """
        affiche la valeur actuelle du paramètre
        """
        print(self.name + ':' + str(self.value))
    def update_config(self):
        """actualise la configuration dans les configs

        Returns
        -------
        type
            Description of returned object.

        """
        Configs.get()['CALIBRATION'][self.name] = self.value


class Configurator:
    """ajoute un configurateur à une fenêtre Tkinter

    Parameters
    ----------
    parent : Tk
        fenêtre Tkinter parent

    Attributes
    ----------
    vc : VideoCapture
        capture de la caméra
    w : int
        largeur de l'image
    h : int
        hauteur de l'image
    on_closing : func
        fonction de fermeture de la fenêtre
    panel : Label
        label pour contenir l'image
    calibration_params : array of TunableParam
        tableau des paramètres à calibrer
    save : func
        fonction de sauvegarde des paramètres
    refresh_label : func
        fonction à lancer pour rafraichir l'image du panel
    parent

    """
    def __init__(self, parent):
        self.vc = cv2.VideoCapture(Configs.get()['CAMERA']['ID'])
        self.vc.set(cv2.CAP_PROP_FPS,Configs.get()['CAMERA']['FPS'])
        self.w = Configs.get()['CAMERA']['WIDTH']
        self.h = Configs.get()['CAMERA']['HEIGHT']
        self.vc.set(cv2.CAP_PROP_FRAME_WIDTH,self.w)
        self.vc.set(cv2.CAP_PROP_FRAME_HEIGHT,self.h)
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.panel = tk.Label(self.parent)
        self.panel.pack(side = "top")
        self.calibration_params = [TunableParam(self.parent,'K1',-1e-6),
        TunableParam(self.parent,'K2',-1e-6),
        TunableParam(self.parent,'P1',-1e-6),
        TunableParam(self.parent,'P2',-1e-6),
        TunableParam(self.parent,'CROP_TOP',1),
        TunableParam(self.parent,'CROP_BOTTOM',1),
        TunableParam(self.parent,'CROP_RIGHT',1),
        TunableParam(self.parent,'CROP_LEFT',1),
        TunableParam(self.parent,'THETA',1)]
        button_save = tk.Button(self.parent,text='save',command = self.save)
        button_save.pack(side="left")
        self.refresh_label()
    def get_param_value(self,name):
        """renvoie la valeur du paramètre ayant comme nom name

        Parameters
        ----------
        name : string
            nom du paramètre

        Returns
        -------
        float
            valeur actuel du paramètre

        """
        return [e for e in self.calibration_params if e.name == name][0].value

    def save(self):
        """sauvegarde les param dans calibration_params

        """
        for param in self.calibration_params:
            param.update_config()
        Configs.save()



    def refresh_label(self):
        """refraichi le panel avec une nouvelle image


        """
        rval,cv2_img = self.vc.read()

        warper = wrap.Warp(
        self.w,
        self.h,
        self.get_param_value('K1'),
        self.get_param_value('K2'),
        self.get_param_value('P1'),
        self.get_param_value('P2'),
        int(self.get_param_value('CROP_TOP')),
        int(self.get_param_value('CROP_BOTTOM')),
        int(self.get_param_value('CROP_LEFT')),
        int(self.get_param_value('CROP_RIGHT')),
        self.get_param_value('THETA'))


        cv2_img = warper(cv2_img,draw=True)

        self.image = Image.fromarray(cv2_img[:,:,::-1])
        self.imgtk=ImageTk.PhotoImage(image=self.image)
        self.panel.configure(image=self.imgtk)
        self.parent.after(2, self.refresh_label)

    def on_closing(self):
        """détruit la fenêtre principale


        """
        self.parent.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    conf = Configurator(root)
    root.mainloop()
