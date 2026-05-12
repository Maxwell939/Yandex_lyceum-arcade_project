import arcade
import sys
import os

from constants import SPIKE_SCALE


def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


BASE_PATH = get_base_path()


class Tree(arcade.Sprite):
    def __init__(self):
        super().__init__()
        tree_path = os.path.join(BASE_PATH, "textures", "obstacles", "stick.png")
        self.texture = arcade.load_texture(tree_path)
        self.scale = 0.5


class SpikeCluster(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        spike_path = os.path.join(BASE_PATH, "textures", "obstacles", "spikes.png")
        self.texture = arcade.load_texture(spike_path)
        self.scale = SPIKE_SCALE
        self.center_x = x
        self.bottom = y
        self.is_obstacle = True

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        if self.right < 0:
            self.kill()
