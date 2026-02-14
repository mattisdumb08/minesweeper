import pygame as pg

pg.mixer.init()

class SoundEffect(pg.mixer.Sound):

    def __init__(self , fileName):
        pg.mixer.Sound.__init__(self , )