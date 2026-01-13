import pygame as pg
from map import *

pg.init()

def main():


    window = pg.display
    window.set_mode((600 , 500))

    running = True

    while running:

        segments.draw()
        bombs.draw()

        window.flip()

        keys = pg.key.get_pressed()

        events = pg.event.get()

        for event in events:
            if event == pg.QUIT:
                running = False    