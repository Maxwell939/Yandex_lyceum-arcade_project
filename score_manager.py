import os

class ScoreManager:
    def __init__(self):
        self.current_score = 0
        self.high_score = 0
        self.score_file = "records/highscore.txt"
        self.load_high_score()
    
    def load_high_score(self):
        if not os.path.exists("records"):
            os.makedirs("records", exist_ok=True)
        
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
        try:
            with open(self.score_file, 'w') as f:
                f.write(str(self.high_score))
        except:
            print("Не удалось сохранить рекорд")
    
    def update_score(self, new_score):
        if new_score > self.current_score:
            self.current_score = new_score
            if self.current_score > self.high_score:
                self.high_score = self.current_score
                self.save_high_score()
    
    def reset(self):
        self.current_score = 0