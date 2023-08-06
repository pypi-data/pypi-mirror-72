from .config import *

class GameObject():
    def __init__(self):
        self._sprite = None
        self._body = None
        self._tiledmap_bodies = None
        self._pos = vec(0, 0)
        self._rot = 0
        self._scl = vec(1, 1)
        self.alive = True

    def __repr__(self):
        return f"Sprite;Physics"

    def set_sprite(self, sprite):
        self._sprite = sprite
        self._sprite.set_parent(self)

    def set_body(self, body):
        self._body = body
        if self._body:
            self._body.set_parent(self)

    def set_tiledmap_bodies(self, tiledmap_bodies):
        self._tiledmap_bodies = tiledmap_bodies
        if self._tiledmap_bodies:
            self._tiledmap_bodies.set_parent(self)

    @property
    def sprite(self):
        return self._sprite

    @property
    def body(self):
        return self._body
    
    @ property
    def tiledmap_bodies(self):
        return self._tiledmap_bodies

    @ property
    def pos(self):
        return self._pos

    @ pos.setter
    def pos(self, pos):
        if self._sprite:
            self._pos = vec(pos)
        if self._body:
            self._body.set_pos(pos)
        if self._tiledmap_bodies:
            self._tiledmap_bodies.set_pos(pos)

            
    @ property
    def x(self):
        return self._pos[0]

    @ property
    def y(self):
        return self._pos[1]

    @ x.setter
    def x(self, x):
        pos = vec(x, self._pos[1])
        self.pos = pos

    @ y.setter
    def y(self, y):
        pos = vec(self._pos[0], y)
        self.pos = pos

    @ property
    def rot(self):
        return self._rot

    @ rot.setter
    def rot(self, rot):
        if self.sprite:
            self.sprite.rotated = True
        self._rot = rot

    @ property
    def scl(self):
        return self._scl

    @ scl.setter
    def scl(self, xscl, *yscl):
        if yscl:
            self._scl = vec(xscl, *yscl)
        else:
            self._scl = vec(xscl)

    def kill(self):
        if self._sprite:
            self._sprite.kill()
            self._sprite
        if self._body:
            self._body.kill()
        if self._tiledmap_bodies:
           self._tiledmap_bodies.kill()
        self._sprite = None
        self._body = None
        self._tiledmap_bodies = None
        self.alive = False

    