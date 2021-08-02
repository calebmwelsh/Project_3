import pygame
from ...text import Font
from ...text import Button_text
from ...text import Button_img
from ...core_fucs import *

COLORKEY = (0,0,0)

# fonts
font_1_gold = Font(r'data\font\font_image.png',(218,169,108),1)
font_1_white = Font(r'data\font\font_image.png',(230, 234, 214),1)
font_2_gold = Font(r'data\font\font_image.png',(218,169,108),2)



class Current_Events():
    def __init__(self,app):
        self.app = app
        self.load_imgs()
        self.init_obj()


    def load_imgs(self):
        self.task_img = load_img(r'data\images\misc\schedule\add_task.png',COLORKEY)
        self.task_close_img = load_img(r'data\images\misc\schedule\close.png',COLORKEY)
        self.task_back_img = load_img(r'data\images\misc\schedule\back.png',COLORKEY)

    def init_obj(self):
        self.page = False




    '''
    --------------------------------------------------------------------------- current events page -------------------------------------------
    '''
    def render(self):
        if self.current_event_page[0]:
            # surf and outline of task page
            self.app.window.display.blit(self.task_page_outline,(self.app.window.display.get_width() // 4 - 2,self.app.window.display.get_height() // 5 - 2))
            self.app.window.display.blit(self.task_page_surf,(self.app.window.display.get_width() // 4 ,self.app.window.display.get_height() // 5))
            self.task_page_surf.fill((240, 255, 255))
            self.task_page_outline.fill((50,50,50))

            # render day str
            font_2_gold.render(self.days_data[self.new_event_page[2]][0],self.task_page_surf,(int(self.task_page_surf.get_width() * .1 ),5))
