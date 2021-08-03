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



class Homework():
    def __init__(self,app,renderer):
        self.app = app
        self.renderer = renderer
        self.init_obj()


    def init_obj(self):
        # homework objects (rects and buttons) ------------------------------------------- #
        # tab buttons
        self.homework_tab_1 = Button_text(font_1_white,'Home',(20,45),self.app,(182,141,90))
        self.homework_tab_2 = Button_text(font_1_white,'Schedule',(120,45),self.app,(182,141,90))
        self.homework_tab_3 = Button_text(font_1_white,'Groups',(220,45),self.app,(182,141,90))
        self.homework_tab_4 = Button_text(font_1_white,'Game',(320,45),self.app,(182,141,90))
        self.tabs = [self.homework_tab_1,self.homework_tab_2,self.homework_tab_3,self.homework_tab_4]

        # ------------------------------------------------------------------------------ #

    '''
    -------------------------------------------- homework page ------------------------------------------------------------
    '''
    def render(self):
        # tabs
        for i,tab in enumerate(self.tabs):
            if tab.render(self.app.window.display):
                self.app.renderer.page = tab.str.lower()

        # message
        font_2_gold.render('Homework Tab Coming Soon',self.app.window.display,(int(self.app.window.display.get_width() * .005 ),int(self.app.window.display.get_height() * .25 )))
