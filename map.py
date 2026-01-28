import pygame as pg
import random as rndm

# Empty Space 0 - 8
# Revealed 9
# Bomb -1

worldMap = [

[1 , 1 , 1 , 1 , 1 , 0 , 1 , 1 , 1 , 1 , 1 , 1],
[1 , 0 , 0 , 1 , 1 , 0 , 0 , 0 , 0 , 1 , 1 , 1],
[1 , 0 , 1 , 1 , 1 , 0 , 0 , 0 , 0 , 3 , 1 , 1],
[1 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1],
[1 , 0 , 0 , 0 , 1 , 1 , 0 , 0 , 0 , 1 , 1 , 1],
[1 , 0 , 0 , 0 , 1 , 1 , 0 , 0 , 0 , 1 , 1 , 1],
[1 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1],
[1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1]

]

revealMap = [] # 0 unrevealed 1 reveled

tiles = pg.sprite.Group()
bombs = pg.sprite.Group()

class Segment(pg.sprite.Sprite):

    def __init__(self , newWidth , newHeight , newCenter , groupToAdd , newIndex : tuple ):
        pg.sprite.Sprite.__init__(self)
        self.width = newWidth
        self.height = newHeight
        self.center = newCenter
        self.image = pg.Surface((newWidth , newHeight) , pg.SRCCOLORKEY)
        # self.image.fill((255 , 255 , 255))
        # self.image.fill(colour)
        self.rect = pg.rect.Rect(newCenter[0] , newCenter[1] , newWidth , newHeight)
        self.index = newIndex

        self.revealed = False

        self.xCoord = newCenter[0]
        self.yCoord = newCenter[1]

        self.add(groupToAdd)

    def getCenter(self):
        return self.center
    def setCenter(self , newCenter):
        self.center = newCenter
        self.rect.center = self.center
    
    def getWidth(self):
        return self.width
    def setWidth(self , newWidth):
        self.width = newWidth

    def getHeight(self):
        return self.height
    def setHeight(self , newHeight):
        self.height = newHeight
    
    def update(self):
        pass

class Tile(Segment):

    def __init__(self , newWidth , newHeight , newCenter , groupToAdd , newIndex , colour):
        super().__init__(newWidth , newHeight , newCenter , groupToAdd , newIndex)
        self.image.fill(colour)
        self.numberOfBombs = 0

    def update(self , surface : pg.surface.Surface):
        
        self.numberOfBombs = checkBombCount(self.index)

        if revealMap[self.index[0]][self.index[1]] == 1:

            self.image.fill((100 , 100 , 100))

            text = pg.sysfont.SysFont("Serif" , 16 , True)
            image = text.render(str(self.numberOfBombs) , True , (0 , 200 , 0))
            imageRect = image.get_rect()
            imageRect.center = (self.center[0] + (self.getWidth() / 2) , self.center[1] + (self.getHeight() / 2))
            image.convert()
            surface.blit(image , imageRect)
        elif revealMap[self.index[0]][self.index[1]] == 3:
            self.image.fill((0 , 0 , 100))
            
class Bomb(Segment):
    
    def __init__(self, newWidth, newHeight, newCenter, groupToAdd , newIndex , newColour):
        super().__init__(newWidth, newHeight, newCenter, groupToAdd , newIndex)

        self.image.fill(newColour)

    def update(self , surface : pg.surface.Surface):

        if revealMap[self.index[0]][self.index[1]] == 2:
            self.image.fill((100 , 0 , 0))
        elif revealMap[self.index[0]][self.index[1]] == 3:
            self.image.fill((0 , 0 , 100))


rows = len(worldMap)
columns = len(worldMap[0])

