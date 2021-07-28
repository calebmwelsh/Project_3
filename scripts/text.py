# Create a font
import pygame, sys, math
from pygame.locals import *
from .core_fucs import *


colorkey = (0, 0, 0)

def load_font_img(path,color):
    global colorkey
    font_img = pygame.image.load(path)
    img_list = []
    corners_list = []
    start_pos = 0
    for x in range(font_img.get_width()):
        c = font_img.get_at((x, 0))
        c = (c[0], c[1], c[2])
        if c == (200, 200, 200):
            corner = ((start_pos, 0), (x, font_img.get_height()))
            start_pos = x + 1
            corners_list.append(corner)
    for corner in corners_list:
        width = abs(corner[0][0] - corner[1][0])
        height = abs(corner[0][1] - corner[1][1])
        img = clip(font_img, corner[0][0], corner[0][1], width, height)
        img = swap_color(img,(255, 0, 255),color)
        img.set_colorkey(colorkey)
        img_list.append((img, width))
    return img_list


class Font():
    def __init__(self, path,color=(255,255,255)):
        self.letter_imgs = load_font_img(path,color)
        self.order_list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
            'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '!',
            ':', '_', '.', '/', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0','-'
            ]

    def render(self, str, surf, pos):
        offset = 0
        for char in str:
            if char in self.order_list:
                idx = self.order_list.index(char)
                img, width = self.letter_imgs[idx]
                surf.blit(img, (pos[0] + offset, pos[1]))
                offset += width + 1


    def get_size(self, str):
        self.text_size = 0
        for char in str:
            if char in self.order_list:
                idx = self.order_list.index(char)
                img, width = self.letter_imgs[idx]
                self.text_size += width + 1
        return self.text_size
