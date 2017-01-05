import pygame
from pygame import gfxdraw
from pygame.locals import *
from sys import exit

class Display(object):
    def __init__(self):
        self.screen = None
        self.key_num = [12,13,11,10]
        self.key = [["KEY_1","KEY_2","KEY_3","KEY_4","KEY_5","KEY_6","KEY_7","KEY_8","KEY_9","KEY_0","KEY_MINUS","KEY_EQUAL","KET_BACKSPACE"],
                    ["KEY_Q","KEY_W","KEY_E","KEY_R","KEY_T","KEY_Y","KEY_U","KEY_I","KEY_O","KEY_P","KEY_LEFTBRACE","KEY_RIGHTBRACE","KEY_BACKSLASH"],
                    ["KEY_A","KEY_S","KEY_D","KEY_F","KEY_G","KEY_H","KEY_J","KEY_K","KEY_L","KEY_SEMICOLON","KEY_APOSTROPHE"],
                    ["KEY_Z","KEY_X","KEY_C","KEY_V","KEY_B","KEY_N","KEY_M","KEY_COMMA","KEY_DOT","KEY_SLASH"]]
        # Picture Size = 1281, 721
        # Key Size = 57, 52
        self.start_position_v = [260]
        self.start_position_h = [200]
        self.width_slot = 15
        self.height_slot = 10
        for i in range(3):
            self.start_position_v.append(self.start_position_v[0]+(i+1)*(10+52))
            self.start_position_h.append(self.start_position_h[0]+(i+1)*(20))
        self.keyImage = dict()
        self.keyType = dict()
        self.key2pos = dict()
        

    def set_image(self, key):
        if key not in self.key2pos.keys():
            return
        v = self.start_position_v[self.key2pos[key][0]]
        h = self.start_position_h[self.key2pos[key][0]] + (self.key2pos[key][1] * (self.width_slot + 57))
        self.screen.blit(self.press, (h,v))


    def unset_image(self, key):
        if key not in self.key2pos.keys():
            return
        v = self.start_position_v[self.key2pos[key][0]]
        h = self.start_position_h[self.key2pos[key][0]] + (self.key2pos[key][1] * (self.width_slot + 57))
        self.screen.blit(self.keyImage[key], (h,v))


    def setupKey(self):
        with open("keytype.txt") as f:
            for line in f:
                (keyname, kType) = line.split()
                self.keyType[keyname] = int(kType)
        for i in range(4):
            for j in range(self.key_num[i]):
                if self.key[i][j] not in self.keyType.keys():
                    self.keyType[self.key[i][j]] = 2
        for i in range(4):
            for j in range(self.key_num[i]):
                self.key2pos[self.key[i][j]] = (i,j)
                if self.keyType[self.key[i][j]] == 0:
                    self.keyImage[self.key[i][j]] = pygame.image.load("picture/white.png").convert()
                if self.keyType[self.key[i][j]] == 1:
                    self.keyImage[self.key[i][j]] = pygame.image.load("picture/black.png").convert()
                if self.keyType[self.key[i][j]] == 2:
                    self.keyImage[self.key[i][j]] = pygame.image.load("picture/undefined.png").convert()
        self.press = pygame.image.load("picture/press.png").convert()

        for key,value in self.keyImage.items():
            v = self.start_position_v[self.key2pos[key][0]]
            h = self.start_position_h[self.key2pos[key][0]] + (self.key2pos[key][1] * (self.width_slot + 57))
            self.screen.blit(value, (h,v))



    def setup(self):
        pygame.init()
        self.img = pygame.image.load("picture/music.png")
        print self.img.get_size()
        self.screen = pygame.display.set_mode(self.img.get_size(), pygame.RESIZABLE)
        pygame.display.set_caption("Mr.Music")
        self.img = self.img.convert()
        self.screen.blit(self.img,(0,0))

    def update(self):
        pygame.display.update()


    def close(self):
        pygame.display.quit()
