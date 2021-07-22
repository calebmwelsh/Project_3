# Setup pygame/window ---------------------------------------- #
import pygame, sys, math, random
from pygame.locals import *
import scripts.text as text


# might need to be modified depending on game
def x_varience(type,i,scale,game_time,scroll=[0,0]):
    if type == None:
        return 0
    elif type == 'b':
        # x varience str base - b
        return math.sin((game_time + i * 120) / 4) * scale
    elif type == 's':
        # x varience str fog shake - s
        return math.sin((game_time + i * 120) / 1) * scale
    elif type == 'sw':
        # x varience str fog sway - sw
        return math.sin((game_time  + i * 60) / 9) * scale
    elif type == 'pr':
        # x varience str fog point then round - pr
        return math.sin((game_time  + i * 3) / 4) * scale
    elif type == 'p_r':
        # x varience str fog point to round p_r
        return math.sin((game_time  + i * 4) / 4) * scale
    elif type == 'p':
        # x varience str fog paralax - p
        return math.sin((game_time  + i * 130 - scroll[0] * .5 ) / 10) * scale
