import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class JumpGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("textures/background.png")

    def setup(self):
        ...

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.LBWH(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))