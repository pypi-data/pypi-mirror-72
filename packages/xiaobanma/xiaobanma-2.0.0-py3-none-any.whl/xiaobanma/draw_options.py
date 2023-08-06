from .config import *

def camera_offset(p):
    o = vec(global_var.SCREEN.size) - vec(global_var.CAMERA.size)
    newp = p - o //2
    newp = (int(newp[0]), int(newp[1]))   
    return newp 

class NewDrawOptions(pymunk.SpaceDebugDrawOptions):
    def __init__(self, surface):
        self.surface = surface
        super(NewDrawOptions, self).__init__()


    def draw_circle(self, pos, angle, radius, outline_color, fill_color):
        p = pymunk2Cartesian(pos, self.surface)
        pygame.draw.circle(self.surface, fill_color, p, _rndint(radius), 0)
        
        circle_edge = pos + Vec2d(radius, 0).rotated(angle)
        p2 = pymunk2Cartesian(circle_edge, self.surface)
        line_r = 2 if radius > 20 else 1
        pygame.draw.lines(self.surface, outline_color, False, [p,p2], line_r)    


    def draw_segment(self, a, b, color):
        p1 = pymunk2Cartesian(a, self.surface)
        p2 = pymunk2Cartesian(b, self.surface)

        pygame.draw.aalines(self.surface, color, False, [p1,p2])


    def draw_fat_segment(self, a, b, radius, outline_color, fill_color):
        p1 = pymunk2Cartesian(a, self.surface)
        p2 = pymunk2Cartesian(b, self.surface)
        
        r = _rndint(max(1, radius*2))
        pygame.draw.lines(self.surface, fill_color, False, [p1,p2], r)
        if r > 2:
            delta = ( p2[0]-p1[0], p2[1]-p1[1] )
            orthog = [ delta[1], -delta[0] ]
            scale = radius / (orthog[0]*orthog[0] + orthog[1]*orthog[1])**0.5
            orthog[0]*=scale; orthog[1]*=scale
            points = [
                ( p1[0]-orthog[0], p1[1]-orthog[1] ),
                ( p1[0]+orthog[0], p1[1]+orthog[1] ),
                ( p2[0]+orthog[0], p2[1]+orthog[1] ),
                ( p2[0]-orthog[0], p2[1]-orthog[1] )
            ]
            pygame.draw.polygon(self.surface, fill_color, points)
            pygame.draw.circle(self.surface, fill_color, 
                (_rndint(p1[0]),_rndint(p1[1])), _rndint(radius))
            pygame.draw.circle(self.surface, fill_color, 
                (_rndint(p2[0]),_rndint(p2[1])), _rndint(radius))

        
    def draw_polygon(self, verts, radius, outline_color, fill_color):
        ps = [pymunk2Cartesian(v, self.surface) for v in verts]
        ps += [ps[0]]

        pygame.draw.polygon(self.surface, fill_color, ps)

        if radius > 0:
            for i in range(len(verts)):
                a = verts[i]
                b = verts[(i+1) % len(verts)]
                self.draw_fat_segment(a, b, radius, outline_color, 
                    outline_color)


    def draw_dot(self, size, pos, color):
        p = pymunk2Cartesian(pos, self.surface)
        pygame.draw.circle(self.surface, color, p, _rndint(size), 0)

def pymunk2Cartesian(p, surface):
    return camera_offset((int(p[0] + global_var.WIDTH // 2), int(global_var.HEIGHT // 2 - p[1])))

def from_pygame(p, surface):
    """Convenience method to convert pygame surface local coordinates to 
    pymunk coordinates    
    """
    return to_pygame(p,surface)


def _rndint(x): 
    return int(round(x))      