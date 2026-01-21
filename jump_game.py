import arcade
from pyglet.graphics import Batch

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY


class JumpGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("textures/background.png")

        self.player_list = arcade.SpriteList()

        self.player = None

        self.engine = None

        self.left, self.right, self.up, self.down = False, False, False, False

        self.score = 0
        self.batch = Batch()
        ... #text

    def setup(self):
        self.player_list = arcade.SpriteList()

        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            gravity_constant=GRAVITY,
        )

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.LBWH(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player_list.draw()

        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = True
        elif key in (arcade.key.UP, arcade.key.W):
            self.up = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = True

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = False
        elif key in (arcade.key.UP, arcade.key.W):
            self.up = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = False