import arcade

from constants import JUMP_SPEED


class OneWayPlatformPhysicsEngine(arcade.PhysicsEnginePlatformer):
    def __init__(self, player_sprite, gravity_constant, platforms):
        super().__init__(player_sprite=player_sprite, gravity_constant=gravity_constant)
        self.oneway_platforms = platforms

    def update(self):
        super().update()
        player = self.player_sprite
        for platform in self.oneway_platforms:
            if (platform.collides_with_sprite(player)
                    and player.center_y > platform.center_y
                    and player.change_y < 0):
                        player.bottom = platform.top
                        player.change_y = 0
                        self.jump(JUMP_SPEED)