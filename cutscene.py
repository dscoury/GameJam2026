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

        player_y = table.woman_rect.centery

        p1.rect.midright = (
            table.woman_rect.left - 20,
            player_y
        )

        p2.rect.midleft = (
            table.woman_rect.right + 20,
            player_y
        )


    def update(self, p1, p2):
        self.timer += 1

        # Warmup shake
        if self.phase == "warmup":
            offset = 3 if (self.timer // 10) % 2 == 0 else -3
            p1.rect.x += offset
            p2.rect.x -= offset

            if self.timer >= 120:
                self.phase = "final"

        # Final push
        elif self.phase == "final":
            size_diff = abs(p1.size - p2.size)
            force = 2 + size_diff // 10

            if p1.size > p2.size:
                p2.rect.x += force
            elif p2.size > p1.size:
                p1.rect.x -= force
            else:
                p1.rect.x -= 2
                p2.rect.x += 2

        # End condition
        if p1.rect.right < 0 or p2.rect.left > self.width:
            self.active = False
            return True  # Cutscene finished

        return False
