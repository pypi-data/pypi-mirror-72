from .config import *

class Spring():
    def __init__(self):
        pass

class Connect(pymunk.constraint.PinJoint):
    def __init__(self, a, b):
        pymunk.constraint.PinJoint.__init__(a._gameObject.body.body, b._gameObject.body.body, (0,0), (0, 0))
        global_var.SPACE.add(self) 

def connect(a, b):
    for vertice1 in a.vertices:
        for vertice2 in b.vertices:
            #global_var.SPACE.add(pymunk.constraint.PinJoint(a.body, b.body, vertice1, vertice2))
            global_var.SPACE.add(pymunk.constraint.GearJoint(a.body, b.body, 0, 1))
            pass



