import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        for i in range(2):
            self.textures.append(arcade.load_texture("textures/player/fall_right.png",
                                                     flipped_horizontally=i))
            self.textures.append(arcade.load_texture("textures/player/idle_right.png",
                                                     flipped_horizontally=i))
            self.textures.append(arcade.load_texture("textures/player/jump_right.png",
                                                     flipped_horizontally=i))
        self.left = x
        self.bottom = y

    def update(self, delta_time):
        super().update(delta_time)
        if self.right <= 0:
            self.left = SCREEN_WIDTH
        elif self.left >= SCREEN_WIDTH:
            self.right = 0

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT