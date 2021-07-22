import pygame, os, json, random, math
import scripts.core_fucs as core_fucs
from pygame.locals import *

'''
---------------------------------------------- global vars -----------------------------------------------
'''
COLORKEY = (0, 0, 0)
PARTICLE_PATH = r'data\images\particles'


'''
---------------------------------------- particle preset data ---------------------------------------------
'''
# loads all data from animations files for particles and creates or loads configs --- #
class ParticleData():
    # path is a specific folder the has each frame ex (player idle) ---------- #
    def __init__(self, path, colorkey):
        # makes a list of all images in folder according to path -- #
        imgs = os.listdir(path)
        # load imgs and put in list
        self.img_list = []
        for img in imgs:
            if img.split('.')[-1] == 'png':
                self.img_list.append(core_fucs.load_img(path + '/' + img, colorkey))
        # create or load config file for animation ---- #
        json_name = '_' + path.split('/')[-1]
        try:
            f = open(path + '/' + json_name + '.json', 'r')
            dat = f.read()
            f.close()
            self.config = json.loads(dat)

        except FileNotFoundError:
            self.config = {
                'offset': [0, 0],
                'pause': False,
                'center': False,
                'scale': [1, 1],
                'speed': 1
            }
            f = open(path + '/' + json_name + '.json', 'w')
            f.write(json.dumps(self.config))
            f.close()


'''
--------------------------------------------------- particle -----------------------------------------------------------
'''
class Particle():
    def __init__(self, particle_data, type, pos, vel, frame, decay, color):
        # data including imgs and config
        self.particle_data = particle_data
        # position
        self.pos = list(pos)
        # velocity
        self.vel = list(vel)
        # color of partical
        self.color = color
        # folder or type of particle
        self.type = type
        # config data
        self.pause = particle_data.config['pause']
        self.center = particle_data.config['center']
        self.scale = particle_data.config['scale']
        self.speed = particle_data.config['speed']
        # decay of particle
        self.decay = decay
        # var to determine when to remove
        self.pop = False
        # list of images from Particle Data
        self.imgs = self.particle_data.img_list
        # which img to start on
        self.frame = frame
        # len of imgs in animations also used in relation to particle life span
        self.timer = len(self.imgs) + 1 - frame
        # finds img according to frame
        self.calc_img()

    # returns glow surf
    def glow(self,game_time,color,scale):
        rand = random.randint(20, 30) / 30
        surf = core_fucs.circle_surf(self.timer * (math.sin(game_time * rand * .01) + scale),
                           (color[0] + self.timer, color[1] + self.timer, color[2] + self.timer))
        return surf

    # finds img and can edit it
    def calc_img(self):
        self.img = self.imgs[int(self.frame)]
        self.img = pygame.transform.scale(self.img, (
            self.img.get_width() // self.scale[0], self.img.get_height() // self.scale[1]))

    # pause or play
    def pause_play(self):
        self.pause = not self.pause

    # reset frame
    def rewind(self):
        self.frame = 0

    # increases frame by decay and dt and config speed
    def play(self, dt):
        # if not paused increase frame
        if not self.pause:
            self.frame += self.decay * dt * self.speed
            self.timer = len(self.imgs) + 1 - self.frame
        if self.frame >= len(self.imgs):
            self.pop = True

    # update particle
    def update(self, dt):
        self.play(dt)
        self.timer += self.decay
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if self.timer <= 0:
            # delete particle
            self.pop = True

    # render particle
    def render(self, surf, scroll):
        # find img
        self.calc_img()
        if self.pause == False:
            if self.center:
                if self.color:
                    img = core_fucs.swap_color(self.img, (255, 255, 255), self.color)
                    core_fucs.blit_center(surf, img, (self.pos[0] - scroll[0], self.pos[1] - scroll[1]))
                else:
                    core_fucs.blit_center(surf, self.img, (self.pos[0] - scroll[0], self.pos[1] - scroll[1]))

            else:
                surf.blit(self.img, (self.pos[0] - scroll[0], self.pos[1] - scroll[1]))

'''
--------------------------------------------------- particle manager ---------------------------------------------
'''
# manges particle folder
class ParticleManager():
    def __init__(self):
        self.particle_data = {}
        self.particles = []
        self.glows = []
        particles_anime = os.listdir(PARTICLE_PATH)
        for anime in particles_anime:
            self.particle_data[anime] = ParticleData(PARTICLE_PATH + '/' + anime, COLORKEY)

    # reset all particles
    def reset(self):
        self.particles = []

    # creates a new particle and appends to particle list
    def new(self, anime_name, pos, vel, frame, decay=.05, color=None):
        self.particles.append(Particle(self.particle_data[anime_name], anime_name, pos, vel, frame, decay, color))

    # update all particles
    def update(self,display,scroll,dt,game_time):
        for i, p in sorted(enumerate(self.particles), reverse=True):
            # remove dead particles
            if p.pop == True:
                self.particles.pop(i)
                continue
            # render all particles
            p.render(display, scroll)
            # update all particles
            p.update(dt)
            # if glow type
            if p.type == 'green_light':
                color = (3,6,4)
                surf = p.glow(game_time,color,3)
                core_fucs.blit_center_special(display, surf, (p.pos[0] + 3 - scroll[0], p.pos[1] - scroll[1]))
            if p.type == 'yellow_light':
                color = (20, 15, 1)
                surf = p.glow(game_time,color,2)
                core_fucs.blit_center_special(display, surf, (p.pos[0] + 5 - scroll[0], p.pos[1] + 5 - scroll[1]))
            if p.type == 'red_light':
                color = (20,12,11)
                surf = p.glow(game_time,color,1)
                core_fucs.blit_center_special(display, surf, (p.pos[0] + 5 - scroll[0], p.pos[1] + 5 - scroll[1]))


    # create particles in module rather in main.py changes depending on game
    # basically an outline if you want to use the same particle data
    '''
    def create_particle(self,pos):
        # particles
        if random.randint(1, 6) == 1:
            # create particles
            self.new_particle('light', pos, (random.randint(95, 105) / 100 - 1, random.randint(100, 150) / -1000),
                                          3 + random.randint(0, 20) / 10, .1)'''