def displayMap(surface : pg.surface.Surface):

    tiles.empty()
    bombs.empty()

    rows = len(worldMap)
    columns = len(worldMap[0])
    sizeOfSurface = surface.get_size()

    # widthOfSegment = sizeOfSurface / columns
    # heightOfSegment = sizeOfSurface / rows

    widthOfSegment = sizeOfSurface[0] / columns
    heightOfSegment = sizeOfSurface[1] / rows

    currentCenterx = 0
    currentCentery = 0
  
    for rowIndex in range(0 , worldMap.__len__()):

        for columnIndex in range(0 , worldMap[rowIndex].__len__()):

            match worldMap[rowIndex][columnIndex]:
                case 0:
                    newColour = (0 , 0 ,0)
                    if revealMap[rowIndex][columnIndex] == 1:
                        newColour = (100 , 100 , 100)
                    elif revealMap[rowIndex][columnIndex] == 3:
                        newColour = (0 , 0 , 100)
                    else:
                        newColour = (255 , 255 , 255)
                    tile = Tile(widthOfSegment , heightOfSegment , (currentCenterx , currentCentery) , tiles , (rowIndex , columnIndex) , newColour)
                    bombCount = checkBombCount(tile.index)
                    tile.numberOfBombs = bombCount
                    # tile.update(surface)
                    
                case 1:
                    colour = (255 , 255 , 255)
                    if revealMap[rowIndex][columnIndex] == 2:
                        colour = (100 , 0 , 0)
                    elif revealMap[rowIndex][columnIndex] == 3:
                        colour = (0 , 0 , 100)

                    Bomb(widthOfSegment , heightOfSegment , (currentCenterx, currentCentery) , bombs , (rowIndex , columnIndex) , colour)

            currentCenterx = currentCenterx + widthOfSegment + 1
            # print(segmentRect.center)
            # print( "r : " + str(rowIndex))
            # print("c : " + str(columnIndex))
        currentCenterx = 0
        currentCentery = currentCentery + heightOfSegment + 1
    
    bombs.draw(surface)
    tiles.draw(surface)

def defineMap(rows , columns):

    worldMap.clear() # Remove all sprites to save memory

    print("Define")

    for i in range(0 , rows):
        worldMap.append([])
        for number in range(0 , columns):
            worldMap[i].append([0])
    
    for i in range(0 , rows):
        revealMap.append([])
        for k in range(0 , columns):
            revealMap[i].append(0)

def randomiseMap(rows , columns): # Uses dimensions

    worldMap.clear() # Remove all sprites to save memory
    revealMap.clear()

    chance = 15 # Out of 100

    for i in range(0 , rows):
        worldMap.append([])
        for number in range(0 , columns):

            appendNumber = 0
            randomNumber = rndm.randint(0 , 100)

            if 0 <= randomNumber <= chance:
                appendNumber = 1
                print("Bomb planted")

            worldMap[i].append(appendNumber)

    for i in range(0 , rows):
        revealMap.append([])
        for k in range(0 , columns):
            revealMap[i].append(0)
    
def checkBombCount(index : tuple):




    topWallNull = False
    bottomWallNull = False
    leftWallNull = False
    rightWallNull = False

    if index[0] == len(worldMap[0]) - 1: # Right Wall Null
        rightWallNull = True
    if index[0] == 0: # Left Wall Null
        leftWallNull = True
    if index[1] == len(worldMap) - 1: # Bottom Wall Null
        bottomWallNull = True
    if index[1] == 0: # Top Wall Null
        topWallNull = True

    total = 0
    if not rightWallNull: # Middle Right
        if worldMap[index[0] + 1][index[1]] == 1:
            total += 1
    if  not (topWallNull or rightWallNull): # Top Right
        if worldMap[index[0] + 1][index[1] - 1] == 1:
            total += 1
    if not topWallNull: # Top Middle
        if worldMap[index[0]][index[1] - 1] == 1:
            total += 1
    if not (topWallNull or leftWallNull): # Top Left
        if worldMap[index[0] - 1][index[1] - 1] == 1:
            total += 1
    if not leftWallNull: # Middle Left
        if worldMap[index[0] - 1][index[1]] == 1:
            total += 1
    if not (bottomWallNull or leftWallNull): # Bottom Left
        if worldMap[index[0] - 1][index[1] + 1] == 1:
            total += 1
    if not bottomWallNull: # Bottom Middle
         if worldMap[index[0]][index[1] + 1] == 1:
            total += 1
    if not (bottomWallNull or rightWallNull): # Bottom Right
         if worldMap[index[0] + 1][index[1] + 1] == 1:
            total += 1

    return total

def checkLoss():
    sprite : Bomb

    for sprite in bombs:
        if revealMap[sprite.index[0]][sprite.index[1]] == 2:
            return True
    
    return False