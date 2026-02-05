import random
import os
import sys
import arcade
from arcade.particles import Emitter, EmitBurst, FadeParticle
from pyglet.graphics import Batch

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, MOVE_SPEED, MAX_PLATFORMS, JUMP_SPEED, \
    MAX_DELTA_PLATFORMS_DISTANCE, ENEMIES_SPAWN_SCORE_THRESHOLD, MOVING_PLATFORMS_SCORE_THRESHOLD, SPARK_TEXTURES

from enemies import EnemyBird, EnemyBat
from physics_engine import OneWayPlatformPhysicsEngine
from platforms import Platform, MovingPlatform
from player import Player
from score_manager import ScoreManager
from game_over_view import GameOverView
from sound_manager import SoundManager


def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

BASE_PATH = get_base_path()

def gravity_drag(p):
    p.change_y -= 0.03
    p.change_x *= 0.92
    p.change_y *= 0.92

def make_explosion(x, y, count=80):
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(count),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(SPARK_TEXTURES),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 9.0),
            lifetime=random.uniform(0.5, 1.1),
            start_alpha=255, end_alpha=0,
            scale=random.uniform(0.35, 0.6),
            mutation_callback=gravity_drag,
        ),
    )


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        background_path = os.path.join(BASE_PATH, "textures", "background.png")
        self.background = arcade.load_texture(background_path)
        self.player_list = arcade.SpriteList()

        self.platforms = arcade.SpriteList()
        self.platform = None
        self.delta_platforms_distance = 0
        self.moving_platforms_amount = 0

        self.enemies = arcade.SpriteList()

        self.player = None
        self.spawn_point = (SCREEN_WIDTH // 2, 60)

        self.engine = None

        self.left = False
        self.right = False

        self.background_scroll = 0

        self.emitters = None

        self.score_manager = ScoreManager()
        self.sound_manager = SoundManager()

        self.batch = Batch()
        self.score_text = None
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

        self.emitters = []

        self.score_manager.reset()
        self.score = 0
        self.create_score_display()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.LBWH(0, self.background_scroll, SCREEN_WIDTH, SCREEN_HEIGHT))
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.LBWH(0, SCREEN_HEIGHT + self.background_scroll,
                                                  SCREEN_WIDTH, SCREEN_HEIGHT))

        for e in self.emitters:
            e.draw()
        self.platforms.draw(pixelated=True)
        self.enemies.draw(pixelated=True)
        self.player_list.draw(pixelated=True)
        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT - 35, SCREEN_HEIGHT, (0, 0, 0, 120))
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

        self.score -= self.player.scroll
        new_score = int(self.score)
        self.score_manager.update_score(new_score)
        self.update_score_display()

        for platform in self.platforms:
            platform.change_y = self.player.scroll
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
        self.platforms.update()

        if len(self.enemies) == 0 and self.score > ENEMIES_SPAWN_SCORE_THRESHOLD:
            self.enemies.append(EnemyBird(SCREEN_HEIGHT * 2 + random.choice((-1, 1)) * random.randint(100, 1200)))
            self.enemies.append(EnemyBat(SCREEN_HEIGHT * 1.7 + random.choice((-1, 1)) * random.randint(100, 900)))
        for enemy in self.enemies:
            enemy.change_y = self.player.scroll
        self.enemies.update(self.player)
        self.enemies.update_animation(delta_time)
        for enemy in self.enemies:
            if enemy.make_explosion:
                self.emitters.append(make_explosion(enemy.center_x, enemy.center_y))
                self.emitters.append(make_explosion(enemy.center_x, enemy.center_y))
                enemy.kill()

        emitters_copy = self.emitters.copy()
        for e in emitters_copy:
            e.update(delta_time)
        for e in emitters_copy:
            if e.can_reap():
                self.emitters.remove(e)

        self.engine.update(sound_manager=self.sound_manager)

        if self.player.is_dead:
            game_over_view = GameOverView(self.score_manager, self.sound_manager)
            self.window.show_view(game_over_view)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = True

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = False
    
    def create_score_display(self):
        self.score_text = arcade.Text(
            f"{self.score_manager.current_score}",
            10, SCREEN_HEIGHT - 30,
            arcade.color.BLACK, 15, font_name="Press Start 2P",
            batch=self.batch)

    def update_score_display(self):
        self.score_text.text = f"{self.score_manager.current_score}"