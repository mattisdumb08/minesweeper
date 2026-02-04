import pygame as pg

pg.font.init()

serifFont = pg.font.Font("Serif" , 16 , True)

class LivesDisplay(pg.sprite):

    def __init__(self , newNumberOfLives):

        self.numberOfLives = newNumberOfLives