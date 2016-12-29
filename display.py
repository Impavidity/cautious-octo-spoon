import pygame
from pygame import gfxdraw
from pygame.locals import *
from sys import exit

class Display(object):
    def __init__(self):
        pass

    def setup(self):
        pygame.init()
        screen = pygame.display.set_mode((640,480), 0, 24)
        pygame.display.set_caption("Cautious")
        create = pygame.font.SysFont("comicsansms", 30)

    def update(self):
        pygame.display.update()

    def check_exit(self):
        for i in pygame.event.get():
            if i.type == QUIT:
                exit()

    def close(self):
        pygame.display.quit()
