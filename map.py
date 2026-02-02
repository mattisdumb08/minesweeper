import pygame as pg
import random as rndm

pg.font.init()

turtleName = "turtle.jpg"
turtleImage = pg.image.load(turtleName)

text = pg.sysfont.SysFont("Serif" , 16 , True)

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

    def setIndex(self , newIndex):
        self.index = newIndex
    def getIndex(self):
        return self.index
    
    def update(self):
        pass

class Tile(Segment):

    numberOfBombs = 0

    def __init__(self , newWidth , newHeight , newCenter , groupToAdd , newIndex , colour):
        super().__init__(newWidth , newHeight , newCenter , groupToAdd , newIndex)
        self.image.fill(colour)
        self.numberImage = None
        self.imageRect = None

    def update(self , surface : pg.surface.Surface):
        
        if revealMap[self.index[0]][self.index[1]] == 1 and self.numberOfBombs == 0:
            self.image.fill((100 , 100 , 100))

        elif revealMap[self.index[0]][self.index[1]] == 1:

            self.image.fill((100 , 100 , 100))

            imageRect : pg.Rect

            if self.numberImage == None:

                self.numberImage = text.render(str(self.numberOfBombs) , True , (0 , 0 , 0))
                self.imageRect = self.numberImage.get_rect()
                self.imageRect.center = ((self.getWidth() / 2) , (self.getHeight() / 2))
                self.numberImage.convert()
    
            self.image.blit(self.numberImage , self.imageRect)
            
        elif revealMap[self.index[0]][self.index[1]] == 3:
            
            turtleRect = turtleImage.get_rect()

            scaled = pg.transform.scale(turtleImage , (int(self.width) , int(self.height)))

            self.image.fill((0 , 0 , 0))
            self.image.blit(scaled , turtleRect)
        
        elif revealMap[self.index[0]][self.index[1]] == 0:
            self.image.fill((255 , 255 , 255))
            
class Bomb(Segment):
    
    def __init__(self, newWidth, newHeight, newCenter, groupToAdd , newIndex , newColour):
        super().__init__(newWidth, newHeight, newCenter, groupToAdd , newIndex)

        self.image.fill(newColour)

    def update(self , surface : pg.surface.Surface):

        if revealMap[self.index[0]][self.index[1]] == 0:
            self.image.fill((255 , 255 , 255))
        elif revealMap[self.index[0]][self.index[1]] == 2:
            self.image.fill((100 , 0 , 0))

        elif revealMap[self.index[0]][self.index[1]] == 3:
            # self.image.fill((0 , 0 , 100))
            self.image.fill((255 , 255 , 255))

            turtleRect = turtleImage.get_rect()

            scaled = pg.transform.scale(turtleImage , (int(self.width) , int(self.height)))

            self.image.blit(scaled , turtleRect)


rows = len(worldMap)
columns = len(worldMap[0])

def displayMap(surface : pg.surface.Surface):

    tiles.empty()
    bombs.empty()

    rows = len(worldMap)
    columns = len(worldMap[0])
    sizeOfSurface = (600 , 600)

    # widthOfSegment = sizeOfSurface / columns
    # heightOfSegment = sizeOfSurface / rows

    widthOfSegment = sizeOfSurface[0] / columns
    heightOfSegment = sizeOfSurface[1] / rows

    currentCenterx = (surface.get_size()[0] / 2) - (sizeOfSurface[0] / 2)
    currentCentery = (surface.get_size()[1] / 2) - (sizeOfSurface[1] / 2)
  
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
                    bombCount = checkBombCountAlternate(tile.getIndex())
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
        currentCenterx = (surface.get_size()[0] / 2) - (sizeOfSurface[0] / 2)
        currentCentery = (currentCentery + heightOfSegment + 1)
    
    # bombs.draw(surface)
    # tiles.draw(surface)

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

checkBombCount = None

def checkBombCountAlternate(index : tuple):
    xIndex = index[1]
    yIndex = index[0]

    total = 0

    for dx in [-1 , 0 , 1]:
        for dy in [-1 ,  0 , 1]:

            if dx == 0 and dy == 0:
                continue

            elif 0 <= xIndex + dx < len(worldMap[0]) and 0 <= yIndex + dy < len(worldMap):

                if worldMap[yIndex + dy][xIndex + dx] == 1:
                    total += 1
    
    return total

