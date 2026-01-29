import arcade
import os
import sys

class SoundManager:
    def __init__(self):
        self.jump_sound = None
        self.death_sound = None
        self.death_from_monster_sound = None
        self.monster_death_sound = None
        self.sounds_loaded = False
        self.load_sounds()
    
    def load_sounds(self):
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            sounds_dir = os.path.join(base_path, "sounds")
            
            if not os.path.exists(sounds_dir):
                self.sounds_loaded = False
                return
            
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
            
            self.sounds_loaded = (self.jump_sound is not None
                                  and self.death_sound is not None
                                  and self.death_from_monster_sound is not None
                                  and self.monster_death_sound is not None)
                
        except Exception as e:
            self.sounds_loaded = False
    
    def play_jump(self):
        if self.jump_sound and self.sounds_loaded:
            arcade.play_sound(self.jump_sound, volume=0.5)
    
    def play_death(self):
        if self.death_sound and self.sounds_loaded:
            arcade.play_sound(self.death_sound, volume=0.7)

    def play_death_from_monster(self):
        if self.death_from_monster_sound and self.sounds_loaded:
            arcade.play_sound(self.death_from_monster_sound, volume=0.2)

    def play_monster_death(self):
        if self.monster_death_sound and self.sounds_loaded:
            arcade.play_sound(self.monster_death_sound, volume=0.3)
    
    def is_loaded(self):
        return self.sounds_loaded