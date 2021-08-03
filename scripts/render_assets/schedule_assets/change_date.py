import pygame
import datetime
from ...text import Font
from ...text import Button_text
from ...text import Button_img
from ...core_fucs import *

COLORKEY = (0,0,0)

# fonts
font_1_gold = Font(r'data\font\font_image.png',(218,169,108),1)
font_1_white = Font(r'data\font\font_image.png',(230, 234, 214),1)
font_2_gold = Font(r'data\font\font_image.png',(218,169,108),2)



class Change_Date():
    def __init__(self,app):
        self.app = app
        #self.load_imgs()
        self.init_obj()


    def init_obj(self):
        self.page = False
        self.error = False

    def render(self):
        # parent object for page changes
        task_obj = self.app.renderer.schedule.task
        schedule_obj = self.app.renderer.schedule
        # surf and outline of task page
        self.app.window.display.blit(task_obj.page_outline,(self.app.window.display.get_width() // 4 - 2,self.app.window.display.get_height() // 5 - 2))
        self.app.window.display.blit(task_obj.page_surf,(self.app.window.display.get_width() // 4 ,self.app.window.display.get_height() // 5))
        task_obj.page_surf.fill((240, 255, 255))
        task_obj.page_outline.fill((50,50,50))




        # intro 7
        if schedule_obj.intro[6]:
            font_1_gold.render('This Is Where You Will Change the',task_obj.page_surf,(int(task_obj.page_surf.get_width() * .05),int(task_obj.page_surf.get_height() * .09 )))
            font_1_gold.render('day to see future events',task_obj.page_surf,(int(task_obj.page_surf.get_width() * .05 ),int(task_obj.page_surf.get_height() * .15 )))


        # days tabs render and events
        for i, tab in enumerate(task_obj.days_tabs):
            if tab.render(self.app.window.display):
                self.app.renderer.schedule.intro[6] = False
                self.page = False
                # tiem ajustment
                schedule_obj.user_day_idx = i
                schedule_obj.user_day_of_week = schedule_obj.day_type.days_of_the_week[i]
                idx = schedule_obj.user_day_idx - schedule_obj.day_idx
                if idx < 0:
                    idx = idx + 7
                delta = datetime.timedelta(days=idx)
                schedule_obj.user_tday = schedule_obj.tday + delta
                schedule_obj.user_day_of_week = schedule_obj.day_type.days_of_the_week[schedule_obj.user_tday.weekday()]
                schedule_obj.user_num_date = str(schedule_obj.user_tday.month) + ' / ' + str(schedule_obj.user_tday.day) + ' / ' + str(schedule_obj.user_tday.year)
                schedule_obj.event_close()




        # event to close task page
        if task_obj.close_button.render(self.app.window.display):
            # closes current page
            self.page = False
