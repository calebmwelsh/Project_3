import pygame, math, json

COLORKEY = (0,0,0)

'''
------------------------------------------ path funcs -------------------------------------------
'''
# open file read and set data to a var return var
def read_f(path):
    f = open(path, 'r')
    dat = f.read()
    f.close()
    return dat
# edit a file and dump data into file
def write_f(path, dat):
    f = open(path, 'w')
    f.write(dat)
    f.close()

# loads json file and extracts data
def load_json(path):
    f = open(path, 'r')
    dat = f.read()
    f.close()
    json_dat = json.loads(dat)
    return json_dat
'''
------------------------------------------ surface funcs ---------------------------------------------
'''
# swap the color of a image
def swap_color(img, old_c, new_c):
    global COLORKEY
    img.set_colorkey(old_c)
    surf = img.copy()
    surf.fill(new_c)
    surf.blit(img, (0, 0))
    surf.set_colorkey(COLORKEY)
    return surf

# clip part of a surface
def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()
# loads img
def load_img(img_path, colorkey):
    img = pygame.image.load(img_path)
    img.set_colorkey(colorkey)
    return img
'''
------------------------------------------------- physics funcs ----------------------------------------------
'''
# fines 4 corners using top left and bottom right corners
def rect_corners(points):
    point_1 = points[0]
    point_2 = points[1]
    out_1 = [min(point_1[0], point_2[0]), min(point_1[1], point_2[1])]
    out_2 = [max(point_1[0], point_2[0]), max(point_1[1], point_2[1])]
    return [out_1, out_2]
# creates rect out of corners
def corner_rect(points):
    points = rect_corners(points)
    r = pygame.Rect(points[0][0], points[0][1], points[1][0] - points[0][0], points[1][1] - points[0][1])
    return r
# fines all points given top left and bottom right corners
def points_between_2d(points):
    points = rect_corners(points)
    width = points[1][0] - points[0][0] + 1
    height = points[1][1] - points[0][1] + 1
    point_list = []
    for y in range(height):
        for x in range(width):
            point_list.append([points[0][0] + x, points[0][1] + y])
    return point_list
# determines if two point lists intercept
def point_list_collide(list1,list2):
    for point in list1:
        if point in list2:
            return True
        else:
            return False
# fines midpoint of 2 points
def midpoint(selection_points):
    point1 = selection_points[0]
    point2 = selection_points[1]
    x = (point2[0] + point1[0]) / 2
    y = (point2[1] + point1[1]) / 2
    return [x,y]

def angle_to(points):
    return math.atan2(points[1][1] - points[0][1], points[1][0] - points[0][0])



# circle glow ------------------ #
# create circle
def circle_surf(size, color):
    surf = pygame.surface.Surface((size * 2 + 2, size * 2 + 2))
    pygame.draw.circle(surf, color, (size + 1, size + 1), size)
    return surf
'''
------------------------------------------------- display funcs ----------------------------------------------
'''
# for glow
def blit_center_special(target_surf, surf, loc):
    target_surf.blit(surf, (loc[0] - surf.get_width() // 2, loc[1] - surf.get_height() // 2),special_flags=pygame.BLEND_RGBA_ADD)
# ------------------------------- #

# renders center of given surf
def blit_center(target_surf, surf, loc):
    target_surf.blit(surf, (loc[0] - surf.get_width() // 2, loc[1] - surf.get_height() // 2))
