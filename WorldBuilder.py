'''
Contains the level basic class, Levels will inherit from this class to make a level
'''

import pygame as pg
import random
from Collectibles import Collectible
from Checkpoints import Checkpoint 
from itertools import chain
from AssetLoader import BACKGROUNDS, TERRAINS, COLLECTIBLES
from Config import SCREEN, MAIN_CHARACTER, TERRAIN, BACKGROUND, NUMBER_OF_BOTS, FPS, NUMBER_OF_AI
from itertools import chain
from WorldBuilderClasses import text

SCREEN_WIDTH, SCREEN_HIGHT = SCREEN['SIZE']

class Level():
    ''' Default level '''
    
    level_limit = -1000
    world_shift = 0
    tick = 0

    def __init__(self, lvl_type='Blue',  ter_type='Wood',worldNbr = 0):

        self.platforms = pg.sprite.Group()
        self.collectibles = pg.sprite.Group() 
        self.checkpoints = pg.sprite.Group()
        self.tempItems = pg.sprite.Group()
        self.level_type = lvl_type
        self.terrain_type = ter_type

        self.boxSize = None 
        self.gridSize = None 
        self.worldNbr = worldNbr

        #Load sprite groups from file
        self.generateSpritesFromFile()

        

    def _platforms(self):
        ''' Platform(width, height, x, y) '''

        ground = (5000, 96, self.level_limit, SCREEN_HIGHT - 64)
        left_block = (64, SCREEN_HIGHT-64, self.level_limit, 0)
        right_block = (64, SCREEN_HIGHT-500, 1600, 100)
        roof =(5000, 64, self.level_limit, - 64)
        wall = (96, 200, 1000, SCREEN_HIGHT - 550)
        big_block = (320, 160, 1200, SCREEN_HIGHT - 500)
        platform1 = (210, 70, 600, SCREEN_HIGHT - 200)
        platform2 = (210, 70, 600, SCREEN_HIGHT - 600)

        return [ground, left_block, right_block, roof, wall, big_block, platform1, platform2]

    def update(self,additionals = None):
        ''' Update everything '''

        self.platforms.update()
        self.collectibles.update()
        self.checkpoints.update()
        self.tempItems.update()

    def draw(self, screen):
        ''' Draw content on screen '''
        
        if self.tick == 60:
            self.tick = 0

        offset = (BACKGROUND['SIZE'][0]*(self.tick/60-1), BACKGROUND['SIZE'][0]*(self.tick/60-1))

        screen.blit(BACKGROUNDS[self.level_type], offset)

        self.platforms.draw(screen)
        self.collectibles.draw(screen)
        self.checkpoints.draw(screen)
        self.tempItems.draw(screen)

        self.tick += 1
    
    def shift_world(self, speed_x):
        ''' Scroll world '''

        self.world_shift += speed_x

        for item in chain(self.platforms,self.collectibles,self.checkpoints,self.tempItems):
            item.rect.x += speed_x

    def loadFromFile(self,lvl = 'Test.txt'):
        #Load file into matrix 
        f = open("Levels/"+lvl,'r')
        ret = []
        self.boxSize = int(f.readline()) 
        self.gridSize =(int(f.readline()),int(f.readline()))
        for entry in f:
            ret.append(entry.split())
        return ret 

    def generateSprites(self):

        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                widthP = 0 
                heightP = 0
                if self.board[row][column] == 'P' and self.board[row][column-1] != 'P' and self.board[row-1][column] != 'P': #Hittat ett övre vänster hörn 
                    i = column
                    k = row
                    while self.board[row][i] == 'P':
                        widthP += 32 
                        i+=1
                    while self.board[k][column] == 'P' and len(self.board) > k+1:
                        heightP += 32
                        k+=1


                    print(widthP,heightP)
                    self.platforms.add(Platform(widthP, heightP, column*self.boxSize, row*self.boxSize, 'Wood')) 
                           
                if self.board[row][column] == 'A': #Apple
                    self.collectibles.add(Collectible(column*self.boxSize,row*self.boxSize))
                if self.board[row][column] == 'F': #Flag
                    self.checkpoints.add(Checkpoint(column*self.boxSize,row*self.boxSize))

    def generateSpritesFromFile(self): 
        f = open("Levels/One/world"+str(self.worldNbr)+".txt",'r')
        for entry in f:
            data = entry.split()
            if "Platform" in entry: 
                self.platforms.add(Platform(int(data[2]), int(data[3]), int(data[0]), int(data[1])))
            if "Collectible" in entry: 
                self.collectibles.add(Collectible(int(data[0]), int(data[1])))
            if "Checkpoint" in entry: 
                self.checkpoints.add(Checkpoint(int(data[0]), int(data[1])))


    def save(self): 
        saveFile = open("Levels/One/world"+str(self.worldNbr)+".txt",'w')
        saveFile.write("32 \n") #Save of each box 
        saveFile.write("30 \n") #Save of each box 
        saveFile.write("30 \n") #Save of each box 

        for item in chain(self.platforms,self.collectibles,self.checkpoints):
            saveFile.write((str(item.rect.x)+" "+str(item.rect.y)+" "+str(item.image.get_width())+" "+str(item.image.get_height())+" "+str(type(item))+"\n"))

        saveFile.close()

    def savePlatforms(self): #Should only be used if the spritegroup platform contains sprites missing from board
        for plat in self.platforms: 
            print(plat.rect.x,plat.rect.y)
            x = int(plat.rect.x / 32)
            if x < 0: 
                x = 0
            y = int(plat.rect.y / 32)
            width = int(plat.image.get_width() / 32)
            height = int(plat.image.get_height() / 32)
            print(x,y,width,height)

            for i in range(int(width)): 
                for k in range(int(height)): 
                    if len(self.board) > x+i and len(self.board[0]) > y+k:
                        print(x+i,y+k)
                        self.board[y+k][x+i] = 'P'


