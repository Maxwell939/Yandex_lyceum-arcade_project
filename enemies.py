import random

import arcade

from constants import RIGHT_FACING, LEFT_FACING, SCREEN_WIDTH, ENEMY_BIRD_SPEED


class Enemy(arcade.Sprite):
    def __init__(self, y):
        super().__init__()
        self.bottom = y

    def update(self, delta_time, player) -> None:
        super().update(delta_time)
        if self.collides_with_sprite(player):
            self.kill()


class EnemyBird(Enemy):
    def __init__(self, y):
        super().__init__(y)
        for i in range(1, 10):
            self.textures.append(arcade.load_texture(f"textures/bird/bird{i}.png"))

        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]
        self.texture_change_time = 0
        self.texture_change_delay = 0.05  # секунд на кадр

        direction = random.choice((RIGHT_FACING, LEFT_FACING))
        if direction == RIGHT_FACING:
            self.left = 0
        elif direction == LEFT_FACING:
            self.right = SCREEN_WIDTH

        self.scale_x = direction * -1
        self.change_x = direction * ENEMY_BIRD_SPEED

    def update(self, delta_time, player) -> None:
        super().update(delta_time, player)
        if self.left == 0 or self.right == SCREEN_WIDTH:
            self.scale_x *= -1
            self.change_x *= -1

    def update_animation(self, delta_time: float = 1 / 60):
        self.texture_change_time += delta_time
        if self.texture_change_time >= self.texture_change_delay:
            self.texture_change_time = 0
            if self.cur_texture_index >= len(self.textures) - 1:
                self.cur_texture_index = 0
            else:
                self.cur_texture_index += 1
            self.texture = self.textures[self.cur_texture_index]