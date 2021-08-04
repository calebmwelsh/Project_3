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
# from .schedule_assets.current_events import Current_Events
from .schedule_assets.change_date import Change_Date
# pages on pages lol
from .schedule_assets.new_event_assets.prompt_1 import Prompt_1
from .schedule_assets.new_event_assets.prompt_2 import Prompt_2
from .schedule_assets.new_event_assets.prompt_3 import Prompt_3



COLORKEY = (0,0,0)

# fonts
font_1_gold = Font(r'data\font\font_image.png',(218,169,108),1)
font_1_black = Font(r'data\font\font_image.png',(0,1,0),1)
font_2_black = Font(r'data\font\font_image.png',(0,1,0),2)
font_1_white = Font(r'data\font\font_image.png',(230, 234, 214),1)
font_2_gold = Font(r'data\font\font_image.png',(218,169,108),2)



class Schedule():
    def __init__(self,app,renderer):
        self.app = app
        # task page
        self.task = Task(app)
        # change data for user view
        self.change_date = Change_Date(app)
        # day type page
        self.day_type = Day_Type(app)
        # new event page
        self.new_event = New_Event(app)
        # current event page
        #self.current_events = Current_Events(app)
        # class name page
        self.prompt_1 = Prompt_1(app)
        # asssignment name page
        self.prompt_2 = Prompt_2(app)
        # assigment due data page
        self.prompt_3 = Prompt_3(app)
        self.load_imgs()
        self.init_obj()


    def init_obj(self):
        # time
        self.tday = datetime.date.today()
        self.day_idx = self.tday.weekday()
        self.day_of_week = self.day_type.days_of_the_week[self.tday.weekday()]
        self.num_date = str(self.tday.month) + ' / ' + str(self.tday.day) + ' / ' + str(self.tday.year)
        # user time
        self.user_tday = datetime.date.today()
        self.user_day_idx = self.tday.weekday()
        self.user_day_of_week = self.day_type.days_of_the_week[self.tday.weekday()]
        self.user_num_date = str(self.tday.month) + ' / ' + str(self.tday.day) + ' / ' + str(self.tday.year)

        # task open img
        self.task_button = Button_img(self.task_img,(self.app.window.display.get_width() - 20,7),self.app)
        # intro to add task tab
        self.intro = [True,True,True,True,True,True,True,True,True,True]
        # tab buttons
        self.schedule_tab_1 = Button_text(font_1_white,'Home',(20,45),self.app,(182,141,90))
        self.schedule_tab_2 = Button_text(font_1_white,'Homework',(120,45),self.app,(182,141,90))
        self.schedule_tab_3 = Button_text(font_1_white,'Groups',(220,45),self.app,(182,141,90))
        self.schedule_tab_4 = Button_text(font_1_white,'Game',(320,45),self.app,(182,141,90))
        self.tabs = [self.schedule_tab_1,self.schedule_tab_2,self.schedule_tab_3,self.schedule_tab_4]
        # change date
        self.change_date_button = Button_text(font_1_gold,'Change Date',(self.app.window.display.get_width() * .82,self.app.window.display.get_height() * .4),self.app)

        # event delete var
        self.event_del = True
        # del button
        self.event_del_list = []


    def load_imgs(self):
        self.task_img = load_img(r'data\images\misc\schedule\add_task.png',COLORKEY)
        self.del_img = load_img(r'data\images\misc\schedule\delete.png',COLORKEY)



    def event_close(self):
        # del button
        self.event_del_list = []
        # if user is viewing furture schedules
        if self.day_idx != self.user_day_idx:
            pre_len = 0
            for i, event in enumerate(self.day_type.days_data[self.user_day_idx]):
                # find the longest length to create the surf for sections
                length = 0
                for section in event:
                    length = max(font_1_black.get_size(section),length)
                width = max(length + self.app.window.display.get_width() * .01,self.app.window.display.get_width() * .2)

                # button
                b = Button_img(self.del_img,(pre_len + width - self.app.window.display.get_width() * .025, self.app.window.display.get_height() * .4 ),self.app)
                self.event_del_list.append(b)


                # offset for events
                pre_len += width + int(self.app.window.display.get_width() * .05 )
        else:
            pre_len = 0
            for i, event in enumerate(self.day_type.days_data[self.day_idx]):
                # find the longest length to create the surf for sections
                length = 0
                for section in event:
                    length = max(font_1_black.get_size(section),length)
                width = max(length + self.app.window.display.get_width() * .01,self.app.window.display.get_width() * .2)

                # button
                b = Button_img(self.del_img,(pre_len + width - self.app.window.display.get_width() * .025, self.app.window.display.get_height() * .4 ),self.app)
                self.event_del_list.append(b)


                # offset for events
                pre_len += width + int(self.app.window.display.get_width() * .05 )


    def render(self):
        # task render
        font_1_gold.render('Add',self.app.window.display,(int(self.app.window.display.get_width() * .9 ),2))
        font_1_gold.render('Task',self.app.window.display,(int(self.app.window.display.get_width() * .9 ),15))

        # tabs
        for i,tab in enumerate(self.tabs):
            if tab.render(self.app.window.display):
                self.app.renderer.page = tab.str.lower()
        '''
        ---------------- task button ---------------
        '''
        # check for event
        if self.task_button.render(self.app.window.display):
            self.task.page = True
            # reset all other pages
            for i, page in enumerate(self.task.days_pages):
                page = False


        '''
        ---------------- change date button ---------
        '''
        if self.change_date_button.render(self.app.window.display):
            self.change_date.page = True


        # display schedule

        # create change buttons
        if self.event_del:
            self.event_close()
            self.event_del = False
        # if user is viewing furture schedules
        if self.day_idx != self.user_day_idx:
            # users schedule
            font_2_gold.render(f'Your Schedule on {self.user_day_of_week}',self.app.window.display,(int(self.app.window.display.get_width() * .005 ),int(self.app.window.display.get_height() * .25 )))
            # date display
            font_1_gold.render(self.user_num_date,self.app.window.display,(int(self.app.window.display.get_width() * .83 ),int(self.app.window.display.get_height() * .31 )))
            if self.day_type.days_data[self.user_day_idx] == []:
                font_1_gold.render(f'You have no events on {self.user_day_of_week}',self.app.window.display,(int(self.app.window.display.get_width() * .005 ),int(self.app.window.display.get_height() * .4 )))
            else:
                pre_len = 0
                for i, event in enumerate(self.day_type.days_data[self.user_day_idx]):
                    # find the longest length to create the surf for sections
                    length = 0
                    for section in event:
                        length = max(font_1_black.get_size(section),length)
                    # create surf
                    width = max(length + self.app.window.display.get_width() * .01,self.app.window.display.get_width() * .2)
                    surf = pygame.surface.Surface((width, self.app.window.display.get_height() * .38 ))
                    surf.fill((218,169,108))


                    # blit surf
                    self.app.window.display.blit(surf,( int(self.app.window.display.get_width() * .005 + pre_len),int(self.app.window.display.get_height() * .375 ) ) )


                    # display del button
                    if self.event_del_list[i].render(self.app.window.display):
                        self.day_type.data_manager.delete(self.user_day_idx,i)
                        self.event_close()
                        self.day_type.data_manager.write(r'data\files\json\user_data.json')


                    # render text
                    font_1_black.render('Task Occurance:',self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .45 )))
                    font_1_black.render(event[0],self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .5 )))
                    font_1_black.render('Task Name:',self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .55 )))
                    font_1_black.render(event[2],self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .6 )))
                    font_1_black.render('Task Notes:',self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .65 )))
                    font_1_black.render(event[1],self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .7 )))
                    # offset for events
                    pre_len += width + int(self.app.window.display.get_width() * .05 )

        # if user is viewing todays schedule
        else:
            # title display
            font_2_gold.render(f'Your Schedule Today',self.app.window.display,(int(self.app.window.display.get_width() * .005 ),int(self.app.window.display.get_height() * .25 )))
            # date display
            font_1_gold.render(self.num_date,self.app.window.display,(int(self.app.window.display.get_width() * .83 ),int(self.app.window.display.get_height() * .31 )))
            if self.day_type.days_data[self.day_idx] == []:
                font_1_gold.render(f'You have no events today',self.app.window.display,(int(self.app.window.display.get_width() * .005 ),int(self.app.window.display.get_height() * .4 )))
            else:
                pre_len = 0
                for i, event in enumerate(self.day_type.days_data[self.day_idx]):
                    # find the longest length to create the surf for sections
                    length = 0
                    for section in event:
                        length = max(font_1_black.get_size(section),length)

                    # create surf
                    width = max(length + self.app.window.display.get_width() * .01,self.app.window.display.get_width() * .2)
                    surf = pygame.surface.Surface((width, self.app.window.display.get_height() * .38 ))
                    surf.fill((218,169,108))

                    # blit surf
                    self.app.window.display.blit(surf,( int(self.app.window.display.get_width() * .005 + pre_len),int(self.app.window.display.get_height() * .375 ) ) )




                    # display del button
                    if self.event_del_list[i].render(self.app.window.display):
                        self.day_type.data_manager.delete(self.day_idx,i)
                        self.event_close()
                        self.day_type.data_manager.write(r'data\files\json\user_data.json')


                    # render text
                    font_1_black.render('Task Occurance:',self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .45 )))
                    font_1_black.render(event[0],self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .5 )))
                    font_1_black.render('Task Name:',self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .55 )))
                    font_1_black.render(event[2],self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .6 )))
                    font_1_black.render('Task Notes:',self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .65 )))
                    font_1_black.render(event[1],self.app.window.display,(int(self.app.window.display.get_width() * .008 + pre_len),int(self.app.window.display.get_height() * .7 )))
                    # offset for events
                    pre_len += width + int(self.app.window.display.get_width() * .05 )







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
        ---------- change date page ---------
        '''
        if self.change_date.page:
            self.change_date.render()
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
        ------------ prompt 1 page ------------
        '''
        # if user choses to input class name
        if self.prompt_1.page:
            self.prompt_1.render()
        '''
        ------------ prompt 2 page ------------
        '''
        # if user choses to input assignment name
        if self.prompt_2.page:
            self.prompt_2.render()
        '''
        ------------ prompt 3 date page ------------
        '''
        # if user choses to input assignment due date
        if self.prompt_3.page:
            self.prompt_3.render()
        '''
        ------------- current events page --------------

        # if user choses to view or edit a current task
        if self.current_events.page:
            self.current_events.render()    '''
