import pygame
from ..text import Font
from ..text import Button_text
from ..text import Button_img
from ..core_fucs import *

COLORKEY = (0,0,0)

# fonts
font_1_gold = Font(r'data\font\font_image.png',(218,169,108),1)
font_1_white = Font(r'data\font\font_image.png',(230, 234, 214),1)
font_2_gold = Font(r'data\font\font_image.png',(218,169,108),2)



class Menu():
    def __init__(self,app,renderer):
        self.app = app
        self.renderer = renderer
        self.init_obj()


    '''
    ---------------------------------------------- rects and buttons inits ----------------------------------
    '''
    def init_obj(self):
        # menu objects (rects and buttons) ------------------------------------------- #
        # header rect
        self.black_header = pygame.rect.Rect(0,30,self.app.window.display.get_width(),40)
        # tab buttons
        self.menu_tab_1 = Button_text(font_1_white,'Schedule',(20,45),self.app,(182,141,90))
        self.menu_tab_2 = Button_text(font_1_white,'Homework',(120,45),self.app,(182,141,90))
        self.menu_tab_3 = Button_text(font_1_white,'Groups',(220,45),self.app,(182,141,90))
        #self.tab_4 = Button_text(font_1_white,'Schedule',(20,50),self.app,(182,141,90))

    '''
    -------------------------------------------- menu page ------------------------------------------------------------
    '''
    def render(self):
        # tabs
        if self.menu_tab_1.render(self.app.window.display):
            self.renderer.page = 'schedule'
        if self.menu_tab_2.render(self.app.window.display):
            self.renderer.page = 'homework'
        if self.menu_tab_3.render(self.app.window.display):
            self.renderer.page = 'groups'
