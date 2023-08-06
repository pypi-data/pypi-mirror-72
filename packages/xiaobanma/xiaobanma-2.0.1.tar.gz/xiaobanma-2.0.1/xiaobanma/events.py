from .config import *
#pygame.key.set_repeat(300, 100)
def get_mouse_pos():
    # 获得鼠标坐标
    return pygame2Cartesian(pygame.mouse.get_pos())


def get_mouse_rel():
    # 获得鼠标运动
    '''
    x, y = pygame.mouse.get_rel()
    return vec(x, -y)
    '''
    for event in global_var.EVENTS:
        if event.type == MOUSEMOTION:
            x, y = event.rel
            return vec(x, -y)
    else:
        return vec(0, 0)

def get_mouse_clicked():
    # 检测鼠标左键是否在按下的状态下
    for event in global_var.EVENTS:
        if event and event.type == MOUSEBUTTONDOWN:
            global_var.GET_CLICKED = True
    get_mouse_just_released()
    if global_var.GET_CLICKED:
        return True
    else:
        return False
    
def get_mouse_just_clicked():
    # 检测鼠标是否刚刚被按下
    for event in global_var.EVENTS:
        if event and event.type == MOUSEBUTTONDOWN:
            global_var.GET_CLICKED = True
            return True
    else:
        return False

def get_mouse_just_released():
    # 检测鼠标是否刚刚被松开
    if global_var.JUST_RELEASED:
        return True
    get_mouse_just_clicked()
    if global_var.GET_CLICKED:
        for event in global_var.EVENTS:
            if event and event.type == MOUSEBUTTONUP:
                global_var.GET_CLICKED = False
                global_var.JUST_RELEASED = True
        if global_var.GET_CLICKED:
            return False
        else:
            return True
    else:
        return False

def key_pressed(key = None):
    if not key:
        if 1 in pygame.key.get_pressed():
            return True
        else:
            return False
    if pygame.key.get_pressed()[key]:
        return True
    else:
        return False

def key_just_pressed(*keys):
    keyEvents = []
    for event in global_var.EVENTS:
        if event.type == KEYDOWN:
            keyEvents.append(event.key)
    if not keys:
        return keyEvents
    for key in keys:
        if key not in keyEvents:
            break
    else:
        return True
    return False


def key_released(*keys): 
    keyEvents = []
    for event in global_var.EVENTS:
        if event.type == KEYUP:
            keyEvents.append(event.key)
    if not keys:
        return keyEvents
    for key in keys:
        if key not in keyEvents:
            break
    else:
        return True
    return False