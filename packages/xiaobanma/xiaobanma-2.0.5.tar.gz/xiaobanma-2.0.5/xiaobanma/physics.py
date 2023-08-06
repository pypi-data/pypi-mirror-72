from .config import *
from .constraints import *


class BodiesGroup():
    def __init__(self):
        self._group = []

    def update(self):
        for body in self._group:
            body.update()

    def add(self, body):
        self._group.append(body)

    def remove(self, body):
        self._group.remove(body)

class TiledMapBodiesGroup():
    def __init__(self):
        self._group = []

    def update(self):
        for tiledmapbodies in self._group:
            tiledmapbodies.update()

    def add(self, tiledmapbodies):
        self._group.append(tiledmapbodies)

    def remove(self, tiledmapbodies):
        self._group.remove(tiledmapbodies)

class Body():
    def __init__(self, body_type, shape, size, sensor):
        mass = 1
        moment = 1
        if shape == 'CIRCLE':
            moment = pymunk.moment_for_circle(mass, 0, size)    
        if body_type == 'KINEMATIC':
            self.body = pymunk.Body(mass, moment, body_type = pymunk.Body.KINEMATIC)
        elif body_type == 'DYNAMIC':
            self.body = pymunk.Body(mass, moment, body_type = pymunk.Body.DYNAMIC)
        elif body_type == 'STATIC':
            self.body = pymunk.Body(mass, moment, body_type = pymunk.Body.STATIC)
        self.body.position = 0,0
        if shape == 'CIRCLE':
            self.shape = pymunk.Circle(self.body, size) 
        elif shape == 'BOX':
            width, height = size
            points = [(-width//2, -height//2), (-width//2, height//2), (width//2,height//2), (width//2, -height//2)]
            self.shape = pymunk.Poly(self.body, points)
        elif shape == 'POLY':
            self.shape = pymunk.Poly(self.body, size)

        self.shape.sensor = sensor
        global_var.SPACE.add(self.body, self.shape) 
        global_var.BODIES.add(self)


    def set_parent(self, parent):
        self._parent = parent
        if 'offset' in self.__dict__:
            self.shape.body.position = self._parent.pos + self.offset
        else:
            self.shape.body.position = self._parent.pos
            
    def set_pos(self, pos):
        self.shape.body.position = pos
        global_var.SPACE.reindex_shapes_for_body(self.body)

    def update(self):
        if 'offset' not in self.__dict__:
            self._parent.pos = self.shape.body.position
        self._parent.rot = self.body.angle / 3.1415926 * 180
        
    def collide(self, other):
        if self.shape.shapes_collide(other.shape).points:
            return True
        else:
            return False

    def point_query(self, p):
        if self.shape.point_query(p)[0] <= 0:
            return True
        else:
            return False

    def kill(self):
        global_var.SPACE.remove(self.body, self.shape)
        global_var.BODIES.remove(self)  

    def set_rot(self, rot):
        self.body.angle = rot / 180 * 3.1415926
        global_var.SPACE.reindex_shapes_for_body(self.body)       

    @ property
    def velocity(self):
        return self.body.velocity 

    @ velocity.setter
    def velocity(self, v):
        self.body.velocity = v

    @ property
    def angular_velocity(self):
        return self.body.angular_velocity

    @ angular_velocity.setter
    def angular_velocity(self, av):
        self.body.angular_velocity = av

    def apply_impulse_at_local_point(self, impulse):
        self.body.apply_impulse_at_local_point(impulse)

    @ property
    def elasticity(self):
        return self.shape.elasticity

    @ elasticity.setter
    def elasticity(self, e):
        self.shape.elasticity = e

    @ property
    def friction(self):
        return self.shape.friction

    @ friction.setter
    def friction(self, f):
        self.shape.friction = f  

    @ property
    def mass(self):
        return self.body.mass

    @ mass.setter
    def mass(self, m): 
        self.body.mass = m

    def set_vertices(self, vertices, transform):
        self.shape.unsafe_set_vertices(vertices, transform)

class TiledMapBodies(list):
    def __init__(self, body_type, objs, sensor):
        list.__init__(self)
        global_var.TMBG.add(self)
        self._velocity = vec(0, 0)
        self._angular_velocity = 0
        self._mass = 1
        self._friction = 0
        self._elasticity = 1
        self.pos = vec(0, 0)
        for obj in objs:
            try:
                body = Body(body_type, 'POLY', obj.points, sensor)
            except:
                print(obj.__dict__)
            body.offset = vec(0, 0)
            body.vertices = body.shape.get_vertices()
            body.offsetrot = 0
            body.offsetscale = vec(1, 1)
            body.set_parent(self)
            self.append(body)
        if body_type == 'DYNAMIC':
            print('不建议将网格地图设置为Character')
            dict = []
            for body in self:
                for other in self:
                    if body != other and {body, other} not in dict:
                        connect(body, other)
                        dict.append({body, other})

    def set_parent(self, parent):
        self._parent = parent
        self.pos = self._parent.pos
            
    def set_pos(self, pos):
        self.pos = pos          
        for body in self:
            body.offset_scaled = vec(body.offset[0] * body.offsetscale[0], body.offset[1] * body.offsetscale[1])
            body.body.position = self.pos + body.offset_scaled.rotate(body.offsetrot)
            global_var.SPACE.reindex_shapes_for_body(body.body)  
        
    def update(self):
        positions = vec(0,0)
        for body in self:
                positions += body.body.position
        positions /= len(self)
        self.pos = positions
        self._parent.pos = self.pos
        self._parent.rot = self[0].body.angle / 3.1415926 * 180
        

    def collide(self, other):
        for body in self:
            if body.shape.shapes_collide(other.shape).points:
                return True
        else:
            return False

    def point_query(self, p):
        for body in self:
            if body.shape.point_query(p)[0] <= 0:
                return True
        else:
            return False

    def kill(self):
        for body in self:
            global_var.SPACE.remove(body.body, body.shape)
            global_var.BODIES.remove(body) 

    def set_rot(self, rot):
        for body in self:
            body.body.angle = rot / 180 * 3.1415926  
            body.offsetrot = rot 
            global_var.SPACE.reindex_shapes_for_body(body.body)       

    @ property
    def velocity(self):
        return self._velocity 

    @ velocity.setter
    def velocity(self, v):
        self._velocity = v
        for body in self:
            body.body.velocity = v

    @ property
    def angular_velocity(self):
        return self._angular_velocity

    @ angular_velocity.setter
    def angular_velocity(self, av):
        self._angular_velocity = av
        for body in self:
            body.body.angular_velocity = av
        

    def apply_impulse_at_local_point(self, pos):
        for body in self:
            body.body.apply_impulse_at_local_point(pos)

    @ property
    def elasticity(self):
        return self._elasticity

    @ elasticity.setter
    def elasticity(self, e):
        self._elasticity = e
        for body in self:
            body.body.elasticity = e

    @ property
    def friction(self):
        return self._friction

    @ friction.setter
    def friction(self, f):
        self._friction = f  
        for body in self:
            body.body.friction = f

    @ property
    def mass(self):
        return self._mass

    @ mass.setter
    def mass(self, m): 
        self._mass = m
        for body in self:
            body.body.mass = m

    def set_vertices(self, scalex, scaley):
        for body in self:
            body.set_vertices(body.vertices, transform=pymunk.Transform(a = scalex, d = scaley))
            body.offsetscale = vec(scalex, scaley)
            