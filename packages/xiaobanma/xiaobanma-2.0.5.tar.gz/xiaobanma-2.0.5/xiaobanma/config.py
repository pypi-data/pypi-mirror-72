import pygame
from pygame.locals import *
import os
from .settings import *
import pymunk
import pymunk.pygame_util
from pymunk.vec2d import Vec2d
import time
from .facilitate import *
vec = pygame.math.Vector2
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.mixer.init()
pygame.mixer.set_num_channels(20)
pygame.init()

pygame.font.init()



cwd = os.path.dirname(__file__)
class global_var:
    WIDTH = 0
    HEIGHT = 0
    EVENTS = []
    ALL_SPRITES = None
    ALL_BODIES = None
    SCREEN = None
    SPACE = None
    CAMERA = None
    DEBUG_DRAW = False
    GET_CLICKED = False
    JUST_RELEASED = False
    TMBG = None
    LINES = []

    @ classmethod
    def set_value(cls, var, value):
        cls.var = value

    @ classmethod
    def get_value(cls, var):
        return cls.var

def pygame2Cartesian(x, *y):
    if y:
        return (x - global_var.WIDTH // 2, global_var.HEIGHT // 2 - y)
    else:
        return (x[0] - global_var.WIDTH // 2, global_var.HEIGHT // 2 - x[1])

def Cartesian2pygame(x, *y):
    if y:
        return (x + global_var.WIDTH // 2, global_var.HEIGHT // 2 - y)
    else:
        return (x[0] + global_var.WIDTH // 2, global_var.HEIGHT // 2 - x[1])

class Group():
    def __init__(self):
        self._group = []

    def add(self, obj):
        self._group.append(obj)

    def update(self):
        for obj in self._group:
            obj._update()
            if obj._gameObject.alive:
                obj.update()

    def remove(self, obj):
        self._group.remove(obj)

global_var.GROUP = Group()