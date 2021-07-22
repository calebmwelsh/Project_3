# Setup pygame/window ---------------------------------------- #
import os
#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, sys, cv2
from pathlib import Path
from pygame.locals import *

parent = os.path.dirname(__file__)
dir_path = Path(parent).parent.absolute()
os.chdir(dir_path)

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('tile_editor')
window_size = [1300, 700]
# fonts
font = pygame.font.SysFont(None, 20)

run = True
while run:
    path = input('Name of file: ')
    try:
        img = pygame.image.load(os.path.join(path))
    except FileNotFoundError:
        path = ''
        pass
    else:
        run = False

tile_size = 15
# setting up screens and tileset -------------------------- #
img = pygame.image.load(path)
img_size = img.get_size()
scale = window_size[0] // img_size[0]
img = pygame.transform.scale(img, (img_size[0] * scale, img_size[1] * scale))
img_size = img.get_size()
window_size = img_size
screen = pygame.display.set_mode(window_size, 0, 32)
cv2_img = cv2.imread(path)
cv2_img_p = cv2.imread(path)
cv2_img = cv2.resize(cv2_img, (0, 0), fx=scale, fy=scale)
tileset = cv2_img[0:1, 0:1]
tileset = cv2.resize(tileset, (0, 0), fx=tile_size + (tile_size // 2), fy=tile_size * 11 + 1)

sel_point = False

img_list = []
img_rects = []

'''
cv2.imshow('image',cv2_img)
cv2.waitKey(0)'''

while True:
    screen.fill((0, 0, 0))
    screen.blit(img, (0, 0))

    pos = pygame.mouse.get_pos()
    mouse = pygame.mouse.get_pressed()

    if mouse[0] == 1:
        rev_pos = pos[1], pos[0]
        b, r, g = cv2_img[rev_pos]
        if b != 0 and r != 0 and g != 0:
            # going left ------------------------------------------ #
            l_list = []
            x = 0
            y = 0
            run = True
            # going to the left up -------------- #
            while run:
                new_pos = rev_pos[0] - y, rev_pos[1] - x
                b, r, g = cv2_img[new_pos]
                if b == 0 and r == 0 and g == 0:
                    y += 1
                    x = 0
                    temp = [new_pos[1], new_pos[0]]
                    l_list.append(temp)
                    temp_pos = rev_pos[0] - y, rev_pos[1] - x
                    b, r, g = cv2_img[temp_pos]
                    if b == 0 and r == 0 and g == 0:
                        run = False
                else:
                    x += 1
            x = 0
            y = 0
            run = True
            # going to the left down -------------- #
            while run:
                new_pos = rev_pos[0] + y, rev_pos[1] - x
                b, r, g = cv2_img[new_pos]
                if b == 0 and r == 0 and g == 0:
                    y += 1
                    x = 0
                    temp = [new_pos[1], new_pos[0]]
                    l_list.append(temp)
                    temp_pos = rev_pos[0] + y, rev_pos[1] - x
                    b, r, g = cv2_img[temp_pos]
                    if b == 0 and r == 0 and g == 0:
                        run = False
                else:
                    x += 1

            # going right -------------------------------------------------------- #
            r_list = []
            x = 0
            y = 0
            run = True
            # going to the right up -------------- #
            while run:
                new_pos = rev_pos[0] - y, rev_pos[1] + x
                b, r, g = cv2_img[new_pos]
                if b == 0 and r == 0 and g == 0:
                    y += 1
                    x = 0
                    temp = [new_pos[1], new_pos[0]]
                    r_list.append(temp)
                    temp_pos = rev_pos[0] - y, rev_pos[1] + x
                    b, r, g = cv2_img[temp_pos]
                    if b == 0 and r == 0 and g == 0:
                        run = False
                else:
                    x += 1

            x = 0
            y = 0
            run = True
            # going to the right down -------------- #
            while run:
                new_pos = rev_pos[0] + y, rev_pos[1] + x
                b, r, g = cv2_img[new_pos]
                if b == 0 and r == 0 and g == 0:
                    y += 1
                    x = 0
                    temp = [new_pos[1], new_pos[0]]
                    r_list.append(temp)
                    temp_pos = rev_pos[0] + y, rev_pos[1] + x
                    b, r, g = cv2_img[temp_pos]
                    if b == 0 and r == 0 and g == 0:
                        run = False
                else:
                    x += 1

            # going up ------------------------------------------------------------ #
            u_list = []
            x = 0
            y = 0
            run = True
            # going to the up left -------------- #
            while run:
                new_pos = rev_pos[0] - y, rev_pos[1] - x
                b, r, g = cv2_img[new_pos]
                if b == 0 and r == 0 and g == 0:
                    x += 1
                    y = 0
                    temp = [new_pos[1], new_pos[0]]
                    u_list.append(temp)
                    temp_pos = rev_pos[0] - y, rev_pos[1] - x
                    b, r, g = cv2_img[temp_pos]
                    if b == 0 and r == 0 and g == 0:
                        run = False
                else:
                    y += 1
            x = 0
            y = 0
            run = True
            # going to the up right -------------- #
            while run:
                new_pos = rev_pos[0] - y, rev_pos[1] + x
                b, r, g = cv2_img[new_pos]
                if b == 0 and r == 0 and g == 0:
                    x += 1
                    y = 0
                    temp = [new_pos[1], new_pos[0]]
                    u_list.append(temp)
                    temp_pos = rev_pos[0] - y, rev_pos[1] + x
                    b, r, g = cv2_img[temp_pos]
                    if b == 0 and r == 0 and g == 0:
                        run = False
                else:
                    y += 1

            # going down -------------------------------------------------------- #
            d_list = []
            x = 0
            y = 0
            run = True
            # going to the down left -------------- #
            while run:
                new_pos = rev_pos[0] + y, rev_pos[1] - x
                b, r, g = cv2_img[new_pos]
                if b == 0 and r == 0 and g == 0:
                    x += 1
                    y = 0
                    temp = [new_pos[1], new_pos[0]]
                    d_list.append(temp)
                    temp_pos = rev_pos[0] + y, rev_pos[1] - x
                    b, r, g = cv2_img[temp_pos]
                    if b == 0 and r == 0 and g == 0:
                        run = False
                else:
                    y += 1

            x = 0
            y = 0
            run = True
            # going to the down right -------------- #
            while run:
                new_pos = rev_pos[0] + y, rev_pos[1] + x
                b, r, g = cv2_img[new_pos]
                if b == 0 and r == 0 and g == 0:
                    x += 1
                    y = 0
                    temp = [new_pos[1], new_pos[0]]
                    d_list.append(temp)
                    temp_pos = rev_pos[0] + y, rev_pos[1] + x
                    b, r, g = cv2_img[temp_pos]
                    if b == 0 and r == 0 and g == 0:
                        run = False
                else:
                    y += 1

            sel_point = True

    # show selected item ----------------------------- #
    if sel_point == True:
        for i in l_list:
            rect = pygame.rect.Rect(i[0], i[1], 2, 2)
            pygame.draw.rect(screen, 'red', rect)
        for i in r_list:
            rect = pygame.rect.Rect(i[0], i[1], 2, 2)
            pygame.draw.rect(screen, 'red', rect)
        for i in u_list:
            rect = pygame.rect.Rect(i[0], i[1], 2, 2)
            pygame.draw.rect(screen, 'red', rect)
        for i in d_list:
            rect = pygame.rect.Rect(i[0], i[1], 2, 2)
            pygame.draw.rect(screen, 'red', rect)

        # find furthest points
        l_vals = []
        r_vals = []
        u_vals = []
        d_vals = []
        for points in l_list:
            l_vals.append(points[0])
            l_vals.sort()
            left = l_vals[0]
        for points in r_list:
            r_vals.append(points[0])
            r_vals.sort()
            right = r_vals[-1]
        for points in d_list:
            d_vals.append(points[1])
            d_vals.sort()
            down = d_vals[-1]
        for points in u_list:
            u_vals.append(points[1])
            u_vals.sort()
            up = u_vals[0]
        # find corners ----------- #
        lc = [left, up]
        rc = [right, down]
        # create potential image ----------------- #
        img_ = cv2_img_p[lc[1] // scale:rc[1] // scale, lc[0] // scale:rc[0] // scale]

    if len(img_rects) > 0:
        for corners in img_rects:
            t_l = corners[0][0], corners[0][1]
            t_r = corners[1][0], corners[0][1]
            b_l = corners[0][0], corners[1][1]
            b_r = corners[1][0], corners[1][1]
            pygame.draw.line(screen, 'white', (t_l), (t_r), 2)
            pygame.draw.line(screen, 'white', (t_r), (b_r), 2)
            pygame.draw.line(screen, 'white', (b_r), (b_l), 2)
            pygame.draw.line(screen, 'white', (b_l), (t_l), 2)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                img_list.append(img_)
                img_rects.append([lc, rc])
                sel_point = False
            if event.key == K_f:
                row_end = 1
                row_begin = 0
                for tile in img_list:
                    tile[0, 0] = [255, 0, 255]
                    row_begin = 0 + row_end
                    row_end += tile.shape[0]
                    tileset[row_begin:row_end, 1:tile.shape[1] + 1] = tile
                    row_end += 1
                    tileset[row_begin, 0] = [0, 255, 255]
                    tileset[row_begin, tile.shape[1] + 1] = [255, 255, 0]
                    tileset[row_begin + tile.shape[0], 1] = [255, 255, 0]


                path = os.path.join(r'data\images\tilesets\tileset.png')
                cv2.imwrite(path, tileset)

            if event.key == K_g:
                try:
                    img_ = ''
                    img_list = []
                    img_rects = []
                    lc, rc = 0, 0
                    sel_point = False
                except:
                    pass

    pygame.display.update()
    clock.tick(60)
