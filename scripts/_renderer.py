import pygame
from .text import Font
from .text import Button


font_1_gold = Font(r'data\font\font_image.png',(218,169,108),1)
font_1_white = Font(r'data\font\font_image.png',(218,169,108),1)
font_2_gold = Font(r'data\font\font_image.png',(218,169,108),2)


class Renderer():
    def __init__(self,app):
        self.app = app
        self.init_objects()


    def init_objects(self):
        self.black_header = pygame.rect.Rect(0,30,self.app.window.display.get_width(),40)
        self.tab_1 = Button(font_1_white,'Schedule',(20,35),self.app,'blue')



    def menu(self):
        # header
        pygame.draw.rect(self.app.window.display,'white',self.black_header)
        # purdue advanced Learning
        font_2_gold.render('Purdue',self.app.window.display,(20,5))
        font_1_gold.render('Advance Learning',self.app.window.display,(95,7))
        font_1_gold.render('Application',self.app.window.display,(95,17))
        # tabs
        if self.tab_1.render(self.app.window.display):
            print(44)


    def render(self):
        self.app.world.render()
        self.menu()
