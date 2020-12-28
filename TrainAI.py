import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import tensorflow as tf 
from tensorflow import keras 

states = [] #left,right,jump,none,PL,PR
actions = []

def prepareData(): 
    files = os.listdir("Models/")
    for k,f in enumerate(files): 
        if "states" in f:
            print("In states file")
            openFile = open("Models/"+f) 
            for i,entry in enumerate(openFile): 
                print(i,entry)
                #add the previous action
                if i < 1: 
                    states.append([0,0,0,0])
                else: 
                    states.append(actions[k][-1])
                #add platforms 
                if entry == 'left': 
                    states[i] =[states[i],[1,0]]
                if entry == 'right': 
                    states[i] =[states[i],[0,1]]
            openFile.close()
            print(len(states))

        if "actions" in f:
            print("In actions file")
            openFile = open("Models/"+f) 
            for entry in openFile: 
                print(entry)
                if entry == 'left':
                    actions.append([1,0,0,0])
                if entry == 'right':
                    actions.append([0,1,0,0])
                if entry == 'jump':
                    actions.append([0,0,1,0])
                if entry == 'none':
                    actions.append([0,0,0,1])
            openFile.close()
            print(len(states))

def createModel(states = 6, actions = 3): #states=previous action (left,right,jump), platform position (3)
    model = keras.Sequential()
    model.add(keras.layers.Input(states))
    model.add(keras.layers.Dense(32,activation = 'relu'))
    model.add(keras.layers.Dense(actions,activation = 'softmax'))

def trainModel(model): 
    model.compile(loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

prepareData()
AI = createModel()