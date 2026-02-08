# table.py
import pygame
from config import *

class Table:
    def __init__(self):
        self.table_rect = pygame.Rect(100, 260, 600, 80)

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

        self.woman_rect = pygame.Rect(
            self.table_rect.centerx - 25,
            self.table_rect.bottom + 10,
            50,
            80
        )

        self.p1_dish_rect = pygame.Rect(
            self.table_rect.left + 120,
            self.table_rect.centery - 20,
            40, 40
        )

        self.p2_dish_rect = pygame.Rect(
            self.table_rect.right - 120,
            self.table_rect.centery - 20,
            40, 40
        )

    def draw(self, surface):
        pygame.draw.rect(surface, TABLE_COLOR, self.table_rect)
        pygame.draw.rect(surface, TRASH_COLOR, self.trash_left)
        pygame.draw.rect(surface, TRASH_COLOR, self.trash_right)
        pygame.draw.rect(surface, WOMAN_COLOR, self.woman_rect)
