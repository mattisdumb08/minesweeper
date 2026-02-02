import pygame as pg
import time
import threading
import map

# Reveal map Key = 1 revealed 0 is unrevealed 2 is a bomb that is revealed 3 is flagged
pg.init()

window = pg.display

def checkNumberOfBombsOpen():

    total = 0

    for yIndex in range(0 , len(map.revealMap)):
        for xIndex in range(0 , len(map.revealMap[0])):
            if map.revealMap[yIndex][xIndex] == 2:
                total += 1

    return 0


running = True

def shutdown():
   global running
   running = False

def revealAdjacent0(spread : bool , delay : int):
    
    sprite : map.Tile

    for sprite in map.tiles:

        if map.revealMap[sprite.index[0]][sprite.index[1]] == 3:
            continue

        if map.revealMap[sprite.index[0]][sprite.index[1]] == 1 and map.worldMap[sprite.index[0]][sprite.index[1]] == 0 and map.checkBombCountAlternate(sprite.index) == 0 :

            if spread:

                pg.time.delay(delay)

                window.flip()

            map.revealAdjacentAlternate(sprite.index)
        
        # elif map.revealMap[sprite.index[0]][sprite.index[1]] == 1 and map.worldMap[sprite.index[0]][sprite.index[1]] == 0 and map.checkFlagCount(sprite.index) != sprite.numberOfBombs:
        #     map.revealAdjacentAlternate(sprite.index)
        


def main():

    global running

    window = pg.display
    window.set_caption("Minesweeper")
    window.set_mode((1600 , 900))
    map.turtleImage.convert_alpha()
    surface = window.get_surface()


    map.randomiseMap(16 , 16)
    map.displayMap(surface)

    lives = 3

    while running:

        surface.fill((0 , 0 , 225))
        
        # map.displayMap(surface)

        map.bombs.draw(surface)
        map.tiles.draw(surface)

        map.bombs.update(surface)
        map.tiles.update(surface)
        revealAdjacent0(True , 2)

        window.flip()

        keys = pg.key.get_pressed()

        events = pg.event.get()

        if checkNumberOfBombsOpen() == lives:
            running = False

        for event in events:

            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:

                mouses = pg.mouse.get_pressed() # Left, Middle , Right
                location = pg.mouse.get_pos()

                if mouses[0]:

                    for sprite in map.tiles:
                        if map.revealMap[sprite.index[0]][sprite.index[1]] != 3 and sprite.rect.collidepoint(location[0] , location[1]):
                            map.revealMap[sprite.index[0]][sprite.index[1]] = 1
                            # map.revealAdjacent(sprite.index , 0)
                            map.revealAdjacentAlternate(sprite.index)
                            # revealAdjacent0()
                    for sprite in map.bombs:
                        if map.revealMap[sprite.index[0]][sprite.index[1]] != 3 and sprite.rect.collidepoint(location[0] , location[1]):
                            map.revealMap[sprite.index[0]][sprite.index[1]] = 2
                            


                if mouses[2]:

                    sprite : map.Tile

                    for sprite in map.tiles:
                        if map.revealMap[sprite.index[0]][sprite.index[1]] == 0 and sprite.rect.collidepoint(location[0] , location[1]):
                            map.revealMap[sprite.index[0]][sprite.index[1]] = 3
                        elif map.revealMap[sprite.index[0]][sprite.index[1]] == 3 and sprite.rect.collidepoint(location[0] , location[1]):
                            map.revealMap[sprite.index[0]][sprite.index[1]] = 0
                    for sprite in map.bombs:
                        if map.revealMap[sprite.index[0]][sprite.index[1]] == 0 and sprite.rect.collidepoint(location[0] , location[1]):
                            map.revealMap[sprite.index[0]][sprite.index[1]] = 3
                        elif map.revealMap[sprite.index[0]][sprite.index[1]] == 3 and sprite.rect.collidepoint(location[0] , location[1]):
                            map.revealMap[sprite.index[0]][sprite.index[1]] = 0
                            


    return 0   

exitCode = main() 