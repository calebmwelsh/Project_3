import pygame, os, json
from core_fucs import *

colorkey = (0, 0, 0)


def load_spritesheet(spritesheet):
    rows = []
    spritesheet_dat = []
    for y in range(spritesheet.get_height()):
        c = spritesheet.get_at((0, y))
        c = (c[0], c[1], c[2])
        # yellow pixel --------------------- #
        if c == (255, 255, 0):
            rows.append(y)
    # for every yellow pixel (row) ------------------ #
    for row in rows:
        row_content = []
        for x in range(spritesheet.get_width()):
            c = spritesheet.get_at((x, row))
            c = (c[0], c[1], c[2])
            # magenta pixel --------------------- #
            if c == (255, 0, 255):
                x2 = 0
                # parse through x axis
                while True:
                    x2 += 1
                    c = spritesheet.get_at((x + x2, row))
                    c = (c[0], c[1], c[2])
                    # cyan pixel --------------------- #
                    if c == (0, 255, 255):
                        # saves width for tile --------------------- #
                        width = x2
                        break
                y2 = 0
                # parse through y axis
                while True:
                    y2 += 1
                    c = spritesheet.get_at((x, row + y2))
                    c = (c[0], c[1], c[2])
                    # cyan pixel --------------------- #
                    if c == (0, 255, 255):
                        # saves height for tile --------------------- #
                        height = y2
                        break
                # clips tile from spritesheet --------------------- #
                img = clip(spritesheet, x + 1, row + 1, x2 - 1, y2 - 1)
                img.set_colorkey(colorkey)
                row_content.append(img)
        spritesheet_dat.append(row_content)
    return spritesheet_dat

# opens folder of spritesheets  --------------------- #
def load_spritesheets(path):
    spritesheet_list = os.listdir(path)
    spritesheets = {}
    spritesheets_data = {}
    # for all the sheets in a spritesheet folder --------------------- #
    for file in spritesheet_list:
        if file.split('.')[ - 1] == 'png':
            spritesheet_dat = load_spritesheet(pygame.image.load(path + '/' + file))
            spritesheets[file.split('.')[0]] = spritesheet_dat
            try:
                dat = read_f(path + '/' + file.split('.')[0] + '.json')
                spritesheets_data[file.split('.')[0]] = json.loads(dat)
            except FileNotFoundError:
                    pass

    return spritesheets,spritesheets_data

def get_img(spritesheets, img_loc):
    return spritesheets[img_loc[0]][img_loc[1]][img_loc[2]]
