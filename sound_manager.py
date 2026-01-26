import arcade
import os

class SoundManager:
    def __init__(self):
        self.jump_sound = None
        self.death_sound = None
        self.sounds_loaded = False
        self.load_sounds()
    
    def load_sounds(self):
        """Загружает звуковые файлы"""
        try:
            sounds_dir = "sounds"
            if not os.path.exists(sounds_dir):
                os.makedirs(sounds_dir, exist_ok=True)
                self.sounds_loaded = False
                return
            jump_path = os.path.join(sounds_dir, "jump.mp3")
            death_path = os.path.join(sounds_dir, "death.mp3")
            if os.path.exists(jump_path):
                self.jump_sound = arcade.load_sound(jump_path)
            else:
                print(f"Файл {jump_path} не найден")
            if os.path.exists(death_path):
                self.death_sound = arcade.load_sound(death_path)
            else:
                print(f"Файл {death_path} не найден")
            
            self.sounds_loaded = self.jump_sound is not None and self.death_sound is not None
                
        except Exception as e:
            print(f"Ошибка загрузки звуков: {e}")
            self.sounds_loaded = False
    
    def play_jump(self):
        if self.jump_sound and self.sounds_loaded:
            arcade.play_sound(self.jump_sound, volume=0.5)
    
    def play_death(self):
        if self.death_sound and self.sounds_loaded:
            arcade.play_sound(self.death_sound, volume=0.7)
    
    def is_loaded(self):
        return self.sounds_loaded