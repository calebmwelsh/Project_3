# import modules
import math

import pygame
from pygame.locals import *

from .camera import Camera
#from .entities import EntityManager
#from .chunker import TileMap
from . import spritesheet_loader




class World():
    def __init__(self,app):
        # app
        self.app = app
        # camera
        self.camera = Camera(app)

    # update world attributes
    def update(self):
        pass

    # render
    def render(self):
        pass
