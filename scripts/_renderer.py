import pygame
from .text import Font
from .text import Button_text
from .text import Button_img
from .core_fucs import *

COLORKEY = (0,0,0)

# fonts
font_1_gold = Font(r'data\font\font_image.png',(218,169,108),1)
font_1_white = Font(r'data\font\font_image.png',(230, 234, 214),1)
font_2_gold = Font(r'data\font\font_image.png',(218,169,108),2)


class Renderer():
    # renderer init
    def __init__(self,app):
        self.app = app
        self.page = 'menu'
        # init imgs
        self.load_imgs()
        # init objects
        self.init_objects()


    '''
    ----------------------------------------------- load imgs --------------------------------------------
    '''
    def load_imgs(self):
        self.task_img = load_img(r'data\images\misc\schedule\add_task.png',COLORKEY)




    '''
    ---------------------------------------------- rects and buttons inits ----------------------------------
    '''
    def init_objects(self):
        # menu objects (rects and buttons) ------------------------------------------- #
        # header rect
        self.black_header = pygame.rect.Rect(0,30,self.app.window.display.get_width(),40)
        # tab buttons
        self.menu_tab_1 = Button_text(font_1_white,'Schedule',(20,45),self.app,(182,141,90))
        self.menu_tab_2 = Button_text(font_1_white,'Homework',(120,45),self.app,(182,141,90))
        self.menu_tab_3 = Button_text(font_1_white,'Groups',(220,45),self.app,(182,141,90))
        #self.tab_4 = Button_text(font_1_white,'Schedule',(20,50),self.app,(182,141,90))
        # task img
        self.task_button = Button_img(self.task_img,(self.app.window.display.get_width() - 20,7),self.app)
        self.task_page = False
        self.task_page_rect = pygame.rect.Rect(self.app.window.display.get_width() // 4,self.app.window.display.get_height() // 5,self.app.window.display.get_width() // 2 ,self.app.window.display.get_height() // 1.5 )
        self.task_page_outline = pygame.rect.Rect(self.app.window.display.get_width() // 4,self.app.window.display.get_height() // 5 ,self.app.window.display.get_width() // 2 ,self.app.window.display.get_height() // 1.5 )



        # ------------------------------------------------------------------------------ #

        # schedule objects (rects and buttons) ------------------------------------------- #
        # tab buttons
        self.schedule_tab_1 = Button_text(font_1_white,'Home',(20,45),self.app,(182,141,90))
        self.schedule_tab_2 = Button_text(font_1_white,'Homework',(120,45),self.app,(182,141,90))
        self.schedule_tab_3 = Button_text(font_1_white,'Groups',(220,45),self.app,(182,141,90))
        #self.tab_4 = Button_text(font_1_white,'Schedule',(20,50),self.app,(182,141,90))
        # ------------------------------------------------------------------------------ #

        # homework objects (rects and buttons) ------------------------------------------- #
        # tab buttons
        self.homework_tab_1 = Button_text(font_1_white,'Home',(20,45),self.app,(182,141,90))
        self.homework_tab_2 = Button_text(font_1_white,'Schedule',(120,45),self.app,(182,141,90))
        self.homework_tab_3 = Button_text(font_1_white,'Groups',(220,45),self.app,(182,141,90))
        #self.tab_4 = Button_text(font_1_white,'Schedule',(20,50),self.app,(182,141,90))

        # ------------------------------------------------------------------------------ #

        # groups objects (rects and buttons) ------------------------------------------- #
        # tab buttons
        self.groups_tab_1 = Button_text(font_1_white,'Home',(20,45),self.app,(182,141,90))
        self.groups_tab_2 = Button_text(font_1_white,'Schedule',(120,45),self.app,(182,141,90))
        self.groups_tab_3 = Button_text(font_1_white,'Homework',(220,45),self.app,(182,141,90))
        #self.tab_4 = Button_text(font_1_white,'Schedule',(20,50),self.app,(182,141,90))
        # ------------------------------------------------------------------------------ #


    '''
    -------------------------------------------- menu page ------------------------------------------------------------
    '''
    def menu(self):
        # tabs
        if self.menu_tab_1.render(self.app.window.display):
            self.page = 'schedule'
        if self.menu_tab_2.render(self.app.window.display):
            self.page = 'homework'
        if self.menu_tab_3.render(self.app.window.display):
            self.page = 'groups'

    '''
    -------------------------------------------- schedule page ------------------------------------------------------------
    '''
    def schedule(self):
        # tabs
        if self.schedule_tab_1.render(self.app.window.display):
            self.page = 'menu'
        if self.schedule_tab_2.render(self.app.window.display):
            self.page = 'homework'
        if self.schedule_tab_3.render(self.app.window.display):
            self.page = 'groups'

        # task render
        font_1_gold.render('Add',self.app.window.display,(int(self.app.window.display.get_width() * .85 ),2))
        font_1_gold.render('Task',self.app.window.display,(int(self.app.window.display.get_width() * .83 ),15))

        if self.task_page:
            # rect and outline of task page
            pygame.draw.rect(self.app.window.display,(240, 255, 255),self.task_page_rect)
            pygame.draw.rect(self.app.window.display,(50,50,50),self.task_page_outline,1)


        # check for event
        if self.task_button.render(self.app.window.display):
            self.task_page = True



    '''
    -------------------------------------------- homework page ------------------------------------------------------------
    '''
    def homework(self):
        # tabs
        if self.homework_tab_1.render(self.app.window.display):
            self.page = 'menu'
        if self.homework_tab_2.render(self.app.window.display):
            self.page = 'schedule'
        if self.homework_tab_3.render(self.app.window.display):
            self.page = 'groups'



    '''
    -------------------------------------------- groups page ------------------------------------------------------------
    '''
    def groups(self):
        # tabs
        if self.groups_tab_1.render(self.app.window.display):
            self.page = 'menu'
        if self.groups_tab_2.render(self.app.window.display):
            self.page = 'schedule'
        if self.groups_tab_3.render(self.app.window.display):
            self.page = 'homework'

    '''
    --------------------------------------------- constant render objects ---------------------------------------
    '''
    def perm_render(self):
        # header
        pygame.draw.rect(self.app.window.display,'black',self.black_header)
        # purdue advanced Learning
        font_2_gold.render('Purdue',self.app.window.display,(20,5))
        font_1_gold.render('Advance Learning',self.app.window.display,(100,7))
        font_1_gold.render('Application',self.app.window.display,(100,17))

    '''
    ---------------------------------------------- render ----------------------------------------------
    '''
    def render(self):
        # render world attributes
        self.app.world.render()
        # render constant objects
        self.perm_render()
        # menu page
        if self.page == 'menu':
            self.menu()
        # schedule page
        elif self.page == 'schedule':
            self.schedule()
        # homework page
        elif self.page == 'homework':
            self.homework()
        # groups page
        elif self.page == 'groups':
            self.groups()
