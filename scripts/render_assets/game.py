import pygame
import random
import math
from ..text import Font
from ..text import Button_text
from ..text import Button_img
from ..core_fucs import *
from ..particles import ParticleManager
from ..projectiles import ProjectileManager
from ..sparks import SparkManager

COLORKEY = (0,0,0)

# fonts
font_1_gold = Font(r'data\font\font_image.png',(218,169,108),1)
font_1_white = Font(r'data\font\font_image.png',(230, 234, 214),1)
font_4_black = Font(r'data\font\font_image.png',(0,1,0),4)



class Game():
    def __init__(self,app):
        self.app = app
        self.init_obj()
        self.load_imgs()


    def init_obj(self):
        # homework objects (rects and buttons) ------------------------------------------- #
        # tab buttons
        self.game_tab_1 = Button_text(font_1_white,'Home',(20,45),self.app,(182,141,90))
        self.game_tab_2 = Button_text(font_1_white,'Schedule',(120,45),self.app,(182,141,90))
        self.game_tab_3 = Button_text(font_1_white,'Groups',(220,45),self.app,(182,141,90))
        self.game_tab_4 = Button_text(font_1_white,'Homework',(320,45),self.app,(182,141,90))
        self.tabs = [self.game_tab_1,self.game_tab_2,self.game_tab_3,self.game_tab_4]

        # particles manager ---- #
        self.particles_manager = ParticleManager()
        # projectiles manager ------- #
        self.projectiles_manager = ProjectileManager()
        # sparks manager ------- #
        self.sparks_manager = SparkManager()
        # player death
        self.death = False
        self.temp_death = False
        self.death_timer = 0
        # game timer
        self.game_timer = 0
        self.numbery = 60
        self.game_init = True
        self.win = False
        self.pos = [0,0]


    def load_imgs(self):
        self.smily_img = load_img(r'data\images\misc\game\player.png',COLORKEY)


    # reset player
    def reset(self):
        # reset particles, projectiles, sparks
        self.particles_manager.reset()
        self.projectiles_manager.reset()
        self.sparks_manager.reset()
        # reset player death and pos
        self.death = False
        self.app.window.mouse_img = self.smily_img
        self.game_timer = 0



    # explosion render
    def explode(self):
        # check death for player one frame --- #
        if self.death and self.temp_death:
            for i in range(60):
                type = random.choice(['s','i'])
                # create spark explosion
                angle = math.radians(random.randint(1,360))
                if type == 's':
                    speed = 7 + random.randint(7,15)/15
                else:
                    speed = 7
                self.sparks_manager.new(self.pos,angle,speed,3,(150, 200, 140),type)
            for i in range(360):
                # create particle explosion
                angle = i
                speed = random.randint(70,150)/15 * .5
                vel = (math.cos(angle) * speed ,math.sin(angle) * speed)
                self.particles_manager.new('green_light',self.pos, vel,1 + random.randint(0, 20) / 10, .5)
            self.temp_death = False

    # when game page loads
    def init_game(self):
        self.reset()
        # mouse button change
        self.app.window.mouse_img = self.smily_img
        pygame.mouse.set_visible(False)
        self.game_init = False



    def update(self):
        if self.game_init:
            self.init_game()
        # game time
        self.game_timer +=1
        # projectiles
        # increase difficulty
        self.numbery = self.game_timer // 300
        num = int(60 - self.numbery)
        if num > 0 :
            if random.randint(1,num) == 1:
                for i in range(2):
                    self.projectiles_manager.new('img_0', (
                    self.app.window.display.get_width() * random.random() , self.app.window.display.get_height() * .25),
                                               (random.randint(50, 150) / 100 - 1, random.randint(10,30) / 10), random.random(), 'enemy',(6,3,2))

        # if cheating
        if self.pos[1] < self.app.window.display.get_height() * .25:
            self.projectiles_manager.reset()
            self.game_timer = 0

        # check for collision with player

        # mouse pos
        x,y = pygame.mouse.get_pos()
        # scale mouse pos
        temp_x =  int( x / self.app.window.scaled_res[0] * self.app.window.base_res[0])
        temp_y =  int( y / self.app.window.scaled_res[1] * self.app.window.base_res[1])
        self.pos = (temp_x,temp_y)
        self.size = 10,10
        r = pygame.rect.Rect(self.pos[0] - self.size[0] // 2 ,self.pos[1] - self.size[1] // 2,self.size[0],self.size[1])
        if not self.death:
            if self.projectiles_manager.collision(r):
                self.app.window.mouse_img = False
                self.death = True
                self.temp_death =True

        # mouse img
        if not self.death:
            if random.randint(1, 12) == 1:
                angle = math.radians(random.randint(0,180))
                speed = random.randint(7,15)/15 * .5
                vel = (math.cos(angle) * speed ,math.sin(angle) * speed)
                self.particles_manager.new('green_light',self.pos, vel,2 + random.randint(0, 20) / 10, .2)

        # create particle explosion
        if self.death and self.temp_death:
            self.explode()
        if self.death:
            # start death timer
            self.death_timer +=1
            if self.death_timer > 240:
                self.death_timer = 0
                self.reset()



    def render(self):
        # tabs
        for i,tab in enumerate(self.tabs):
            if tab.render(self.app.window.display):
                self.app.renderer.page = tab.str.lower()
                # change back mouse img
                self.app.window.mouse_img = False
                pygame.mouse.set_visible(True)
                # reset game init
                self.game_init = True
                self.win = False

        # render and update all projectiles ------ #
        self.projectiles_manager.update(self.app.window.display, [0,0], self.game_timer, 1/10)
        # render and update all particles - #
        self.particles_manager.update(self.app.window.display, [0,0], 1 / 10, self.game_timer)
        # render and update all sparks -- #
        self.sparks_manager.update(self.app.window.display, [0,0])

        # if player wins game
        if self.win:
            font_4_black.render(f'You Win',self.app.window.display,(int(self.app.window.display.get_width() * .3 ),int(self.app.window.display.get_height() * .5 )))
