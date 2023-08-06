from .game_object import *
from .screen import *
from .sprite import *
from .physics import *
from .events import *
from .tiledmap import TiledMap
from .textbox import *
from .music import *
from .draw import *
from .constraints import *
import random
import time
import sys



IS_UPDATED = 0
SPEED = 1

def tracer(f):
    global IS_UPDATED
    IS_UPDATED = f

def speed(s):
    global SPEED
    SPEED = s

def random_pos():
    return (random.randint(- global_var.WIDTH // 2, global_var.WIDTH // 2), random.randint(- global_var.HEIGHT // 2, global_var.HEIGHT // 2))

def debug():
    global_var.DEBUG_DRAW = True

def set_gravity(x, *y):
    if y:
        global_var.SPACE.gravity = (x, *y)
    else:
        global_var.SPACE.gravity = x

def set_mouse_visible(v):
    pygame.mouse.set_visible(v)

def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0

class NewGameObject():
    def __init__(self, imgs = None, size = None, body_type = pymunk.Body.KINEMATIC, sensor = False): 

        self._gameObject = GameObject()
        if imgs:
            self._gameObject.set_sprite(Sprite(imgs))
  
        if size:
            if isinstance(size, int):
                self._gameObject.set_body(Body(body_type, 'CIRCLE', size = size, sensor = sensor))
                self.radius = self._gameObject.body.shape.radius
            elif isinstance(size, tuple):
                self._gameObject.set_body(Body(body_type, 'BOX', size = size, sensor = sensor))
                self.vertices = self._gameObject.body.shape.get_vertices()
            elif isinstance(size, list):
                if isinstance(size[0], list):
                    self._gameObject.set_body(Body(body_type, 'POLY', size = size, sensor = sensor))
                    self.vertices = self._gameObject.body.shape.get_vertices()  
                else:
                    objs = size
                    tiledmap_objects = TiledMapBodies(body_type, objs, sensor)
                    self._gameObject.set_tiledmap_bodies(tiledmap_objects) 
                       
        self._direction = vec(1, 0)
        self._dialogBox = None
        self._get_clicked = False

        global_var.GROUP.add(self)
        self._just_released = False
        self.collision_dict = {}
        self.sounds = []
        self.volume = 1
        if self._gameObject.sprite:
            self._gameObject.sprite.update()

          

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self):
        raise NotImplementedError

    def __setitem__(self):
        raise NotImplementedError

    def __bool__(self):
        return True

    def __del__(self):
        pass

    '''
    运动命令
    '''
    def forward(self, d):
        n = 0
        #d = int(d)
        speed = min(abs(d), SPEED)
        while n < abs(d):
            self._gameObject.pos += self._direction * speed * sign(d)
            n += speed
            if IS_UPDATED:
                update()

    def backward(self, d):
        n = 0
        #d = int(d)
        speed = min(abs(d), SPEED)
        while n < abs(d):
            self._gameObject.pos -= self._direction * speed * sign(d)
            n += speed
            if IS_UPDATED:
                update()

    def _rotate(self, rot):
        self.rotate_image(rot)
        self.rotate_direction(rot) 

    def rotate_direction(self, rot):
        self.dir = self.dir.rotate(rot)

    def rotate_image(self, rot):
        self.rot += rot

    @ property
    def rot(self):
        return self._gameObject.rot

    @ rot.setter
    def rot(self, r):
        self._gameObject.rot = r
        if self._gameObject.sprite:
            self._gameObject.sprite.rotated = True
        if self._gameObject.body:
            self._gameObject.body.set_rot(r)
        if self._gameObject.tiledmap_bodies:
            self._gameObject.tiledmap_bodies.set_rot(r)


    @ property
    def dir(self):
        return self._direction

    @ dir.setter
    def dir(self, d):
        self._direction = d

    def left(self, a): 
        n = 0
        #a = int(a)
        speed = min(abs(a), SPEED)
        while n < abs(a):
            self._rotate(speed * sign(a))
            n += speed
            if IS_UPDATED:
                update()

    def right(self, a):
        n = 0
        #a = int(a)
        speed = min(abs(a), SPEED)
        while n < abs(a):
            self._rotate(-speed * sign(a))
            n += speed
            if IS_UPDATED:
                update()

    def slide_to(self, pos, v = 1):
        distance = vec(pos) - self._gameObject.pos
        if distance.length() < v:
            self._gameObject.pos = vec(pos)
            return True
        self._gameObject.pos += distance.normalize() * v
        return False

    def goto(self, x, *y):
        if y:
            self._gameObject.pos = vec(x, *y)
        else:
            self._gameObject.pos = vec(x)
        if self._gameObject.body:
            self._gameObject.body.velocity = vec(0,0)
        #update()

    def face_to(self, x, *y, VEC = False):
        if not VEC:
            if y:
                self.rot = - (vec(x, *y) - self._gameObject.pos).angle_to(vec(1, 0)) 
                self.dir = (vec(x, *y) - self._gameObject.pos).normalize()
            else:
                self.rot = - (vec(x) - self._gameObject.pos).angle_to(vec(1, 0))  
                if  (vec(x) - self._gameObject.pos).length() != 0:
                    self.dir = (vec(x) - self._gameObject.pos).normalize()   
        else:
            if y:
                self.rot = - vec(x, *y).angle_to(vec(1, 0)) 
                self.dir = vec(x, *y).normalize()
            else:
                self.rot = - vec(x).angle_to(vec(1, 0))  
                if  vec(x).length() != 0:
                    self.dir = vec(x).normalize()               

    @ property
    def pos(self):
        return self._gameObject.pos

    @ property
    def dir(self):
        return self._direction
        
    @ property
    def x(self):
        return self._gameObject.pos[0]

    @ property
    def y(self):
        return self._gameObject.pos[1]

    @ pos.setter
    def pos(self,p):
        self._gameObject.pos = p
        if self._gameObject.body:
            self._gameObject.body.velocity = vec(0,0)
        if self._gameObject.tiledmap_bodies:
            self._gameObject.tiledmap_bodies.velocity = vec(0,0)      
        

    @ dir.setter
    def dir(self, dir):
        self._direction = dir

    @ x.setter
    def x(self, x):
        if self._gameObject.body:
            self._gameObject.body.velocity = vec(0,0)
        if self._gameObject.tiledmap_bodies:
            self._gameObject.tiledmap_bodies.velocity = vec(0,0)
        self._gameObject.x = x

    @ y.setter
    def y(self, y):
        if self._gameObject.body:
            self._gameObject.body.velocity = vec(0,0)
        if self._gameObject.tiledmap_bodies:
            self._gameObject.tiledmap_bodies.velocity = vec(0,0)
        self._gameObject.y = y

    @ property
    def velocity(self):
        if self._gameObject.body:
            return self._gameObject.body.velocity
        elif self._gameObject.tiledmap_bodies:
            return self._gameObject.tiledmap_bodies.velocity

    @ velocity.setter
    def velocity(self, v):
        if self._gameObject.body:
            self._gameObject.body.velocity = v
        elif self._gameObject.tiledmap_bodies:
            self._gameObject.tiledmap_bodies.velocity = v

    @ property
    def angular_velocity(self):
        if self._gameObject.body:
            return self._gameObject.body.angular_velocity
        elif self._gameObject.tiledmap_bodies:
            return self._gameObject.tiledmap_bodies.angular_velocity
            
    @ angular_velocity.setter
    def angular_velocity(self, v):
        if self._gameObject.body:
            self._gameObject.body.angular_velocity = v
        elif self._gameObject.tiledmap_bodies:
            self._gameObject.tiledmap_bodies.angular_velocity = v
    '''
    图片命令
    '''
    def scale(self, scalex, scaley = None):
        if scaley == None:
            if self._gameObject.sprite:
                self._gameObject.sprite.scaled = True
                self._gameObject.scl = scalex
            if self._gameObject.body:
                self.body_scale(scalex, scaley)
            if self._gameObject.tiledmap_bodies:
                self.body_scale(scalex, scaley)
        else:
            if self._gameObject.sprite:
                self._gameObject.sprite.scaled = True
                self._gameObject.scl = (scalex, scaley)
            if self._gameObject.body:
                self.body_scale(scalex, scaley)            
            if self._gameObject.tiledmap_bodies:
                self.body_scale(scalex, scaley)            
            

    def flipx(self, h):
        self._gameObject.sprite.fliped = True
        self._gameObject.sprite.is_flip_h = h

    def flipy(self, v):
        self._gameObject.sprite.fliped = True
        self._gameObject.sprite.is_flip_v = v

    @ property
    def red(self):
        return self._gameObject.sprite.red

    @ red.setter
    def red(self, red):
        self._gameObject.sprite.modified = True
        self._gameObject.sprite.red = red

    @ property
    def green(self):
        return self._gameObject.sprite.green

    @ green.setter
    def green(self, green):
        self._gameObject.sprite.modified = True
        self._gameObject.sprite.green = green

    @ property
    def blue(self):
        return self._gameObject.sprite.blue

    @ blue.setter
    def blue(self, blue):
        self._gameObject.sprite.modified = True
        self._gameObject.sprite.blue = blue

    @ property
    def alpha(self):
        return self._gameObject.sprite.alpha

    @ alpha.setter
    def alpha(self, alpha):
        self._gameObject.sprite.modified = True
        self._gameObject.sprite.alpha = alpha

    @ property
    def color(self):
        return (self._gameObject.sprite.red,
                self._gameObject.sprite.green,
                self._gameObject.sprite.blue,
                self._gameObject.sprite.alpha)

    @ color.setter
    def color(self, color):
        # 不建议对过大的地图进行此操作，会导致动画变慢
        self._gameObject.sprite.modified = True
        self._gameObject.sprite.red = color[0]
        self._gameObject.sprite.green = color[1]
        self._gameObject.sprite.blue = color[2]
        self._gameObject.sprite.alpha = color[3]

    def show(self):
        # 不建议对过大的地图进行此操作，会导致动画变慢
        self._gameObject.sprite.modified = True
        self._gameObject.sprite.visible = True

    def hide(self):
        # 不建议对过大的地图进行此操作，会导致动画变慢
        self._gameObject.sprite.modified = True
        self._gameObject.sprite.visible = False
    
    @ property
    def visible(self):
        return self._gameObject.sprite.visible

    @ property
    def width(self):
        return self._gameObject.sprite.width

    @ property
    def height(self):
        return self._gameObject.sprite.height

    # 动画命令
    @ property
    def frame(self):
        return self._gameObject.sprite.sprite_strategy.frame

    @ frame.setter
    def frame(self, f):
        self._gameObject.sprite.sprite_strategy.frame = f

    def play_anim(self):
        self._gameObject.sprite.sprite_strategy.playing = True

    @ property
    def state(self):
        return self._gameObject.sprite.sprite_strategy.state

    @ state.setter
    def state(self, state):
        self._gameObject.sprite.sprite_strategy.state = state

    def set_dt(self, *args):
        self._gameObject.sprite.sprite_strategy.set_dt(*args)

    @ property
    def dt(self):
        if isinstance(self._gameObject.sprite.sprite_strategy, ListSpriteStrategy):
            return self._gameObject.sprite.sprite_strategy.dt
        else:
            raise NotImplementedError

    @ dt.setter
    def dt(self, dt):
        if isinstance(self._gameObject.sprite.sprite_strategy, ListSpriteStrategy):
            self.set_dt(dt)
        else:
            raise NotImplementedError
        


    def set_next_state(self, state, next_state):
        self._gameObject.sprite.sprite_strategy.set_next_state(state, next_state)

    def set_start_func(self, state, func):
        self._gameObject.sprite.sprite_strategy.set_start_func(state, func)

    def set_end_func(self, state, func):
        self._gameObject.sprite.sprite_strategy.set_end_func(state, func)

    # 图层
    @ property
    def layer(self):
        return global_var.ALL_SPRITES.get_layer_of_sprite(self._gameObject.sprite)

    @ layer.setter
    def layer(self, layer):
        global_var.ALL_SPRITES.change_layer(self._gameObject.sprite, layer)

    def move_to_front(self):
        global_var.ALL_SPRITES.move_to_front(self._gameObject.sprite)

    def move_to_back(self):
        global_var.ALL_SPRITES.move_to_back(self._gameObject.sprite)    

    # 音效
    def play_snd(self, snd = None, volume=None):
        if snd:
            s = pygame.mixer.Sound(snd)
            if not volume:
                volume = self.volume
            s.set_volume(volume)
            if len(self.sounds) == 20:
                pre_s = self.sounds.pop(0)
                pre_s.stop()
            s.play()

    def set_volume(self, volume):
        self.volume = volume
        
    # 交互
    
    def get_mouse_clicked(self):
        # 检测鼠标左键是否在按下的状态下
        for event in global_var.EVENTS:
            if event and event.type == MOUSEBUTTONDOWN and self.get_mouse_upon():
                self._get_clicked = True
        self.get_mouse_just_released()
        if self._get_clicked:
            return True
        else:
            return False
    
    def get_mouse_just_clicked(self):
        # 检测鼠标是否刚刚被按下
        for event in global_var.EVENTS:
            if event and event.type == MOUSEBUTTONDOWN and self.get_mouse_upon():
                self._get_clicked = True
                return True
        else:
            return False

    def get_mouse_just_released(self):
        # 检测鼠标是否刚刚被松开
        if self._just_released:
            return True
        self.get_mouse_just_clicked()
        if self._get_clicked:
            for event in global_var.EVENTS:
                if event and event.type == MOUSEBUTTONUP:
                    self._get_clicked = False
                    self._just_released = True
            if self._get_clicked:
                return False
            else:
                return True
        else:
            return False

    def get_mouse_upon(self):
        # 检测鼠标是否在图片上
        if self.collide(get_mouse_pos()):
            return True
        else:
            return False

    

    # 其他
    def collide(self, other):
        if self._gameObject.sprite and self._gameObject.sprite.visible:
            if isinstance(other, tuple) or isinstance(other, vec):
                if self._gameObject.body:  
                    return self._gameObject.body.point_query(other)
                elif self._gameObject.tiledmap_bodies:
                    return self._gameObject.tiledmap_bodies.point_query(other)
                else:
                    mask = pygame.mask.from_surface(self._gameObject.sprite.image)
                    offset = self._gameObject.pos - other \
                        + vec(self._gameObject.sprite.width//2, self._gameObject.sprite.height//2)
                    try:
                        return bool(mask.get_at([int(i) for i in offset]))
                    except:
                        return False
            else:         
                if self._gameObject.body:       
                    if other._gameObject.body:    
                        return self._gameObject.body.collide(other._gameObject.body)
                    elif other._gameObject.tiledmap_bodies:    
                        return other._gameObject.tiledmap_bodies.collide(self._gameObject.body)

                elif self._gameObject.tiledmap_bodies:
                    if other._gameObject.body:    
                        return self._gameObject.tiledmap_bodies.collide(other._gameObject.body)
                    elif other._gameObject.tiledmap_bodies:    
                        return self._gameObject.tiledmap_bodies.collide(other._gameObject.tiledmap_bodies)
                else:
                    mask1 = pygame.mask.from_surface(self._gameObject.sprite.image)
                    mask2 = pygame.mask.from_surface(other._gameObject.sprite.image)
                    offset = self._gameObject.pos - other._gameObject.pos \
                        + vec(self._gameObject.sprite.width//2, self._gameObject.sprite.height//2)\
                        - vec(other._gameObject.sprite.width//2, other._gameObject.sprite.height//2)
                    return bool(mask1.overlap(mask2, [int(i) for i in offset]))
        elif not self._gameObject.sprite:
            if isinstance(other, tuple) or isinstance(other, vec):
                if self._gameObject.body:  
                    return self._gameObject.body.point_query(other)
                elif self._gameObject.tiledmap_bodies:
                    return self._gameObject.tiledmap_bodies.point_query(other)
            else:         
                if self._gameObject.body:       
                    return self._gameObject.body.collide(other._gameObject.body)
                elif self._gameObject.tiledmap_bodies:
                    if other._gameObject.body:    
                        return self._gameObject.tiledmap_bodies.collide(other._gameObject.body)
                    elif other._gameObject.tiledmap_bodies:    
                        return self._gameObject.tiledmap_bodies.collide(other._gameObject.tiledmap_bodies)
         
        else:
            return False

    def separate(self, other): 
        # 不要检测是否与get_mouse_pos()函数的分离，因为只能检测和固定点之间的分离
        if other not in self.collision_dict:
            self.collision_dict[other] = False
        if not self.collide(other) and self.collision_dict[other]:
            self.collision_dict[other] = False
            return True
        else:
            if self.collide(other):
                self.collision_dict[other] = True
            else:
                self.collision_dict[other] = False
            return False


    def distance(self, other):
        if isinstance(other, tuple):
            return self._gameObject.pos.distance_to(other)
        else:
            return self._gameObject.pos.distance_to(other._gameObject.pos)

    def say(self, text = None):
        if not self._dialogBox:
            self._dialogBox = DialogBox(self)
        if text:
            self._dialogBox.show()
            self._dialogBox.say(text)
        else:
            self._dialogBox.hide()
        if IS_UPDATED:
            update()

    def kill(self):
        self._gameObject.kill()
        if self._dialogBox:
            self._dialogBox.kill()

    def apply_force(self, x, *y):
        if self._gameObject.body:
            if y:
                self._gameObject.body.apply_impulse_at_local_point((x, *y))
            else:
                self._gameObject.body.apply_impulse_at_local_point(x)
        elif self._gameObject.tiledmap_bodies:
            if y:
                self._gameObject.tiledmap_bodies.apply_impulse_at_local_point((x, *y))
            else:
                self._gameObject.tiledmap_bodies.apply_impulse_at_local_point(x)            


    @ property
    def elasticity(self):
        if self._gameObject.body:
            return self._gameObject.body.elasticity
        elif self._gameObject.tiledmap_bodies:
            return self._gameObject.tiledmap_bodies.elasticity

    @ elasticity.setter
    def elasticity(self, e):
        if self._gameObject.body:
            self._gameObject.body.elasticity = e
        elif self._gameObject.tiledmap_bodies:
            self._gameObject.tiledmap_bodies.elasticity = e


    @ property
    def friction(self):
        if self._gameObject.body:
            return self._gameObject.body.friction
        elif self._gameObject.tiledmap_bodies:
            return self._gameObject.tiledmap_bodies.friction

    @ friction.setter
    def friction(self, f):
        if self._gameObject.body:
            self._gameObject.body.friction = f 
        elif self._gameObject.tiledmap_bodies:
            self._gameObject.tiledmap_bodies.friction = f 

    @ property
    def mass(self):
        if self._gameObject.body:
            return self._gameObject.body.mass
        elif self._gameObject.tiledmap_bodies:
            return self._gameObject.tiledmap_bodies.mass

    @ mass.setter
    def mass(self, m): 
        if self._gameObject.body:
            self._gameObject.body.mass = m
        elif self._gameObject.tiledmap_bodies:
            self._gameObject.tiledmap_bodies.mass = m

    def body_scale(self, scalex, scaley):
        if "radius" in self.__dict__:
            if scaley:
                print('圆形无法进行不同方向的拉伸')
            self._gameObject.body.shape.unsafe_set_radius(int(self.radius * scalex))
        elif "vertices" in self.__dict__:
            if scaley:
                self._gameObject.body.set_vertices(self.vertices, transform=pymunk.Transform(a = scalex, d = scaley))
            else:
                self._gameObject.body.set_vertices(self.vertices, transform=pymunk.Transform(a = scalex, d = scalex))
        elif self._gameObject.tiledmap_bodies:
            if scaley:
                self._gameObject.tiledmap_bodies.set_vertices(scalex, scaley)
            else:
                self._gameObject.tiledmap_bodies.set_vertices(scalex, scalex)
        else:
            raise NotImplementedError

    def _update(self):
        # 私有方法, 不要重载!!
        self._just_released = False
        if self.angular_velocity:
            self.dir = self.dir.rotate(self.angular_velocity)
            '''
        if sys.getrefcount(self) <= 6:
            self.kill()'''

    def update(self):
        # 允许重载的方法
        pass
        
class Character(NewGameObject):
    '''
    允许通过代码控制其运动的类
    '''
    def __init__(self, imgs = None, size = None):
        # 可以通过给出一张图片或图片列表或来实现人物创建
        NewGameObject.__init__(self, imgs = imgs, size = size, body_type = "DYNAMIC", sensor = False)

class Sensor(NewGameObject):
    def __init__(self, imgs = None, size = None):
        # 可以通过给出一张图片或图片列表或来实现人物创建
        NewGameObject.__init__(self, imgs = imgs, size = size, body_type = "KINEMATIC", sensor = True)

class Wall(NewGameObject):
    '''
    墙壁,无法运动的物体
    '''
    def __init__(self, imgs = None, size = None):
        # 可以通过给出一张图片或图片列表或来实现人物创建
        NewGameObject.__init__(self, imgs = imgs, size = size, body_type = "STATIC", sensor = False)
        self._velocity = vec(0, 0)

    @ property
    def velocity(self):
        return self._velocity

    @ velocity.setter
    def velocity(self, v):
        self._velocity = v

    def _update(self):
        super()._update()
        self.pos += self._velocity


class Mouse(Character):
    def __init__(self, imgs = None):
        Character.__init__(self, imgs)
        if imgs:
            set_mouse_visible(False)

    def body_scale(self, scalex, scaley = None):
        pass
        
    def get_pos(self):
        return get_mouse_pos()

    def get_rel(self):
        return get_mouse_rel()

    def get_clicked(self):
        return get_mouse_clicked()

    def get_just_clicked(self):
        return get_mouse_just_clicked()

    def get_just_released(self):
        return get_mouse_just_released()

    def update(self):
        self.goto(get_mouse_pos())


def load_image(img):
    return pygame.image.load(img)




def bgpic(img):
    if isinstance(img, str):
        bg = Character(img)
    else:
        bg = img
    if isinstance(bg, TiledMap):
        global_var.CAMERA = Camera((bg.width, bg.height))
    else:
        global_var.CAMERA = Camera((bg._gameObject.sprite.width, bg._gameObject.sprite.height))
