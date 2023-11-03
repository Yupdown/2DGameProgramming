import random

from picowork import picowork
from picowork.ptilemapobject import *
from picowork.presource import *
from player import *

class Tilemap(PObject):
    def __init__(self, w, h, front_format, back_format):
        super().__init__()
        self._w = w
        self._h = h
        self._tilemap = [[0 for _ in range(h)] for _ in range(w)]
        self._image_front = [get_image(front_format % n) if n > 0 else None for n in range(0, 17)]
        self._image_back = get_image(back_format)
        self._tilemap_back = PTileMapObject(w, h, 32 / PIXEL_PER_UNIT)
        self._tilemap_front = PTileMapObject(w * 2 + 1, h * 2 + 1, 16 / PIXEL_PER_UNIT)
        self._tilemap_front.set_position(Vector2(-0.25, -0.25))
        self.add_element(self._tilemap_back)
        self.add_element(self._tilemap_front)
        self._dirty_queue = []

    def on_draw(self):
        while self._dirty_queue:
            x = self._dirty_queue[0][0]
            y = self._dirty_queue[0][1]
            self._dirty_queue.pop(0)
            self.update_tile(x, y)

    def set_tile(self, x, y, tile):
        self._tilemap[x][y] = tile
        for dx in range(0, min(2, self._w - x)):
            for dy in range(0, min(2, self._h - y)):
                self._dirty_queue.append((x + dx, y + dy))

    def get_tile(self, x, y):
        return self._tilemap[x][y]

    def update_tile(self, x, y):
        solid = [[False for _ in range(2)] for _ in range(2)]
        image_grid = [[0 for _ in range(2)] for _ in range(2)]

        for dx in range(0, min(2, self._w - x)):
            for dy in range(0, min(2, self._h - y)):
                solid[dx][dy] = self._tilemap[x + dx][y + dy] > 0

        self._tilemap_back.set_tile(x, y, self._image_back if solid[0][0] else None)

        if solid[0][0] and not solid[0][1]:
            image_grid[0][1] = 2
        if not solid[0][0] and solid[0][1]:
            image_grid[0][1] = 10
        if solid[0][0] and not solid[1][0]:
            image_grid[1][0] = 8
        if not solid[0][0] and solid[1][0]:
            image_grid[1][0] = 7
        if solid[0][0]:
            if solid[1][1]:
                if not solid[0][1]:
                    image_grid[1][1] = 14
                if not solid[1][0]:
                    image_grid[1][1] = 15
            else:
                if solid[0][1] and solid[1][0]:
                    image_grid[1][1] = 13
                elif solid[0][1]:
                    image_grid[1][1] = 8
                elif solid[1][0]:
                    image_grid[1][1] = 2
                else:
                    image_grid[1][1] = 4
        else:
            if not solid[1][1]:
                if solid[0][1]:
                    image_grid[1][1] = 12
                if solid[1][0]:
                    image_grid[1][1] = 1
            else:
                if solid[0][1] and solid[1][0]:
                    image_grid[1][1] = 16
                elif solid[0][1]:
                    image_grid[1][1] = 10
                elif solid[1][0]:
                    image_grid[1][1] = 7
                else:
                    image_grid[1][1] = 9

        for dx in range(2):
            for dy in range(2):
                self._tilemap_front.set_tile(x * 2 + dx + 1, y * 2 + dy + 1, self._image_front[image_grid[dx][dy]])


    def apply_velocity(self, obj: Player, pre_pos: Vector2, post_position: Vector2):
        world_pos = post_position
        world_vel = obj.velocity

        w = 0.2
        h = 0.4

        post_pos = world_pos
        post_vel = world_vel

        landed = False
        collided = False

        x_min = floor(pre_pos.x - w * 0.5)
        x_max = ceil(pre_pos.x + w * 0.5) - 1
        y_min = floor(world_pos.y)
        y_max = ceil(world_pos.y + h) - 1

        if x_min >= 0 and x_max < self._w and y_min >= 0 and y_max < self._h:
            for x in range(x_min, x_max + 1):
                if world_vel.y < 0 and self.get_tile(x, y_min) > 0:
                    post_pos = Vector2(post_pos.x, y_min + 1)
                    post_vel = Vector2(post_vel.x, 0)
                    landed = True
                    collided = True
                    break
                if world_vel.y > 0 and self.get_tile(x, y_max) > 0:
                    post_pos = Vector2(post_pos.x, y_max - h)
                    post_vel = Vector2(post_vel.x, 0)
                    collided = True
                    break

        if world_pos.x - w * 0.5 < 0:
            post_pos = Vector2(w * 0.5, post_pos.y)
            post_vel = Vector2(0, post_vel.y)

        if world_pos.x + w * 0.5 > self._w:
            post_pos = Vector2(self._w - w * 0.5, post_pos.y)
            post_vel = Vector2(0, post_vel.y)

        x_min = floor(post_pos.x - w * 0.5)
        x_max = ceil(post_pos.x + w * 0.5) - 1
        y_min = floor(post_pos.y)
        y_max = ceil(post_pos.y + h) - 1

        if x_min >= 0 and x_max < self._w and y_min >= 0 and y_max < self._h:
            for y in range(y_min, y_max + 1):
                if world_vel.x < 0 and self.get_tile(x_min, y) > 0:
                    post_pos = Vector2(x_min + 1 + w * 0.5, post_pos.y)
                    post_vel = Vector2(0, post_vel.y)
                    collided = True
                    break
                if world_vel.x > 0 and self.get_tile(x_max, y) > 0:
                    post_pos = Vector2(x_max - w * 0.5, post_pos.y)
                    post_vel = Vector2(0, post_vel.y)
                    collided = True
                    break

        obj.set_position(post_pos)
        obj.velocity = post_vel

        return landed