import os
import sys
import arcade
from pyglet.graphics import Batch
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()

class GameOverView(arcade.View):
    def __init__(self, score_manager, sound_manager):
        super().__init__()
        self.score_manager = score_manager
        self.sound_manager = sound_manager
        self.batch = Batch()
        self.game_over_text = None
        self.score_text = None
        self.high_score_text = None
        self.instruction_text = None
        font_path = os.path.join(BASE_PATH, "fonts", "PressStart2P-Regular.ttf")
        arcade.load_font(font_path)
        self.create_text_elements()
    
    def create_text_elements(self):
        self.game_over_text = arcade.Text(
            "GAME OVER",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.7,
            arcade.color.RED,
            30,
            font_name="Press Start 2P",
            anchor_x="center",
            batch=self.batch
        )
        self.score_text1 = arcade.Text(
            " Ваш результат:",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.6,
            arcade.color.WHITE,
            20,
            font_name="Press Start 2P",
            anchor_x="center",
            batch=self.batch
        )
        self.score_text2 = arcade.Text(
            f"{self.score_manager.current_score}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.55,
            arcade.color.WHITE,
            20,
            font_name="Press Start 2P",
            anchor_x="center",
            batch=self.batch
        )
        self.high_score_text1 = arcade.Text(
            " Рекорд:",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.4,
            arcade.color.GOLD,
            15,
            font_name="Press Start 2P",
            anchor_x="center",
            batch=self.batch
        )
        self.high_score_text2 = arcade.Text(
            f"{self.score_manager.high_score}",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.35,
            arcade.color.GOLD,
            15,
            font_name="Press Start 2P",
            anchor_x="center",
            batch=self.batch
        )
        self.instruction_text = arcade.Text(
            "SPACE for restart",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT * 0.2,
            arcade.color.LIGHT_GRAY,
            15,
            anchor_x="center",
            font_name="Press Start 2P",
            batch=self.batch
        )
    
    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.BLACK)
        self.batch.draw()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            from game_view import GameView
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)