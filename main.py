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

    return total


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

            shouldReveal0 = True
        
        # elif map.revealMap[sprite.index[0]][sprite.index[1]] == 1 and map.worldMap[sprite.index[0]][sprite.index[1]] == 0 and map.checkFlagCount(sprite.index) != sprite.numberOfBombs:
        #     map.revealAdjacentAlternate(sprite.index)
        
shouldReveal0 = False


def main():

    global shouldReveal0

    global running

    window = pg.display
    window.set_caption("Minesweeper")
    window.set_mode((1600 , 900))
    map.turtleImage.convert_alpha()
    surface = window.get_surface()


    map.randomiseMap(16 , 16)
    map.displayMap(surface)

    map.turtleImage.convert_alpha()

    lives = 3

    shouldReveal0 = False

    while running:

        pg.time.delay(16)

        surface.fill((0 , 0 , 225))
        
        # map.displayMap(surface)

        map.bombs.update(surface)
        map.tiles.update(surface)

        map.bombs.draw(surface)
        map.tiles.draw(surface)

        window.flip()

        keys = pg.key.get_pressed()

        events = pg.event.get()

        if checkNumberOfBombsOpen() == lives:
            running = False
        
        revealAdjacent0(True , 2)

        if len(events) !=0:

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

                                # firstIndex = sprite.index[0]
                                # secondIndex = sprite.index[1]
                                
                                # if map.revealMap[firstIndex][secondIndex] == 1 and sprite.numberOfBombs == 0:
                                #     sprite.image.fill((100 , 100 , 100))

                                # elif map.revealMap[firstIndex][secondIndex] == 1:

                                #     sprite.image.fill((255 , 255 , 255))

                                #     sprite.image.fill((100 , 100 , 100))

                                #     imageRect : pg.Rect

                                #     if sprite.numberImage == None:

                                #         sprite.numberImage = map.text.render(str(sprite.numberOfBombs) , True , (0 , 0 , 0))
                                #         sprite.imageRect = sprite.numberImage.get_rect()
                                #         sprite.imageRect.center = ((sprite.getWidth() / 2) , (sprite.getHeight() / 2))
                                #         sprite.numberImage.convert()
                            
                                #     sprite.image.blit(sprite.numberImage , sprite.imageRect)
                                    
                                # elif map.revealMap[firstIndex][secondIndex] == 3:
                                    
                                #     turtleRect = map.turtleImage.get_rect()

                                #     scaled = pg.transform.scale(map.turtleImage , (int(sprite.width) , int(sprite.height)))

                                #     sprite.image.fill((0 , 0 , 0))
                                #     sprite.image.blit(scaled , turtleRect)
                                
                                # elif map.revealMap[firstIndex][secondIndex] == 0:
                                #     sprite.image.fill((255 , 255 , 255))

                                # map.revealAdjacent(sprite.index , 0)
                                map.revealAdjacentAlternate(sprite.index)
                                
                        for sprite in map.bombs:
                            if map.revealMap[sprite.index[0]][sprite.index[1]] != 3 and sprite.rect.collidepoint(location[0] , location[1]):
                                map.revealMap[sprite.index[0]][sprite.index[1]] = 2

                        # map.tiles.update(surface)
                        # map.bombs.update(surface)
                        shouldReveal0 = True
                                


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

                        # map.tiles.update(surface)
                        # map.bombs.update(surface)

                                


    return 0   

exitCode = main() 