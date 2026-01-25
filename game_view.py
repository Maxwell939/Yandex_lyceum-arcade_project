import random

import arcade
from pyglet.graphics import Batch

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, MOVE_SPEED, MAX_PLATFORMS, JUMP_SPEED
from physics_engine import OneWayPlatformPhysicsEngine
from platform_ import Platform
from player import Player
from score_manager import ScoreManager

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("textures/background.png")

        self.player_list = arcade.SpriteList()
        self.platforms = arcade.SpriteList()
        self.platform = None

        self.player = None
        self.spawn_point = (SCREEN_WIDTH // 2, 60)

        self.engine = None

        self.left, self.right, self.up, self.down = False, False, False, False
        self.background_scroll = 0

        self.score = 0
        self.score_manager = ScoreManager()
        self.batch = Batch()
        self.score_text = None
        self.high_score_text = None
        self.total_scroll = 0
        ... #text

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player = Player(*self.spawn_point)
        self.player_list.append(self.player)

        self.platform = Platform()
        self.platform.position = [SCREEN_WIDTH // 2, 50]
        self.platforms.append(self.platform)

        self.engine = OneWayPlatformPhysicsEngine(
            player_sprite=self.player,
            gravity_constant=GRAVITY,
            platforms=self.platforms
        )
        self.engine.disable_multi_jump()
        self.score_manager.reset()
        self.total_scroll = 0
        self.create_score_display()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.LBWH(0, self.background_scroll, SCREEN_WIDTH, SCREEN_HEIGHT))
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.LBWH(0, SCREEN_HEIGHT + self.background_scroll,
                                                  SCREEN_WIDTH, SCREEN_HEIGHT))

        self.player_list.draw()
        self.platforms.draw()

        self.batch.draw()

    def on_update(self, delta_time):
        move = 0
        if self.left and not self.right:
            move = -MOVE_SPEED
        elif self.right and not self.left:
            move = MOVE_SPEED
        self.player.change_x = move

        self.player_list.update()

        if self.player.scroll != 0:
            for platform in self.platforms:
                platform.center_y += self.player.scroll

        self.total_scroll -= self.player.scroll

        new_score = int(self.total_scroll // 10)
        self.score_manager.update_score(new_score)
        self.update_score_display()

        self.background_scroll += self.player.scroll // 2
        if self.background_scroll <= -SCREEN_HEIGHT:
            self.background_scroll = 0

        if len(self.platforms) < MAX_PLATFORMS:
            platform_x = random.randint(0, int(SCREEN_WIDTH - self.platform.width))
            platform_y = self.platforms[-1].top + self.platform.height + random.randint(80, 120)
            platform = Platform()
            platform.left, platform.bottom = platform_x, platform_y
            self.platforms.append(platform)

        self.platforms.update()

        if self.engine.can_jump(y_distance=6):
            self.engine.jump(JUMP_SPEED)

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
    
    def create_score_display(self):
        self.score_text = arcade.Text(
            f"Счёт: {self.score_manager.current_score}",
            10, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 20,
            batch=self.batch)
        self.high_score_text = arcade.Text(
            f"Рекорд: {self.score_manager.high_score}",
            SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30,
            arcade.color.GOLD, 20,
            batch=self.batch,
            align="right",
            width=140)

    def update_score_display(self):
        self.score_text.text = f"Счёт: {self.score_manager.current_score}"
        self.high_score_text.text = f"Рекорд: {self.score_manager.high_score}"