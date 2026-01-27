import random

import arcade
from pyglet.graphics import Batch

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, MOVE_SPEED, MAX_PLATFORMS, JUMP_SPEED
from enemies import EnemyBird, EnemyBat
from physics_engine import OneWayPlatformPhysicsEngine
from platform_ import Platform
from player import Player


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("textures/background.png")

        self.player_list = arcade.SpriteList()
        self.platforms = arcade.SpriteList()
        self.platform = None
        self.enemies = arcade.SpriteList()

        self.player = None
        self.spawn_point = (SCREEN_WIDTH // 2, 60)

        self.engine = None

        self.left, self.right, self.up, self.down = False, False, False, False
        self.background_scroll = 0

        self.score = 0
        self.batch = Batch()
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

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.LBWH(0, self.background_scroll, SCREEN_WIDTH, SCREEN_HEIGHT))
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.LBWH(0, SCREEN_HEIGHT + self.background_scroll,
                                                  SCREEN_WIDTH, SCREEN_HEIGHT))

        self.platforms.draw(pixelated=True)
        self.enemies.draw(pixelated=True)
        self.player_list.draw(pixelated=True)

        self.batch.draw()

    def on_update(self, delta_time):
        move = 0
        if self.left and not self.right:
            move = -MOVE_SPEED
        elif self.right and not self.left:
            move = MOVE_SPEED
        self.player.change_x = move

        self.player_list.update()

        self.background_scroll += self.player.scroll // 2
        if self.background_scroll <= -SCREEN_HEIGHT:
            self.background_scroll = 0

        if self.player.scroll != 0:
            for platform in self.platforms:
                platform.center_y += self.player.scroll

        if len(self.platforms) < MAX_PLATFORMS:
            platform_x = random.randint(0, int(SCREEN_WIDTH - self.platform.width))
            platform_y = self.platforms[-1].top + self.platform.height + random.randint(80, 120)
            platform = Platform()
            platform.left, platform.bottom = platform_x, platform_y
            self.platforms.append(platform)

        self.platforms.update()

        if len(self.enemies) == 0:
            self.enemies.append(EnemyBird(SCREEN_HEIGHT * 2 + random.choice((-1, 1)) * random.randint(50, 200)))
            self.enemies.append(EnemyBat(SCREEN_HEIGHT * 2 + random.choice((-1, 1)) * random.randint(50, 200)))

        for enemy in self.enemies:
            enemy.change_y = self.player.scroll

        self.enemies.update(self.player)

        self.enemies.update_animation(delta_time)

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