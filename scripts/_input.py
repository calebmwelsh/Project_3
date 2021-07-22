# import modules
import sys
import pygame
from .config import config
#config = config.copy()
from pygame.locals import *

class Input():
    def __init__(self, game):
        # game
        self.game = game
        # all input states
        self.states = {}
        # mouse pos
        self.mouse_pos = (0,0)
        # input mode
        self.input_mode = 'core'
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
        temp_x =  int( x / self.game.window.scaled_res[0] * self.game.window.base_res[0])
        temp_y =  int( y / self.game.window.scaled_res[1] * self.game.window.base_res[1])
        self.mouse_pos = (temp_x,temp_y)

        # soft reset
        self.soft_reset()

        # iterate through events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_b:
                    pygame.quit()
                    sys.exit()




            # keyboard events
            peripheral = config['input']['keyboard']
            # key down events
            if event.type == KEYDOWN:
                # binding: jump, moving right, moving left, ect
                for binding in peripheral:
                    # if mode is all or input mode == core
                    if set(peripheral[binding]['mode']).intersection({'all',self.input_mode}):
                            # if key is a press or hold
                            if peripheral[binding]['trigger'] in ['press','hold']:
                                # if key in config is in events set states to true
                                if event.key == peripheral[binding]['binding'][1]:
                                        self.states[binding] = True
            # key up events
            if event.type == KEYUP:
                # binding: jump, moving right, moving left, ect
                for binding in peripheral:
                    # if mode is all or input mode == core
                    if set(peripheral[binding]['mode']).intersection({'all',self.input_mode}):
                            # if key is a press or hold
                            if peripheral[binding]['trigger'] in ['press','hold']:
                                # if key in config is in events set states to true
                                if event.key == peripheral[binding]['binding'][1]:
                                        self.states[binding] = False
            # mouse events
            peripheral = config['input']['mouse']
            # mousedown events
            if event.type == MOUSEBUTTONDOWN:
                # binding: jump, moving right, moving left, ect
                for binding in peripheral:
                    # if mode is all or input mode == core
                    if set(peripheral[binding]['mode']).intersection({'all',self.input_mode}):
                            # if key is a press or hold
                            if peripheral[binding]['trigger'] in ['press','hold']:
                                # if key in config is in events set states to true
                                if event.button == peripheral[binding]['binding'][1]:
                                        self.states[binding] = True
            # mouseup events
            if event.type == MOUSEBUTTONUP:
                # binding: shoot, reload, change weapon ect
                for binding in peripheral:
                    # if mode is all or input mode == core
                    if set(peripheral[binding]['mode']).intersection({'all',self.input_mode}):
                            # if mouse button is a press or hold
                            if peripheral[binding]['trigger'] in ['press','hold']:
                                # if mouse button in config is in events set states to true
                                if event.button == peripheral[binding]['binding'][1]:
                                        self.states[binding] = False
