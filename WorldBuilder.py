import pygame as pg
from Config import SCREEN
from WorldBuilderClasses import text

pg.init()

screen = pg.display.set_mode(SCREEN['SIZE'])
screen.fill((0,255,0))
pg.display.set_caption("World builder")
fps = 60

sprites = pg.sprite.Group()

def main(): 
    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

            if event.type == pg.MOUSEBUTTONDOWN:
                asstest = text("Röööv",pg.mouse.get_pos()[0],pg.mouse.get_pos()[1])
                sprites.add(asstest.image)
                print(pg.mouse.get_pos())

        sprites.draw(screen)
        pg.display.flip()

main()