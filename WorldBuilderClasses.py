import pygame as pg

class text():
<<<<<<< Updated upstream
    def __init__(self,text,x=0,y=0,size=50): 
        font = pg.font.SysFont(None,size) # use default system font, size 10
=======
    def __init__(self,text,x=0,y=0): 
        font = pg.font.SysFont(None,50) # use default system font, size 10
>>>>>>> Stashed changes

        self.text = text

        self.surf = font.render(text,False,(0,0,255))
        self.rect = self.surf.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.image = pg.sprite.Sprite() 
        self.image.image = self.surf
        self.image.rect = self.rect