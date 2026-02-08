# table.py
import pygame
from config import *

class Table:
    def __init__(self, image, woman_image):

        table_width = 600
        table_height = 80
        TABLETOP_OFFSET = 265

        self.table_rect = pygame.Rect(
            (WIDTH - table_width) // 2,
            BOTTOM_THIRD,
            table_width,
            table_height
        )

        self.trash_left = pygame.Rect(
            self.table_rect.left - 40,
            self.table_rect.top,
            30,
            self.table_rect.height
        )

        self.trash_right = pygame.Rect(
            self.table_rect.right + 10,
            self.table_rect.top,
            30,
            self.table_rect.height
        )
        
        visual_left = self.trash_left.left
        visual_right = self.trash_right.right
        visual_width = visual_right - visual_left

        scale = visual_width / image.get_width()
        img_w = int(image.get_width() * scale)
        img_h = int(image.get_height() * scale)

        self.image = pygame.transform.scale(image, (img_w, img_h))

        self.image_rect = self.image.get_rect()
        self.image_rect.midtop = self.table_rect.midtop
        self.image_rect.y -= TABLETOP_OFFSET 

        # UPDATE WOMAN SETUP
        self.woman_image = woman_image
        self.woman_rect = self.woman_image.get_rect()

        character_y = self.table_rect.top

        self.woman_rect.midbottom = (
            WIDTH // 2,
            character_y + 10
        )

        food_y = self.table_rect.top + 10  # padding on table surface

        self.p1_dish_rect = pygame.Rect(0, 0, 40, 40)
        self.p1_dish_rect.midtop = (
            self.table_rect.left + 140,
            food_y
        )

        self.p2_dish_rect = pygame.Rect(0, 0, 40, 40)
        self.p2_dish_rect.midtop = (
            self.table_rect.right - 140,
            food_y
        )

    def draw(self, surface):
        surface.blit(self.image, self.image_rect)
        surface.blit(self.woman_image, self.woman_rect)