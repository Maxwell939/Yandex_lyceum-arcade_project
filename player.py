import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCROLL_THRESHOLD


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.textures.append(arcade.load_texture("textures/player/fall_right.png"))
        self.textures.append(arcade.load_texture("textures/player/idle_right.png"))
        self.textures.append(arcade.load_texture("textures/player/jump_right.png"))
        self.texture = self.textures[1]

        self.center_x = x
        self.bottom = y

        self.scroll = 0

    def update(self, delta_time):
        super().update(delta_time)
        if self.right <= 0:
            self.left = SCREEN_WIDTH
        elif self.left >= SCREEN_WIDTH:
            self.right = 0

        if self.change_x > 0:
            self.scale_x = 1
        elif self.change_x < 0:
            self.scale_x = -1

        if self.change_y != 0:
            self.scroll = 0
        if self.top >= SCROLL_THRESHOLD:
            if self.change_y > 0:
                self.scroll = -self.change_y