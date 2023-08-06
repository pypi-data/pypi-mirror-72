from .config import *

def bgmusic(bgm):
    pygame.mixer.music.load(bgm)
    pygame.mixer.music.play(loops = -1)

def set_volume(vol):
    pygame.mixer.music.set_volume(vol)