import arcade


class Platform(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("textures/platform.png")
        self.scale_y = 0.5

    def update(self, delta_time):
        if self.rect.top < 0:
            self.kill()