import pygame
import random
import sys
import math
from player import Player
from cutscene import CutsceneController
from config import *
from assets import Assets
from table import Table
from hud import HUD
from game_state import GameState

# SETUP

pygame.init()
pygame.mixer.init()

BASE_SURFACE = pygame.Surface((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load(
    "PixelArt_GameJam/backgroundRestaurant.png"
).convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
pygame.display.set_caption("Ramen Rumble")
clock = pygame.time.Clock()
assets = Assets()
table = Table()
hud = HUD(assets, WIDTH)
game_state = GameState()

# CONSTANTS

CUTSCENE_WARMUP_FRAMES = 120
BASE_PUSH_FORCE = 2

TIMING_Y = 420
TIMING_HEIGHT = 24

LANES = {
    1: 200, # Player 1 lane (WASD)
    2: 550, # Player 2 lane (Piltaster)
}

# ZOOM
zoom = 1.0
cutscene = CutsceneController(WIDTH)

# PLAYER 1 AND 2

p1 = Player(
    color = (200, 80, 80),
    controls = {
        "good": pygame.K_w,
        "bad": pygame.K_a,
        "spicy": pygame.K_d
    },
    dish_rect = table.p1_dish_rect
)

p2 = Player(
    color = (80, 80, 220),
    controls = {
        "good": pygame.K_UP,
        "bad": pygame.K_RIGHT,
        "spicy": pygame.K_LEFT
    },
    dish_rect = table.p2_dish_rect
)

p1.rect.center = (WIDTH // 2 - 150, HEIGHT - 120)
p2.rect.center = (WIDTH // 2 + 150, HEIGHT - 120)


# Optional: scale them to 30x30 to match your old rectangle size
for key in assets.food_images:
    assets.food_images[key] = pygame.transform.scale(assets.food_images[key], (70, 70))

MISS_PENALTY = {
    "good": 4,
    "bad": 2,
    "spicy": 1
}

# GAME STATE

cutscene_timer = 0
push_phase = "warmup"

# SCREEN SHAKE
shake_intensity = 0
shake_timer = 0

# ZOOM
zoom = 1.0
TARGET_ZOOM = 1.15

chant_sound = None 

# GAME LOOP

while True:
    clock.tick(FPS)
    BASE_SURFACE.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  

    keys = pygame.key.get_pressed()

    # PLAYING STATE

    if game_state.state == "PLAYING":

        if not p1.current_dish:
            p1.spawn_dish()

        if not p2.current_dish:
            p2.spawn_dish()

        # Pass 'table' into handle_input
        p1.handle_input(keys, table)
        p2.handle_input(keys, table)

        # Update the sliding animation
        p1.update_animation()
        p2.update_animation()

        result = game_state.update()

        if result == "CUTSCENE":
            zoom = 1.0
            cutscene.start(p1, p2, table)


            if chant_sound:
                chant_sound.play(-1)

            if chant_sound:
                chant_sound.play(-1)

    # CUTSCENE

    elif game_state.state == "CUTSCENE":
        zoom = min(TARGET_ZOOM, zoom + 0.002)

        finished = cutscene.update(p1, p2)

        if finished:
            game_state.state = "RESULT"
            zoom = 1.0

            if chant_sound:
                chant_sound.stop()

    # CLAMP SIZE

    p1.clamp()
    p2.clamp()

    # DRAW WORLD

    if game_state.state in ("PLAYING", "CUTSCENE"):

        # PLAYER 1 AND 2 DISH
        if game_state.state == "PLAYING":
            table.draw(BASE_SURFACE)
            p1.draw_dish(BASE_SURFACE, assets.food_images)
            p2.draw_dish(BASE_SURFACE, assets.food_images)

            # Keep players aligned with table during PLAYING
            character_y = table.table_rect.top

            # Align players to the TOP edge of the table, same as the woman
            character_y = table.table_rect.top

            p1.rect.midbottom = (p1.rect.centerx, character_y)
            p2.rect.midbottom = (p2.rect.centerx, character_y)

            


    
    p1.draw(BASE_SURFACE)
    p2.draw(BASE_SURFACE)

    # SHAKE AND ZOOM
    
    shake_x = shake_y = 0
    if shake_timer > 0:
        shake_timer -= 1
        shake_x = random.randint(-shake_intensity, shake_intensity)
        shake_y = random.randint(-shake_intensity, shake_intensity)

    scaled = pygame.transform.scale(
        BASE_SURFACE,
        (int(WIDTH * zoom), int(HEIGHT * zoom))
    )

    rect = scaled.get_rect(center = (WIDTH // 2 + shake_x, HEIGHT // 2 + shake_y))
    screen.blit(scaled, rect)

    # HUD
    if game_state.state == "PLAYING":
        hud.draw_playing(screen, p1, p2)
        hud.draw_food_legend(screen)

    elif game_state.state == "RESULT":
        winner = "DRAW"
        if p1.size > p2.size:
            winner = "PLAYER 1 WINS!"
        elif p2.size > p1.size:
            winner = "PLAYER 2 WINS!"

        hud.draw_result(screen, winner)

    pygame.display.flip()