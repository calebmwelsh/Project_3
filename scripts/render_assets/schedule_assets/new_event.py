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



class New_Event():
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
        # class name tab
        self.class_name_tab = Button_text(font_1_white,'Class Name',(int(self.app.window.display.get_width() * .25),int(self.app.window.display.get_height() * .4)),self.app,(182,141,90))
        self.class_name_page = False
        # assigment name
        self.assignment_name_tab = Button_text(font_1_white,'Assignment Name',(int(self.app.window.display.get_width() * .25),int(self.app.window.display.get_height() * .6)),self.app,(182,141,90))
        self.assignment_name_page = False
        # assigment due date
        self.assignment_date_tab = Button_text(font_1_white,'Assignment Due Date',(int(self.app.window.display.get_width() * .25),int(self.app.window.display.get_height() * .8)),self.app,(182,141,90))
        self.assignment_date_page = False



    def render(self):
        # parent object for page changes
        parent_obj = self.app.renderer.schedule.task
        schedule_obj = self.app.renderer.schedule
        i = parent_obj.current_day_idx
        # surf and outline of task page
        self.app.window.display.blit(parent_obj.page_outline,(self.app.window.display.get_width() // 4 - 2,self.app.window.display.get_height() // 5 - 2))
        self.app.window.display.blit(parent_obj.page_surf,(self.app.window.display.get_width() // 4 ,self.app.window.display.get_height() // 5))
        parent_obj.page_surf.fill((240, 255, 255))
        parent_obj.page_outline.fill((50,50,50))

        # render day str
        font_2_gold.render(schedule_obj.day_type.days_data[i][0],parent_obj.page_surf,(int(parent_obj.page_surf.get_width() * .1 ),5))

        # intro 3
        if self.app.renderer.schedule.intro[2]:
            font_1_gold.render('This Is Where You ',parent_obj.page_surf,(int(parent_obj.page_surf.get_width() * .47),int(parent_obj.page_surf.get_height() * .05 )))
            font_1_gold.render('Will Enter All the ',parent_obj.page_surf,(int(parent_obj.page_surf.get_width() * .47 ),int(parent_obj.page_surf.get_height() * .12 )))
            font_1_gold.render('Info for Your',parent_obj.page_surf,(int(parent_obj.page_surf.get_width() * .47 ),int(parent_obj.page_surf.get_height() * .19 )))
            font_1_gold.render('Assignment',parent_obj.page_surf,(int(parent_obj.page_surf.get_width() * .47 ),int(parent_obj.page_surf.get_height() * .26 )))

        # the class name of the assignment
        if self.class_name_tab.render(self.app.window.display):
            self.class_name_page = True
            self.page = False
            self.app.renderer.schedule.intro[2] = False

        # enter name of assignment
        if self.assignment_name_tab.render(self.app.window.display):
            self.class_name_page = True
            self.page = False
            self.app.renderer.schedule.intro[2] = False

        # enter time of assignment
        if self.assignment_date_tab.render(self.app.window.display):
            self.class_name_page = True
            self.page = False
            self.app.renderer.schedule.intro[2] = False

        # event to close task page
        if parent_obj.close_button.render(self.app.window.display):
            # closes current page
            self.page = False
        if parent_obj.back_button.render(self.app.window.display):
            # closes current page
            self.page = False
            # opens current and new event tab
            parent_obj.days_pages[i] = True
