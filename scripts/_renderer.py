import pygame
from .text import Font


font_1 = Font(r'data\font\font_image.png',(218,169,108),1)
font_2 = Font(r'data\font\font_image.png',(218,169,108),2)


class Renderer():
    def __init__(self,app):
        self.app = app
        self.assign_rects()


    def assign_rects(self):
        self.white_tab = pygame.rect.Rect(0,30,self.app.window.display.get_width(),40)

    def menu(self):
        pygame.draw.rect(self.app.window.display,'white',self.white_tab)
        font_2.render('Purdue',self.app.window.display,(20,5))
        font_1.render('Advance Learning',self.app.window.display,(95,7))
        font_1.render('Application',self.app.window.display,(95,17))


    def render(self):
        self.app.world.render()
        self.menu()
