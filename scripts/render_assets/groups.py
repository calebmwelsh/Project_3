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



class Groups():
    def __init__(self,app,renderer):
        self.app = app
        self.renderer = renderer
        self.init_obj()


    def init_obj(self):
        # groups objects (rects and buttons) ------------------------------------------- #
        # tab buttons
        self.groups_tab_1 = Button_text(font_1_white,'Home',(20,45),self.app,(182,141,90))
        self.groups_tab_2 = Button_text(font_1_white,'Schedule',(120,45),self.app,(182,141,90))
        self.groups_tab_3 = Button_text(font_1_white,'Homework',(220,45),self.app,(182,141,90))
        #self.tab_4 = Button_text(font_1_white,'Schedule',(20,50),self.app,(182,141,90))
        # ------------------------------------------------------------------------------ #

    '''
    -------------------------------------------- groups page ------------------------------------------------------------
    '''
    def render(self):
        # tabs
        if self.groups_tab_1.render(self.app.window.display):
            self.renderer.page = 'menu'
        if self.groups_tab_2.render(self.app.window.display):
            self.renderer.page = 'schedule'
        if self.groups_tab_3.render(self.app.window.display):
            self.renderer.page = 'homework'
