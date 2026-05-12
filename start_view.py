import os
import sys
import arcade

from pyglet.graphics import Batch
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


BASE_PATH = get_base_path()


class StartView(arcade.View):
    def __init__(self, game_view, score_manager):
        super().__init__()
        self.score_manager = score_manager
        bg_path = os.path.join(BASE_PATH, "textures", "backgrounds", "yellow_menu_bg.png")
        self.game_view = game_view
        self.start_text = None
        self.any_key_text1 = None
        self.any_key_text2 = None
        self.batch = None
        self.background = arcade.load_texture(bg_path)

        font_path = os.path.join(BASE_PATH, "fonts", "PressStart2P-Regular.ttf")
        arcade.load_font(font_path)

    def on_draw(self) -> None:
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.LBWH(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.batch = Batch()
        self.start_text = arcade.Text(SCREEN_TITLE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.7, arcade.color.BLACK,
                                      font_size=30, font_name="Press Start 2P", anchor_x="center", batch=self.batch)
        self.any_key_text1 = arcade.Text("Нажмите ПРОБЕЛ", SCREEN_WIDTH / 2,
                                         SCREEN_HEIGHT * 0.2, arcade.color.AERO_BLUE, font_size=15,
                                         font_name="Press Start 2P", anchor_x="center", batch=self.batch)
        self.any_key_text2 = arcade.Text("для запуска", SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.15,
                                         arcade.color.AERO_BLUE, font_size=15, font_name="Press Start 2P",
                                         anchor_x="center", batch=self.batch)
        self.high_score_text1 = arcade.Text(
            " Рекорд:",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.55,
            arcade.color.GOLD,
            15,
            font_name="Press Start 2P",
            anchor_x="center",
            batch=self.batch
        )
        self.high_score_text2 = arcade.Text(
            f"{self.score_manager.high_score}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.5,
            arcade.color.GOLD,
            15,
            font_name="Press Start 2P",
            anchor_x="center",
            batch=self.batch
        )
        self.instruction_text1 = arcade.Text(
            "A, D для управления",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.3,
            arcade.color.AERO_BLUE,
            15,
            font_name="Press Start 2P",
            anchor_x="center",
            batch=self.batch
        )
        self.batch.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.game_view.setup()
        self.window.show_view(self.game_view)
