import arcade
from constants import JUMP_SPEED
from sound_manager import SoundManager


class OneWayPlatformPhysicsEngine(arcade.PhysicsEnginePlatformer):
    def __init__(self, player_sprite, gravity_constant, platforms):
        super().__init__(player_sprite=player_sprite, gravity_constant=gravity_constant)
        self.oneway_platforms = platforms

    def update(self, sound_manager: SoundManager) -> None:
        super().update()
        player: arcade.Sprite = self.player_sprite
        for platform in self.oneway_platforms:
            if (platform.collides_with_sprite(player)
                    and player.center_y > platform.center_y
                    and player.change_y < 0):
                player.bottom = platform.top
                player.change_y = 0
                self.jump(JUMP_SPEED)
                if sound_manager:
                    sound_manager.play_jump()

            if platform.change_x != 0 or platform.change_y != 0:
                if (platform.boundary_left is not None
                        and platform.left <= platform.boundary_left):
                    platform.left = platform.boundary_left
                    if platform.change_x < 0:
                        platform.change_x *= -1

                if (platform.boundary_right is not None
                        and platform.right >= platform.boundary_right):
                    platform.right = platform.boundary_right
                    if platform.change_x > 0:
                        platform.change_x *= -1
                if platform.boundary_top is not None and platform.top >= platform.boundary_top:
                    platform.top = platform.boundary_top
                    if platform.change_y > 0:
                        platform.change_y *= -1

                if (platform.boundary_bottom is not None
                        and platform.bottom <= platform.boundary_bottom):
                    platform.bottom = platform.boundary_bottom
                    if platform.change_y < 0:
                        platform.change_y *= -1