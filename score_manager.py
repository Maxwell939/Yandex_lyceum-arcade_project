import os
import sys


class ScoreManager:
    def __init__(self):
        self.current_score = 0
        self.high_score = 0

        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        self.records_dir = os.path.join(base_path, "records")
        self.score_file = os.path.join(self.records_dir, "highscore.txt")
        self.load_high_score()
    
    def load_high_score(self):
        if not os.path.exists(self.records_dir):
            os.makedirs(self.records_dir, exist_ok=True)
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as f:
                    content = f.read().strip()
                    if content.isdigit():
                        self.high_score = int(content)
            except:
                self.high_score = 0
        else:
            self.high_score = 0
            with open(self.score_file, 'w') as f:
                f.write("0")
    
    def save_high_score(self):
        with open(self.score_file, 'w') as f:
            f.write(str(self.high_score))
    
    def update_score(self, new_score):
        if new_score > self.current_score:
            self.current_score = new_score
            if self.current_score > self.high_score:
                self.high_score = self.current_score
                self.save_high_score()
    
    def reset(self):
        self.current_score = 0