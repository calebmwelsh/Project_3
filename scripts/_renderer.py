import pygame
from .text import Font



class Renderer():
    def __init__(self,app):
        self.app = app


    def menu(self):
        white_tab = pygame.rect.Rect(0,30,self.app.window.display.get_width(),40)
        pygame.draw.rect(self.app.window.display,'white',white_tab)

    def render(self):
        self.app.world.render()
        self.menu()
