from .config import *
from .tiledmap import TiledMap

class EasySpriteStrategy():
    ''' 
    这是一个动画精灵类
    输入：一张图片名称
    方法：调用update方法来输出图片
    '''
    def __init__(self, img):
        if isinstance(img, str):
            self._image = pygame.image.load(img).convert_alpha()
        else:
            self._image = img

    def __len__(self):
        return 1

    def __getitem__(self, frame):
        raise NotImplementedError

    def __setitem__(self, frame):
        raise NotImplementedError
    
    def update(self):
        return self._image

class TiledMapStrategy():
    def __init__(self, tiledmap):
        self.tm = tiledmap.make_map().convert_alpha()


    def update(self):
        return self.tm


class ListSpriteStrategy():
    ''' 
    这是一个动画精灵类
    输入：以列表形式存储的图片名称
    方法：调用update方法来输出图片
    '''
    def __init__(self, imgs):
        self._frame = 0
        self._images = []
        self.playing = False
        self.dt = 0.05
        self._last_update_time = 0
        for img in imgs:
            if isinstance(img, str):
                self._images.append(pygame.image.load(img).convert_alpha())
            else:
                self._images.append(img)
    def __repr__(self):
        return f"sprites = {self._images}, frame = {self._frame}"

    def __len__(self):
        return len(self._images)

    def __getitem__(self, frame):
        assert frame < len(self._images), 'IndexError'
        return self.images[frame]

    def __setitem__(self):
        raise NotImplementedError

    @ property
    def frame(self):
        return self._frame

    @ frame.setter
    def frame(self, frame):
        self._frame = frame % len(self._images)

    def set_dt(self, dt):
        self.dt = dt
    
    def update(self):
        image = self._images[self._frame]
        if self.playing and time.time() - self._last_update_time > self.dt:
            self._last_update_time = time.time()
            self._frame += 1
            if self._frame == len(self._images):
                self._frame = 0
        return image

class AnimatorStrategy():
    ''' 
    这是一个动画精灵类
    输入：以字典形式存储的图片名称
    方法：调用update方法来输出图片
    '''
    def __init__(self, imgs_dict):
        self._frame = 0
        self._imgs_dict = {}
        self.playing = False
        self._last_update_time = 0
        self._state = 0
        
        for state in imgs_dict:
            self._imgs_dict[state] = {'animation':[],
                                      'dt':0.05,
                                      'next_state':state,
                                      'start_func':None,
                                      'end_func':None}

            for img in imgs_dict[state]:
                if isinstance(img, str):
                    self._imgs_dict[state]['animation'].append(pygame.image.load(img).convert_alpha())
                else:
                    self._imgs_dict[state]['animation'].append(img)

        self._state = state
        self._prestate = self._state
        self._state_temp = self._state

    def __repr__(self):
        return f"sprites = {self._imgs_dict}, frame = {self._frame}, state = {self._state}"

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, frame):
        raise NotImplementedError

    @ property
    def frame(self):
        return self._frame

    @ frame.setter
    def frame(self, frame):
        self._frame = frame % len(self._imgs_dict[self.state]['animation'])

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if state not in self._imgs_dict:
            raise KeyError
        self._state_temp = state

    def set_dt(self, state, dt):
        if state:
            self._imgs_dict[state]['dt'] = dt
        else:
            for state in self._imgs_dict:
                self._imgs_dict[state]['dt'] = dt

    def set_next_state(self, state, next_state):
        self._imgs_dict[state]['next_state'] = next_state

    def set_start_func(self, state, func):
        self._imgs_dict[state]['start_func'] = func

    def set_end_func(self, state, func):
        self._imgs_dict[state]['end_func'] = func

    def update(self):
        self._prestate = self._state
        self._state = self._state_temp
        if self._state != self._prestate:
            self._frame = 0
        image = self._imgs_dict[self._state]['animation'][self._frame]
        
        if self.playing and time.time() - self._last_update_time > self._imgs_dict[self._state]['dt']:
            self._last_update_time = time.time()
            self._frame += 1
            if self._frame == len(self._imgs_dict[self._state]['animation']):
                if self._imgs_dict[self.state]['end_func']:
                    self._imgs_dict[self.state]['end_func']()
                self.state = self._imgs_dict[self._state]['next_state']
                if self._imgs_dict[self.state]['start_func']:
                    self._imgs_dict[self.state]['start_func']()
                self._frame = 0
        return image


