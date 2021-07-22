import pygame, os, math, random
import scripts.core_fucs as core_fucs

'''
---------------------------------------------- global vars -----------------------------------------------
'''
PROJECTILE_PATH = r'data/images/projectiles/'
COLORKEY = (0, 0, 0)

'''
---------------------------------------------------- projectile ---------------------------------------------
'''
class Projectile():
    def __init__(self, img, pos, vel,rand_c, type,color):
        self.img = img
        self.pos = list(pos)
        self.vel = list(vel)
        self.rand_c = rand_c
        self.type = type
        self.color = color

    # rect object
    @property
    def rect(self):
        return pygame.rect.Rect(self.pos[0], self.pos[1], self.img.get_width(), self.img.get_height())

    # increases pos by vel
    def update(self,dt):
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt

    # renders projectile and glow
    def render(self, display, scroll,game_time):
        if self.type == 'enemy':
            display.blit(self.img, (self.pos[0] - scroll[0], self.pos[1] - scroll[1]))
            surf = core_fucs.circle_surf(5 + 2 * math.sin(self.rand_c * game_time * .5) + 3,self.color)
            core_fucs.blit_center_special(display,surf,(self.pos[0] - scroll[0] + 2, self.pos[1] - scroll[1] + 2))

'''
--------------------------------------------------- particle manager ---------------------------------------------
'''
class ProjectileManager():
    def __init__(self):
        self.projectile_imgs = {}
        self.projectiles = []
        for img_path in os.listdir(PROJECTILE_PATH):
            img = core_fucs.load_img(PROJECTILE_PATH + '/' + img_path, COLORKEY)
            img_path = img_path.split('.')[0]
            self.projectile_imgs[img_path] = img

    # reset all projectiles
    def reset(self):
        self.projectiles = []

    # creates a new projectile
    def new(self, img_id, pos, vel,rand_c, type,color):
        self.projectiles.append(Projectile(self.projectile_imgs[img_id], pos, vel,rand_c, type,color))

    # updates all projectiles in projectile list
    def update(self,display,scroll,game_time,dt):
        for p in self.projectiles:
            p.update(dt)
            p.render(display,scroll,game_time)
        self.projectiles = self.projectiles[-300:]

    def collision(self,rect):
        for p in self.projectiles:
            if rect.collidepoint(p.pos):
                return True


    # create projectiles in module rather in main.py changes depending on game
    # basically an outline if you want to use the same projectile data
    '''
    def create_projectile(self,img_str,display,scroll):
        # create projectiles
        if random.randint(1, 6) == 1:
            self.new_projectile('img_0', (
            random.randint(0, display.get_width()) + scroll[0], display.get_height() + scroll[1]),
                                               (random.randint(5, 15) / 10 - 1, -1), random.random(), 'enemy')'''
