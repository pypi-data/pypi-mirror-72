from .config import *
from .camera import Camera
from .physics import *

def setup(*size):
    if (not isinstance(size[0], int)) or (not isinstance(size[1], int)):
        raise TypeError('类型错误:参数必须为整数')
    if len(size) != 2:
        raise TypeError('类型错误:参数数目错误，只允许两个参数')
    global_var.SCREEN = Screen(size)
    global_var.WIDTH, global_var.HEIGHT = size
    global_var.ALL_SPRITES = pygame.sprite.LayeredDirty()
    global_var.CAMERA = Camera(size)
    global_var.SPACE = pymunk.Space()
    global_var.SPACE.collision_bias = 0
    global_var.SPACE.gravity = (0, 0)
    global_var.BODIES = BodiesGroup()
    global_var.TMBG = TiledMapBodiesGroup()
    return global_var.SCREEN


def title(title):
    pygame.display.set_caption(title)

def update():
    global_var.SCREEN.update()
    global_var.JUST_RELEASED = False

def save_screen(name):
    global_var.SCREEN.save_name = name

def done():
    while True:
        global_var.SCREEN.update()

class Screen():
    def __init__(self, size):
        self.size = size
        self._screen = pygame.display.set_mode(size)
        self._clock = pygame.time.Clock()
        self.save_name = None
 

    def update(self):
        global_var.EVENTS =  pygame.event.get()
        for event in global_var.EVENTS:
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(0)
        global_var.GROUP.update()
        global_var.BODIES.update()   
        global_var.TMBG.update()     
        global_var.SPACE.step(1/60)
        rects = global_var.CAMERA.update()
        size = vec(global_var.CAMERA.size) * global_var.CAMERA.scl
        self._screen.blit(pygame.transform.scale(global_var.CAMERA.surface, [int(i) for i in size]), \
            global_var.CAMERA.offset + (vec(self.size) - size)//2)

        self.draw()
        if self.save_name:
            pygame.image.save(self._screen, self.save_name)
            self.save_name = None

        pygame.display.update()
        self._clock.tick(40)
        self._screen.fill(BLACK)

    def draw(self):
        for p1, p2, color, width in global_var.LINES:
            pygame.draw.lines(self._screen, color, 0, [p1, p2], width)
        global_var.LINES = []

        





