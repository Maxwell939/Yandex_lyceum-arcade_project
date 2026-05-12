import os
import sys
import arcade

from constants import SCREEN_WIDTH, SCROLL_THRESHOLD, PLAYER_SCALE, HORIZONTAL_SCREEN_WIDTH, RUN_SPEED
from sound_manager import SoundManager


def get_base_path():
    if getattr(sys, "frozen", False):
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
        self.boost_active = False

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

        if self.boost_active and self.change_y < 0:
            self.boost_active = False


class PlayerHorizontal(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.run_textures = [arcade.load_texture(os.path.join(BASE_PATH, "textures", "player", f"run{i}.png"))
                             for i in range(12)]
        self.double_jump_textures = [
            arcade.load_texture(os.path.join(BASE_PATH, "textures", "player", f"double_jump{i}.png")) for i in range(6)
        ]

        self.center_x = x
        self.bottom = y
        self.scale = PLAYER_SCALE
        self.cur_texture_index = 0
        self.texture = self.run_textures[self.cur_texture_index]
        self.texture_change_time = 0
        self.texture_change_delay = 0.05

        self.is_dead = False
        self.boost_active = False
        self.change_x = RUN_SPEED

        self.is_double_jumping = False
        self.current_animation = "run"

    def update(self, delta_time: float = 1 / 60) -> None:
        super().update(delta_time)
        if self.top < 0:
            self.is_dead = True

        if self.left <= 0:
            self.left = 0
        elif self.right >= HORIZONTAL_SCREEN_WIDTH:
            self.right = HORIZONTAL_SCREEN_WIDTH

        if self.change_y > 0 and self.is_double_jumping:
            self.current_animation = "double_jump"
        elif self.change_y > 0:
            self.current_animation = "jump"
        elif self.change_y < 0:
            self.current_animation = "jump"
        else:
            self.current_animation = "run"
            self.is_double_jumping = False

    def start_double_jump_animation(self):
        self.is_double_jumping = True
        self.cur_texture_index = 0
        self.texture_change_time = 0

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        self.texture_change_time += delta_time
        if self.texture_change_time >= self.texture_change_delay:
            self.texture_change_time -= self.texture_change_delay

            if self.current_animation == "double_jump":
                texture_list = self.double_jump_textures
            else:
                texture_list = self.run_textures

            if texture_list:
                self.cur_texture_index = (self.cur_texture_index + 1) % len(texture_list)
                self.texture = texture_list[self.cur_texture_index]
