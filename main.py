import pygame as pg
import time
import threading
import map
import menu

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

       if map.worldMap[sprite.index[0]][sprite.index[1]] == 0 and map.revealMap[sprite.index[0]][sprite.index[1]] == 1 and sprite.numberOfBombs == 0:
            
            if spread:

                pg.time.delay(delay)

            map.revealAdjacentAlternate(sprite.index)

            window.flip()

            shouldReveal0 = True
        
        # elif map.revealMap[sprite.index[0]][sprite.index[1]] == 1 and map.worldMap[sprite.index[0]][sprite.index[1]] == 0 and map.checkFlagCount(sprite.index) != sprite.numberOfBombs:
        #     map.revealAdjacentAlternate(sprite.index)
        
shouldReveal0 = False

def lossScreen():

    displaying = True

    surface = window.get_surface()

    rendered = False

    while displaying:

        if rendered == False:

            surface.fill((0 , 0 , 0))

            text = menu.serifFont.render("Game over!" , True , (255 , 255 , 255 , 0))
            text.convert_alpha()
            textRect = text.get_rect()
            textRect.center = (surface.get_size()[0] / 2 - textRect.width / 2 , surface.get_size()[1] / 2 - textRect.height / 2)

            surface.blit(text , textRect.center)

            playAgainText = menu.serifFont.render("Press R to play again or Q to quit." , True , (255 , 255 ,255))
            playAgainTextRect = playAgainText.get_rect()
            playAgainTextRect.center = (surface.get_size()[0] / 2 , surface.get_size()[1] / 3)
            playAgainText.convert_alpha()

            surface.blit(playAgainText , playAgainTextRect)

        window.update()
        
        events = pg.event.get()

        for event in events:

            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()

                if keys[pg.K_r]:
                    return True
                if keys[pg.K_q]:
                    return False

        


def main():

    global shouldReveal0

    global running

    window = pg.display
    window.set_caption("Minesweeper")
    window.set_mode((1600 , 900))
    map.turtleImage.convert_alpha()
    surface = window.get_surface()

    livesDisplay = menu.LivesDisplay(3)

    map.randomiseMap(16 , 16)
    map.displayMap(surface)

    map.turtleImage.convert_alpha()

    lives = 3

    shouldReveal0 = False
    firstClick = True

    while running:

        pg.time.delay(16)

        startTime = time.time()

        surface.fill((0 , 0 , 225))
        
        # map.displayMap(surface)

        # revealTime = time.time()
        map.bombs.update(surface)
        map.tiles.update(surface)
        
        menu.menuElements.update(surface)

        # print(time.time() - revealTime)

        map.bombs.draw(surface)
        map.tiles.draw(surface)
        menu.menuElements.draw(surface)

        window.update()

        keys = pg.key.get_pressed()
        events = pg.event.get()

        lives = 3 - checkNumberOfBombsOpen()

        livesDisplay.setLives(lives)

        # if lives <= 0:

        #     keepRunning = lossScreen()

        #     if keepRunning == True:
        #         firstClick = True
        #         map.randomiseMap(16 , 16)
        #         map.displayMap(surface)
        #     else:
        #         running = False
        
        # revealTime = time.time()
        # # revealAdjacent0(False , 2)
        # print(time.time() - revealTime)

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
                                print(sprite.numberOfBombs)
                                map.revealAdjacentAlternate(sprite.index)
                                
                        for sprite in map.bombs:
                            if firstClick == True and sprite.rect.collidepoint(location[0] , location[1]):
                                map.worldMap[sprite.index[0]][sprite.index[1]] = 0
                                map.revealMap[sprite.index[0]][sprite.index[1]] = 1
                                center = sprite.getCenter()
                                height = sprite.getHeight()
                                width = sprite.getWidth()
                                index = sprite.index

                                newTile = map.Tile(width , height , center , map.tiles , index , (255 , 255 , 255))
                                bombCount = map.checkBombCountAlternate(index)
                                newTile.numberOfBombs = bombCount
                                newTile.previousRevealed = -1

                                del sprite
                         
                                map.displayMap(surface)
                                firstClick = False

                                continue

                            if map.revealMap[sprite.index[0]][sprite.index[1]] != 3 and sprite.rect.collidepoint(location[0] , location[1]) and firstClick == False:
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
                
                if event.type == pg.KEYDOWN:

                    print("Pressed")

                    match event.key:
                        
                        case pg.K_b:
                            map.revealAll()

                        

        # print(time.time() - startTime)

                                


    return 0   

exitCode = main() 