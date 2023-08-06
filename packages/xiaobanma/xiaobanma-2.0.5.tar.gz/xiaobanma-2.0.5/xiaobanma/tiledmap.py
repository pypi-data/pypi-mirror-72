from .config import *
import pytmx
from pytmx.util_pygame import load_pygame
from .camera import Camera



class TiledMap():
    def __init__(self, tilemap):
        tm = load_pygame(tilemap, pixelalpha = False)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self._tmxdata = tm
        self._get_objects()


    def render(self, surface):
        ti = self._tmxdata.get_tile_image_by_gid
        for layer in self._tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self._tmxdata.tilewidth, y * self._tmxdata.tileheight))


    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height)).convert_alpha()
        temp_surface.fill((0,0,0,0))
        self.render(temp_surface)
        return temp_surface

    @ property
    def objects(self):
        objects = []
        for obj in self._tmxdata.objects:
            obj.x = obj.x - (self.width - obj.width) // 2
            obj.y = (self.height - obj.height) // 2 - obj.y
            objects.append(obj)
        return objects

    def _get_objects(self, name = None):
        from .API import NewGameObject
        from .game_object import GameObject
        from .physics import Body, TiledMapBodies
        from .textbox import DialogBox
        for obj in self.objects:
            if obj.name == name or name == None:
                if 'points' in obj.__dict__:
                    points = []
                    for x, y in obj.points:
                        x = x - self.width // 2
                        y = self.height // 2 - y       
                        points.append((x, y))
                    obj.points = points 
                else:
                    if obj.width == 0:
                        obj.width = 20
                        obj.height = 20 
                    points = [(obj.x - obj.width // 2, obj.y - obj.height // 2),
                              (obj.x - obj.width // 2, obj.y + obj.height // 2),
                              (obj.x + obj.width // 2, obj.y - obj.height // 2),
                              (obj.x + obj.width // 2, obj.y + obj.height // 2)]
                    obj.points = points                

    def get_objects(self, name = None):
        objects = []
        for obj in self.objects:
            if obj.name == name or name == None:
                objects.append(obj)
        return objects