import os
import sys
import arcade
from constants import SCREEN_WIDTH, SCROLL_THRESHOLD, PLAYER_SCALE
from sound_manager import SoundManager


def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        fall_path = os.path.join(BASE_PATH, "textures", "player", "fall.png")
        idle_path = os.path.join(BASE_PATH, "textures", "player", "idle.png")
        jump_path = os.path.join(BASE_PATH, "textures", "player", "jump.png")

        self.textures.append(arcade.load_texture(fall_path))
        self.textures.append(arcade.load_texture(idle_path))
        self.textures.append(arcade.load_texture(jump_path))
        self.texture = self.textures[1]

        self.center_x = x
        self.bottom = y
        self.scale = PLAYER_SCALE

        self.is_dead = False

        self.scroll = 0

    def update(self, delta_time: float = 1 / 60) -> None:
        super().update(delta_time)
        if self.top < 0:
            self.is_dead = True
            sound_manager = SoundManager()
            sound_manager.play_death()

        if self.right <= 0:
            self.left = SCREEN_WIDTH
        elif self.left >= SCREEN_WIDTH:
            self.right = 0

        if self.change_x > 0:
            self.scale_x = PLAYER_SCALE
        elif self.change_x < 0:
            self.scale_x = -PLAYER_SCALE

        if self.change_y > 0:
            self.texture = self.textures[2]
        elif self.change_y < 0:
            self.texture = self.textures[0]
        else:
            self.texture = self.textures[1]

        self.scroll = 0

        if self.top >= SCROLL_THRESHOLD:
            above_threshold = self.top - SCROLL_THRESHOLD
            self.top = SCROLL_THRESHOLD
            self.scroll = -above_threshold