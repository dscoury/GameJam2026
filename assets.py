# assets.py
import os
import pygame
from config import WIDTH, HEIGHT

class Assets:
    def __init__(self):
        base_path = os.path.dirname(__file__)

        self.menu_images = {
            "background": pygame.image.load(
                os.path.join(base_path,"PixelArt_GameJam/startScreen.png")
            ).convert_alpha(),
            "play_button": pygame.image.load(
                os.path.join(base_path,"PixelArt_GameJam/startscreenPlaybutton.png")
            ).convert_alpha()
        }

        self.menu_images["background"] = pygame.transform.scale(
            self.menu_images["background"], (WIDTH, HEIGHT)
        )

        button = self.menu_images["play_button"]
        self.menu_images["play_button"] = pygame.transform.scale(
            button, (button.get_width() * 2, button.get_height() * 2)
        )

        self.food_images = {
            "good": pygame.image.load("Food_Images/Vanlig.png").convert_alpha(),
            "bad": pygame.image.load("Food_Images/Rotten_0003.png").convert_alpha(),
            "spicy": pygame.image.load("Food_Images/Spicy.png").convert_alpha()
        }

        self.player_images = {
            "p1": pygame.image.load(
                os.path.join(base_path,"PixelArt_GameJam/Player_Sprites/sumo1-haar.png")
                ).convert_alpha(),

            "p2": pygame.image.load(
                os.path.join(base_path,"PixelArt_GameJam/Player_Sprites/sumo2-8_0001.png")
                ).convert_alpha(),
        }
        
        self.table_image = pygame.image.load(
            os.path.join(base_path,"PixelArt_GameJam/tableRestaurant.png")
        ).convert_alpha()

        for key in self.food_images:
            self.food_images[key] = pygame.transform.scale(
                self.food_images[key], (70, 70)
            )

        self.font = pygame.font.SysFont(None, 48)
        self.legend_font = pygame.font.SysFont(None, 24)
