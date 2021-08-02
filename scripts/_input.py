# import modules
import sys
import pygame
from .config import config
#config = config.copy()
from pygame.locals import *

class Input():
    def __init__(self, app):
        # app
        self.app = app
        # all input states
        self.states = {}
        # mouse pos
        self.mouse_pos = (0,0)
        # input mode
        self.input_mode = 'core'
        # user input
        self.user_text = ''
        # reset all input states for initation
        self.full_reset()

    # reset all input states
    def full_reset(self):
        # keyboard
        peripheral = config['input']['keyboard']
        # iterate thorugh all keyboard events and reset all
        for binding in peripheral:
            self.states[binding] = False
        # mouse
        peripheral = config['input']['mouse']
        # iterate thorugh all mouse events and reset all
        for binding in peripheral:
            self.states[binding] = False

    # press reset
    def soft_reset(self):
        # keyboard or mouse
        peripheral = config['input']['keyboard']
        # iterate thorugh all keyboard events and reset all press type keyboard events
        for binding in peripheral:
            if peripheral[binding]['trigger'] == 'press':
                self.states[binding] = False

    # update input
    def update(self):
        # mouse pos
        x,y = pygame.mouse.get_pos()
        # scale mouse pos
        temp_x =  int( x / self.app.window.scaled_res[0] * self.app.window.base_res[0])
        temp_y =  int( y / self.app.window.scaled_res[1] * self.app.window.base_res[1])
        self.mouse_pos = (temp_x,temp_y)

        # soft reset
        self.soft_reset()

        # iterate through events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                # keyboard events
                if event.key == K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                    #center_val -= 12
                else:
                    self.user_text += event.unicode
                    #center_val += 12


            # screen events
            if event.type == VIDEORESIZE:
                self.app.window.window = pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)
