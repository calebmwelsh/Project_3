import pygame
from ...core_fucs import *


class User_Data():
    def __init__(self,day):
        #self.app = app
        self.day = day
        self.data = []
        self.temp = [0,0,0]

    def add_event(self):
        self.data.append(self.temp)
        self.temp = [0,0,0]
