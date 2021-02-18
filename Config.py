'''
Import configurations from this class
'''

NUMBER_OF_BOTS = 10
NUMBER_OF_AI = 10
FPS = 60

# Screen dimensions
SCREEN = {
    'SIZE': (1600, 800) #(800, 600)
}

# 'Mask Dude', 'Ninja frog', 'Pink Man', 'Virtual Guy'
MAIN_CHARACTER =  {
    'NAME': ['Mask_Dude', 'Ninja_Frog', 'Pink_Man', 'Virtual_Guy'],
    'SIZE': (64, 64)
}

TERRAIN = {
    'NAME': ['Gray_Stone', 'Green_Dirt', 'Wood', 'Yellow_Dirt', 'Bricks', 'Leafs', 'Pink_Dirt'],
    'OFFSET': [0, 6, 88, 94, 105, 176, 182],
    'SIZE': (32, 32)
}

BACKGROUND = {
    'NAME': ['Blue', 'Brown', 'Gray', 'Green', 'Pink', 'Purple', 'Yellow'],
    'SIZE': (64, 64)
}

COLLECTIBLE = {
    'NAME': ['Apple'],
    'SIZE': (32,32)
}

CHECKPOINT = {
    'NAME': ['Flag'],
    'SIZE': (128,128)
}



