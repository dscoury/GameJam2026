import pygame
import random

class Player:
    def __init__(self, color, controls, dish_rect, start_size = 50):
        self.color = color
        self.controls = controls
        self.size = start_size
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.dish_rect = dish_rect
        self.current_dish = None

    def spawn_dish(self):
        self.current_dish = random.choice(["good", "bad", "spicy"])

    def handle_input(self, keys):
        if not self.current_dish:
            return

        dish = self.current_dish

        if dish == "good" and keys[self.controls["good"]]:
            self.size += 5
            self.current_dish = None

        elif dish == "bad" and keys[self.controls["bad"]]:
            self.current_dish = None

        elif dish == "spicy" and keys[self.controls["spicy"]]:
            self.current_dish = None

    def clamp(self):
        self.size = max(30, self.size)
        center = self.rect.center
        self.rect.size = (self.size, self.size)
        self.rect.center = center

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def draw_dish(self, surface, food_images):
        if not self.current_dish:
            return

        img = food_images[self.current_dish]
        surface.blit(
            img,
            (
                self.dish_rect.centerx - img.get_width() // 2,
                self.dish_rect.centery - img.get_height() // 2
            )
        )
