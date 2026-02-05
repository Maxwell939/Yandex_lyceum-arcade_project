import random
import os
import sys
import arcade

from constants import RIGHT_FACING, LEFT_FACING, SCREEN_WIDTH, ENEMY_BIRD_SPEED, ENEMY_SCALE
from sound_manager import SoundManager


def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()


class Enemy(arcade.Sprite):
    def __init__(self, y: int):
        super().__init__()
        self.bottom = y
        self.make_explosion = False
        self.sound_manager = SoundManager()

    def update(self, player: arcade.Sprite, delta_time: float = 1 / 60) -> None:
        super().update(delta_time)
        if self.collides_with_sprite(player):
            if (self.collides_with_sprite(player)
                    and player.center_y > self.center_y
                    and player.change_y < 0):
                self.make_explosion = True
                self.sound_manager.play_monster_death()
            else:
                player.is_dead = True
                self.sound_manager.play_death_from_monster()

        if self.top < 0:
            self.kill()


class EnemyBat(Enemy):
    def __init__(self, y: int):
        super().__init__(y)
        for i in range(1, 8):
            bat_path = os.path.join(BASE_PATH, "textures", "bat", f"bat{i}.png")
            self.textures.append(arcade.load_texture(bat_path))

        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]
        self.texture_change_time = 0
        self.texture_change_delay = 0.05

        self.scale = ENEMY_SCALE
        self.left = random.randint(SCREEN_WIDTH // 10, SCREEN_WIDTH - int(self.width) - SCREEN_WIDTH // 10)

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.texture_change_time += delta_time
        if self.texture_change_time >= self.texture_change_delay:
            self.texture_change_time -= self.texture_change_delay
            self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
            self.texture = self.textures[self.cur_texture_index]


class EnemyBird(Enemy):
    def __init__(self, y: int):
        super().__init__(y)
        for i in range(1, 10):
            bird_path = os.path.join(BASE_PATH, "textures", "bird", f"bird{i}.png")
            self.textures.append(arcade.load_texture(bird_path))

        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]
        self.texture_change_time = 0
        self.texture_change_delay = 0.05

        self.direction = random.choice((RIGHT_FACING, LEFT_FACING))
        if self.direction == RIGHT_FACING:
            self.left = 0
        elif self.direction == LEFT_FACING:
            self.right = SCREEN_WIDTH

        self.change_x = self.direction * ENEMY_BIRD_SPEED

    def update(self, player: arcade.Sprite, delta_time: float = 1 / 60) -> None:
        super().update(player=player, delta_time=delta_time)
        if self.left == 0 or self.right == SCREEN_WIDTH:
            self.direction *= -1
            self.change_x = self.direction * ENEMY_BIRD_SPEED

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.texture_change_time += delta_time
        if self.texture_change_time >= self.texture_change_delay:
            self.texture_change_time -= self.texture_change_delay
            self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
            self.texture = self.textures[self.cur_texture_index]

            if self.direction == RIGHT_FACING:
                self.texture = self.textures[self.cur_texture_index].flip_horizontally()
            else:
                self.texture = self.textures[self.cur_texture_index]