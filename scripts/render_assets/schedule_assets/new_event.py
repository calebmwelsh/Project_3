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
        self.check_img = load_img(r'data\images\misc\schedule\check_mark.png',COLORKEY)

    def init_obj(self):
        self.page = False
        # class name tab
        self.class_name_tab = Button_text(font_1_white,'Class Name',(int(self.app.window.display.get_width() * .25),int(self.app.window.display.get_height() * .4)),self.app,(182,141,90))
        # assigment name
        self.assignment_name_tab = Button_text(font_1_white,'Assignment Name',(int(self.app.window.display.get_width() * .25),int(self.app.window.display.get_height() * .6)),self.app,(182,141,90))
        # assigment due score
        self.assignment_score_tab = Button_text(font_1_white,'Assignment Due Score',(int(self.app.window.display.get_width() * .25),int(self.app.window.display.get_height() * .8)),self.app,(182,141,90))
        # submit tab
        self.submit_tab = Button_text(font_1_white,'Submit',(int(self.app.window.display.get_width() * .66),int(self.app.window.display.get_height() * .7)),self.app,(182,141,90))
        # submit error
        self.error = False

    def render(self):
        # parent object for page changes
        task_obj = self.app.renderer.schedule.task
        schedule_obj = self.app.renderer.schedule
        i = task_obj.current_day_idx
        # surf and outline of task page
        self.app.window.display.blit(task_obj.page_outline,(self.app.window.display.get_width() // 4 - 2,self.app.window.display.get_height() // 5 - 2))
        self.app.window.display.blit(task_obj.page_surf,(self.app.window.display.get_width() // 4 ,self.app.window.display.get_height() // 5))
        task_obj.page_surf.fill((240, 255, 255))
        task_obj.page_outline.fill((50,50,50))

        # render day str
        font_2_gold.render(schedule_obj.day_type.days_data[i].day,task_obj.page_surf,(int(task_obj.page_surf.get_width() * .05 ),int(task_obj.page_surf.get_height() * .05 )))


        # intro 3
        if schedule_obj.intro[2]:
            font_1_gold.render('This Is Where You ',task_obj.page_surf,(int(task_obj.page_surf.get_width() * .47),int(task_obj.page_surf.get_height() * .15 )))
            font_1_gold.render('Will Enter All the ',task_obj.page_surf,(int(task_obj.page_surf.get_width() * .47 ),int(task_obj.page_surf.get_height() * .22 )))
            font_1_gold.render('Info for Your',task_obj.page_surf,(int(task_obj.page_surf.get_width() * .47 ),int(task_obj.page_surf.get_height() * .29 )))
            font_1_gold.render('Assignment',task_obj.page_surf,(int(task_obj.page_surf.get_width() * .47 ),int(task_obj.page_surf.get_height() * .36 )))

        # if error is True
        if self.error:
            font_1_gold.render('Complete',task_obj.page_surf,(int(task_obj.page_surf.get_width() * .6),int(task_obj.page_surf.get_height() * .5 )))
            font_1_gold.render('all sections!',task_obj.page_surf,(int(task_obj.page_surf.get_width() * .6 ),int(task_obj.page_surf.get_height() * .6 )))


        # check marks if class name section is completed
        if type(schedule_obj.day_type.days_data[i].temp[2]) == str :
            self.app.window.display.blit(self.check_img,(int(self.app.window.display.get_width() * .4),int(self.app.window.display.get_height() * .35)))

        # check marks if assignment name section is completed
        if type(schedule_obj.day_type.days_data[i].temp[1]) == str:
            self.app.window.display.blit(self.check_img,(int(self.app.window.display.get_width() * .47),int(self.app.window.display.get_height() * .57)))

        # check marks if assignment score section is completed
        if type(schedule_obj.day_type.days_data[i].temp[0]) == str :
            self.app.window.display.blit(self.check_img,(int(self.app.window.display.get_width() * .53),int(self.app.window.display.get_height() * .75)))


        # the class name of the assignment
        if self.class_name_tab.render(self.app.window.display):
            self.app.input.user_text = ''
            schedule_obj.class_name.page = True
            self.page = False
            self.app.renderer.schedule.intro[2] = False

        # enter name of assignment
        if self.assignment_name_tab.render(self.app.window.display):
            self.app.input.user_text = ''
            schedule_obj.assignment_name.page = True
            self.page = False
            self.app.renderer.schedule.intro[2] = False

        # enter time of assignment
        if self.assignment_score_tab.render(self.app.window.display):
            self.app.input.user_text = ''
            schedule_obj.assignment_score.page = True
            self.page = False
            self.app.renderer.schedule.intro[2] = False

        # submit tab
        if self.submit_tab.render(self.app.window.display):
            submit = True
            # checks if all arguments are str
            for j, v in enumerate(schedule_obj.day_type.days_data[i].temp):
                if type(v) != str:
                    submit = False
            if submit:
                schedule_obj.day_type.days_data[i].add_event()
                self.page = False
            else:
                self.error = True


        # event to close task page
        if task_obj.close_button.render(self.app.window.display):
            # closes current page
            self.page = False
        if task_obj.back_button.render(self.app.window.display):
            # closes current page
            self.page = False
            # opens current and new event tab
            task_obj.days_pages[i] = True
