from math import *
import os
import time

import pygame
import pygame.gfxdraw


## GLOBAL VARIABLES ##
width = 1200
height = 800
pressed_keys = []
just_pressed_keys = []
is_mouse_down = False
is_mouse_just_down = False
is_mouse_right_down = False
is_mouse_right_just_down = False
mouse_pos = (0, 0)
mouse_scroll = 0


## INTERNAL VARIABLES ##
pygame.init()
_window = pygame.display.set_mode((width, height))
_clock = pygame.time.Clock()
_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)))
def _key_name(event):
    #print(event.scancode)
    if event.scancode == 40:
        return "[RETURN]"
    elif event.scancode == 41:
        return "[ESC]"
    elif event.scancode == 42:
        return "[BACKSPACE]"
    elif event.scancode == 43:  
        return "[TAB]"
    elif event.scancode == 44:
        return " "
    elif event.scancode == 69:
        return "[F12]"
    elif event.scancode == 74:
        return "[HOME]"
    elif event.scancode == 75:
        return "[PG_UP]"
    elif event.scancode == 76:
        return "[DELETE]"
    elif event.scancode == 77:
        return "[END]"
    elif event.scancode == 78:
        return "[PG_DOWN]"
    elif event.scancode == 79:
        return "[ARR_RIGHT]"
    elif event.scancode == 80:
        return "[ARR_LEFT]"
    elif event.scancode == 81:
        return "[ARR_DOWN]"
    elif event.scancode == 82:
        return "[ARR_UP]"
    elif event.scancode == 225 or event.scancode == 229:
        return "[SHIFT]"
    else:
        return event.unicode


## RENDER FUNCTIONS ##
_cached_images = {}
def render_img(path, coords, rotation=None, size=None, cache=True, opacity=None):
    full_path = os.path.join(_directory, path)
    img_id = f"{full_path} {round(rotation or 0, 2)} {size} {round(opacity or 0, 2)}"

    if _cached_images.get(img_id) == None:
        new_img = pygame.image.load(full_path).convert_alpha()

        if size != None:
            new_img = pygame.transform.scale(new_img, size)

        if rotation != None:
            new_img = pygame.transform.rotate(new_img, rotation)
        
        if opacity != None:
            new_img.set_alpha(opacity)

        _cached_images[img_id] = new_img
    
    _window.blit(_cached_images[img_id], coords)

    if not cache:
        del _cached_images[img_id]

_cached_fonts = {}
_cached_texts = {}
def render_text(value, pos, size, color=(0, 0, 0), opacity=None, cache=True):
    font_path = os.path.join(_directory, "font.ttf")

    if _cached_fonts.get(size) == None:
        _cached_fonts[size] = pygame.font.Font(font_path, size)
    
    text_id = f"{value} {size} {color} {round(opacity or 0, 2)}"

    if _cached_texts.get(text_id) == None:
        new_text = _cached_fonts[size].render(value, True, color)

        if opacity != None:
            new_text.set_alpha(opacity)
        
        _cached_texts[text_id] = new_text
    
    _window.blit(_cached_texts[text_id], pos)

    if not cache:
        del _cached_texts[text_id]

def render_rect(area, color=(0, 0, 0)):
    pygame.gfxdraw.box(_window, area, color)

def render_hrect(area, color=(0, 0, 0)):
    pygame.gfxdraw.rectangle(_window, area, color)

def render_circle(coords, r, color=(0, 0, 0)):
    pygame.gfxdraw.aacircle(_window, round(coords[0]), round(coords[1]), r, color)
    pygame.gfxdraw.filled_circle(_window, round(coords[0]), round(coords[1]), r, color)


## CALLBACKS ##
_start_hooks = []
_update_hooks = []
_event_hooks = []

def on_start(callback):
    _start_hooks.append(callback)

def on_update(callback):
    _update_hooks.append(callback)

def on_event(callback):
    _event_hooks.append(callback)


## CLICKABLES ##
_clickables = {}
_pressed_clickable = None

def add_clickable(area, callback):
    _clickables[f"{area} {id(callback)}"] = (area, callback)

