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
from menu import Menu
import asyncio


# Two players compete in eating the right food to grow and win

# SETUP
pygame.init() 
# pygame.mixer.init() 

# screen setup 
BASE_SURFACE = pygame.Surface((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load(
    "PixelArt_GameJam/backgroundRestaurant.png"
).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
pygame.display.set_caption("Ramen Rumble")
clock = pygame.time.Clock()
assets = Assets()
table = Table(assets.table_image, assets.woman_image)
hud = HUD(assets, WIDTH)
game_state = GameState()
menu = Menu(assets)

# CONSTANTS
CUTSCENE_WARMUP_FRAMES = 120
BASE_PUSH_FORCE = 2

TIMING_Y = 420
TIMING_HEIGHT = 24

LANES = {
    1: 200, 
    2: 550, 
}

# ZOOM
zoom = 1.0
cutscene = CutsceneController(WIDTH)

# MAKING PLAYER 1 AND 2
p1 = Player(
    color = (200, 80, 80),
    controls = {
        "good": pygame.K_w,
        "bad": pygame.K_a,
        "spicy": pygame.K_d
    },
    dish_rect = table.p1_dish_rect,
    image = assets.player_images["p1"],
    reaction_images = assets.p1_reactions 
)

p2 = Player(
    color = (80, 80, 220),
    controls = {
        "good": pygame.K_UP,
        "bad": pygame.K_RIGHT,
        "spicy": pygame.K_LEFT
    },
    dish_rect = table.p2_dish_rect,
    image = assets.player_images["p2"],
    reaction_images = assets.p2_reactions 
)

p1.rect.center = (WIDTH // 2 - 150, HEIGHT - 120)
p2.rect.center = (WIDTH // 2 + 150, HEIGHT - 120)

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
previous_state = game_state.state



# GAME LOOP
# main.py
async def main():
    global shake_timer, shake_intensity, previous_state, zoom, cutscene_timer, push_phase


    while True:
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
        keys = pygame.key.get_pressed()

        # MENU STATE
        if game_state.state == "MENU":
            menu.handle_input(events, game_state)
            menu.draw(BASE_SURFACE)

        # PLAYING STATE
        elif game_state.state == "PLAYING":
            BASE_SURFACE.blit(background, (0, 0))

            table.draw(BASE_SURFACE)

            if not p1.current_dish and p1.stun_timer == 0:
                p1.spawn_dish()

            if not p2.current_dish and p2.stun_timer == 0:
                p2.spawn_dish()

            p1.handle_input(keys, table)
            p2.handle_input(keys, table)

            # Update timers
            p1.update() 
            p2.update() 

            p1.update_animation()
            p2.update_animation()

            result = game_state.update()
            if result == "CUTSCENE":
                zoom = 1.0
                cutscene.start(p1, p2, table)
                if chant_sound: chant_sound.play(-1)

        # CUTSCENE STATE
        elif game_state.state == "CUTSCENE":
            BASE_SURFACE.blit(assets.outside_image, (0, 0)) 

            zoom = min(TARGET_ZOOM, zoom + 0.002)
            finished = cutscene.update(p1, p2)

            if finished:
                game_state.state = "RESULT"
                zoom = 1.0
                if chant_sound: chant_sound.stop()

        # RESULT STATE
        elif game_state.state == "RESULT":

            if p1.size > p2.size:
                result_key = "P1"
            elif p2.size > p1.size:
                result_key = "P2"
            else:
                result_key = "DRAW"

            BASE_SURFACE.blit(assets.result_images[result_key], (0, 0))

            menu.draw_button(BASE_SURFACE)


            # hanlding input
            menu.handle_input(events, game_state)

            if game_state.state == "PLAYING":

                # Reset players
                p1.reset((WIDTH // 2 - 150, HEIGHT - 120))
                p2.reset((WIDTH // 2 + 150, HEIGHT - 120))

                # Reset scene
                zoom = 1.0
                cutscene_timer = 0
                push_phase = "warmup"


        # CLAMP & DRAW CHARACTERS 
        p1.clamp()
        p2.clamp()

        if game_state.state in ("PLAYING", "CUTSCENE"):
            

            if game_state.state == "PLAYING":
                p1.draw_dish(BASE_SURFACE, assets.food_images)
                p2.draw_dish(BASE_SURFACE, assets.food_images)
                
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

        if zoom == 1.0:
            screen.blit(BASE_SURFACE, (0,0))
        else:
            scaled = pygame.transform.scale(
                BASE_SURFACE, (int(WIDTH * zoom), int(HEIGHT * zoom))
            )
            rect = scaled.get_rect(center=(WIDTH//2 + shake_x, HEIGHT//2 + shake_y))
            screen.blit(scaled, rect)


        # Detect state change to PLAYING
        if game_state.state == "PLAYING" and previous_state != "PLAYING":
            p1.reset((WIDTH // 2 - 150, HEIGHT - 120))
            p2.reset((WIDTH // 2 + 150, HEIGHT - 120))

            zoom = 1.0
            cutscene_timer = 0
            push_phase = "warmup"

        previous_state = game_state.state


        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())

