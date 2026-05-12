import random
import os
import sys
import arcade

from arcade.particles import Emitter, EmitBurst, FadeParticle
from pyglet.graphics import Batch
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, MOVE_SPEED, MAX_PLATFORMS, JUMP_SPEED, \
    MAX_DELTA_PLATFORMS_DISTANCE, ENEMIES_SPAWN_SCORE_THRESHOLD, MOVING_PLATFORMS_SCORE_THRESHOLD, SPARK_TEXTURES, \
    HORIZONTAL_SCREEN_WIDTH, HORIZONTAL_SCREEN_HEIGHT, HORIZONTAL_MOVE_SPEED, SPIKE_SCALE, WORLD_SPEED, \
    HORIZONTAL_JUMP_SPEED, SWITCH_THRESHOLD, SWITCH_CHANCE
from enemies import EnemyBird, EnemyBat, EnemyBee
from physics_engine import OneWayPlatformPhysicsEngine
from platforms import Platform, MovingPlatform, PlatformHorizontal, GroundPlatform
from player import Player, PlayerHorizontal
from score_manager import ScoreManager
from game_over_view import GameOverView
from sound_manager import SoundManager
from obstacles import Tree, SpikeCluster


def get_base_path():
    if getattr(sys, "frozen", False):
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
    def __init__(self, score=0, from_horizontal=False):
        super().__init__()
        background_path = os.path.join(BASE_PATH, "textures", "backgrounds", "background.png")
        self.background = arcade.load_texture(background_path)
        self.player_list = arcade.SpriteList()

        self.platforms = arcade.SpriteList()
        self.platform = None
        self.delta_platforms_distance = 0
        self.moving_platforms_amount = 0

        self.spring = arcade.SpriteList()
        self.enemies = arcade.SpriteList()

        self.player = None
        self.spawn_point = (SCREEN_WIDTH // 2, 60)

        self.engine = None

        self.left = False
        self.right = False

        self.background_scroll = 0

        self.emitters = None

        self.sound_manager = SoundManager()

        self.batch = Batch()
        self.score_text = None
        self.score = score

        self.score_manager = ScoreManager(self.score)

        self.horizontal_world = False
        self.old_score = 0
        self.score_on_last_transition = score
        self.from_horizontal = from_horizontal
        self.score_on_last_transition = score
        self.from_horizontal = from_horizontal

    def setup(self):
        self.player = Player(*self.spawn_point)
        self.player_list.append(self.player)
        self.platforms = arcade.SpriteList()
        self.spring = arcade.SpriteList()
        self.platform = Platform()
        self.platform.position = [SCREEN_WIDTH // 2, 50]
        self.platforms.append(self.platform)
        if self.platform.boost:
            self.spring.append(self.platform.boost)

        self.engine = OneWayPlatformPhysicsEngine(
            player_sprite=self.player,
            gravity_constant=GRAVITY,
            platforms=self.platforms
        )
        self.engine.disable_multi_jump()

        self.emitters = []

        if not hasattr(self, 'score_manager') or self.score_manager is None:
            self.score_manager = ScoreManager(self.score)

        self.score = self.score_manager.current_score

        self.create_score_display()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.LBWH(0, self.background_scroll, SCREEN_WIDTH, SCREEN_HEIGHT),
                                 pixelated=True)
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.LBWH(0, SCREEN_HEIGHT + self.background_scroll,
                                                  SCREEN_WIDTH, SCREEN_HEIGHT), pixelated=True)

        for e in self.emitters:
            e.draw()
        self.platforms.draw(pixelated=True)
        self.spring.draw(pixelated=True)
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
                if platform.boost:
                    self.spring.append(platform.boost)
            if self.score > MOVING_PLATFORMS_SCORE_THRESHOLD:
                self.moving_platforms_amount = int(self.score) // (SCREEN_HEIGHT * 2)
        self.platforms.update()

        for boost in list(self.spring):
            boost.update(self.player, delta_time)
            if hasattr(boost, "update_animation"):
                boost.update_animation(delta_time)

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
            game_over_view = GameOverView(self.score_manager)
            self.window.show_view(game_over_view)

        score_since_last_transition = self.score - self.score_on_last_transition
        if score_since_last_transition >= SWITCH_THRESHOLD:
            if random.random() < SWITCH_CHANCE:
                self.horizontal_world = True
                horizontal_view = GameViewHorizontal(self.score_manager)
                horizontal_view.score_on_last_transition = self.score
                horizontal_view.setup()
                self.window.show_view(horizontal_view)
                self.window.set_size(HORIZONTAL_SCREEN_WIDTH, HORIZONTAL_SCREEN_HEIGHT)

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


