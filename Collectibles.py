import pygame as pg
from Config import SCREEN, COLLECTIBLE
from AssetLoader import COLLECTIBLES

SCREEN_HEIGHT, SCREEN_WIDTH = SCREEN['SIZE']

class Collectible(pg.sprite.Sprite):
    ''' An apple '''

    width, height = COLLECTIBLE['SIZE'] 
    level = None
    tick = 1
    state_img = 0
    level = None
    level_no = 0

    def __init__(self, x,y, name='Coin', item='Apple'):
        super(Collectible, self).__init__()

        self.name = name
        self.item = item
        self.image = COLLECTIBLES[item][self.state_img]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y  


    def update(self):
        ''' Update position, movementspeed and animation, called once every fps'''

        # Update every 3
        if self.tick == 3:
            self.tick = 1
            self._animation_tick()
            self._tint_image()
        else:
            self.tick += 1

    def _animation_tick(self):
        ''' Swap surface to next in animation '''
        
        if self.state_img == len(COLLECTIBLES[self.item]):
            self.state_img = 0        

        self.image = COLLECTIBLES[self.item][self.state_img]
        # Get next image next tick
        self.state_img += 1

    def _change_state(self, new_state):
        ''' Update state with different behavior'''

        self.state_img = 0
        self.state = new_state

    def _tint_image(self):
        ''' for subclasses to be able to tint '''
        pass
        
if __name__ == '__main__':

    p = Coin()
    pass