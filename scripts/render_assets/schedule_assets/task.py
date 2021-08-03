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



class Task():
    def __init__(self,app):
        self.app = app
        self.load_imgs()
        self.init_obj()


    def load_imgs(self):
        self.close_img = load_img(r'data\images\misc\schedule\close.png',COLORKEY)
        self.back_img = load_img(r'data\images\misc\schedule\back.png',COLORKEY)

    def init_obj(self):
        # task open close var
        self.page = False
        # task page surface and outline
        self.page_surf = pygame.surface.Surface((self.app.window.display.get_width() // 2 ,self.app.window.display.get_height() // 1.5 ))
        self.page_surf.fill((240, 255, 255))
        self.page_outline = pygame.surface.Surface((self.app.window.display.get_width() // 2 + 4,self.app.window.display.get_height() // 1.5 + 4))
        self.page_outline.fill((50,50,50))
        # task close img
        self.close_button = Button_img(self.close_img,(int(self.page_surf.get_width() * 1.45),int(self.page_surf.get_height() * .35)),self.app)
        self.back_button = Button_img(self.back_img,(int(self.page_surf.get_width() * .5),int(self.page_surf.get_height() * .35)),self.app)

        # days tabs
        length = -font_1_white.get_size('Monday')//2
        self.tab_monday = Button_text(font_1_white,'Monday',(length + int(self.app.window.display.get_width() * .33),int(self.app.window.display.get_height() * .4)),self.app,(182,141,90))
        length = -font_1_white.get_size('Tuesday')//2
        self.tab_tuesday = Button_text(font_1_white,'Tuesday',(length + int(self.app.window.display.get_width() * .48),int(self.app.window.display.get_height() * .4)),self.app,(182,141,90))
        length = -font_1_white.get_size('Wednesday')//2
        self.tab_wednesday = Button_text(font_1_white,'Wednesday',(length + int(self.app.window.display.get_width() * .63),int(self.app.window.display.get_height() * .4)),self.app,(182,141,90))
        length = -font_1_white.get_size('Thursday')//2
        self.tab_thursday = Button_text(font_1_white,'Thursday',(length + int(self.app.window.display.get_width() * .33),int(self.app.window.display.get_height() * .5)),self.app,(182,141,90))
        length = -font_1_white.get_size('Friday')//2
        self.tab_friday = Button_text(font_1_white,'Friday',(length + int(self.app.window.display.get_width() * .48),int(self.app.window.display.get_height() * .5)),self.app,(182,141,90))
        length = -font_1_white.get_size('Saturday')//2
        self.tab_saturday = Button_text(font_1_white,'Saturday',(length + int(self.app.window.display.get_width() * .63),int(self.app.window.display.get_height() * .5)),self.app,(182,141,90))
        length = -font_1_white.get_size('Sunday')//2
        self.tab_sunday = Button_text(font_1_white,'Sunday',(length + int(self.app.window.display.get_width() * .48),int(self.app.window.display.get_height() * .6)),self.app,(182,141,90))
        # list of all day tabs
        self.days_tabs = [self.tab_monday,self.tab_tuesday,self.tab_wednesday,self.tab_thursday,self.tab_friday,self.tab_saturday,self.tab_sunday]

        # days open or close pages
        self.monday_page = False
        self.tuesday_page = False
        self.wednesday_page = False
        self.thursnday_page = False
        self.friday_page = False
        self.saturdayday_page = False
        self.sunday_page = False
        self.days_pages = [self.monday_page,self.tuesday_page,self.wednesday_page,self.thursnday_page,self.friday_page,self.saturdayday_page,self.sunday_page]


        self.current_day_idx = 0



    '''
    ----------------------------------------------------------------- intro task page --------------------------------------
    '''
    def render(self):
        # surf and outline of task page
        self.app.window.display.blit(self.page_outline,(self.app.window.display.get_width() // 4 - 2,self.app.window.display.get_height() // 5 - 2))
        self.app.window.display.blit(self.page_surf,(self.app.window.display.get_width() // 4 ,self.app.window.display.get_height() // 5))
        self.page_surf.fill((240, 255, 255))
        self.page_outline.fill((50,50,50))

        # intro 1
        if self.app.renderer.schedule.intro[0]:
            font_1_gold.render('Welcome to the add task section',self.page_surf,(int(self.page_surf.get_width() * .1 ),5))
            font_1_gold.render('click on one of the days to start!',self.page_surf,(int(self.page_surf.get_width() * .1 ),15))

        # days tabs render and events
        for i, tab in enumerate(self.days_tabs):
            if tab.render(self.app.window.display):
                self.app.renderer.schedule.intro[0] = False
                self.page = False
                self.days_pages[i] = True
                self.current_day_idx = i


        # event to close task page
        if self.close_button.render(self.app.window.display):
            self.page = False
