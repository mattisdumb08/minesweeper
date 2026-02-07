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

    map.randomiseMap(16 , 16) # Generate the map in the given dimensions and assign bombs based on a chance out of 100
    map.displayMap(surface) # Create all of the sprites and draw to the screen

    map.turtleImage.convert_alpha() # Make blits faster for image in map module

    lives = 3 # Number of lives to begin with

    shouldReveal0 = False
    firstClick = True

    while running:

        pg.time.delay(16)

        startTime = time.time()

        surface.fill((0 , 0 , 225)) # reset the window

        # Updating all sprites in the game

        map.bombs.update(surface)
        map.tiles.update(surface)
        
        menu.menuElements.update(surface)

        # print(time.time() - revealTime)

        # draw all of the sprites

        map.bombs.draw(surface)
        map.tiles.draw(surface)
        menu.menuElements.draw(surface)

        # display changes

        window.update()

        keys = pg.key.get_pressed()
        events = pg.event.get()

        lives = 3 - checkNumberOfBombsOpen()

        livesDisplay.setLives(lives)

        if lives <= 0:

            keepRunning = lossScreen()

            if keepRunning == True:
                firstClick = True
                map.randomiseMap(16 , 16)
                map.displayMap(surface)
            else:
                running = False
        
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
                            
                            clicked = sprite.rect.collidepoint(location[0] , location[1])

                            if clicked == False:
                                continue

                            if map.revealMap[sprite.index[0]][sprite.index[1]] != 3:
                                map.revealMap[sprite.index[0]][sprite.index[1]] = 1

                            if sprite.numberOfBombs == 0:
                                map.revealAdjacentAlternate(sprite.index)
                            
                            if sprite.flagCount + sprite.revealedAdjacentBombs == sprite.numberOfBombs:
                                map.revealTypeless(sprite.index)

                            # if map.revealMap[sprite.index[0]][sprite.index[1]] != 3 and 
                                
                        for sprite in map.bombs:

                            clicked = sprite.rect.collidepoint(location[0] , location[1])
                            
                            if firstClick == True and clicked:

                                map.worldMap[sprite.index[0]][sprite.index[1]] = 0
                                map.revealMap[sprite.index[0]][sprite.index[1]] = 1

                                map.revealAdjacentAlternate(sprite.index)

                                del sprite
                         
                                map.displayMap(surface)

                                continue

                            if map.revealMap[sprite.index[0]][sprite.index[1]] != 3 and clicked and firstClick == False:
                                map.revealMap[sprite.index[0]][sprite.index[1]] = 2
                            

                        # map.tiles.update(surface)
                        # map.bombs.update(surface)
                        shouldReveal0 = True
                        if firstClick == True:
                            firstClick = False
                                


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