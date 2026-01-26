import random

import arcade

from constants import RIGHT_FACING, LEFT_FACING, SCREEN_WIDTH, ENEMY_BIRD_SPEED


class Enemy(arcade.Sprite):
    def __init__(self):
        super().__init__()

    def update(self, player, delta_time: float = 1 / 60) -> None:
        super().update(delta_time)
        if self.collides_with_sprite(player):
            self.kill()


class EnemyBird(Enemy):
    def __init__(self):
        super().__init__()
        for i in range(1, 10):
            self.textures.append(arcade.load_texture(f"textures/bird/bird{i}"))

        self.cur_texture_index = 0

    def update(self, player, delta_time: float = 1 / 60) -> None:
        super().update(delta_time)