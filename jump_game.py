import arcade
from pyglet.graphics import Batch

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, MOVE_SPEED
from player import Player


class JumpGame(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("textures/background.png")

        self.player_list = arcade.SpriteList()

        self.player = None
        self.spawn_point = (SCREEN_WIDTH / 2, SCREEN_HEIGHT)

        self.engine = None

        self.left, self.right, self.up, self.down = False, False, False, False

        self.score = 0
        self.batch = Batch()
        ... #text

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player = Player(*self.spawn_point)
        self.player_list.append(self.player)

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

    def on_update(self, delta_time):
        move = 0
        if self.left and not self.right:
            move = -MOVE_SPEED
        elif self.right and not self.left:
            move = MOVE_SPEED
        self.player.change_x = move

        self.player_list.update()

        self.engine.update()

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