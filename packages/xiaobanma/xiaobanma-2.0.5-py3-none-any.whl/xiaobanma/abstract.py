from abc import ABCMeta, abstractmethod
import pygame
from pygame.locals import *
vec = pygame.math.Vector2

class AbsStrategy(metaclass = ABCMeta):
    '''
    Return the image property to the sprite
    '''
    @abstractmethod
    def update(self, position, rotation, scale):
        pass

class AbsSprite(metaclass = ABCMeta):
    @abstractmethod
    def update(self):
        pass



class AbsGameObject(metaclass = ABCMeta):

    def __init__(self, sprite_strategy, physics_strategy):
        self._sprite_strategy = sprite_strategy()
        self._physics_strategy = physics_strategy()
        self._position = vec2(0, 0)
        self._rotation = 0
        self._scale = vec2(0, 0)

    def update(self):
        self._physics_strategy.update(self._position, self._rotation, self._scale)
        self._sprite_strategy.update(self._position, self._rotation, self._scale)

    @abstractmethod
    def next_image(self):
        pass

    @abstractmethod
    def set_image(self, frame):
        pass

    @abstractmethod
    def forward(self, d):
        pass

    @abstractmethod
    def backward(self, d):
        pass

    @abstractmethod
    def left(self, a):
        pass

    @abstractmethod
    def right(self, a):
        pass

    @abstractmethod
    def goto(self, x, *y):
        pass

    @abstractmethod
    def slide_to(self, x, *y):
        pass

    @abstractmethod
    def face_to(self, x, *y):
        pass
