import pygame as pg
import random as rndm

# Empty Space 0 - 8
# Bomb -1

worldMap=[

[1 , 1 , 1 , 1 , 1 , 0 , 1 , 1 , 1 , 1 , 1 , 1],
[1 , 0 , 0 , 1 , 1 , 0 , 0 , 0 , 0 , 1 , 1 , 1],
[1 , 0 , 1 , 1 , 1 , 0 , 0 , 0 , 0 , 3 , 1 , 1],
[1 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1 , 1],
[1 , 0 , 0 , 0 , 1 , 1 , 0 , 0 , 0 , 1 , 1 , 1],
[1 , 0 , 0 , 0 , 1 , 1 , 0 , 0 , 0 , 1 , 1 , 1],
[1 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 1 , 1],
[1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1]

]

segments = pg.sprite.Group()
bombs = pg.sprite.Group()

class Segment(pg.sprite.Sprite):

    def __init__(self , newWidth , newHeight , newCenter , groupToAdd):
        pg.sprite.Sprite.__init__(self)
        self.width = newWidth
        self.height = newHeight
        self.center = newCenter
        self.image = pg.Surface((newWidth , newHeight) , pg.SRCCOLORKEY).convert()
        self.image.fill((255 , 255 , 255))
        self.rect = pg.rect.Rect(newCenter[0] , newCenter[1] , newWidth , newHeight)

        self.xCoord = newCenter[0]
        self.yCoord = newCenter[1]

        self.bombNumber = 0

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

class Bomb(Segment):
    def __init__(self, newWidth, newHeight, newCenter, groupToAdd):
        super().__init__(newWidth, newHeight, newCenter, groupToAdd)
        self.image.fill((30 , 0 , 0))



rows = len(worldMap)
columns = len(worldMap[0])

def displayMap(surface : pg.surface.Surface):

    segments.empty()
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
                    newSegment = Segment(widthOfSegment , heightOfSegment , (currentCenterx , currentCentery) , segments)
                case 1:
                    newSegment = Bomb(widthOfSegment , heightOfSegment , (currentCenterx, currentCentery) , bombs)

            currentCenterx = currentCenterx + widthOfSegment + 1
            # print(segmentRect.center)
            # print( "r : " + str(rowIndex))
            # print("c : " + str(columnIndex))
        currentCenterx = 0
        currentCentery = currentCentery + heightOfSegment + 1
    
    bombs.draw(surface)
    segments.draw(surface)

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

def checkBOOOOOOOOOOOOOOOOM(index : tuple):
    total = 0

    if worldMap[index[0] + 1][index[1]] == 1: # Middle Right
        total += 1
    if worldMap[index[0] + 1][index[1] + 1] == 1: # Top Right
        total += 1
    if worldMap[index[0]][index[1] + 1]: # Top Middle
        total += 1
    if worldMap[index[0] - 1][index[1] + 1]: # Top Left
        total += 1
    if worldMap[index[0] - 1][index[1]]: # Middle Left
        total += 1
    if worldMap[index[0] - 1][index[1] - 1]: # Bottom Left 
        total += 1
    if worldMap[index[0]][index[1] - 1]: # Bottom Middle
        total += 1
    if worldMap[index[0] + 1][index[1] - 1]: # Bottom Right
        total += 1