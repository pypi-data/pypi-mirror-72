from .config import *
from .game_object import GameObject
from .event import get_mouse_pos
class Coordinate(Sensor):
    def __init__(self):
        Sensor.__init__(self, './img/cursor.png')
        self.text = TextBox(25)

    def update(self):
        super().update()
        self.move_to_front()
        self.goto(get_mouse_pos() + vec(120, 70))
        self.text.goto(get_mouse_pos() + vec(120, 70))
        self.text.print(get_mouse_pos())