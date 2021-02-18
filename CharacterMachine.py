
import pygame as pg
from Character import Character
from numpy.random import choice
from random import randint, choices
from Config import MAIN_CHARACTER
from functools import lru_cache
import time

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import tensorflow as tf 
from tensorflow import keras 
import numpy as np

class CharacterMachine(Character):
    ''' The main character sprite in the game '''

    width, height = MAIN_CHARACTER['SIZE'] 
    speed_x , speed_y = (0, 0)
    level = None
    tick = 1
    state = 'IDLE' # ['DOUBLE JUMP', 'FALL', 'HIT', 'IDLE', 'JUMP', 'RUN', 'WALL JUMP']
    state_img = 0
    direction = 'RIGHT' #['LEFT', 'RIGHT']
    double_jump = True
    

    def __init__(self, name='Bot1', character='Ninja frog'):
        super(CharacterMachine, self).__init__(name, character)
        self.model = keras.models.load_model("Models/model.h5")
        self.actionDict = {}

    def _tint_image(self):
        ''' Add a colored tint to image in order to make it destinct '''
        tint_color = self._get_tint()
        self.image = self.image.copy()
        self.image.fill(tint_color, None, pg.BLEND_RGBA_MULT)

    @lru_cache(maxsize=None)
    def _get_tint(self):
        return (randint(0,255), randint(0,255), randint(0,255))

    def makePrediction(self,AI): 
        ret = None

        lastAction = self.actions_made[-1]
        lastStates = []
        lastStates = self.states[-1]

        AIinput=[0,0,0,0]
        if lastAction.strip("\n") == 'left':
            AIinput[0] += 1
        if lastAction.strip("\n") == 'right':
            AIinput[1] += 1
        if lastAction.strip("\n") == 'jump':
            AIinput[2] += 1
        if lastAction.strip("\n") == 'none':
            AIinput[3] += 1

        if lastStates.strip("\n") == 'PL': 
            AIinput =AIinput+[1,0]
        if lastStates.strip("\n") == 'PR': 
            AIinput =AIinput+[0,1]
        if lastStates.strip("\n") == 'None': 
            AIinput =AIinput+[0,0]

        print(AIinput)
        AIinputString = " "
        for elm in AIinput:
            AIinputString += str(elm)
        print(AIinputString)

        if AIinputString in self.actionDict: 
            ret = self.actionDict[AIinputString]
        else: 
            start = time.time()
            self.actionDict[AIinputString] = AI.predict(np.array([AIinput]))
            #print("Prediction took: ",time.time()-start)
            ret = self.actionDict[AIinputString]
        
        ret = ret.tolist()
        return ret

    def predictAction(self):
        nextAction = [0,0,0,1]
        if len(self.actions_made) > 1: 
            nextAction = self.makePrediction(self.model)
            nextAction = nextAction[0]
            #nextAction[1] = nextAction[1] +0.5
            #print("Next action: ",nextAction)

        probabilityList = [x/sum(nextAction) for x in nextAction]
        action = choices([self.left,self.right,self.jump,self.none],
            k=1,
            weights=probabilityList
            )

        #When forcing 
        """
        action = choice([self.right,self.right,self.right,self.right],
            1,
            probabilityList
            )
        """
        action[0]()
        allActions = action[0].__name__
        self.actions_made.append(allActions)


