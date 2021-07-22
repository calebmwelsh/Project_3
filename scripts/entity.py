# import modules
import pygame
import sys
from pygame.locals import *


# funcs
# return a list of collide tiles
def collision_test(player_rect, tile_rects):
    impact_list = []
    for tile in tile_rects:
        if player_rect.colliderect(tile):
            impact_list.append(tile)
    return impact_list


class Entity():
    def __init__(self, game, assets, pos, size, type):
        # game
        self.game = game
        # entity type ex - player,enemy,ect
        self.type = type
        # death
        self.death = False
        '''
        -------------------- Animation ------------------
        '''
        # anime_assets is a AnimationManager obj
        self.anime_assets = assets
        # the current folder or anime
        self.current_animation = None
        # current action
        self.action = None
        # img changes
        self.flip = [0, 0]
        self.opacity = 255
        self.scale = [1,1]
        # sets current animation to a default idle if in file directory -- #
        # warning if no idle anime must edit code --- #
        if self.type + '_idle' in self.anime_assets.animation_data:
            self.set_action('idle')
        '''
        ----------------------- physics ---------------------------
        '''
        # Physics Object pos
        self.pos = pos
        # Physics Object size
        self.size = size
        # centered object
        self.centered = True

    '''
   -------------------------------------------- physics ---------------------------------------
    '''

    # rect object
    @property
    def rect(self):
        if not self.centered:
            return pygame.rect.Rect(self.pos[0] // 1, self.pos[1] // 1, self.size[0], self.size[1])
        else:
            return pygame.rect.Rect((self.pos[0] - self.size[0] // 2) // 1, (self.pos[1]  - self.size[1] // 2) // 1, self.size[0], self.size[1])


    # center points
    @property
    def center(self):
        # if centered return pos
        if self.centered:
            return self.pos.copy()
        # if not centered return a centered pos of entity
        else:
            return [self.pos[0] + self.size[0]//2,self.pos[1] + self.size[1]//2]

    # player movement and collision aspects
    def movement(self, motion, tile_rects):
        collision_types = {i: False for i in ['top', 'bottom', 'right', 'left']}
        self.pos[0] += motion[0]
        # create a temp rect so x collisions is not affecting the y collisions
        temp_rect = self.rect
        impact_list = collision_test(self.rect, tile_rects)
        for tile in impact_list:
            if motion[0] > 0:
                temp_rect.right = tile.left
                self.pos[0] = temp_rect.x
                collision_types['right'] = True
            if motion[0] < 0:
                temp_rect.left = tile.right
                self.pos[0] = temp_rect.x
                collision_types['left'] = True
            if self.centered:
                self.pos[0] += self.size[0]//2
        self.pos[1] += motion[1]
        # create a temp rect so y collisions is not affecting the x collisions
        temp_rect = self.rect
        impact_list = collision_test(self.rect, tile_rects)
        for tile in impact_list:
            if motion[1] > 0:
                temp_rect.bottom = tile.top
                self.pos[1] = temp_rect.y
                collision_types['bottom'] = True
            if motion[1] < 0:
                temp_rect.top = tile.bottom
                self.pos[1] = temp_rect.y
                collision_types['top'] = True
            if self.centered:
                self.pos[1] += self.size[1]//2
        return collision_types


    '''
    ------------------------------------------------- animation ------------------------------------------------
    '''

    # retrieve img
    @property
    def img(self):
        if not self.current_animation:
            img = self.current_img
        else:
            self.set_image(self.current_animation.img)
            img = self.current_img
        # if any thing in self.flip is True
        if any(self.flip):
            img = pygame.transform.flip(img, self.flip[0], self.flip[1])
        if self.opacity != 255:
            img.set_alpha(self.opacity)
        if self.scale[0] > 1 or self.scale[1] > 1:
            img = pygame.transform.scale(img,(img.get_width() + self.scale[0],img.get_height() + self.scale[1]))
        return img

    # change action idle ,run, jump
    def set_action(self, anime_id):
        if anime_id != self.action:
            self.current_animation = self.anime_assets.loc_anime(self.type + '_' + anime_id)
        self.action = anime_id

    # set image
    def set_image(self, surf):
        self.current_img = surf.copy()
        self.dimensions = list(surf.get_size())

    # render
    def render(self, surf, offset=(0, 0)):
        offset = list(offset)
        if self.current_animation:
            # gets offset from config file
            offset[0] += self.current_animation.animation_data.config['offset'][0]
            offset[1] += self.current_animation.animation_data.config['offset'][1]
        if self.centered:
            # if centered pos
            offset[0] += self.img.get_width() // 2
            offset[1] += self.img.get_height() // 2
        surf.blit(self.img, ((self.pos[0] - offset[0]) //1, (self.pos[1] - offset[1])//1))

    # play animation
    def play(self, dt):
        if self.current_animation:
            self.current_animation.play(dt)
