import pygame
from ...text import Font
from ...text import Button_text
from ...text import Button_img
from ...core_fucs import *
from .user_data import User_Data

COLORKEY = (0,0,0)

# fonts
font_1_gold = Font(r'data\font\font_image.png',(218,169,108),1)
font_1_white = Font(r'data\font\font_image.png',(230, 234, 214),1)
font_2_gold = Font(r'data\font\font_image.png',(218,169,108),2)



class Day_Type():
    def __init__(self,app):
        self.app = app
        self.load_imgs()
        self.init_obj()


    def load_imgs(self):
        pass

    def init_obj(self):
        self.page = False
        # users days data
        # [day, class name, assignment due date, assigment name]
        self.monday_data = User_Data('Monday')
        self.tuesday_data = User_Data('Tuesday')
        self.wednesday_data = User_Data('Wednesday')
        self.thursday_data = User_Data('Thursday')
        self.friday_data = User_Data('Friday')
        self.saturday_data = User_Data('Saturday')
        self.sunday_data = User_Data('Sunday')
        # list of all day data
        self.days_data = [self.monday_data,self.tuesday_data,self.wednesday_data,self.thursday_data,self.friday_data,self.saturday_data,self.sunday_data]


        # new event for users
        self.new_event_tab = Button_text(font_1_white,'New Event',(int(self.app.window.display.get_width() * .25),int(self.app.window.display.get_height() * .6)),self.app,(182,141,90))
        # page var for new event
        self.new_event_page = [False,0,0]

        # current event for users
        self.current_event_tab = Button_text(font_1_white,'Current Events',(int(self.app.window.display.get_width() * .5),int(self.app.window.display.get_height() * .6)),self.app,(182,141,90))
        # page var for current event
        self.current_event_page = [False,0,0]



    def render(self):
        parent_obj = self.app.renderer.schedule.task
        i = parent_obj.current_day_idx
        # surf and outline of task page
        self.app.window.display.blit(parent_obj.page_outline,(self.app.window.display.get_width() // 4 - 2,self.app.window.display.get_height() // 5 - 2))
        self.app.window.display.blit(parent_obj.page_surf,(self.app.window.display.get_width() // 4 ,self.app.window.display.get_height() // 5))
        parent_obj.page_surf.fill((240, 255, 255))
        parent_obj.page_outline.fill((50,50,50))


        # render day str
        font_2_gold.render(self.days_data[i].day,parent_obj.page_surf,(int(parent_obj.page_surf.get_width() * .05 ),int(parent_obj.page_surf.get_height() * .05 )))


        # intro 2
        if self.app.renderer.schedule.intro[1]:
            font_1_gold.render('Select New Event or Current',parent_obj.page_surf,(int(parent_obj.page_surf.get_width() * .1),int(parent_obj.page_surf.get_height() * .15 )))
            font_1_gold.render('Events to see your',parent_obj.page_surf,(int(parent_obj.page_surf.get_width() * .1 ),int(parent_obj.page_surf.get_height() * .22 )))
            font_1_gold.render(f'schedule on {self.days_data[i].day}',parent_obj.page_surf,(int(parent_obj.page_surf.get_width() * .1 ),int(parent_obj.page_surf.get_height() * .29 )))

        # user creates new event for selected day
        if self.new_event_tab.render(self.app.window.display):
            self.app.renderer.schedule.new_event.page = True
            parent_obj.days_pages[i] = False
            self.app.renderer.schedule.intro[1] = False

        # user access their cuurent events for selected day
        if self.current_event_tab.render(self.app.window.display):
            self.app.renderer.schedule.current_events.page = True
            parent_obj.days_pages[i] = False
            self.app.renderer.schedule.intro[1] = False


        # event to close task page
        if parent_obj.close_button.render(self.app.window.display):
            parent_obj.days_pages[i] = False
        if parent_obj.back_button.render(self.app.window.display):
            parent_obj.days_pages[i] = False
            parent_obj.page = True
