# hud.py
import pygame

class HUD:
    def __init__(self, assets, width):
        self.assets = assets
        self.width = width

    def draw_playing(self, screen, p1, p2):
        lf = self.assets.legend_font
        f = self.assets.font

        """legend_p1 = [
            "PLAYER 1 (LEFT) - WASD",
            "W : Eat good food",
            "A : Throw away bad food",
            "D : Give away spicy food"
        ]

        legend_p2 = [
            "PLAYER 2 (RIGHT) - ARROWS",
            "UP    : Eat good food",
            "RIGHT : Throw away bad food",
            "LEFT  : Give away spicy food"
        ]

        for i, line in enumerate(legend_p1):
            screen.blit(lf.render(line, True, (220, 100, 100)), (20, 20 + i * 22))

        for i, line in enumerate(legend_p2):
            text = lf.render(line, True, (100, 100, 220))
            screen.blit(text, (self.width - text.get_width() - 20, 20 + i * 22))

        screen.blit(f.render(str(p1.size), True, (255, 255, 255)), (160, 520))
        screen.blit(f.render(str(p2.size), True, (255, 255, 255)), (510, 520)

        )"""

    def draw_result(self, screen, winner):
        f = self.assets.font
        text = f.render(winner, True, (255, 255, 255))
        screen.blit(
            text,
            (self.width // 2 - text.get_width() // 2, 200)
        )

    def draw_food_legend(self, screen):
        lf = self.assets.legend_font

        food_legend_y = 120

        """screen.blit(
            lf.render("FOOD TYPES:", True, (255, 255, 255)),
            (self.width // 2 - 60, food_legend_y)
        )

        food_info = [
            ("Good food (Eat)", "good"),
            ("Bad food (Throw away)", "bad"),
            ("Spicy food (Give away)", "spicy"),
        ]

        for i, (label, food_type) in enumerate(food_info):
            icon = self.assets.food_images[food_type]

            screen.blit(
                pygame.transform.scale(icon, (20, 20)),
                (self.width // 2 - 80, food_legend_y + 30 + i * 26)
            )

            screen.blit(
                lf.render(label, True, (0, 0, 0)),
                (self.width // 2 - 50, food_legend_y + 28 + i * 26)
            )"""

