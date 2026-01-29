import arcade


SCREEN_WIDTH: int = 400
SCREEN_HEIGHT: int = 800
SCREEN_TITLE: str = "JumpGame"
GRAVITY: float = 0.25
MOVE_SPEED: int = 3
MAX_PLATFORMS: int = 20
MAX_DELTA_PLATFORMS_DISTANCE: int = 130
MOVING_PLATFORMS_SCORE_THRESHOLD: int = 1000
MOVING_PLATFORM_SPEED_RANGE: tuple[float, float] = (1.0, 2.0)
JUMP_SPEED: int = 7
PLAYER_SCALE: float = 1.4
SCROLL_THRESHOLD: int = SCREEN_HEIGHT // 2
ENEMY_BIRD_SPEED: int = 2
RIGHT_FACING: int = 1
LEFT_FACING: int = -1
ENEMY_SCALE: float = 1.5
ENEMIES_SPAWN_SCORE_THRESHOLD: int = 2500
SPARK_TEXTURES = [
    arcade.make_soft_circle_texture(8, arcade.color.ALIZARIN_CRIMSON),
    arcade.make_soft_circle_texture(8, arcade.color.COQUELICOT),
    arcade.make_soft_circle_texture(8, arcade.color.LAVA),
    arcade.make_soft_circle_texture(8, arcade.color.ELECTRIC_CRIMSON),
    arcade.make_soft_circle_texture(8, arcade.color.DARK_TANGERINE)
]