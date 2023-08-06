from .config import *

class DialogBox(pygame.sprite.DirtySprite):
    def __init__(self, parent):
        pygame.sprite.DirtySprite.__init__(self, global_var.ALL_SPRITES)

        self.dirty = 2
        self.orig_image = pygame.image.load(cwd+'\static\DialogBox.png')
        self.font = pygame.font.Font(cwd+'\static\simkai.ttf', 25)
        self._text = ''
        self._parent = parent
        self.hide()

    def say(self, text = None):
        if text:
            self._text = str(text)
        else:
            self.hide()

    def show(self):
        self._visible = True

    def hide(self):
        self._visible = False


    def update(self):
        self.image = self.orig_image.copy()
        if self._parent.pos[0] > 0:
            flipx = True
        else:
            flipx = False
        
        if flipx:
            self.image = pygame.transform.flip(self.image, flipx, 0)
        lines = len(self._text)//12+1
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.6), int(self.image.get_height() * lines / 10 + 50)))
        for i in range(lines):
            text = self.font.render(f"{self._text[i*12:(i+1)*12]}", 1, (0, 0, 0), (255, 255, 255))
            self.image.blit(text, (int(10*lines/5)+30,20+int(40*lines/5) + i * 30))
        if not self._visible:
            self.image.fill((255, 255, 255, 0), None, pygame.BLEND_RGBA_MULT)        
        self.rect = self.image.get_rect()
        camera_offset = vec(global_var.SCREEN.size) - vec(global_var.CAMERA.size)
        if not flipx:
            if self._parent._gameObject.sprite:
                self.rect.center = Cartesian2pygame(self._parent.pos) - camera_offset//2 \
                    + 0.5 * vec(self._parent._gameObject.sprite.width, -self._parent._gameObject.sprite.height)+vec(30,-50)
            else:
                self.rect.center = Cartesian2pygame(self._parent.pos) - camera_offset//2 +vec(30,-50)                
        else:
            if self._parent._gameObject.sprite:
                self.rect.center = Cartesian2pygame(self._parent.pos) - camera_offset//2 \
                    - 0.5 * vec(self._parent._gameObject.sprite.width, self._parent._gameObject.sprite.height) +vec(-30,-50)
            else:
                self.rect.center = Cartesian2pygame(self._parent.pos) - camera_offset//2 +vec(-30,-50)
        global_var.ALL_SPRITES.move_to_front(self)

class TextBox(pygame.sprite.DirtySprite):
    def __init__(self, size = 20, font = cwd+'\static\simkai.ttf'):
        pygame.sprite.DirtySprite.__init__(self, global_var.ALL_SPRITES)
        self.font = pygame.font.Font(font, size)
        self._text = ''
        self._pos = vec(0, 0)
        self._color = (0, 0, 0)

    def print(self, text = None):
        self._text = str(text)

    def goto(self, x, *y):
        if y:
            self.pos = (x, *y)
        else:
            self.pos = x
    @ property
    def pos(self):
        return self._pos

    @ pos.setter
    def pos(self, pos):
        self._pos = pos

    @ property
    def color(self):
        return self._color

    @ color.setter
    def color(self, color):
        self._color = color

    def update(self):
        self.image = self.font.render(f"{self._text}", 2, self._color)
        self.rect = self.image.get_rect()
        self.rect.center = Cartesian2pygame(self._pos)
        global_var.ALL_SPRITES.move_to_front(self)