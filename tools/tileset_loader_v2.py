# Setup pygame/window ---------------------------------------- #
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, sys
from core_fucs import clip
from pathlib import Path
from pygame.locals import *

parent = os.path.dirname(__file__)
dir_path = Path(parent).parent.absolute()
os.chdir(dir_path)

# data\images\image_0.png

path = input('Name of file: ')

SCALE = 2
COLORKEY = (0, 0, 0)
FORCE_IMG = (200, 200, 200)
FORCE_BG = (0, 0, 0)

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Spritesheet gen")
screen = pygame.display.set_mode((500, 500) ,0,32)
img = pygame.image.load(path)
display_dimensions = [img.get_width() * SCALE, img.get_height() * SCALE]
screen = pygame.display.set_mode(display_dimensions, 0,32)

display = img.copy()


clicking = None

def generate_borders(base_range):
    # base range = (two points) [[0,0],[200,200]]
    corners = [
        # top left
        [min(base_range[0][0], base_range[1][0]), min(base_range[0][1],base_range[1][1])],
        # top right
        [max(base_range[0][0], base_range[1][0]), min(base_range[0][1],base_range[1][1])],
        # bottom right
        [max(base_range[0][0], base_range[1][0]), max(base_range[0][1],base_range[1][1])],
        # bottom left
        [min(base_range[0][0], base_range[1][0]), max(base_range[0][1],base_range[1][1])]
        ]
    # edit preset for corners
    while True:
        full_clear = True
        for i in range(4):
            clear = True
            if i == 0: # top
                for j in range(corners[1][0] - corners[0][0] + 1):
                    c = img.get_at((corners[0][0] + j, corners[0][1]))
                    c = (c[0], c[1], c[2])
                    if c != COLORKEY:
                        clear = False
                        full_clear = False
                if not clear:
                    corners[0][1] -= 1
                    corners[1][1] -= 1

            clear = True
            if i == 1: # right
                for j in range(corners[2][1] - corners[1][1] + 1):
                    c = img.get_at((corners[1][0], corners[1][1] + j))
                    c = (c[0], c[1], c[2])
                    if c != COLORKEY:
                        clear = False
                        full_clear = False
                if not clear:
                    corners[1][0] += 1
                    corners[2][0] += 1

            clear = True
            if i == 2: # bottom
                for j in range(corners[2][0] - corners[3][0] + 1):
                    c = img.get_at((corners[3][0] + j, corners[3][1]))
                    c = (c[0], c[1], c[2])
                    if c != COLORKEY:
                        clear = False
                        full_clear = False
                if not clear:
                    corners[2][1] += 1
                    corners[3][1] += 1

            clear = True
            if i == 3: # left
                for j in range(corners[3][1] - corners[0][1] + 1):
                    c = img.get_at((corners[0][0], corners[0][1] + j))
                    c = (c[0], c[1], c[2])
                    if c != COLORKEY:
                        clear = False
                        full_clear = False
                if not clear:
                    corners[3][0] -= 1
                    corners[0][0] -= 1

        # if every side has reached a black pixel
        if full_clear:
            break

    return corners

def generate_tileset():
    # list for rects the correspond to img on display img
    rect_form_clips = []
    # fill rect form clip with rects for display img
    for sec in clip_sections:
        row = sec[0]
        while row >= len(rect_form_clips):
            rect_form_clips.append([])
        corners = sec[1]
        # create rect and add to rect list with row as a index for rect
        x,y = corners[0][0] + 1, corners[0][1] + 1
        width = corners[1][0] - corners[0][0] - 1
        height = corners[2][1] - corners[1][1] - 1
        rect_form_clips[row].append(pygame.Rect(x, y, width, height))
    # create empty spritesheet
    max_width = 0
    height = 0
    for row in rect_form_clips:
        width = sum([sec.width + 2 for sec in row]) + 1
        height += max([sec.height + 2 for sec in row])
        max_width = max(width, max_width)
    tileset_surf = pygame.Surface((max_width, height))
    tileset_surf.fill(FORCE_BG)

    # place imgs on spritesheet
    y = 0
    for row in rect_form_clips:
        tileset_surf.set_at((0, y), (255, 255, 0))
        x = 1
        for sec in row:
            sec_img = clip(img, sec.x, sec.y, sec.width, sec.height)
            if FORCE_IMG:
                sec_img.set_colorkey(FORCE_IMG)
            tileset_surf.blit(sec_img, (x + 1, y + 1))
            tileset_surf.set_at((x, y), (255, 0, 255))
            tileset_surf.set_at((x + sec.width + 1, y), (0, 255, 255))
            tileset_surf.set_at((x, y + sec.height + 1), (0, 255, 255))
            x += sec.width + 2
        y += max([sec.height + 2 for sec in row])
    return tileset_surf

clip_sections = []
current_row = 0
generate_mode = False
save_count = 0
while True:
    display.fill((0,0,0))
    if not generate_mode:
        display.blit(img, (0, 0))
        mx, my = pygame.mouse.get_pos()
        mx = int (mx / SCALE)
        my = int (my / SCALE)

        for sec in clip_sections:
            c = (255, 0, 255)
            if sec[0] != current_row:
                c = (0, 255, 255)
            pygame.draw.polygon(display, c, sec[1], 1)



        #if clicking:
            #pygame.draw.rect(display, (255, 0, 255), pygame.Rect(clicking[0], clicking[1],mx - clicking[0], my - clicking[1]),1)

    else:
        display.blit(genned_tileset, (0, 0))


    # Buttons --

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_z:
                if clip_sections != []:
                    clip_sections.pop(-1)
            if event.key == K_r:
                current_row += 1
            if event.key == K_c:
                clip_sections = []
            if event.key == K_s:
                pygame.image.save(display,'data/images/tilesets/tileset.png')
                save_count += 1
            if event.key == K_g:
                if not generate_mode:
                    generate_mode = True
                    genned_tileset = generate_tileset()
                    display_dimensions = [genned_tileset.get_width() * SCALE, genned_tileset.get_height() * SCALE]
                    screen = pygame.display.set_mode(display_dimensions, 0,32)
                    display = genned_tileset.copy()
                else:
                    generate_mode = False
                    display = img.copy()
                    display_dimensions = [genned_tileset.get_width() * SCALE, genned_tileset.get_height() * SCALE]
                    screen = pygame.display.set_mode(display_dimensions, 0,32)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                clicking = [mx, my]
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if clicking != None:
                    clip_sections.append([current_row,generate_borders([(clicking[0],clicking[1]),(clicking[0] + 1,clicking[1] + 1)])])
                    clicking = None

    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(60)
