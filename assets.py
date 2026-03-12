import os
import pygame
from config import WIDTH, HEIGHT

class Assets:
    def __init__(self):
        base_path = os.path.dirname(__file__)
        char_path = os.path.join(base_path, "Character_Images")

        # SCREEN IMAGES
        self.menu_images = {
            "background": pygame.image.load(
                os.path.join(base_path, "PixelArt_GameJam/startScreen.png")
            ).convert(),
            "play_button": pygame.image.load(
                os.path.join(base_path, "PixelArt_GameJam/startscreenPlaybutton.png")
            ).convert_alpha()
        }

        self.menu_images["background"] = pygame.transform.scale(
            self.menu_images["background"], (WIDTH, HEIGHT)
        )

        button = self.menu_images["play_button"]

        self.menu_images["play_button"] = pygame.transform.scale(
            self.menu_images["play_button"], (WIDTH, HEIGHT)
        )

        self.outside_image = pygame.image.load(
            os.path.join(base_path, "PixelArt_GameJam/backgroundOutside.png")
        ).convert()

        self.outside_image = pygame.transform.scale(
            self.outside_image, (WIDTH, HEIGHT)
        )

        # FOOD IMAGES

        self.food_images = {
            "good": pygame.image.load("Food_Images/Vanlig.png").convert_alpha(),
            "bad": pygame.image.load("Food_Images/Rotten_0003.png").convert_alpha(),
            "spicy": pygame.image.load("Food_Images/Spicy.png").convert_alpha()
        }

        # Resize food
        for key in self.food_images:
            self.food_images[key] = pygame.transform.scale(
                self.food_images[key], (70, 70)
            )


        # PLAYER REACTIONS

        self.player_images = {
            "p1": pygame.image.load(
                os.path.join(base_path, "PixelArt_GameJam/Player_Sprites/sumo1-haar.png")
            ).convert_alpha(),
            "p2": pygame.image.load(
                os.path.join(base_path, "PixelArt_GameJam/Player_Sprites/sumo2-8_0001.png")
            ).convert_alpha(),
        }

        self.result_images = {
            "P1": pygame.image.load("PixelArt_GameJam/winnerOne.png").convert(),
            "P2": pygame.image.load("PixelArt_GameJam/winnerTwo.png").convert(),
            "DRAW": pygame.image.load("PixelArt_GameJam/drawScreen.png").convert()
        }
        for key in self.result_images:
            self.result_images[key] = pygame.transform.scale(
                self.result_images[key], (WIDTH, HEIGHT)
            )

        self.p1_reactions = {
            "good": pygame.image.load(os.path.join(char_path, "sumo1_good.png")).convert_alpha(),
            "bad":  pygame.image.load(os.path.join(char_path, "sumo1_sick.png")).convert_alpha(),
            "spicy": pygame.image.load(os.path.join(char_path, "sumo1_spicy.png")).convert_alpha(),
        }

        self.p2_reactions = {
            "good": pygame.image.load(os.path.join(char_path, "sumo2_good.png")).convert_alpha(),
            "bad":  pygame.image.load(os.path.join(char_path, "sumo2_sick.png")).convert_alpha(),
            "spicy": pygame.image.load(os.path.join(char_path, "sumo2_spicy.png")).convert_alpha(),
        }
        
        
        # WOMAN REACTIONS

        self.woman_image = pygame.image.load(
            os.path.join(base_path, "Character_Images/chillLady.gif")
        ).convert_alpha()

        scale_factor = 3
        w = self.woman_image.get_width() * scale_factor
        h = self.woman_image.get_height() * scale_factor
        self.woman_image = pygame.transform.scale(self.woman_image, (w, h))
         

        self.woman_animations = {
            "happy": [],
            "angry": []
        }

        woman_anim_path = os.path.join(base_path, "Character_Images")

        # happy
        happy_path = os.path.join(woman_anim_path, "ladyHappy")

        for file in sorted(os.listdir(happy_path)):
            if file.endswith(".png"):
                img = pygame.image.load(
                    os.path.join(happy_path, file)
                ).convert_alpha()
                self.woman_animations["happy"].append(img)


        # angry
        angry_path = os.path.join(woman_anim_path, "ladyMad")

        for file in sorted(os.listdir(angry_path)):
            if file.endswith(".png"):
                img = pygame.image.load(
                    os.path.join(angry_path, file)
                ).convert_alpha()
                self.woman_animations["angry"].append(img)


        # TABLE PICTURE
        self.table_image = pygame.image.load(
            os.path.join(base_path, "PixelArt_GameJam/tableRestaurant.png")
        ).convert_alpha()

        self.fulltrashL = pygame.image.load(
            os.path.join(base_path, "PixelArt_GameJam/leftTrashFull.png")
        ).convert_alpha()
        self.fulltrashR = pygame.image.load(
            os.path.join(base_path, "PixelArt_GameJam/rightTrashFull.png")
        ).convert_alpha()


        

        self.font = pygame.font.SysFont(None, 48)
        self.legend_font = pygame.font.SysFont(None, 24)