class SpriteSheet():
    def __init__(self, sheet, w, h):
        self.sheet = pygame.image.load(sheet).convert_alpha()
        self.imgs = []
        width, height = self.sheet.get_size()
        tile_width = width // w
        tile_height = height // h
        for i in range(h):
            for j in range(w):
                self.imgs.append(self.sheet.subsurface(pygame.Rect(j*tile_width, i*tile_height, tile_width, tile_height)))

    def __getitem__(self, key):
        return self.imgs[key]

    def __repr__(self):
        return self.imgs

class Sprite(pygame.sprite.DirtySprite):
    '''
    Only allow one image
    '''
    
    autos = {pygame.Surface:EasySpriteStrategy,
             str:EasySpriteStrategy,
             TiledMap:TiledMapStrategy,
             list:ListSpriteStrategy,
             dict:AnimatorStrategy,
             SpriteSheet:ListSpriteStrategy}

    def __init__(self, imgs):
        
        pygame.sprite.DirtySprite.__init__(self, global_var.ALL_SPRITES)
        self.dirty = 2
        self._offset = vec(0, 0)
        self._is_flip_h = False
        self._is_flip_v = False
        sprite_strategy = Sprite.autos[type(imgs)]

        self._sprite_strategy = sprite_strategy(imgs)

        self._red = 255
        self._green = 255
        self._blue = 255
        self._alpha = 255
        self._visible = True
        self.rect = self._sprite_strategy.update().get_rect()
        # Flags to inform the class whether to perform the transformation
        self.fliped = False
        self.scaled = False
        self.rotated = False
        self.modified = False


    def set_parent(self, parent):
        self._parent = parent

    @property
    def sprite_strategy(self):
        return self._sprite_strategy

    @property
    def is_flip_h(self):
        return self._is_flip_h

    @is_flip_h.setter
    def is_flip_h(self, h):
        self._is_flip_h = h

    @property
    def is_flip_v(self):
        return self._is_flip_v

    @is_flip_v.setter
    def is_flip_v(self, v):
        self._is_flip_v = v

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, r):
        self._red = r

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, g):
        self._green = g

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, b):
        self._blue = b

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, a):
        self._alpha = a

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, v):
        self._visible = v 

    @property
    def width(self):
        return self.rect.size[0]

    @property
    def height(self):
        return self.rect.size[1]

    def update(self):
        self.image = self._sprite_strategy.update().copy()
        # 翻转
        if self.fliped:
            self.image = pygame.transform.flip(self.image, self._is_flip_h, self._is_flip_v)
        # 放缩
        if self.scaled:
            width, height = self.image.get_rect().size    
            self.image = pygame.transform.scale(self.image, (int(self._parent.scl[0]*width), int(self._parent.scl[1]*height)))  
        # 旋转  
        if self.rotated:    
            self.image = pygame.transform.rotate(self.image, self._parent.rot)
        if self.modified:
            if self._visible:
                self.image.fill((self._red, self._green, self._blue, self._alpha), None, pygame.BLEND_RGBA_MULT)
            else:
                self.image.fill((self._red, self._green, self._blue, 0), None, pygame.BLEND_RGBA_MULT)

        self.rect = self.image.get_rect()
        camera_offset = vec(global_var.SCREEN.size) - vec(global_var.CAMERA.size)
        self.rect.center = Cartesian2pygame(self._parent.pos) - camera_offset//2 # 转化为笛卡尔坐标系




    

