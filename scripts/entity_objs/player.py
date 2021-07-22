# import modules
import pygame
from pygame.locals import *
from ..entity import Entity

class Player(Entity):
    def __init__(self,*args):
        super().__init__(*args)
        self.air_timer = 0
        self.vel = [0,0]

    # update player
    def update(self,dt):
        # motion ------------------------------------------------------------------------ #

        # increase air air timer
        self.air_timer += dt
        if self.game.input.states['jump']:
            self.vel[1] = -300
        # accounts for gravity and x input movement
        self.vel[1] = min(500, self.vel[1] + dt * 700)
        motion = self.vel.copy()
        if self.game.input.states['moving_right']:
            motion[0] += 120
        if self.game.input.states['moving_left']:
            motion[0] += -120
        motion[0] *= dt
        motion[1] *= dt

        if self.game.input.states['shoot']:
            print('bang')


        # collisions ---------------------------------------------------------------------- #

        # get potential near by collsions
        collisions = self.movement(motion, self.game.world.tile_map.get_near_by_rects(self.pos.copy()))

        if collisions['top'] or collisions['bottom']:
            self.vel[1] = 0
            self.air_timer = 0

        # animation ------------------------------------------------------------------------ #

        # gets animation action
        if self.air_timer > .07:
            self.set_action('jump')
        elif motion[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

        # determines to flip img or not
        if motion[0] > 0:
            self.flip[0] = False
        if motion[0] < 0:
            self.flip[0] = True

        # if not dead
        if not self.death:
            # update animation
            self.play(dt)

    # render player
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)
