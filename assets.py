# assets.py
import pygame

class Assets:
    def __init__(self):
        self.food_images = {
            "good": pygame.image.load("Food_Images/Vanlig.png").convert_alpha(),
            "bad": pygame.image.load("Food_Images/Rotten_0003.png").convert_alpha(),
            "spicy": pygame.image.load("Food_Images/Spicy.png").convert_alpha()
        }

        for key in self.food_images:
            self.food_images[key] = pygame.transform.scale(
                self.food_images[key], (70, 70)
            )

        self.font = pygame.font.SysFont(None, 48)
        self.legend_font = pygame.font.SysFont(None, 24)
