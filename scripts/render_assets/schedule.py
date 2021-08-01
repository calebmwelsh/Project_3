import pygame
from ..text import Font
from ..text import Button_text
from ..text import Button_img
from ..core_fucs import *
# pages
from .schedule_assets.task import Task
from .schedule_assets.day_type import Day_Type
from .schedule_assets.new_event import New_Event
from .schedule_assets.current_events import Current_Events

COLORKEY = (0,0,0)

# fonts
font_1_gold = Font(r'data\font\font_image.png',(218,169,108),1)
font_1_white = Font(r'data\font\font_image.png',(230, 234, 214),1)
font_2_gold = Font(r'data\font\font_image.png',(218,169,108),2)



class Schedule():
    def __init__(self,app,renderer):
        self.app = app
        self.task = Task(app)
        self.day_type = Day_Type(app)
        self.new_event = New_Event(app)
        self.current_events = Current_Events(app)
        self.load_imgs()
        self.init_obj()


    def init_obj(self):
        # task open img
        self.task_button = Button_img(self.task_img,(self.app.window.display.get_width() - 20,7),self.app)
        self.user_input = ''
        # intro to add task tab
        self.intro = [True,True,True,True]
        # ------------------------------------------------------------------------------ #

        # schedule objects (rects and buttons)

        # tab buttons
        self.schedule_tab_1 = Button_text(font_1_white,'Home',(20,45),self.app,(182,141,90))
        self.schedule_tab_2 = Button_text(font_1_white,'Homework',(120,45),self.app,(182,141,90))
        self.schedule_tab_3 = Button_text(font_1_white,'Groups',(220,45),self.app,(182,141,90))

        # ------------------------------------------------------------------------------ #

    def load_imgs(self):
        self.task_img = load_img(r'data\images\misc\schedule\add_task.png',COLORKEY)



    def render(self):
        # task render
        font_1_gold.render('Add',self.app.window.display,(int(self.app.window.display.get_width() * .9 ),2))
        font_1_gold.render('Task',self.app.window.display,(int(self.app.window.display.get_width() * .9 ),15))


        # tabs
        if self.schedule_tab_1.render(self.app.window.display):
            self.app.renderer.page = 'menu'
        if self.schedule_tab_2.render(self.app.window.display):
            self.app.renderer.page = 'homework'
        if self.schedule_tab_3.render(self.app.window.display):
            self.app.renderer.page = 'groups'



        '''
        ---------------- task button ---------------
        '''
        # check for event
        if self.task_button.render(self.app.window.display):
            self.task.page = True
            # reset all other pages
            for i, page in enumerate(self.task.days_pages):
                page = False


    def update(self):
        # render
        self.render()

        '''
        ---------- task page ---------
        '''
        # create a task page
        if self.task.page:
            self.task.render()
        '''
        ---------- Day Type page ---------
        '''
        # if user has chose a day to edit or inspect
        for i, day_page in enumerate(self.task.days_pages):
            if day_page:
                self.day_type.render()
        '''
        ------------- new event page --------------
        '''
        # if user choses to create a new task
        if self.new_event.page:
            self.new_event.render()
        '''
        ------------- current events page --------------
        '''
        # if user choses to view or edit a current task
        if self.current_events.page:
            self.current_events.render()