class GameViewHorizontal(arcade.View):
    def __init__(self, score_manager: ScoreManager):
        super().__init__()
        background_path = os.path.join(BASE_PATH, "textures", "backgrounds", "wildwest.png")
        self.background = arcade.load_texture(background_path)

        self.player_list = arcade.SpriteList()
        self.platforms = arcade.SpriteList()

        self.player = None
        self.left = False
        self.right = False
        self.spawn_point = (100, 120)

        self.engine = None

        self.sound_manager = SoundManager()

        self.world_speed = WORLD_SPEED
        self.background_speed = 3
        self.background_scroll = 0

        self.last_platform_x = 300

        self.batch = Batch()
        self.score_text = None
        self.score_manager = score_manager
        self.score = self.score_manager.current_score
        self.score_on_last_transition = self.score
        self.old_score = 0

        self.last_tree_score = self.score
        self.first_tree = True
        self.score_start = self.score

    def setup(self):
        self.player = PlayerHorizontal(*self.spawn_point)
        self.player_list.append(self.player)

        self.platforms = arcade.SpriteList()

        # Create initial continuous ground (cover screen width + buffer)
        # Ground texture is 44 pixels wide
        ground_texture_width = 44
        self.platforms_needed = (HORIZONTAL_SCREEN_WIDTH // ground_texture_width) + 3  # +3 for buffer

        for i in range(self.platforms_needed):
            platform = GroundPlatform(i * ground_texture_width + ground_texture_width, 0)
            self.platforms.append(platform)

        self.bees = arcade.SpriteList()
        self.last_bee_score = 0
        self.bee_spawn_interval = random.randint(300, 600)

        self.emitters = []

        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            platforms=self.platforms,
            gravity_constant=GRAVITY
        )
        self.engine.enable_multi_jump(2)

        # Spike management
        self.spike_positions = []  # Track spike x positions to avoid overlap
        self.last_spike_score = 0  # Track when we last generated spikes
        self.spike_cluster_spacing = 100  # Minimum distance between spike clusters

        self.create_score_display()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.LBWH(self.background_scroll, 0,
                                                  HORIZONTAL_SCREEN_WIDTH, HORIZONTAL_SCREEN_HEIGHT), pixelated=True)
        arcade.draw_texture_rect(self.background,
                                 arcade.rect.LBWH(-HORIZONTAL_SCREEN_WIDTH + self.background_scroll, 0,
                                                  HORIZONTAL_SCREEN_WIDTH, HORIZONTAL_SCREEN_HEIGHT), pixelated=True)
        for e in self.emitters:
            e.draw()
        self.platforms.draw(pixelated=True)
        self.bees.draw(pixelated=True)
        self.player_list.draw(pixelated=True)
        self.batch.draw()

    def on_update(self, delta_time: float):
        move = 0
        if self.left and not self.right:
            move = -HORIZONTAL_MOVE_SPEED
        elif self.right and not self.left:
            move = HORIZONTAL_MOVE_SPEED
        self.player.change_x = move
        self.player_list.update()
        self.player_list.update_animation(delta_time)

        self.background_scroll -= self.background_speed
        self.background_scroll %= HORIZONTAL_SCREEN_WIDTH

        self.score += self.world_speed // 2
        self.score_manager.update_score(int(self.score))
        self.update_score_display()

        for platform in self.platforms:
            platform.center_x -= self.world_speed

        for platform in list(self.platforms):
            if platform.right < 0:
                platform.kill()

        # Maintain continuous ground (keep 3 ground platforms ahead)
        ground_platforms = [p for p in self.platforms if p.bottom == 0]
        if len(ground_platforms) < self.platforms_needed:
            # Find the rightmost ground platform
            last_ground = max([p.left for p in ground_platforms])

            if last_ground:
                # Place next ground platform exactly where the last one ends
                # Ground texture is 44 pixels wide with scale 1.0
                ground_width = 44
                new_ground_x = last_ground + ground_width
            else:
                new_ground_x = 200

            # Ground platform with consistent scale
            ground_platform = GroundPlatform(new_ground_x, 0)
            self.platforms.append(ground_platform)

        # Generate spike clusters on ground platforms
        if self.score - self.last_spike_score > random.randint(400, 800):  # Random interval between generations
            if random.random() < random.uniform(0.1, 0.3):  # Random chance between 20% and 50%
                # Find the rightmost ground platform
                ground_platforms = [p for p in self.platforms if isinstance(p, GroundPlatform)]
                if ground_platforms:
                    # Get the ground platform that's farthest to the right
                    rightmost_platform = max(ground_platforms, key=lambda p: p.center_x)

                    # Find the rightmost spike position (if any exist)
                    rightmost_spike_x = max(self.spike_positions) if self.spike_positions else 0

                    cluster_size = random.randint(8, 16)
                    # Generate spikes with random spacing from last cluster
                    safe_start_x = max(rightmost_platform.center_x, rightmost_spike_x) + cluster_size * 16
                    spawn_x = safe_start_x + random.randint(0, 300)
                    spike_y = rightmost_platform.top  # Ground level

                    start_x = spawn_x - (cluster_size - 1) * 8 * SPIKE_SCALE  # Center the cluster

                    for i in range(cluster_size):
                        spike = SpikeCluster(start_x + i * 16 * SPIKE_SCALE, spike_y)
                        self.platforms.append(spike)
                        self.spike_positions.append(spike.center_x)

                    self.last_spike_score = self.score

        # Generate levitating platforms and obstacles
        levitating_platforms = [p for p in self.platforms if p.bottom > 0 and not getattr(p, "is_obstacle", False)]
        if len(levitating_platforms) < 10:  # Limit levitating platforms
            last_levitating = max(levitating_platforms, key=lambda p: p.center_x) if levitating_platforms else None

            if last_levitating:
                gap = random.randint(80, 150)
                new_x = last_levitating.right + gap
            else:
                new_x = 400

            levitating_height = random.randint(80, HORIZONTAL_SCREEN_HEIGHT - 100)
            levitating_scale = random.uniform(1.0, 2.5)
            levitating_platform = PlatformHorizontal(new_x, levitating_height, levitating_scale)
            self.platforms.append(levitating_platform)

        if self.score - self.last_bee_score > self.bee_spawn_interval:
            if random.random() < 0.4:  # 40% chance to spawn a bee
                # Spawn bee from the right side of the screen
                spawn_x = HORIZONTAL_SCREEN_WIDTH + random.randint(50, 200)
                # Random y position, not too close to top or bottom
                spawn_y = random.randint(100, HORIZONTAL_SCREEN_HEIGHT - 100)

                bee = EnemyBee(spawn_x, spawn_y)
                self.bees.append(bee)

                self.last_bee_score = self.score
                self.bee_spawn_interval = random.randint(300, 600)  # Reset with new random interval

            # Update bees
        self.bees.update(self.player, delta_time)
        self.bees.update_animation(delta_time)

        # Handle bee deaths (explosions)
        for bee in self.bees:
            if bee.make_explosion:
                self.emitters.append(make_explosion(bee.center_x, bee.center_y))
                self.emitters.append(make_explosion(bee.center_x, bee.center_y))
                bee.kill()

        emitters_copy = self.emitters.copy()
        for e in emitters_copy:
            e.update(delta_time)
        for e in emitters_copy:
            if e.can_reap():
                self.emitters.remove(e)

        for sprite in self.platforms:
            if getattr(sprite, "is_obstacle", False):
                if arcade.check_for_collision(self.player, sprite):
                    self.player.is_dead = True
                    self.sound_manager.play_death_from_monster()
                    break

        score_since_last_transition = self.score - self.score_on_last_transition
        if score_since_last_transition >= SWITCH_THRESHOLD:
            if random.random() < SWITCH_CHANCE:
                vertical_view = GameView(self.score, from_horizontal=True)
                vertical_view.score_on_last_transition = self.score
                vertical_view.setup()
                self.window.show_view(vertical_view)
                self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.engine.update()
        if self.player.is_dead:
            game_over_view = GameOverView(self.score_manager)
            self.window.show_view(game_over_view)
            self.window.set_size(SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.SPACE, arcade.key.W):
            if self.engine.can_jump():
                if self.engine.jumps_since_ground > 0:
                    self.player.start_double_jump_animation()
                self.player.change_y = HORIZONTAL_JUMP_SPEED
                self.engine.increment_jump_counter()
        elif key in (arcade.key.LEFT, arcade.key.A):
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
            10, HORIZONTAL_SCREEN_HEIGHT - 30,
            arcade.color.BLACK, 15, font_name="Press Start 2P",
            batch=self.batch)

    def update_score_display(self):
        self.score_text.text = f"{self.score_manager.current_score}"

    def back_to_main(self):
        self.score_on_transition = self.score
        vertical_view = GameView()
        vertical_view.spawn_point = (self.player.center_x, self.player.center_y)
        vertical_view.setup()
        vertical_view.score_on_last_transition = self.score
        self.window.show_view(vertical_view)
