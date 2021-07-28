'''button/text fuctions'''
# these functions and classes do not work with small pixel art !!!!
import csv
import os
import sys
import pygame
import random
from pygame.locals import *
# button class
# image turned button ------------------------ #
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.click = False
        self.val = False

    def draw(self,screen,rise=False):
        action = False
        pos_area = False
        pos = pygame.mouse.get_pos()
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

        if rise == True:
            if pos_area == True:
                screen.blit(self.image, (self.rect.x,self.rect.y - self.image.get_size()[1] * .5))
            else:
                screen.blit(self.image, self.rect)
        elif rise == False:
            screen.blit(self.image, self.rect)
        return action

class Button_text():
    def __init__(self, text, font, color, x, y):
        self.img = font.render(text, True, color)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.x_p = x
        self.mouse_over = self.x + 20
        self.mouse_over_rect = pygame.rect.Rect(x, y,self.width  + 20, self.height)
        self.rect_p = self.rect
        self.val = False
        self.click = False


    def draw(self, screen):
        action = False
        pos_area = False
        pos = pygame.mouse.get_pos()
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


        if pos_area == True:
            self.x = self.mouse_over
            self.rect = self.mouse_over_rect
        else:
            self.x = self.x_p
            self.rect = self.rect_p

        screen.blit(self.img, (self.x, self.y))
        return action

# picture frame with text and button and mouse over
class Button_frame():
    def __init__(self, text, font, color, x, y,color_fill,color_border,color_frame,color_over):
        self.img = font.render(text, True, color)
        self.x = x
        self.y = y
        self.color_fill = color_fill
        self.color_border = color_border
        self.color_frame = color_frame
        self.mouse_over = color_over
        self.saved_color = color_fill
        self.size = self.img.get_size()
        self.fill_val = (self.size[0] + self.size[1]) // 20
        self.border_val = (self.size[0] + self.size[1]) // 6
        self.frame_val = (self.size[0] + self.size[1]) // 3
        self.img_fill = pygame.transform.scale(self.img, (self.size[0] + self.fill_val, self.size[1] + self.fill_val))
        self.img_border = pygame.transform.scale(self.img, (self.size[0] + self.border_val, self.size[1] + self.border_val))
        self.img_frame = pygame.transform.scale(self.img, (self.size[0] + self.frame_val, self.size[1] + self.frame_val))
        self.img_rect_fill = self.img_fill.get_rect()
        self.img_rect_border = self.img_border.get_rect()
        self.img_rect_frame = self.img_frame.get_rect()
        self.img_rect_fill.x, self.img_rect_border.x, self.img_rect_frame.x = x - self.fill_val // 2, x - self.border_val // 2, x - self.frame_val // 2
        self.img_rect_fill.y, self.img_rect_border.y, self.img_rect_frame.y = y - self.fill_val // 2, y - self.border_val // 2, y - self.frame_val // 2
        self.click= False
        self.val = False

    def draw(self,screen):
        action = False
        pos_area = False
        pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()
        # if down and pos action true
        if self.img_rect_frame.collidepoint(pos):
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


        if self.val and pos_area == True:
            self.color_fill = self.mouse_over
        else:
            self.color_fill = self.saved_color
        # frame
        pygame.draw.rect(screen, self.color_frame, self.img_rect_frame)
        # border
        pygame.draw.rect(screen, self.color_border, self.img_rect_border)
        # fill
        pygame.draw.rect(screen, self.color_fill, self.img_rect_fill)
        screen.blit(self.img, (self.x, self.y))
        return action

#drawing text
'''def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)'''


def draw_text(text, font, color, x, y,screen):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

#picture frame with text
def draw_frame_w_text(text, font, color, x, y,color_fill,color_border,color_frame,screen):
    img = font.render(text, True, color)
    size = img.get_size()
    fill_val = (size[0] + size[1]) // 20
    border_val = (size[0] + size[1]) // 6
    frame_val = (size[0] + size[1]) // 3
    img_fill = pygame.transform.scale(img,(size[0] + fill_val,size[1] + fill_val))
    img_border = pygame.transform.scale(img,(size[0] + border_val,size[1] + border_val))
    img_frame = pygame.transform.scale(img, (size[0] + frame_val, size[1] + frame_val))
    img_rect_fill = img_fill.get_rect()
    img_rect_border = img_border.get_rect()
    img_rect_frame = img_frame.get_rect()
    img_rect_fill.x,img_rect_border.x,img_rect_frame.x = x - fill_val//2,x - border_val//2,x - frame_val//2
    img_rect_fill.y, img_rect_border.y,img_rect_frame.y = y - fill_val//2, y - border_val//2,y - frame_val//2
    #frame
    pygame.draw.rect(screen, color_frame, img_rect_frame)
    #border
    pygame.draw.rect(screen, color_border, img_rect_border)
    #fill
    pygame.draw.rect(screen,color_fill,img_rect_fill)
    screen.blit(img, (x, y))

#drawing text in the middle of screen
def display_mid(text = '',font ='',color='',image = '',rectx = ''):
    mid_screen = 465
    if image != '':
        img_wid = image.get_width()//2
        middle  = mid_screen - img_wid
        return middle
    elif text != '' and font != '':
        img = font.render(text, True, color)
        size = img.get_size()
        img_wid = size[0]//2
        middle = mid_screen - img_wid
        return middle

def get_size(text,font,color):
    img = font.render(text, True, color)
    size = img.get_size()
    return size[0]
