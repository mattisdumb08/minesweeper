import pygame as pg

pg.font.init()

serifFont = pg.sysfont.SysFont("Serif" , 50 , True)

menuElements = pg.sprite.Group()

class LivesDisplay(pg.sprite.Sprite):

    def __init__(self , newNumberOfLives):

        pg.sprite.Sprite.__init__(self)

        self.previousNumberOfLives = None
        self.numberOfLives = newNumberOfLives
        self.image = pg.surface.Surface(serifFont.size("Lives:" + str(newNumberOfLives)) , pg.SRCALPHA)
        self.text = serifFont.render( "Lives:" + str(newNumberOfLives) , True , (255 , 255 , 255))
        self.text.convert_alpha()
        self.rect = pg.Rect(0 , 0 , 200 , 100)

        self.image.fill((255 , 255 , 255 , 0))
        self.image.blit(self.text , self.rect.center)

        self.add(menuElements)

    def decrementLives(self):
        self.numberOfLives += 1
    def incrementLives(self):
        self.numberOfLives -= 1
    
    def setLives(self , newNumberOfLives):
        self.numberOfLives = newNumberOfLives

    def update(self , surfaceToDraw : pg.surface.Surface):
        
        if self.numberOfLives == self.previousNumberOfLives:
            return None
        self.text = serifFont.render("Lives:" + str(self.numberOfLives) , True , (255 , 255 , 255))
        self.text.convert_alpha()

        self.image.fill((255 , 255 , 255 , 0))
        self.image.blit(self.text , (0 ,0))