import pygame
import random
import sys
import math
from player import Player
from cutscene import CutsceneController
from config import *
from assets import Assets
from table import Table

# SETUP

pygame.init()
pygame.mixer.init()

BASE_SURFACE = pygame.Surface((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sumo Growth DDR")
clock = pygame.time.Clock()
assets = Assets()
table = Table()

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

timer = GAME_LENGTH
state = "PLAYING"

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
    BASE_SURFACE.fill((25, 25, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  

    keys = pygame.key.get_pressed()

    # PLAYING STATE

    if state == "PLAYING":

        if not p1.current_dish:
            p1.spawn_dish()

        if not p2.current_dish:
            p2.spawn_dish()

        p1.handle_input(keys)
        p2.handle_input(keys)
        
        timer -= 1
        if timer <= 0:
            state = "CUTSCENE"
            zoom = 1.0
            cutscene.start(p1, p2)

            if chant_sound:
                chant_sound.play(-1)

            # Move players to sumo starting positions
            p1.rect.center = (WIDTH // 2 - 80, HEIGHT // 2)
            p2.rect.center = (WIDTH // 2 + 80, HEIGHT // 2)

            if chant_sound:
                chant_sound.play(-1)

    # CUTSCENE

    elif state == "CUTSCENE":
        zoom = min(TARGET_ZOOM, zoom + 0.002)

        finished = cutscene.update(p1, p2)

        if finished:
            state = "RESULT"
            zoom = 1.0

            if chant_sound:
                chant_sound.stop()

    # CLAMP SIZE

    p1.clamp()
    p2.clamp()

    # DRAW WORLD

    if state == "PLAYING":
        table.draw(BASE_SURFACE)

        # PLAYER 1 AND 2 DISH
        p1.draw_dish(BASE_SURFACE, assets.food_images)
        p2.draw_dish(BASE_SURFACE, assets.food_images)


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

    rect = scaled.get_rect(center=(WIDTH // 2 + shake_x, HEIGHT // 2 + shake_y))
    screen.fill((0, 0, 0))
    screen.blit(scaled, rect)

    # LEGEND AND INFO
    
    legend_p1 = [
        "PLAYER 1 (RED) - WASD",
        "W : Eat good food",
        "A : Throw away bad food",
        "D : Give away spicy food"
    ]

    legend_p2 = [
        "PLAYER 2 (BLUE) - ARROWS",
        "UP    : Eat good food",
        "RIGHT : Throw away bad food",
        "LEFT  : Give away spicy food"
    ]

    for i, line in enumerate(legend_p1):
        screen.blit(
            assets.legend_font.render(line, True, (220, 100, 100)),
            (20, 20 + i * 22)
        )

    for i, line in enumerate(legend_p2):
        text = assets.legend_font.render(line, True, (100, 100, 220))
        screen.blit(
            text,
            (WIDTH - text.get_width() - 20, 20 + i * 22)
        )

    food_legend_y = 120
    screen.blit(assets.legend_font.render("FOOD TYPES:", True, (255, 255, 255)),
                (WIDTH // 2 - 60, food_legend_y))

    food_info = [
    ("Good food (Eat)", "good"),
    ("Bad food (Throw away)", "bad"),
    ("Spicy food (Give away)", "spicy")
]

    for i, (label, food_type) in enumerate(food_info):
        icon = assets.food_images[food_type]

        screen.blit(
            pygame.transform.scale(icon, (20, 20)),
            (WIDTH // 2 - 80, food_legend_y + 30 + i * 26)
        )

        screen.blit(
            assets.legend_font.render(label, True, (230, 230, 230)),
            (WIDTH // 2 - 50, food_legend_y + 28 + i * 26)
        )
        
    # SIZE TEXT

    screen.blit(assets.font.render(str(p1.size), True, (255, 255, 255)), (160, 520))
    screen.blit(assets.font.render(str(p2.size), True, (255, 255, 255)), (510, 520))

    # RESULT
    
    if state == "RESULT":
        winner = "DRAW"
        if p1.size > p2.size:
            winner = "PLAYER 1 WINS!"
        elif p2.size > p1.size:
            winner = "PLAYER 2 WINS!"

        text = assets.font.render(winner, True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20))

    pygame.display.flip()