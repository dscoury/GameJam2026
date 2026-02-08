# menu.py
import pygame
from config import WIDTH, HEIGHT

class Menu:
    def __init__(self, assets):
        self.assets = assets
        
        # Setup Button
        self.button_img = self.assets.menu_images["play_button"]
        self.button_rect = self.button_img.get_rect()
        self.button_rect.center = (WIDTH // 2, 450)

        self.is_hovered = False

    def handle_input(self, events, game_state):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.button_rect.collidepoint(mouse_pos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # LEFT CLICK
                    if self.is_hovered:
                        if game_state.state == "RESULT":
                            game_state.state = "MENU"
                        else:
                            game_state.state = "PLAYING"
                            game_state.reset() 

    def draw(self, surface):
        # Draw start screen
        surface.blit(self.assets.menu_images["background"], (0, 0))
        self.draw_button(surface)

    def draw_button(self, surface):
        # ONLY BUTTON FOR RESULTS
        surface.blit(self.button_img, self.button_rect)