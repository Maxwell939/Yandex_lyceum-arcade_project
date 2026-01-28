import random

import arcade
from pyglet.graphics import Batch

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, MOVE_SPEED, MAX_PLATFORMS, JUMP_SPEED, \
    MAX_DELTA_PLATFORMS_DISTANCE, ENEMIES_SPAWN_SCORE_THRESHOLD, MOVING_PLATFORMS_SCORE_THRESHOLD

from enemies import EnemyBird, EnemyBat
from physics_engine import OneWayPlatformPhysicsEngine
from platforms import Platform, MovingPlatform
from player import Player
from score_manager import ScoreManager
from game_over_view import GameOverView
from sound_manager import SoundManager


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = arcade.load_texture("textures/background.png")

        self.player_list = arcade.SpriteList()
        self.platforms = arcade.SpriteList()
        self.platform = None
        self.delta_platforms_distance = 0
        self.moving_platforms_amount = 0

        self.enemies = arcade.SpriteList()

        self.player = None
        self.spawn_point = (SCREEN_WIDTH // 2, 60)

        self.engine = None

        self.left, self.right, self.up, self.down = False, False, False, False
        self.background_scroll = 0
        self.was_jumping = False

        self.score_manager = ScoreManager()
        self.sound_manager = SoundManager()
        self.batch = Batch()
        self.score_text = None
        self.high_score_text = None
        self.score = 0

    def setup(self):
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
        self.score = 0
        self.was_jumping = False
        self.create_score_display()

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

        for platform in self.platforms:
            platform.change_y = self.player.scroll

        self.score -= self.player.scroll

        new_score = int(self.score)
        self.score_manager.update_score(new_score)
        self.update_score_display()

        if self.delta_platforms_distance <= MAX_DELTA_PLATFORMS_DISTANCE:
            self.delta_platforms_distance = int(self.score // 200)

        if len(self.platforms) <= MAX_PLATFORMS:
            platform_types = (["moving"] * self.moving_platforms_amount +
                              ["idle"] * (MAX_PLATFORMS - self.moving_platforms_amount))

            random.shuffle(platform_types)

            for platform_type in platform_types:
                platform_y = (self.platforms[-1].top + self.platform.height +
                              random.randint(10 + self.delta_platforms_distance, 50 + self.delta_platforms_distance))
                if platform_type == "moving":
                    platform = MovingPlatform(platform_y)
                else:
                    platform = Platform(platform_y)

                self.platforms.append(platform)

            if self.score > MOVING_PLATFORMS_SCORE_THRESHOLD:
                self.moving_platforms_amount = int(self.score) // (SCREEN_HEIGHT * 2)
            print(self.moving_platforms_amount)

        self.platforms.update()

        if len(self.enemies) == 0 and self.score > ENEMIES_SPAWN_SCORE_THRESHOLD:
            self.enemies.append(EnemyBird(SCREEN_HEIGHT * 3 + random.choice((-1, 1)) * random.randint(100, 800)))
            self.enemies.append(EnemyBat(SCREEN_HEIGHT * 2 + random.choice((-1, 1)) * random.randint(100, 800)))

        for enemy in self.enemies:
            enemy.change_y = self.player.scroll

        self.enemies.update(self.player)

        self.enemies.update_animation(delta_time)

        if self.engine.can_jump(y_distance=6):
            self.engine.jump(JUMP_SPEED)
            if not self.was_jumping:
                self.sound_manager.play_jump()
                self.was_jumping = True
        else:
            self.was_jumping = False

        self.engine.update()

        if self.check_death():
            self.sound_manager.play_death()
            game_over_view = GameOverView(self.score_manager, self.sound_manager)
            self.window.show_view(game_over_view)

    def check_death(self):
        if self.player.top < 0:
            return True
        return False

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