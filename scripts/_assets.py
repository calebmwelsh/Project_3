# import modules
import os
from . import spritesheet_loader
from . import anime_assets as anime

SPRITESHEETPATH = R'data\images\tilesets'
COLORKEY = (0,0,0)


# funcs

# loads img -- #
def load_img(img_path,colorkey):
    img = pygame.image.load(img_path)
    img.set_colorkey(colorkey)
    return img

# assets object
class Assets():
    def __init__(self,game):
        # game
        self.game = game
        # tilesets imgs and offset config for tiles
        self.spritesheets, self.offset_dat = spritesheet_loader.load_spritesheets(SPRITESHEETPATH)
        # animation manager ---- #
        self.animations = anime.AnimationManager()
        # weapons
        self.weapons = self.load_dir('data\images\weapons')

    # load a folder of imgs
    def load_dir(self,path):
        images_dict = {}
        for img_path in os.listdir(path):
            images[img_path.split('.')[0]] = load_img(img_path,COLORKEY)
        return images_dict