class Platform(pg.sprite.Sprite):
    ''' Platform the player can jump on '''
 
    def __init__(self, width, height, x, y, ter_type='Wood'):
        
        super(Platform,self).__init__()
        width -= (width % TERRAIN['SIZE'][0])
        height -= (height % TERRAIN['SIZE'][1])
        self.image = pg.Surface([width, height])

        self._add_terrain(width, height, ter_type)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _add_terrain(self, width, height, ter_type):

        terrain = TERRAINS[ter_type]
        ter_w, ter_h = TERRAIN['SIZE']

        # Add fill to every square
        for w in range(0, width+1 , ter_w):
            for h in range(0, height+1 , ter_h):
                self.image.blit(random.choice(terrain['FILL']),(w,h))

        # Add tops and bottoms
        for w in range(0, width+1 , ter_w):
            self.image.blit(terrain['TOP'], (w, 0))
            self.image.blit(terrain['BOTTOM'], (w, height-ter_h))

        # Add left and rights
        for h in range(0, height+1 , ter_h):
            self.image.blit(terrain['LEFT'], (0, h))
            self.image.blit(terrain['RIGHT'], (width-ter_w, h))
        
        # Add corners 
        self.image.blit(terrain['TOP LEFT'], (0, 0))
        self.image.blit(terrain['TOP RIGHT'], (width-ter_w, 0))
        self.image.blit(terrain['BOTTOM LEFT'], (0, height-ter_h))
        self.image.blit(terrain['BOTTOM RIGHT'], (width-ter_w, height-ter_h))



