import pygame
from .text import Font
from .core_fucs import *
from .render_assets.schedule import Schedule
from .render_assets.homework import Homework
from .render_assets.groups import Groups
from .render_assets.menu import Menu


COLORKEY = (0,0,0)

# fonts
font_1_gold = Font(r'data\font\font_image.png',(218,169,108),1)
font_1_white = Font(r'data\font\font_image.png',(230, 234, 214),1)
font_2_gold = Font(r'data\font\font_image.png',(218,169,108),2)


class Renderer():
    # renderer init
    def __init__(self,app):
        self.app = app
        self.schedule = Schedule(app,self)
        self.homework = Homework(app,self)
        self.groups = Groups(app,self)
        self.menu = Menu(app,self)
        self.page = 'menu'
        self.init_obj()


    '''
    ---------------------------------------------- rects and buttons inits ----------------------------------
    '''
    def init_obj(self):
        # header rect
        self.black_header = pygame.rect.Rect(0,30,self.app.window.display.get_width(),40)

    '''
    --------------------------------------------- constant render objects ---------------------------------------
    '''
    def perm_render(self):
        # header
        pygame.draw.rect(self.app.window.display,'black',self.black_header)
        # purdue advanced Learning
        font_2_gold.render('Purdue',self.app.window.display,(20,5))
        font_1_gold.render('Advance Learning',self.app.window.display,(100,7))
        font_1_gold.render('Application',self.app.window.display,(100,17))

    '''
    ---------------------------------------------- render ----------------------------------------------
    '''
    def render(self):
        # render world attributes
        self.app.world.render()
        # render constant objects
        self.perm_render()
        # menu page
        if self.page == 'menu':
            self.menu.render()
        # schedule page
        elif self.page == 'schedule':
            self.schedule.render()
        # homework page
        elif self.page == 'homework':
            self.homework.render()
        # groups page
        elif self.page == 'groups':
            self.groups.render()
