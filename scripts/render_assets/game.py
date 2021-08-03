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



class Game():
    def __init__(self,app):
        self.app = app
        self.init_obj()


    def init_obj(self):
        # homework objects (rects and buttons) ------------------------------------------- #
        # tab buttons
        self.game_tab_1 = Button_text(font_1_white,'Home',(20,45),self.app,(182,141,90))
        self.game_tab_2 = Button_text(font_1_white,'Schedule',(120,45),self.app,(182,141,90))
        self.game_tab_3 = Button_text(font_1_white,'Groups',(220,45),self.app,(182,141,90))
        self.game_tab_4 = Button_text(font_1_white,'Homework',(320,45),self.app,(182,141,90))
        self.tabs = [self.game_tab_1,self.game_tab_2,self.game_tab_3,self.game_tab_4]

        # ------------------------------------------------------------------------------ #


    def render(self):
        # tabs
        for i,tab in enumerate(self.tabs):
            if tab.render(self.app.window.display):
                self.app.renderer.page = tab.str.lower()



        
