import random

import arcade

from constants import LEFT_FACING, RIGHT_FACING, SCREEN_WIDTH, MOVING_PLATFORM_SPEED_RANGE


class Platform(arcade.Sprite):
    def __init__(self, y: int = 50):
        super().__init__()
        self.texture = arcade.load_texture("textures/platforms/platform.png")
        self.scale_y = 0.7
        self.scale_x = 1.1
        self.left = random.randint(0, int(SCREEN_WIDTH - self.width))
        self.bottom = y

    def update(self, delta_time: float = 1 / 60) -> None:
        super().update(delta_time)

        if self.top < 0:
            self.kill()


class MovingPlatform(Platform):
    def __init__(self, y: int):
        super().__init__()
        self.center_y = y
        self.texture = arcade.load_texture("textures/platforms/moving_platform.png")

        self.direction = random.choice((LEFT_FACING, RIGHT_FACING))
        if self.direction == RIGHT_FACING:
            self.left = 0
        elif self.direction == LEFT_FACING:
            self.right = SCREEN_WIDTH

        self.boundary_left = 0
        self.boundary_right = SCREEN_WIDTH

        self.change_x = random.uniform(*MOVING_PLATFORM_SPEED_RANGE)