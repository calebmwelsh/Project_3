# Create a font
import pygame, sys, math
from pygame.locals import *
from .core_fucs import *


colorkey = (0, 0, 0)

def load_font_img(path,color,scale):
    global colorkey
    font_img = pygame.image.load(path)
    font_img = pygame.transform.scale(font_img,(font_img.get_width() * scale,font_img.get_height() * scale))
    img_list = []
    corners_list = []
    start_pos = 0
    for x in range(font_img.get_width()):
        c = font_img.get_at((x, 0))
        c = (c[0], c[1], c[2])
        if c == (200, 200, 200):
            c = font_img.get_at((x - 1, 0))
            c = (c[0], c[1], c[2])
            if c != (200, 200, 200):
                corner = ((start_pos, 0), (x, font_img.get_height()))
                start_pos = x + scale
                corners_list.append(corner)
    for corner in corners_list:
        width = abs(corner[0][0] - corner[1][0])
        height = abs(corner[0][1] - corner[1][1])
        img = clip(font_img, corner[0][0], corner[0][1], width, height)
        img = swap_color(img,(255, 0, 255),color)
        img.set_colorkey(colorkey)
        img_list.append((img, width))
    return img_list


class Font():
    def __init__(self, path,color=(255,255,255),scale=1):
        # font init
        self.scale = scale
        self.letter_imgs = load_font_img(path,color,scale)
        self.height = self.letter_imgs[0][0].get_height()
        self.order_list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '!',
            ':', '_', '.', '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0','-'
            ]


    # render text
    def render(self, str, surf, pos):
        offset = 0
        for char in str:
            if char in self.order_list:
                idx = self.order_list.index(char)
                img, width = self.letter_imgs[idx]
                surf.blit(img, (pos[0] + offset, pos[1]))
                offset += width + self.scale

    def get_size(self, str):
        self.text_size = 0
        for char in str:
            if char in self.order_list:
                idx = self.order_list.index(char)
                img, width = self.letter_imgs[idx]
                self.text_size += width + self.scale
        return self.text_size


    def get_rect(self,str,pos):
        width = self.get_size(str)
        height = self.letter_imgs[0][0].get_height()
        rect = pygame.rect.Rect(pos[0],pos[1],width, height)
        return rect



class Button():
    # button init
    def __init__(self,font,str,pos,app,color='black'):
        self.app = app
        self.font = font
        self.str = str
        self.rect_color = color
        self.rect = self.get_rect(str)
        self.rect.x,self.rect.y = pos[0],pos[1]
        # events
        self.click = False
        self.val = False

    # get rect based on str
    def get_rect(self,str):
        # get rect ------------------------------------ #

        # find length of str
        offset = 0
        for char in str:
            if char in self.font.order_list:
                idx = self.font.order_list.index(char)
                img, width = self.font.letter_imgs[idx]
                offset += width + self.font.scale

        #create surf for letter to blit
        self.surf = pygame.surface.Surface((offset,self.font.height))

        # blit letters on surf
        offset = 0
        for char in str:
            if char in self.font.order_list:
                idx = self.font.order_list.index(char)
                img, width = self.font.letter_imgs[idx]
                self.surf.blit(img, (offset, 0))
                offset += width + self.font.scale

        # colorkey
        self.surf = swap_color(self.surf,'black',self.rect_color)
        self.surf.set_colorkey(colorkey)

        return self.surf.get_rect()
        # ------------------------------------------------ #



    # render text as a button
    def render(self, display, rise=False):
        # button attributes
        action = False
        pos_area = False
        pos = pygame.mouse.get_pos()
        pos = (pos[0] / self.app.window.scaled_ratio[0], pos[1] / self.app.window.scaled_ratio[1])
        #print(pos)
        mouse = pygame.mouse.get_pressed()
        # if down and pos action true
        if self.rect.collidepoint(pos):
            pos_area = True
        if pos_area and self.click == False and mouse[0] == 1:
            self.click = True
            self.val = True
        if pos_area and self.val == True and mouse[0] == 0:
            action = True
        if mouse[0] == 1:
            self.click = True
        if mouse[0] == 0:
            self.click = False
            self.val = False

        # render rect
        #pygame.draw.rect(display,self.rect_color,self.rect)

        # render text
        if rise == True:
            if pos_area == True:
                display.blit(self.surf, (self.rect.x,self.rect.y - self.surf.get_size()[1] * .5))
            else:
                display.blit(self.surf, self.rect)
        elif rise == False:
            display.blit(self.surf, self.rect)
        return action
