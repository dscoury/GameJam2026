# cutscene.py
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

        # --- PHASE 1: WARMUP (Jitter in place) ---
        if self.phase == "warmup":
            # Create a small jitter (-2 to +2)
            jitter = 2 if (self.timer // 5) % 2 == 0 else -2
            
            # P1 stays on LEFT side of center, P2 on RIGHT
            # They bump at the center line (center_x)
            p1.rect.right = center_x + jitter
            p2.rect.left = center_x - jitter 

            if self.timer >= 120:
                self.phase = "final"

        # --- PHASE 2: THE PUSH (One leaves, one stays) ---
        elif self.phase == "final":
            # Calculate push speed based on size difference
            size_diff = abs(p1.size - p2.size)
            force = 5 + size_diff // 10 # Increase base speed so it feels punchy!

            # CASE A: PLAYER 1 WINS (Push Right)
            if p1.size > p2.size:
                p2.rect.x += force # Loser flies right
                
                # Winner follows ONLY if they are still on screen (Stop at 80% width)
                if p1.rect.right < self.width * 0.8:
                     p1.rect.right = p2.rect.left # Maintain contact
                # Else: Winner stops, P2 detaches and leaves

            # CASE B: PLAYER 2 WINS (Push Left)
            elif p2.size > p1.size:
                p1.rect.x -= force # Loser flies left
                
                # Winner follows ONLY if they are still on screen (Stop at 20% width)
                if p2.rect.left > self.width * 0.2:
                    p2.rect.left = p1.rect.right # Maintain contact
                # Else: Winner stops, P1 detaches and leaves

            # CASE C: DRAW (Both fly back)
            else:
                p1.rect.x -= 5
                p2.rect.x += 5

        # End condition: When the loser is totally off screen
        if p1.rect.right < -50 or p2.rect.left > self.width + 50:
            self.active = False
            return True  # Cutscene finished

        return False