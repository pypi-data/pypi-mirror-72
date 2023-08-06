from .config import *

def draw_line(p1, p2, color, width):
    p1= Cartesian2pygame(p1)
    p2= Cartesian2pygame(p2)
    global_var.LINES.append((p1, p2, color, width))