def checkFlagCount(index : tuple):
    xIndex = index[1]
    yIndex = index[0]

    total = 0

    for dx in [-1 , 0 , 1]:
        for dy in [-1 ,  0 , 1]:

            if dx == 0 and dy == 0:
                continue

            elif 0 <= xIndex + dx < len(revealMap[0]) and 0 <= yIndex + dy < len(revealMap):

                if revealMap[yIndex + dy][xIndex + dx] == 3:
                    total += 1
    
    return total   

def revealAdjacent(index :tuple , round : int | None): # what the fuck is this

    topWallNull = False
    bottomWallNull = False
    leftWallNull = False
    rightWallNull = False

    if round == None:
        round = 0

    if index[0] == len(revealMap[0]) - 1: # Right Wall Null
        rightWallNull = True
    if index[0] == 0: # Left Wall Null
        leftWallNull = True
    if index[1] == len(revealMap) - 1: # Bottom Wall Null
        bottomWallNull = True
    if index[1] == 0: # Top Wall Null
        topWallNull = True

    if round == 0:

        if not rightWallNull: # Middle Right
            numberOfBombs = checkBombCount((index[0] + 1 , index[1]))
            
            # if numberOfBombs == 0:
            #     revealAdjacent((index[0] + 1 , index[1]) , 0)

            if revealMap[index[0] + 1][index[1]] == 0 and numberOfBombs == 0 and worldMap[index[0] + 1][index[1]] == 0:
                revealMap[index[0] + 1][index[1]] = 1

                revealAdjacent((index[0] + 1 , index[1]) , 2)

        if  not (topWallNull or rightWallNull): # Top Right
            numberOfBombs = checkBombCount((index[0] + 1 , index[1] - 1))

            # if numberOfBombs == 0:
            #     revealAdjacent((index[0] + 1 , index[1] - 1) , 0)

            if revealMap[index[0] + 1][index[1] - 1] == 0 and numberOfBombs == 0 and worldMap[index[0] +1][index[1] - 1] == 0:
                revealMap[index[0] + 1][index[1] - 1] = 1
                revealAdjacent((index[0] + 1 , index[1] - 1) , 2)

        if not topWallNull: # Top Middle
            numberOfBombs = checkBombCount((index[0] , index[1] - 1))

            # if numberOfBombs == 0:
            #     revealAdjacent((index[0] , index[1] - 1) , 0)

            if revealMap[index[0]][index[1] - 1] == 0 and numberOfBombs == 0 and worldMap[index[0]][index[1] - 1] == 0:
                revealMap[index[0]][index[1] - 1] = 1
                revealAdjacent((index[0] , index[1] - 1) , 2)

        if not (topWallNull or leftWallNull): # Top Left
            numberOfBombs = checkBombCount((index[0] - 1 , index[1] - 1))

            # if numberOfBombs == 0:
            #     revealAdjacent((index[0] - 1 , index[1] - 1) , 0)

            if revealMap[index[0] - 1][index[1] - 1] == 0 and numberOfBombs == 0 and worldMap[index[0] - 1][index[1] - 1] == 0:
                revealMap[index[0] - 1][index[1] - 1] = 1
                revealAdjacent((index[0] - 1 , index[1] - 1) , 2)

        if not leftWallNull: # Middle Left
            numberOfBombs = checkBombCount((index[0] - 1 , index[1]))

            # if numberOfBombs == 0:
            #     revealAdjacent((index[0] - 1 , index[1]) , 0)
            
            if revealMap[index[0] - 1][index[1]] == 0 and numberOfBombs == 0 and worldMap[index[0] - 1][index[1]] == 0:
                revealMap[index[0] - 1][index[1]] = 1
                revealAdjacent((index[0] - 1 , index[1]) , 2)

        if not (bottomWallNull or leftWallNull): # Bottom Left
            numberOfBombs = checkBombCount((index[0] - 1 , index[1] + 1))
            # if numberOfBombs == 0:
            #     revealAdjacent((index[0] - 1 , index[1] + 1) , 0)

            if revealMap[index[0] - 1][index[1] + 1] == 0 and numberOfBombs == 0 and worldMap[index[0] - 1][index[1] + 1] == 0:
                revealMap[index[0] - 1][index[1] + 1] = 1
                revealAdjacent((index[0] - 1 , index[1] + 1) , 2)

        if not bottomWallNull: # Bottom Middle
            numberOfBombs = checkBombCount((index[0] , index[1] + 1))

            # if numberOfBombs == 0:
            #     revealAdjacent((index[0] , index[1] + 1) , 0)

            if revealMap[index[0]][index[1] + 1] == 0 and numberOfBombs == 0 and worldMap[index[0]][index[1] + 1] == 0:
                revealMap[index[0]][index[1] + 1] = 1
                revealAdjacent((index[0] , index[1] + 1) , 2)

        if not (bottomWallNull or rightWallNull): # Bottom Right
            numberOfBombs = checkBombCount((index[0] + 1 , index[1] + 1))

            # if numberOfBombs == 0:
            #     revealAdjacent((index[0] + 1 , index[1] + 1) , 0)

            if revealMap[index[0] + 1][index[1] + 1] == 0 and numberOfBombs == 0 and worldMap[index[0] + 1][index[1] + 1] == 0:
                revealMap[index[0] + 1][index[1] + 1] = 1
                revealAdjacent((index[0] + 1, index[1] + 1) , 2)
    
    elif round == 2:

        if not rightWallNull: # Middle Right
            numberOfBombs = checkBombCount((index[0] + 1 , index[1]))
            if revealMap[index[0] + 1][index[1]] == 0 and worldMap[index[0] + 1][index[1]] == 0:
                revealMap[index[0] + 1][index[1]] = 1


        if  not (topWallNull or rightWallNull): # Top Right
            numberOfBombs = checkBombCount((index[0] + 1 , index[1] - 1))
            if revealMap[index[0] + 1][index[1] - 1] == 0 and worldMap[index[0] +1][index[1] - 1] == 0:
                revealMap[index[0] + 1][index[1] - 1] = 1

        if not topWallNull: # Top Middle
            numberOfBombs = checkBombCount((index[0] , index[1] - 1))
            if revealMap[index[0]][index[1] - 1] == 0 and worldMap[index[0]][index[1] - 1] == 0:
                revealMap[index[0]][index[1] - 1] = 1

        if not (topWallNull or leftWallNull): # Top Left
            numberOfBombs = checkBombCount((index[0] - 1 , index[1] - 1))
            if revealMap[index[0] - 1][index[1] - 1] == 0 and worldMap[index[0] - 1][index[1] - 1] == 0:
                revealMap[index[0] - 1][index[1] - 1] = 1

        if not leftWallNull: # Middle Left
            numberOfBombs = checkBombCount((index[0] - 1 , index[1]))
            if revealMap[index[0] - 1][index[1]] == 0 and worldMap[index[0] - 1][index[1]] == 0:
                revealMap[index[0] - 1][index[1]] = 1

        if not (bottomWallNull or leftWallNull): # Bottom Left
            numberOfBombs = checkBombCount((index[0] - 1 , index[1] + 1))
            if revealMap[index[0] - 1][index[1] + 1] == 0 and worldMap[index[0] - 1][index[1] + 1] == 0:
                revealMap[index[0] - 1][index[1] + 1] = 1

        if not bottomWallNull: # Bottom Middle
            numberOfBombs = checkBombCount((index[0] , index[1] + 1))
            if revealMap[index[0]][index[1] + 1] == 0 and worldMap[index[0]][index[1] + 1]:
                revealMap[index[0]][index[1] + 1] = 1

        if not (bottomWallNull or rightWallNull): # Bottom Right
            numberOfBombs = checkBombCount((index[0] + 1 , index[1] + 1))
            if revealMap[index[0] + 1][index[1] + 1] == 0 and worldMap[index[0] + 1][index[1] + 1] == 0:
                revealMap[index[0] + 1][index[1] + 1] = 1

revealAdjacent = None

def revealAdjacentAlternate(index : tuple):
    xIndex = index[1]
    yIndex = index[0]

    for dx in [-1 , 0 , 1]:
        for dy in [-1 , 0 , 1]:
            if dx == 0 and dy == 0:
                continue
            
            newXIndex = xIndex + dx
            newYIndex = yIndex + dy

            if 0 <= newXIndex < len(worldMap[0]) and 0 <= newYIndex < len(worldMap):

                if worldMap[newYIndex][newXIndex] == 0 and revealMap[newYIndex][newXIndex] == 0 and checkBombCountAlternate(index) == 0:
                    revealMap[newYIndex][newXIndex] = 1

                # if worldMap[newYIndex][newXIndex] == 0 and checkBombCountAlternate((yIndex , xIndex)) == 0:
                #     revealAdjacentAlternate((newYIndex , newXIndex))

def checkLoss():

    sprite : Bomb

    for sprite in bombs:
        if revealMap[sprite.index[0]][sprite.index[1]] == 2:
            return False
    
    return True