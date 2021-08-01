import pygame
from ....text import Font
from ....text import Button_text
from ....text import Button_img
from ....core_fucs import *

COLORKEY = (0,0,0)

# fonts
font_1_gold = Font(r'data\font\font_image.png',(218,169,108),1)
font_1_white = Font(r'data\font\font_image.png',(230, 234, 214),1)
font_2_gold = Font(r'data\font\font_image.png',(218,169,108),2)



class Class_Name():
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
        self.submit_tab = Button_text(font_1_white,'Submit',(int(self.app.window.display.get_width() * .66),int(self.app.window.display.get_height() * .7)),self.app,(182,141,90))






    '''
    --------------------------------------------------------------------------- class name page -------------------------------------------
    '''
    def render(self):
        # parent object for page changes
        task_obj = self.app.renderer.schedule.task
        schedule_obj = self.app.renderer.schedule
        parent_obj = self.app.renderer.schedule.new_event
        i = task_obj.current_day_idx
        # surf and outline of task page
        self.app.window.display.blit(task_obj.page_outline,(self.app.window.display.get_width() // 4 - 2,self.app.window.display.get_height() // 5 - 2))
        self.app.window.display.blit(task_obj.page_surf,(self.app.window.display.get_width() // 4 ,self.app.window.display.get_height() // 5))
        task_obj.page_surf.fill((240, 255, 255))
        task_obj.page_outline.fill((50,50,50))

        # render day str
        font_2_gold.render(schedule_obj.day_type.days_data[i][0],task_obj.page_surf,(int(task_obj.page_surf.get_width() * .1 ),5))

        # intro 4
        if schedule_obj.intro[3]:
            font_1_gold.render('This Is Where You ',task_obj.page_surf,(int(task_obj.page_surf.get_width() * .47),int(task_obj.page_surf.get_height() * .05 )))
            font_1_gold.render('Will Enter the',task_obj.page_surf,(int(task_obj.page_surf.get_width() * .47 ),int(task_obj.page_surf.get_height() * .12 )))
            font_1_gold.render('Class name to your',task_obj.page_surf,(int(task_obj.page_surf.get_width() * .47 ),int(task_obj.page_surf.get_height() * .19 )))
            font_1_gold.render('Assignment',task_obj.page_surf,(int(task_obj.page_surf.get_width() * .47 ),int(task_obj.page_surf.get_height() * .26 )))




        # submit tab
        if self.submit_tab.render(self.app.window.display):
            self.days_data[i][0] = self.user_input
            self.page = False



        # event to close task page
        if task_obj.close_button.render(self.app.window.display):
            # closes current page
            self.page = False
        if task_obj.back_button.render(self.app.window.display):
            # closes current page
            self.page = False
            # opens currentclass_name_page and new event tab
            parent_obj.page = True
