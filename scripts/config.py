# import modules
import pygame
from pygame.locals import *


# mouse img
try:
    mouse_img = pygame.image.load(r'data\images\misc\mouse_img.png')
    mouse_img.set_colorkey((0,0,0))
except FileNotFoundError:
    mouse_img = None
# icon img
try:
    icon_img = pygame.image.load(r'data\images\misc\icon_img.png')
    icon_img.set_colorkey((0,0,0))
except FileNotFoundError:
    icon_img = None



# config data
config = {

        # types of config open -------------------------------------------------------------------------------------------- #

        # input for events

        'input':
                # input open ------------------------ #
                {
                # keyboard events
                'keyboard':
                    {
                    # jump
                    'jump':
                        {
                        # when key can be used
                        'mode':{'all','core'},
                        # binding key and pygame key
                        'binding': ['w',pygame.K_w],
                        # type of trigger
                        'trigger':'press'
                        },
                    # moving right
                    'moving_right':
                        {
                        # when key can be used
                        'mode':{'all'},
                        # binding key and pygame key
                        'binding': ['d',pygame.K_d],
                        # type of trigger
                        'trigger':'hold'
                        },
                    # moving left
                    'moving_left':
                        {
                        # when key can be used
                        'mode':{'all'},
                        # binding key and pygame key
                        'binding': ['a',pygame.K_a],
                        # type of trigger
                        'trigger':'hold'
                        },
                    # exit
                    'exit':
                        {
                        # when key can be used
                        'mode':{'all'},
                        # binding key and pygame key
                        'binding': ['b',pygame.K_b],
                        # type of trigger
                        'trigger':'press'
                        }
                    },
                    # keyboard close

                # mouse events
                'mouse':
                    {
                    # shoot
                    'shoot':
                        {
                        # when key can be used
                        'mode':{'all'},
                        # binding key and pygame key
                        'binding': ['left_button',1],
                        # type of trigger
                        'trigger':'press'
                        },
                    # shoot
                    'reload':
                        {
                        # when key can be used
                        'mode':{'all'},
                        # binding key and pygame key
                        'binding': ['left_button',1],
                        # type of trigger
                        'trigger':'press'
                        }
                    }
                    # mouse close
                },
                # input close ------------------------ #

        # window data

        'window':
                # window open ------------------------ #
                {
                # base resoultion
                'base_res': [ 300, 200 ],
                # scaled resoultion
                'scaled_res': 'full',
                # offset for screen
                'offset':[0,0],
                # capion for game
                'caption':'app',
                # background color
                'background_color' : (255, 255, 255),
                # mouse img
                'mouse_img': mouse_img,
                # icon img
                'icon_img': icon_img
                }
                # window close ------------------------ #


         }
        # types of config close ------------------------------------------------------------------------------------------ #
