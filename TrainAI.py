import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import tensorflow as tf 
from tensorflow import keras 
import numpy as np

states = [] #prevleft,prevright,prevjump,prevnone,PL,PR
actions = [] #left,right,jump,none

test_cases=[]
test_cases.append([1,0,0,0,0,0])
test_cases.append([0,1,0,0,0,0])
test_cases.append([0,0,1,0,0,0])
test_cases.append([0,1,0,0,0,1])
test_cases.append([0,0,0,0,1,0])
test_cases.append([0,0,0,0,0,1])
test_cases.append([1,0,0,0,1,0])

def prepareData(): 
    directory = "Models/Itterative/"
    files = os.listdir(directory)
    print(files)

    for f in files: 
        print(f)
        if 'action' in f:
            #print("In actions file ",f)
            openFile = open(directory+f) 
            for entry in openFile: 
                #print(entry)
                actions.append([0,0,0,0])
                if entry.strip("\n") == 'left':
                    actions[-1][0] += 1
                if entry.strip("\n") == 'right':
                    actions[-1][1] += 1
                if entry.strip("\n") == 'jump':
                    actions[-1][2] += 1
                if entry.strip("\n") == 'none':
                    actions[-1][3] += 1
            openFile.close()
            #files.remove(f)

    for k,f in enumerate(files): 
        if "states" in f:
            index = 0 
            print("In states file")
            openFile = open(directory+f) 
            for i,entry in enumerate(openFile): 
                #print(i,entry)
                #add the previous action
                if index == 0: 
                    print("First states file")
                    states.append([0,0,0,0])
                else: 
                    states.append(actions[index-1])

                #add states (platforms)
                if entry.strip("\n") == 'PL': 
                    states[-1] =states[-1]+[1,0]
                if entry.strip("\n") == 'PR': 
                    states[-1] =states[-1]+[0,1]
                if entry.strip("\n") == 'None': 
                    states[-1] =states[-1]+[0,0]
                index+=1
            openFile.close()

    print("Actions len ",len(actions))
    print("States len: ",len(states))
    
    #Remove files so that new ones are generated 
    os.remove("Models/Itterative/actions1.txt")
    os.remove("Models/Itterative/actions2.txt")
    os.remove("Models/Itterative/actions3.txt")

    return(np.array(states),np.array(actions))

def createModel(nbr_inputs = 6, nbr_outputs = 4):
    if os.path.isfile("Models/model.h5"): 
        model = model = keras.models.load_model("Models/model.h5")
        print("Improving excisting model")
    else: 
        model = keras.Sequential()
        model.add(keras.layers.Input(nbr_inputs,name='Input layer'))
        #model.add(keras.layers.Dense(8,activation = 'relu'))
        model.add(keras.layers.Dense(nbr_outputs,activation = 'softmax',name='Output_layer'))

    return model

def trainModel(model,np_states,np_actions): 
    model.compile(
        loss='categorical_crossentropy',
        metrics=['accuracy'])

    model.summary()

    model.fit(
        x=np_states,
        y=np_actions,
        batch_size=32,
        verbose=1,
        validation_split=0.1,
        epochs=10)

def predict(model,data):
    return model.predict(data)


x,y = prepareData()
print(x,y)
AI = createModel()
print(AI.layers[0].input_shape)
trainModel(AI,x,y)
print(str(predict(AI,np.array(test_cases))))
print(AI.weights)

AI.save("Models/model.h5")