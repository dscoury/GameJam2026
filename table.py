# table.py
import pygame
from config import *

class Table:
    def __init__(self):
        # --- table dimensions ---
        table_width = 600
        table_height = 80

        # --- table in lower third ---
        self.table_rect = pygame.Rect(
            (WIDTH - table_width) // 2,
            BOTTOM_THIRD,
            table_width,
            table_height
        )

        # --- trash bins (locked to table) ---
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

        # --- shared Y for characters (top of table) ---
        character_y = self.table_rect.top

        # --- woman (centered) ---
        self.woman_rect = pygame.Rect(0, 0, 50, 80)
        self.woman_rect.midbottom = (
            WIDTH // 2,
            character_y
        )

        # --- player positions (middle third) ---
        # --- food positions (ON the table) ---
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
        pygame.draw.rect(surface, TABLE_COLOR, self.table_rect)
        pygame.draw.rect(surface, TRASH_COLOR, self.trash_left)
        pygame.draw.rect(surface, TRASH_COLOR, self.trash_right)
        pygame.draw.rect(surface, WOMAN_COLOR, self.woman_rect)
