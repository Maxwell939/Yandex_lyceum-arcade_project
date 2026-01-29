import arcade
from pyglet.graphics import Batch

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class StartView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.game_view = game_view
        self.start_text = None
        self.any_key_text = None
        self.batch = None

    def on_draw(self) -> None:
        self.clear()
        self.batch = Batch()
        self.start_text = arcade.Text("JumpStep", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                 arcade.color.WHITE, font_size=50, anchor_x="center", batch=self.batch)
        self.any_key_text = arcade.Text("Нажмите любую клавишу для запуска",
                                   self.window.width / 2, self.window.height / 2 - 75,
                                   arcade.color.GRAY, font_size=20, anchor_x="center", batch=self.batch)
        self.batch.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.game_view.setup()
        self.window.show_view(self.game_view)