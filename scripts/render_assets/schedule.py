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



class Schedule():
    def __init__(self,app,renderer):
        self.app = app
        self.renderer = renderer
        self.load_imgs()
        self.init_obj()


    def init_obj(self):
        # ------------------------------------------------------------------------------ #

        # schedule objects (rects and buttons) ------------------------------------------- #
        # tab buttons
        self.schedule_tab_1 = Button_text(font_1_white,'Home',(20,45),self.app,(182,141,90))
        self.schedule_tab_2 = Button_text(font_1_white,'Homework',(120,45),self.app,(182,141,90))
        self.schedule_tab_3 = Button_text(font_1_white,'Groups',(220,45),self.app,(182,141,90))

        # task img
        self.task_button = Button_img(self.task_img,(self.app.window.display.get_width() - 20,7),self.app)
        self.task_page = False
        self.task_page_surf = pygame.surface.Surface((self.app.window.display.get_width() // 2 ,self.app.window.display.get_height() // 1.5 ))
        self.task_page_surf.fill((240, 255, 255))
        self.task_page_outline = pygame.surface.Surface((self.app.window.display.get_width() // 2 + 4,self.app.window.display.get_height() // 1.5 + 4))
        self.task_page_outline.fill((50,50,50))
        # intro to add task tab
        self.schedule_intro = [True,True,True]
        # days tabs
        self.task_tab_monday = Button_text(font_1_white,'Monday',(self.app.window.display.get_width() // 2 - 20,self.app.window.display.get_height() // 2),self.app,(182,141,90))
        self.task_tab_tuesday = Button_text(font_1_white,'Tuesday',(self.app.window.display.get_width() // 2 ,self.app.window.display.get_height() // 2),self.app,(182,141,90))
        self.task_tab_wednesday = Button_text(font_1_white,'Wednesday',(self.app.window.display.get_width() // 2 + 20,self.app.window.display.get_height() // 2),self.app,(182,141,90))
        self.task_tab_thursday = Button_text(font_1_white,'Thursday',(self.app.window.display.get_width() // 2 - 20,self.app.window.display.get_height() // 2 - 20),self.app,(182,141,90))
        self.task_tab_friday = Button_text(font_1_white,'Friday',(self.app.window.display.get_width() // 2 ,self.app.window.display.get_height() // 2 - 20),self.app,(182,141,90))
        self.task_tab_saturday = Button_text(font_1_white,'Saturday',(self.app.window.display.get_width() // 2 + 20,self.app.window.display.get_height() // 2 - 20),self.app,(182,141,90))
        self.task_tab_sunday = Button_text(font_1_white,'Sunday',(self.app.window.display.get_width() // 2 ,self.app.window.display.get_height() // 2 - 40),self.app,(182,141,90))
        self.days_tabs = [self.task_tab_monday,self.task_tab_tuesday,self.task_tab_wednesday,self.task_tab_thursday,self.task_tab_friday,self.task_tab_saturday,self.task_tab_sunday]
        # days data
        # self.monday_data = [assignment due date, assigment name, total points]
        self.monday_data = [0,0,0]
        self.tuesday_data = [0,0,0]
        self.wednesday_data = [0,0,0]
        self.thursday_data = [0,0,0]
        self.friday_data = [0,0,0]
        self.saturday_data = [0,0,0]
        self.sunday_data = [0,0,0]
        self.days_data = [self.monday_data,self.tuesday_data,self.wednesday_data,self.thursday_data,self.friday_data,self.saturday_data,self.sunday_data]



        # ------------------------------------------------------------------------------ #


    '''
    ----------------------------------------------- load imgs --------------------------------------------
    '''
    def load_imgs(self):
        self.task_img = load_img(r'data\images\misc\schedule\add_task.png',COLORKEY)


    '''
    -------------------------------------------- schedule page ------------------------------------------------------------
    '''
    def render(self):
        # tabs
        if self.schedule_tab_1.render(self.app.window.display):
            self.renderer.page = 'menu'
        if self.schedule_tab_2.render(self.app.window.display):
            self.renderer.page = 'homework'
        if self.schedule_tab_3.render(self.app.window.display):
            self.renderer.page = 'groups'

        # task render
        font_1_gold.render('Add',self.app.window.display,(int(self.app.window.display.get_width() * .9 ),2))
        font_1_gold.render('Task',self.app.window.display,(int(self.app.window.display.get_width() * .9 ),15))

        if self.task_page:
            # surf and outline of task page
            self.app.window.display.blit(self.task_page_outline,(self.app.window.display.get_width() // 4 - 2,self.app.window.display.get_height() // 5 - 2))
            self.app.window.display.blit(self.task_page_surf,(self.app.window.display.get_width() // 4 ,self.app.window.display.get_height() // 5))


            # intro
            if self.schedule_intro[0]:
                font_1_gold.render('Welcome to the add task section',self.task_page_surf,(int(self.task_page_surf.get_width() * .1 ),5))
                font_1_gold.render('click on one of the days to start!',self.task_page_surf,(int(self.task_page_surf.get_width() * .1 ),15))

                for i, tab in enumerate(self.days_tabs):
                    if tab.draw():
                        self.schedule_intro[0] = False



                        self.days_data[i] = self.user_input






        # check for event
        if self.task_button.render(self.app.window.display):
            self.task_page = True
