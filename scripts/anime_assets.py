''' animation for entities'''
import os, pygame, json
import scripts.spritesheet_loader as spritesheet_loader
from pygame.locals import *

# change depending on game and folder placement -- #
ANIMATIONPATH = 'data/images/animations/'
COLORKEY = (0,0,0)

# loads img -- #
def load_img(img_path,colorkey):
    img = pygame.image.load(img_path)
    img.set_colorkey(colorkey)
    return img

# loads all data from animations files and creates or loads configs --- #
class AnimationData():
    # path is a specific folder the has each frame ex (player idle) ---------- #
    def __init__(self, path,colorkey):
        # makes a list of all images in folder according to path -- #
        imgs = os.listdir(path)
        # load imgs and put in list
        self.img_list = []
        for img in imgs:
            if img.split('.')[-1] == 'png':
                self.img_list.append([load_img(path + '/' + img,colorkey)])
        # create or load config file for animation ---- #
        json_name = '_'+ path.split('/')[-1]
        try:
            f = open(path + '/' + json_name + '.json' , 'r')
            dat = f.read()
            f.close()
            self.config = json.loads(dat)

        except FileNotFoundError:
            self.config = {
                        'frames':[5 for i in range(len(self.img_list))],
                        'offset': [0,0],
                        'pause': False,
                        'speed': 1,
                        'loop':True
                        }
            f = open(path + '/' + json_name + '.json', 'w')
            f.write(json.dumps(self.config))
            f.close()

        # set each img to a specific frame ex - ([5,img_0],[10,img_1]) each img 5 frames ----- #
        self.frame_data = []
        total_frames = 0
        for n, num_frame in enumerate(self.config['frames']):
            total_frames += num_frame
            self.frame_data.append([total_frames,self.img_list[n][-1]])

        self.duration = sum(self.config['frames'])

# animates a loaded animation from the animations folder
class Animation():
    def __init__(self,animation_data):
        # animations data from animation data class -- #
        self.animation_data = animation_data
        # frame
        self.frame = 0
        # pause animation
        self.pause = animation_data.config['pause']
        # determines weather it is a loop or go through all frames in once
        self.loop = animation_data.config['loop']
        self.just_looped = False
        # finds img according to frame
        self.calc_img()

    def calc_img(self):
        # for all imgs and durations [5,img] -- #
        for frame in self.animation_data.frame_data:
            duration = frame[0]
            if duration > self.frame:
                self.img = frame[1]
                break
            # if the duration of all frames is done the last img in the animation folder is self.img -- #
            if self.animation_data.duration < self.frame:
                self.img = self.animation_data.frame_data[-1][1]

    def play(self,dt):
        self.just_looped = False
        # if not paused increase frame
        if not self.pause:
            self.frame += dt * 60 * self.animation_data.config['speed']
        # if a looped anime loop it
        if self.loop:
            while self.frame > self.animation_data.duration:
                # reset frame
                self.rewind()
                self.just_looped = True
        # find img
        self.calc_img()

    # pause or play
    def pause_play(self):
        self.pause = not self.pause

    # reset frame
    def rewind(self):
        self.frame = 0


# creates a dictionary with all the animations from animation folder --- #
class AnimationManager():
    def __init__(self):
        self.animation_data = {}
        animations = os.listdir(ANIMATIONPATH)
        for anime in animations:
            self.animation_data[anime] = AnimationData(ANIMATIONPATH + '/' + anime,COLORKEY)

    # changes animation folder idle,run,jump
    def loc_anime(self,new_anime_id):
        new_anime = Animation(self.animation_data[new_anime_id])
        return new_anime
