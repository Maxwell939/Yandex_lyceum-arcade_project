import arcade


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SCREEN_TITLE = "JumpGame"

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()