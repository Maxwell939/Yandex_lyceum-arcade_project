import arcade

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
HORIZONTAL_SCREEN_WIDTH = 1120
HORIZONTAL_SCREEN_HEIGHT = 490
SCREEN_TITLE = "JumpStep"
GRAVITY: float = 0.25
MOVE_SPEED = 3
HORIZONTAL_MOVE_SPEED = 2
MAX_PLATFORMS = 20
PLATFORM_SCALE: tuple[float, float] = (1, 1)
MAX_DELTA_PLATFORMS_DISTANCE = 130
MOVING_PLATFORMS_SCORE_THRESHOLD = 1000
MOVING_PLATFORM_SPEED_RANGE: tuple[float, float] = (1.0, 2.0)
JUMP_SPEED = 7
HORIZONTAL_JUMP_SPEED = 5
PLAYER_SCALE: float = 1.4
SCROLL_THRESHOLD = SCREEN_HEIGHT // 2
ENEMY_BIRD_SPEED = 2
SPIKE_SCALE = 4.0
RIGHT_FACING = 1
LEFT_FACING = -1
ENEMY_SCALE: float = 1.5
ENEMIES_SPAWN_SCORE_THRESHOLD = 2500
BOOST_PROBABILITY: float = 0.05
RUN_SPEED = 5
SPARK_TEXTURES: list[arcade.Texture] = [
    arcade.make_soft_circle_texture(8, arcade.color.ALIZARIN_CRIMSON),
    arcade.make_soft_circle_texture(8, arcade.color.COQUELICOT),
    arcade.make_soft_circle_texture(8, arcade.color.LAVA),
    arcade.make_soft_circle_texture(8, arcade.color.ELECTRIC_CRIMSON),
    arcade.make_soft_circle_texture(8, arcade.color.DARK_TANGERINE)
]
