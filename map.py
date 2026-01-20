import pygame as pg
import random as rndm

# Empty Space 0 - 8
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

tiles = pg.sprite.Group()
bombs = pg.sprite.Group()

class Segment(pg.sprite.Sprite):

    def __init__(self , newWidth , newHeight , newCenter , groupToAdd , newIndex : tuple):
        pg.sprite.Sprite.__init__(self)
        self.width = newWidth
        self.height = newHeight
        self.center = newCenter
        self.image = pg.Surface((newWidth , newHeight) , pg.SRCCOLORKEY).convert()
        self.image.fill((255 , 255 , 255))
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

    def _init(self , newWidth , newHeight , newCenter , groupToAdd , newIndex):
        super.__init__(newWidth , newHeight , newCenter , groupToAdd , newIndex)

        self.numberOfBombs = 0
    
    def update(self , surface : pg.surface.Surface):
        
        self.numberOfBombs = checkBombCount(self.index)

        if self.revealed:
            self.numberOnFace = pg.font.SysFont("arial" , 60)
            
            surfaceText = self.numberOnFace.render(str(self.numberOfBombs) , True ,  (200 , 200 , 200) , (0 , 0 , 0))

            surfaceText.convert()
            surface.blit(surfaceText , self.getCenter())
            pg.display.flip()


class Bomb(Segment):
    
    def __init__(self, newWidth, newHeight, newCenter, groupToAdd , newIndex):
        super().__init__(newWidth, newHeight, newCenter, groupToAdd , newIndex)

        self.image.fill((255 , 255 , 255))

        # self.image.fill((30 , 0 , 0))



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

    segmentRect = pg.Rect(currentCenterx , currentCentery , widthOfSegment, heightOfSegment)
  
    for rowIndex in range(0 , worldMap.__len__()):

        for columnIndex in range(0 , worldMap[rowIndex].__len__()):

            match worldMap[rowIndex][columnIndex]:
                case 0:
                    newSegment = Tile(widthOfSegment , heightOfSegment , (currentCenterx , currentCentery) , tiles , (rowIndex , columnIndex))
                case 1:
                    newSegment = Bomb(widthOfSegment , heightOfSegment , (currentCenterx, currentCentery) , bombs , (rowIndex , columnIndex))

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
            worldMap[i].append(1)

def randomiseMap(rows , columns): # Uses dimensions

    worldMap.clear() # Remove all sprites to save memory
    
    for i in range(0 , rows):
        worldMap.append([])
        for number in range(0 , columns):
            worldMap[i].append(rndm.randint(0 , 1))
    
    print(worldMap)

def checkBombCount(index : tuple):

    topWallNull = False
    bottomWallNull = False
    leftWallNull = False
    rightWallNull = False

    if index[0] >= len(worldMap[0]): # Right Wall Null
        rightWallNull = True
    if index[0] == 0: # Left Wall Null
        leftWallNull = True
    if index[1] >= len(worldMap): # Bottom Wall Null
        bottomWallNull = True
    if index[1] == 0: # Top Wall Null
        topWallNull = True

    total = 0

    if rightWallNull: # Middle Right
        if worldMap[index[0] + 1][index[1]] == 1:
            total += 1
    if topWallNull and rightWallNull: # Top Right
        if worldMap[index[0] + 1][index[1] + 1] == 1:
            total += 1
    if topWallNull: # Top Middle
        if worldMap[index[0]][index[1] + 1]:
            total += 1
    if topWallNull and leftWallNull: # Top Left
        if worldMap[index[0] - 1][index[1] + 1]:
            total += 1
    if leftWallNull: # Middle Left
        if worldMap[index[0] - 1][index[1]]:
            total += 1
    if bottomWallNull and leftWallNull: # Bottom Left
        if worldMap[index[0] - 1][index[1] - 1]:
            total += 1
    if bottomWallNull: # Bottom Middle
         if worldMap[index[0]][index[1] - 1]:
            total += 1
    if bottomWallNull and rightWallNull: # Bottom Right
         if worldMap[index[0] + 1][index[1] - 1]:
            total += 1
    
    return total