def game_loop():
    #Variables 
    buildMode = "apple" #Decides what happens when mouse button is pressed 
    ongoingPlatform = False 
    platformX = 0
    platformY = 0
    mouseIsDown = False

    tempItem = None

    #Screen settings
    screen = pg.display.set_mode(SCREEN['SIZE'])
    pg.display.set_caption("Ai-game the world builder")

    # Create all the levels
    level_list = []
    for i in range(3):
        level_list.append(Level(lvl_type=random.choice(BACKGROUND['NAME']),ter_type=random.choice(TERRAIN['NAME']),worldNbr=i))

    current_level_no = 0
    current_level = level_list[current_level_no]

    #All the sprite groups in the game

    # Used to manage how fast the screen updates
    clock = pg.time.Clock()
 
    # -------- Main Program Loop -----------¨
    done = False
    while not done:
        for event in pg.event.get():

            #When game is over 
            if event.type == pg.QUIT:
                for lvl in level_list: 
                    lvl.save()
                    print("save made")
                done = True

            #All mouse actions 
            if event.type == pg.MOUSEBUTTONDOWN:
                mouseIsDown = True
                if event.button == 1:
                    if buildMode == "apple":
                        current_level.collectibles.add(Collectible(int(pg.mouse.get_pos()[0]//32)*32,int(pg.mouse.get_pos()[1]//32)*32))
                    if buildMode == "flag":
                        current_level.checkpoints.add(Checkpoint(int(pg.mouse.get_pos()[0]//32)*32-32,int(pg.mouse.get_pos()[1]//32)*32-128/2))
                    if buildMode == "platform" and not ongoingPlatform: 
                        platformX = (pg.mouse.get_pos()[0]//32)*32
                        platformY = (pg.mouse.get_pos()[1]//32)*32
                        ongoingPlatform = True 

                print(current_level_no,len(current_level.collectibles))


                if event.button == 3: 
                    if buildMode == "apple": 
                        for item in current_level.collectibles:
                            if item.rect.collidepoint(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1]):
                                current_level.collectibles.remove(item)
                    
                    if buildMode == "flag": 
                        for item in current_level.checkpoints:
                            if item.rect.collidepoint(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1]):
                                current_level.checkpoints.remove(item)

                    if buildMode == "platform": 
                        for item in current_level.platforms:
                            if item.rect.collidepoint(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1]):
                                current_level.platforms.remove(item)

            if event.type == pg.MOUSEBUTTONUP:
                mouseIsDown = False 
                if event.button == 1:
                    if buildMode == "platform" and ongoingPlatform: 
                        current_level.platforms.add(Platform(abs(platformX-(pg.mouse.get_pos()[0]//32)*32),abs(platformY-(pg.mouse.get_pos()[1]//32)*32),platformX,platformY))
                        ongoingPlatform = False 
                        current_level.tempItems.empty()

        #Handles keyboard 
        keys = pg.key.get_pressed()
        if keys:
            allActions = ''
            somethingDone = False 

            if keys[pg.K_LCTRL]:
                print("left control")
                if keys[pg.K_1]: 
                    print("1")
                    current_level_no = 0
                if keys[pg.K_2]: 
                    current_level_no = 1
                if keys[pg.K_3]: 
                    current_level_no = 2

            else: 
                if keys[pg.K_LEFT] or keys[pg.K_a]:
                    current_level.shift_world(10)
                if keys[pg.K_RIGHT] or keys[pg.K_d]:
                    current_level.shift_world(-10)
                if keys[pg.K_1]: 
                    print("platform")
                    buildMode = "platform"
                if keys[pg.K_2]: 
                    buildMode = "apple"
                    print("apple")
                if keys[pg.K_3]: 
                    buildMode = "flag"
                    print("flag")


            if keys[pg.K_q]: #To quit without saving 
                done = True 

        #To make a ghost of the item you are currently working with 
        current_level.tempItems.empty()
        if buildMode == "apple":
            current_level.tempItems.add(Collectible(int(pg.mouse.get_pos()[0]//32)*32,int(pg.mouse.get_pos()[1]//32)*32))
        if buildMode == "flag":
            current_level.tempItems.add(Checkpoint(int(pg.mouse.get_pos()[0]//32)*32-32,int(pg.mouse.get_pos()[1]//32)*32-128/2))
        if buildMode == "platform" and ongoingPlatform: 
            current_level.tempItems.add(Platform(abs(platformX-(pg.mouse.get_pos()[0]//32)*32),abs(platformY-(pg.mouse.get_pos()[1]//32)*32),platformX,platformY))

        #Changes level
        current_level = level_list[current_level_no]


        # Update the player and level.
        current_level.update(tempItem)


        # Calculate levelchange and what sprites to draw
        sprites_to_draw = pg.sprite.Group()

 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(FPS)
 
        # Go ahead and update the screen with what we've drawn.
        pg.display.flip()



def main():
    ''' Init pg and run game loop '''
    pg.init()
    game_loop()
    pg.quit()

if __name__ == '__main__':
    main()
        
        