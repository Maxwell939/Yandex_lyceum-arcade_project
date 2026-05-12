import arcade
import sys
import os

from constants import JUMP_SPEED


def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


BASE_PATH = get_base_path()


class Boost(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.is_boost_active = False
        self.texture_change_time = 0

    def update(self, player: arcade.Sprite, delta_time: float = 1 / 60):
        super().update(delta_time)
        if self.collides_with_sprite(player) and player.change_y < 0:
            self.is_boost_active = True
            self.cur_texture_index = 0
            self.texture_change_time = 0
            player.change_y = JUMP_SPEED * self.boost_strength
            if player.change_y > 0:
                player.boost_active = True


class Spring(Boost):
    def __init__(self):
        super().__init__()
        for i in range(8):
            self.textures.append(arcade.load_texture(
                os.path.join(BASE_PATH, "textures", "boosts", "trampoline", f"trampoline{i}.png")))

        self.cur_texture_index = 0
        self.texture = self.textures[self.cur_texture_index]
        self.texture_change_time = 0
        self.texture_change_delay = 0.05
        self.scale = 1.5
        self.boost_strength = 2

    def update_animation(self, delta_time: float = 1 / 60):
        if self.is_boost_active:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time -= self.texture_change_delay
                self.cur_texture_index += 1
                if self.cur_texture_index >= len(self.textures):
                    self.is_boost_active = False
                    self.cur_texture_index = 0
                    self.texture = self.textures[0]
                else:
                    self.texture = self.textures[self.cur_texture_index]
