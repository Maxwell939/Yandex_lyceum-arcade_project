import arcade
import os
import sys


class SoundManager:
    def __init__(self):
        self.jump_sound = None
        self.death_sound = None
        self.death_from_monster_sound = None
        self.monster_death_sound = None
        self.load_sounds()
    
    def load_sounds(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        sounds_dir = os.path.join(base_path, "sounds")
            
        jump_path = os.path.join(sounds_dir, "jump.mp3")
        death_path = os.path.join(sounds_dir, "death.mp3")
        death_from_monster_path = os.path.join(sounds_dir, "jumponmonster.mp3")
        monster_death_path = os.path.join(sounds_dir, "monster_explosion.mp3")
            
        if os.path.exists(jump_path):
            self.jump_sound = arcade.load_sound(jump_path)
            
        if os.path.exists(death_path):
            self.death_sound = arcade.load_sound(death_path)
            
        if os.path.exists(death_from_monster_path):
            self.death_from_monster_sound = arcade.load_sound(death_from_monster_path)
            
        if os.path.exists(monster_death_path):
            self.monster_death_sound = arcade.load_sound(monster_death_path)
    
    def play_jump(self):
        if self.jump_sound:
            arcade.play_sound(self.jump_sound, volume=0.5)
    
    def play_death(self):
        if self.death_sound:
            arcade.play_sound(self.death_sound, volume=0.7)

    def play_death_from_monster(self):
        if self.death_from_monster_sound:
            arcade.play_sound(self.death_from_monster_sound, volume=0.2)

    def play_monster_death(self):
        if self.monster_death_sound:
            arcade.play_sound(self.monster_death_sound, volume=0.3)