# import modules
import math

import pygame
from pygame.locals import *

from .camera import Camera
from .entities import EntityManager
from .chunker import TileMap
from . import spritesheet_loader




class World():
    def __init__(self,game):
        # game
        self.game = game
        # camera
        self.camera = Camera(game)
        # tile map
        self.tile_map = TileMap([12,12], self.game.window.display.get_size())
        # load tile map
        self.tile_map.load_map(r'data\files\json\prototype\save_0.json')
        # entities manager
        self.entities = EntityManager(game)
        # set camera target pos
        self.camera.set_tracked_entity(self.entities.player)

    # update world attributes
    def update(self):
        self.entities.update()
        self.camera.update()

    # render tile map and entities
    def render(self):
        # visible tiles list for all groound tiles
        for layer in self.tile_map.get_visible(self.camera.pos):
            for tile in layer:
                offset = [0, 0]
                offset_dat =  self.game.assets.offset_dat
                if tile[1][0] in self.game.assets.offset_dat:
                    tile_id = str(tile[1][1]) + ';' + str(tile[1][2])
                    if tile_id in offset_dat[tile[1][0]]:
                        if 'tile_offset' in offset_dat[tile[1][0]][tile_id]:
                            offset = offset_dat[tile[1][0]][tile_id]['tile_offset']
                # tile is a the data from the specific key (tile) ------------------ #
                img = spritesheet_loader.get_img(self.game.assets.spritesheets, tile[1])
                self.game.window.display.blit(img,(tile[0][0] - self.camera.pos[0] + offset[0] ,tile[0][1] - self.camera.pos[1] + offset[1]))

        # render entities
        self.entities.render()
