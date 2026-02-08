from config import HEIGHT, WIDTH

class CutsceneController:
    def __init__(self, width):
        self.width = width
        self.timer = 0
        self.phase = "warmup"
        self.active = False

    def start(self, p1, p2, table):
        self.timer = 0
        self.phase = "warmup"
        self.active = True

        center_x = self.width // 2
        floor_y = HEIGHT - 120

        # Start perfectly touching in the center
        p1.rect.midright = (center_x, floor_y)
        p2.rect.midleft = (center_x, floor_y)

    def update(self, p1, p2):
        self.timer += 1
        center_x = self.width // 2

        if self.phase == "warmup":

            jitter = 2 if (self.timer // 5) % 2 == 0 else -2
            
            p1.rect.right = center_x + jitter
            p2.rect.left = center_x - jitter 

            if self.timer >= 120:
                self.phase = "final"

        elif self.phase == "final":

            size_diff = abs(p1.size - p2.size)
            force = 5 + size_diff // 10

            if p1.size > p2.size:
                p2.rect.x += force 
                
                if p1.rect.right < self.width * 0.8:
                     p1.rect.right = p2.rect.left # Maintain contact

            elif p2.size > p1.size:
                p1.rect.x -= force # Loser flies left
                
                if p2.rect.left > self.width * 0.2:
                    p2.rect.left = p1.rect.right # Maintain contact

            else:
                p1.rect.x -= 5
                p2.rect.x += 5

        if p1.rect.right < -50 or p2.rect.left > self.width + 50:
            self.active = False
            return True 
        return False