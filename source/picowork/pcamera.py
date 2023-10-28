from pico2d import *
from .putil import *


class PCamera:
    def __init__(self):
        self._position = Vector2(0, 0)
        self._rotation = 0
        self._size = 5

    def screen_position(self, world_position: Vector2):
        hw = get_canvas_width() / 2
        hh = get_canvas_height() / 2
        v = world_position - self._position
        if self._rotation != 0:
            rad = -radians(self._rotation)
            v = Vector2(v.x * cos(rad) - v.y * sin(rad), v.x * sin(rad) + v.y * cos(rad))
        v = v * (hh / self._size) + Vector2(hw, hh)
        return v

    def screen_rotation(self, world_rotation: float):
        return world_rotation - self._rotation

    def screen_size(self, world_size: Vector2):
        hh = get_canvas_height() / 2
        v = world_size * (hh / self._size)
        return v

camera = PCamera()