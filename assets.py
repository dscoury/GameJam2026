import os
import pygame
from config import WIDTH, HEIGHT

class Assets:
    def __init__(self):
        base_path = os.path.dirname(__file__)
        char_path = os.path.join(base_path, "Character_Images")

        # --- MENU IMAGES ---
        self.menu_images = {
            "background": pygame.image.load(
                os.path.join(base_path, "PixelArt_GameJam/startScreen.png")
            ).convert_alpha(),
            "play_button": pygame.image.load(
                os.path.join(base_path, "PixelArt_GameJam/startscreenPlaybutton.png")
            ).convert_alpha()
        }

        self.menu_images["background"] = pygame.transform.scale(
            self.menu_images["background"], (WIDTH, HEIGHT)
        )

        button = self.menu_images["play_button"]
        self.menu_images["play_button"] = pygame.transform.scale(
            button, (button.get_width() * 2, button.get_height() * 2)
        )

        # --- GAME IMAGES ---
        self.woman_image = pygame.image.load(
            os.path.join(base_path, "GIFS/chillLady.gif")
        ).convert_alpha()

        scale_factor = 3
        w = self.woman_image.get_width() * scale_factor
        h = self.woman_image.get_height() * scale_factor
        self.woman_image = pygame.transform.scale(self.woman_image, (w, h))

        self.food_images = {
            "good": pygame.image.load("Food_Images/Vanlig.png").convert_alpha(),
            "bad": pygame.image.load("Food_Images/Rotten_0003.png").convert_alpha(),
            "spicy": pygame.image.load("Food_Images/Spicy.png").convert_alpha()
        }

        self.player_images = {
            "p1": pygame.image.load(
                os.path.join(base_path, "PixelArt_GameJam/Player_Sprites/sumo1-haar.png")
            ).convert_alpha(),
            "p2": pygame.image.load(
                os.path.join(base_path, "PixelArt_GameJam/Player_Sprites/sumo2-8_0001.png")
            ).convert_alpha(),
        }

        # --- NEW REACTION IMAGES ---
        # Note: Ensure these files exist in the Character_Images folder
        self.p1_reactions = {
            "good": pygame.image.load(os.path.join(char_path, "sumo1_good.png")).convert_alpha(),
            "bad":  pygame.image.load(os.path.join(char_path, "sumo1_sick.png")).convert_alpha(),
            "spic": pygame.image.load(os.path.join(char_path, "sumo1_spicy.png")).convert_alpha(),
        }

        self.p2_reactions = {
            "good": pygame.image.load(os.path.join(char_path, "sumo2_good.png")).convert_alpha(),
            "bad":  pygame.image.load(os.path.join(char_path, "sumo2_sick.png")).convert_alpha(),
            "spic": pygame.image.load(os.path.join(char_path, "sumo2_spicy.png")).convert_alpha(),
        }
        
        self.table_image = pygame.image.load(
            os.path.join(base_path, "PixelArt_GameJam/tableRestaurant.png")
        ).convert_alpha()

        # Resize food
        for key in self.food_images:
            self.food_images[key] = pygame.transform.scale(
                self.food_images[key], (70, 70)
            )

        self.font = pygame.font.SysFont(None, 48)
        self.legend_font = pygame.font.SysFont(None, 24)