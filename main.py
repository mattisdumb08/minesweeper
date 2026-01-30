import pygame as pg
import map

# Reveal map Key = 1 revealed 0 is unrevealed 2 is a bomb that is revealed 3 is flagged

pg.init()

running = True

def shutdown():
   global running
   running = False

def main():

    global running

    window = pg.display
    window.set_caption("Minesweeper")
    window.set_mode((600 , 500) , pg.RESIZABLE)
    surface = window.get_surface()

    map.randomiseMap(16 , 16)
    map.displayMap(surface)

    micePress = [0 , 0 , 0]

    while running:

        surface.fill((0 , 0 , 0))
        
        # map.displayMap(surface)
        map.bombs.update(surface)
        map.tiles.update(surface)

        map.bombs.draw(surface)
        map.tiles.draw(surface)

        map.bombs.update(surface)
        map.tiles.update(surface)

        window.flip()

        keys = pg.key.get_pressed()

        events = pg.event.get()

        running = map.checkLoss()

        for event in events:

            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:

                mouses = pg.mouse.get_pressed() # Left, Middle , Right
                location = pg.mouse.get_pos()

                if mouses[0]:
                    micePress[0] = True

                    for sprite in map.tiles:
                        if map.revealMap[sprite.index[0]][sprite.index[1]] != 3 and sprite.rect.collidepoint(location[0] , location[1]):
                            print(sprite.index)
                            map.revealMap[sprite.index[0]][sprite.index[1]] = True
                    for sprite in map.bombs:
                        if map.revealMap[sprite.index[0]][sprite.index[1]] != 3 and sprite.rect.collidepoint(location[0] , location[1]):
                            map.revealMap[sprite.index[0]][sprite.index[1]] = 2
                            
                if mouses[2]:
                    
                    micePress[2] = True

                    sprite : map.Tile

                    for sprite in map.tiles:
                        if map.revealMap[sprite.index[0]][sprite.index[1]] == 0 and sprite.rect.collidepoint(location[0] , location[1]):
                            map.revealMap[sprite.index[0]][sprite.index[1]] = 3
                            print(sprite.index , " " , map.revealMap[sprite.index[0]][sprite.index[1]])
                        elif map.revealMap[sprite.index[0]][sprite.index[1]] == 3 and sprite.rect.collidepoint(location[0] , location[1]):
                            map.revealMap[sprite.index[0]][sprite.index[1]] = 0
                            print(sprite.index , " " , map.revealMap[sprite.index[0]][sprite.index[1]])
                    for sprite in map.bombs:
                        if map.revealMap[sprite.index[0]][sprite.index[1]] == 0 and sprite.rect.collidepoint(location[0] , location[1]):
                            map.revealMap[sprite.index[0]][sprite.index[1]] = 3
                            print(sprite.index , " " , map.revealMap[sprite.index[0]][sprite.index[1]])
                        elif map.revealMap[sprite.index[0]][sprite.index[1]] == 3 and sprite.rect.collidepoint(location[0] , location[1]):
                            map.revealMap[sprite.index[0]][sprite.index[1]] = 0
                            print(sprite.index , " " , map.revealMap[sprite.index[0]][sprite.index[1]])
                            


    return 0   

exitCode = main() 