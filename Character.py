import pygame as pg
from Config import SCREEN, MAIN_CHARACTER, FPS
from AssetLoader import ANIMATIONS_CHAR
import os 


SCREEN_HEIGHT, SCREEN_WIDTH = SCREEN['SIZE']

class Character(pg.sprite.Sprite):
    ''' The main character sprite in the game '''

    width, height = MAIN_CHARACTER['SIZE'] 
    speed_x , speed_y = (0, 0)
    level = None
    tick = 1
    state = 'IDLE' # ['DOUBLE JUMP', 'FALL', 'HIT', 'IDLE', 'JUMP', 'RUN', 'WALL JUMP']
    state_img = 0
    direction = 'RIGHT' #['LEFT', 'RIGHT']
    double_jump = True
    level = None
    level_no = 0

    def __init__(self, name='Player 1', character='Ninja frog'):
        super(Character, self).__init__()

        self.name = name
        self.character = character
        self.image = ANIMATIONS_CHAR[character][self.state][self.state_img]
        self.rect = self.image.get_rect()
        self.actions_made = []
        self.states = []
        self.points = 0 
        self.time_on_level = 0

    def update(self):
        ''' Update position, movementspeed and animation, called once every fps'''

        self._gravity()
        self._friction()
        self._move()
        self._collect()
        self._saveStates()

        # Update every 3
        if self.tick == 3:
            self.tick = 1
            self._animation_tick()
            self._tint_image()
        else:
            self.tick += 1

        self.time_on_level += 1/FPS #Used to give point depending on how fast level is completed 

    def _gravity(self):
        ''' NOT DONE TODO '''
        self.speed_y += 0.5
        if self.speed_y >= 0 and self.state in['JUMP', 'DOUBLE JUMP']:
            self._change_state('FALL')

        elif self.speed_y >= 2.0 and self.state in ['RUN', 'IDLE']:
            self._change_state('FALL')
        
        elif self.state == 'WALL JUMP':
            # Check if still near wall
            self.rect.x += 2
            collide_right = pg.sprite.spritecollide(self, self.level.platforms, False)
            self.rect.x -= 4 
            collide_left = pg.sprite.spritecollide(self, self.level.platforms, False)
            self.rect.x += 2
            if not collide_right and not collide_left :
                self._change_state('FALL')
            else:
                self.speed_y = 2

    def _friction(self):
        ''' Slow down in x '''

        if self.speed_x > 0.0:
            self.speed_x -= 0.5
        elif self.speed_x < 0.0:
            self.speed_x += 0.5
        
        if self.speed_x == 0.0 and self.state == 'RUN':
            self._change_state('IDLE')

    def _move(self):
        ''' Update coordinates in regards to speed and collitions '''
        
        self.rect.x += self.speed_x

        for block in pg.sprite.spritecollide(self, self.level.platforms, False):
            if self.speed_x > 0:
                self.rect.right = block.rect.left
                self.speed_x = 0
                if self.state == 'FALL':
                    self._change_state('WALL JUMP')
            else:
                self.rect.left = block.rect.right
                self.speed_x = 0
                if self.state == 'FALL':
                    self._change_state('WALL JUMP')

        self.rect.y += self.speed_y
        
        for block in pg.sprite.spritecollide(self, self.level.platforms, False):
            if self.speed_y > 0:
                self.rect.bottom = block.rect.top
                self.speed_y = 0
                if self.state in ['FALL', 'WALL JUMP']:
                    self._change_state('IDLE')
                    self.double_jump = True
            else:
                self.rect.top = block.rect.bottom
                self.speed_y = 0

    def _animation_tick(self):
        ''' Swap surface to next in animation '''
        animations = ANIMATIONS_CHAR[self.character][self.state]
        if self.state_img == len(animations):
            self.state_img = 0        
        
        # Flip image if heading left
        if self.direction == 'LEFT':
            self.image = pg.transform.flip(animations[self.state_img], True, False)
        else:
            self.image = animations[self.state_img]

        # Get next image next tick
        self.state_img += 1

    def _change_state(self, new_state):
        ''' Update state with different behavior'''

        self.state_img = 0
        self.state = new_state

    def jump(self):
        ''' 
        Jump button call
        
        Jump if on ground
        Double jump

         '''
        
        if self.state in ['IDLE', 'RUN','WALL JUMP']:
            self.speed_y = -10      
            if self.state == 'WALL JUMP':
                if self.direction == 'RIGHT':
                    self.speed_x = -15
                else:
                    self.speed_x = 15
            self._change_state('JUMP')
        elif self.state in ['FALL'] and self.double_jump:
            self.speed_y = -10
            self._change_state('DOUBLE JUMP')
            self.double_jump = False

    def right(self):
        ''' Move right button call '''
        if self.speed_x < 6.00:
            self.speed_x += 2.0
        self.direction = 'RIGHT'
        if self.state == 'IDLE':
            self._change_state('RUN')

    def left(self):
        ''' Move left button call '''
        if self.speed_x > -6.00:
            self.speed_x -= 2.0

        self.direction = 'LEFT'
        if self.state == 'IDLE':
            self._change_state('RUN')

    def none(self): #Dummy function 
        pass

    def _tint_image(self):
        ''' for subclasses to be able to tint '''
        pass

    def _collect(self):
        import Game

        for coin in pg.sprite.spritecollide(self, self.level.collectibles, False):
            self.level.collectibles.remove(coin)
            self.points += 10
            print(self.name, " has ",self.points," points.","(",self.level_no,")")

    def is_finished(self):
        for flag in pg.sprite.spritecollide(self, self.level.checkpoints, False):
            self.points += 50
            if 15 - self.time_on_level > 0:
                self.points += int(30 - self.time_on_level)
            self.time_on_level = 0
            print(self.name, " has ",self.points," points.","(",self.level_no,")")
            return True 

    def _saveStates(self): 
        platformFound = False 
        for platform in self.level.platforms: 
            if(abs(platform.rect.right - self.rect.left) < 100 and abs(platform.rect.bottom - self.rect.bottom) < 50):
                #print("Platform to your left")
                self.states.append("PL")
                platformFound = True
            if(abs(platform.rect.left - self.rect.right) < 100 and abs(platform.rect.bottom - self.rect.bottom) < 50):
                #print("Platform to your right")
                self.states.append("PR")
                platformFound = True
        if not platformFound:
            #print("No platform nearby")
            self.states.append('None')

    def quitSave(self): 
        if self.points > 50 and len(self.actions_made) == len(self.states):
            f_actions = open("Models/try2/score"+str(self.points)+"_actions.txt",'a')
            f_states = open("Models/try2/score"+str(self.points)+"_states.txt",'a')

            for action in self.actions_made: 
                f_actions.writelines(str(action))
                f_actions.writelines('\n')
            for state in self.states: 
                f_states.writelines(state)
                f_states.writelines('\n')

            f_actions.close()
            f_states.close() 

            """os.remove("Models/Itterative/actions1.txt")
            os.remove("Models/Itterative/actions2.txt")
            os.remove("Models/Itterative/actions3.txt") """

            if os.path.isfile("Models/Itterative/actions1.txt"):

                if os.path.isfile("Models/Itterative/actions2.txt"):

                    if os.path.isfile("Models/Itterative/actions3.txt"):
                        pass 
                    else: 
                        f_actions = open("Models/Itterative/actions3.txt",'w')
                        f_states = open("Models/Itterative/states3.txt",'w')

                        for action in self.actions_made: 
                            f_actions.writelines(str(action))
                            f_actions.writelines('\n')
                        for state in self.states: 
                            f_states.writelines(state)
                            f_states.writelines('\n')

                else: 
                    f_actions = open("Models/Itterative/actions2.txt",'w')
                    f_states = open("Models/Itterative/states2.txt",'w')

                    for action in self.actions_made: 
                        f_actions.writelines(str(action))
                        f_actions.writelines('\n')
                    for state in self.states: 
                        f_states.writelines(state)
                        f_states.writelines('\n')
            
            else: 
                f_actions = open("Models/Itterative/actions1.txt",'w')
                f_states = open("Models/Itterative/states1.txt",'w')

                for action in self.actions_made: 
                    f_actions.writelines(str(action))
                    f_actions.writelines('\n')
                for state in self.states: 
                    f_states.writelines(state)
                    f_states.writelines('\n')

            f_actions.close()
            f_states.close() 

            print("Save made")
        
        
if __name__ == '__main__':

    p = Character()
    pass