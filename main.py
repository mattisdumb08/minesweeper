import pygame as pg
import map

pg.init()

def main():


    window = pg.display
    window.set_mode((600 , 500))
    surface = window.get_surface()

    map.randomiseMap(16 , 16)
    map.displayMap(surface)

    running = True

    while running:

        surface.fill((0 , 0 , 0))
        
        map.bombs.update()
        map.tiles.update(surface)
        map.displayMap(surface)

        window.flip()

        keys = pg.key.get_pressed()

        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                running = False

    return 0   

exitCode = main() 