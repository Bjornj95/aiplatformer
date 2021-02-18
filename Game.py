'''
Runs the main game

Handles the main game logic

http://programarcadegames.com/python_examples/show_file.php?file=platform_scroller.py
'''

import pygame as pg
import random
import os
from Character import Character
from CharacterBot import CharacterBot
from CharacterMachine import CharacterMachine
from LevelLoader import Level
from Config import SCREEN, MAIN_CHARACTER, TERRAIN, BACKGROUND, NUMBER_OF_BOTS, FPS, NUMBER_OF_AI
from itertools import chain

SCREEN_WIDTH, SCREEN_HEIGHT  = SCREEN['SIZE'] #Detta är inte samma som i LevelLoader?!
global level_list 

def game_loop():
    ''' Main loop for the game engine '''

    screen = pg.display.set_mode(SCREEN['SIZE'])
    pg.display.set_caption("Ai-game")
 
    player = Character(character='Ninja_Frog')
    bots = [] #[CharacterBot(name=f'Bot{i}', character=random.choice(MAIN_CHARACTER['NAME'])) for i in range(NUMBER_OF_BOTS)]
    machines = [CharacterMachine(name=f'AI{i}', character=random.choice(MAIN_CHARACTER['NAME'])) for i in range(NUMBER_OF_AI)]
    finishedBots = 0 

    # Loads all the levels

    level_list = []
    for i in range(len(os.listdir("Levels/One"))):
        level_list.append(Level(player,lvl_type=random.choice(BACKGROUND['NAME']),ter_type=random.choice(TERRAIN['NAME']),worldNbr=i))

    current_level_no = 0
    current_level = level_list[current_level_no]

 
    active_sprite_list = pg.sprite.Group()

    for char in chain([player], bots, machines):
        char.level = current_level
        char.level_no = current_level_no
        char.rect.x = 340
        char.rect.y = SCREEN_HEIGHT / 4
        active_sprite_list.add(char)

    current_level.bots = bots + machines

 
    # Used to manage how fast the screen updates
    clock = pg.time.Clock()
 
    # -------- Main Program Loop -----------¨
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                for bot in chain(bots,[player],machines):
                    bot.quitSave()
                done = True

        if finishedBots > 2: 
            print("Exited because winners were found")
            for bot in chain(bots,[player],machines):
                bot.quitSave()
                
            done = True

        keys = pg.key.get_pressed()
        if keys:
            allActions = ''
            somethingDone = False 
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                player.left()
                allActions+="left"
                somethingDone = True 
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                player.right()
                allActions+="right"
                somethingDone = True 
            if keys[pg.K_SPACE]:
                player.jump()
                allActions+="jump"
                somethingDone = True 
            if not somethingDone: 
                allActions+="none"
            player.actions_made.append(allActions)    

        for bot in bots:
            bot.random_action()

        # Update the player and level.
        active_sprite_list.update()
        current_level.update()

        for machine in machines:
            machine.predictAction()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 200:
            diff = 200 - player.rect.left
            player.rect.left = 200
            current_level.shift_world(diff)

        # Calculate levelchange and what sprites to draw
        sprites_to_draw = pg.sprite.Group()
        for char in chain([player], bots, machines):

            # If any player gets to the end of the level, go to the next level
            current_position = char.rect.x + current_level.world_shift
            if char.is_finished(): #"current_position < current_level.level_limit or" 
                finishedBots += 1
                print("Finished bots: ",finishedBots)
                char.rect.x = 340
                char.rect.y = SCREEN_HEIGHT / 4
                if char.level_no < len(level_list)-1:

                    char.level_no += 1
                    char.level = level_list[char.level_no]
                    if type(char) == Character:
                        current_level_no += 1
                        current_level = level_list[current_level_no]
                else:
                    if type(char) == Character:
                        done = True

            if char.level == current_level:
                sprites_to_draw.add(char)
 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        #active_sprite_list.draw(screen)
        sprites_to_draw.draw(screen)
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
