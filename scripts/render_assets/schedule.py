import pygame
import datetime
from ..text import Font
from ..text import Button_text
from ..text import Button_img
from ..core_fucs import *
# pages
from .schedule_assets.task import Task
from .schedule_assets.day_type import Day_Type
from .schedule_assets.new_event import New_Event
from .schedule_assets.current_events import Current_Events
# pages on pages lol
from .schedule_assets.new_event_assets.class_name import Class_Name
from .schedule_assets.new_event_assets.assignment_name import Assignment_Name
from .schedule_assets.new_event_assets.assignment_date import Assignment_Date



COLORKEY = (0,0,0)

# fonts
font_1_gold = Font(r'data\font\font_image.png',(218,169,108),1)
font_1_black = Font(r'data\font\font_image.png',(0,1,0),1)
font_1_white = Font(r'data\font\font_image.png',(230, 234, 214),1)
font_2_gold = Font(r'data\font\font_image.png',(218,169,108),2)



class Schedule():
    def __init__(self,app,renderer):
        self.app = app
        # task page
        self.task = Task(app)
        # day type page
        self.day_type = Day_Type(app)
        # new event page
        self.new_event = New_Event(app)
        # current event page
        self.current_events = Current_Events(app)
        # class name page
        self.class_name = Class_Name(app)
        # asssignment name page
        self.assignment_name = Assignment_Name(app)
        # assigment due data page
        self.assignment_date = Assignment_Date(app)
        self.load_imgs()
        self.init_obj()


    def init_obj(self):
        # time
        self.tday = datetime.date.today()
        self.day_idx = self.tday.weekday()
        self.day_of_week = self.day_type.days_data[self.tday.weekday()].day
        self.num_date = str(self.tday.month) + ' / ' + str(self.tday.day) + ' / ' + str(self.tday.year)
        # task open img
        self.task_button = Button_img(self.task_img,(self.app.window.display.get_width() - 20,7),self.app)
        # intro to add task tab
        self.intro = [True,True,True,True,True,True,True,True,True,True]
        # tab buttons
        self.schedule_tab_1 = Button_text(font_1_white,'Home',(20,45),self.app,(182,141,90))
        self.schedule_tab_2 = Button_text(font_1_white,'Homework',(120,45),self.app,(182,141,90))
        self.schedule_tab_3 = Button_text(font_1_white,'Groups',(220,45),self.app,(182,141,90))
        # user


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

        # users schedule
        font_2_gold.render(f'Your Schedule Today',self.app.window.display,(int(self.app.window.display.get_width() * .005 ),int(self.app.window.display.get_height() * .25 )))
        font_1_gold.render(self.num_date,self.app.window.display,(int(self.app.window.display.get_width() * .85 ),int(self.app.window.display.get_height() * .25 )))

        # display schedule

        if self.day_type.days_data[self.day_idx].data == []:
            font_1_gold.render(f'You have not events today',self.app.window.display,(int(self.app.window.display.get_width() * .005 ),int(self.app.window.display.get_height() * .4 )))
        else:
            pre_len = 0
            for i, event in enumerate(self.day_type.days_data[self.day_idx].data):
                # find the longest length to create the surf for sections
                length = 0
                for section in event:
                    length = max(font_1_black.get_size(section),length)
                # create surf
                surf = pygame.surface.Surface((length + 4, self.app.window.display.get_height() * .2 ))
                surf.fill((218,169,108))
                # blit surf
                self.app.window.display.blit(surf,( int(self.app.window.display.get_width() * .005 + pre_len),int(self.app.window.display.get_height() * .375 ) ) )
                # render text
                font_1_black.render(event[0],self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .4 )))
                font_1_black.render(event[1],self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .45 )))
                font_1_black.render(event[2],self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .5 )))
                # offset for events
                pre_len += length + int(self.app.window.display.get_width() * .05 )







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
        ------------ class name page ------------
        '''
        # if user choses to input class name
        if self.class_name.page:
            self.class_name.render()
        '''
        ------------ assignment name page ------------
        '''
        # if user choses to input assignment name
        if self.assignment_name.page:
            self.assignment_name.render()
        '''
        ------------ assignment due date page ------------
        '''
        # if user choses to input assignment due date
        if self.assignment_date.page:
            self.assignment_date.render()
        '''
        ------------- current events page --------------
        '''
        # if user choses to view or edit a current task
        if self.current_events.page:
            self.current_events.render()
