# import modules
import time
import pygame
from pygame.locals import *
from .config import config



class Window():
    def __init__(self, app):
        # start pyagme window
        pygame.init()
        # app
        self.app = app
        # retrieve config data
        self.scaled_res = config['window']['scaled_res']
        self.base_res = config['window']['base_res']
        self.offset = config['window']['offset']
        self.mouse_img = config['window']['mouse_img']
        self.icon_img = config['window']['icon_img']
        # scale ratio
        self.scaled_ratio = (self.scaled_res[0]/self.base_res[0],self.scaled_res[1]/self.base_res[1])
        # mouse display
        if self.mouse_img:
            pygame.mouse.set_visible(False)
        # icon set
        if self.icon_img:
            pygame.display.set_icon(self.icon_img)
        # create window
        self.window = pygame.display.set_mode(self.scaled_res,0,32)
        # create window surf
        self.display = pygame.surface.Surface(self.base_res)
        # set caption
        pygame.display.set_caption(config['window']['caption'])
        # dt and fps
        self.dt = .1
        self.frame_history = [0.01]
        self.frame_start = time.time()

    # return avg fps
    def fps(self):
        avg_dt = (sum(self.frame_history) / len(self.frame_history))
        avg_fps = 1 / avg_dt
        return avg_fps

    # render frame
    def render_frame(self):
        # display mouse img
        if self.mouse_img:
            true_mouse_pos = (self.app.input.mouse_pos[0] - self.offset[0] - self.app.world.camera.pos[0] - self.mouse_img.get_width() // 2,self.app.input.mouse_pos[1] -self.offset[1] - self.app.world.camera.pos[1] - self.mouse_img.get_height() // 2)
            self.display.blit(self.mouse_img,true_mouse_pos)
        # get display img data
        display_img = pygame.transform.scale(self.display,(int(self.display.get_width() * self.scaled_ratio[0]) , int(self.display.get_height() * self.scaled_ratio[1])))
        display_pos = (0 , 0 )
        # blit display img *
        self.window.blit(display_img,display_pos)
        # update display
        pygame.display.update()
        # fill screen
        self.display.fill(config['window']['background_color'])

        # dt and fps update
        self.dt = time.time() + .00001 - self.frame_start
        self.frame_start = time.time()
        self.frame_history.append(self.dt)
        self.frame_history = self.frame_history[-200:]


# key ----------------------------------------------------------------------------------------- #
# 1: everything after update is blit on top of whats above
