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

    leftPressed = False
    rightPressed = False
    middlePressed = False

    while running:

        surface.fill((0 , 0 , 0))
        
        map.displayMap(surface)
        map.bombs.update()
        map.tiles.update(surface)
        window.flip()

        keys = pg.key.get_pressed()
        mouses = pg.mouse.get_pressed() # Left, Middle , Right

        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                running = False
        
        if mouses[0]:
            location = pg.mouse.get_pos()

            rect = pg.rect.Rect(0 , 0 , 1 , 1)
            rect.centerx = location[0]
            rect.centery = location[1]

            for sprite in map.tiles:
                if sprite.rect.collidepoint(location[0] , location[1]):
                    print(sprite.index)
                    map.revealMap[sprite.index[0]][sprite.index[1]] = True

        match keys:
            case pg.K_RIGHT:
                print("Mouse pressed")


    return 0   

exitCode = main() 