def remove_clickable(area):
    clickables_to_remove = []

    for i in _clickables:
        if _clickables[i][0] == area:
            clickables_to_remove.append(i)
    
    for i in clickables_to_remove:
        del _clickables[i]


## TWEENING ##
class Tween: # Class used for interpolated animations
    def __init__(self, start_value, end_value, duration, easing_type="linear"):
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.easing_type = easing_type

        self.elapsed_time = 0
        self.last_timestamp = time.time()
        self.value = start_value
    
    def update(self):
        if self.elapsed_time == self.duration:
            return
        
        new_timestamp = time.time()
        self.elapsed_time += new_timestamp - self.last_timestamp
        self.last_timestamp = time.time()
        if self.elapsed_time > self.duration:
            self.elapsed_time = self.duration

        x = self.elapsed_time / self.duration

        # Check out https://easings.net for explanations of these types
        if self.easing_type == "sine":
            val = -(cos(3.1415 * x) - 1) / 2
        elif self.easing_type == "quad":
            if x < 0.5:
                val = 2 * x ** 2
            else:
                val = 1 - (-2 * x + 2) ** 2 / 2
        elif self.easing_type == "cubic":
            if x < 0.5:
                val = 4 * x ** 3
            else:
                val = 1 - (-2 * x + 2) ** 3 / 2
        elif self.easing_type == "quart":
            if x < 0.5:
                val = 8 * x ** 4
            else:
                val = 1 - (-2 * x + 2) ** 4 / 2
        elif self.easing_type == "quint":
            if x < 0.5:
                val = 16 * x ** 5
            else:
                val = 1 - (-2 * x + 2) ** 5 / 2
        else: # Linear
            val = x
        
        self.value = self.start_value + ((self.end_value - self.start_value) * val)


## MAIN LOOP ##
def start():
    global pressed_keys, just_pressed_keys, is_mouse_down, is_mouse_just_down, is_mouse_right_down, is_mouse_right_just_down, mouse_pos, mouse_scroll, _pressed_clickable

    for i in _start_hooks:
        i()

    is_running = True

    while is_running:
        # Internal clock
        _clock.tick()
        elapsed_time = pygame.time.get_ticks()
        delta = _clock.get_time()

        # Clear the screen
        _window.fill("#ff00ff")

        # Event processing
        mouse_scroll = 0
        just_pressed_keys = []
        is_mouse_just_down = False
        is_mouse_right_just_down = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pressed_keys.append(_key_name(event))
                just_pressed_keys.append(_key_name(event))
            elif event.type == pygame.KEYUP:
                pressed_keys.remove(_key_name(event))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_mouse_down = True
                    is_mouse_just_down = True
                elif event.button == 3:
                    is_mouse_right_down = True
                    is_mouse_right_just_down = True
                mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                is_mouse_down = False
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
            elif event.type == pygame.MOUSEWHEEL:
                mouse_scroll = event.y
            elif event.type == pygame.QUIT:
                is_running = False

        # Call all update functions
        for i in _update_hooks:
            i({
                "delta": delta,
                "elapsed_time": elapsed_time,
                "is_mouse_down": is_mouse_down,
                "mouse_pos": mouse_pos,
                "mouse_scroll": mouse_scroll,
                "pressed_keys": pressed_keys,
                "just_pressed_keys": just_pressed_keys
            })
        
        # Update all clickables
        if is_mouse_down:
            __clickables = _clickables.copy()
            for i in __clickables:
                area = __clickables[i][0]
                if mouse_pos[0] > area[0] and mouse_pos[1] > area[1] and mouse_pos[0] < area[2] and mouse_pos[1] < area[3]:
                    if _pressed_clickable != i:
                        _pressed_clickable = i
                        __clickables[i][1]()
        else:
            _pressed_clickable = None

        pygame.display.set_caption(f"Excel more like Mihnoxcel more like Mihnoxanjupans - FPS: {str(round(_clock.get_fps()))}")

        pygame.display.update()
        pygame.event.pump()

    pygame.quit()
