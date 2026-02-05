import random
import os
import sys
import arcade
from constants import LEFT_FACING, RIGHT_FACING, SCREEN_WIDTH, MOVING_PLATFORM_SPEED_RANGE


def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()


class Platform(arcade.Sprite):
    def __init__(self, y: int = 50):
        super().__init__()
        platform_path = os.path.join(BASE_PATH, "textures", "platforms", "platform.png")
        self.texture = arcade.load_texture(platform_path)
        self.scale_y = 0.7
        self.scale_x = 1.1
        self.left = random.randint(0, int(SCREEN_WIDTH - self.width))
        self.bottom = y

    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)
        if self.top < 0:
            self.kill()


class MovingPlatform(Platform):
    def __init__(self, y: int):
        super().__init__()
        self.center_y = y

        moving_platform_path = os.path.join(BASE_PATH, "textures", "platforms", "moving_platform.png")
        self.texture = arcade.load_texture(moving_platform_path)

        self.direction = random.choice((LEFT_FACING, RIGHT_FACING))
        if self.direction == RIGHT_FACING:
            self.left = 0
        elif self.direction == LEFT_FACING:
            self.right = SCREEN_WIDTH

        self.boundary_left = 0
        self.boundary_right = SCREEN_WIDTH

        self.change_x = random.uniform(*MOVING_PLATFORM_SPEED_RANGE)