import pygame
import random
import sys
import math

# SETUP

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
BASE_SURFACE = pygame.Surface((WIDTH, HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sumo Growth DDR")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)
legend_font = pygame.font.SysFont(None, 24)

# CONSTANTS

FPS = 60
GAME_LENGTH = 20 * FPS # 10 sekunder

TIMING_Y = 420
TIMING_HEIGHT = 24

LANES = {
    1: 200, # Player 1 lane (WASD)
    2: 550, # Player 2 lane (Piltaster)
}

# TABLE LAYOUT
TABLE_RECT = pygame.Rect(100, 260, 600, 80)

TRASH_LEFT_RECT = pygame.Rect(
    TABLE_RECT.left - 40, TABLE_RECT.top, 30, TABLE_RECT.height)

TRASH_RIGHT_RECT = pygame.Rect(
    TABLE_RECT.right + 10, TABLE_RECT.top, 30, TABLE_RECT.height)

WOMAN_RECT = pygame.Rect(
    TABLE_RECT.centerx - 25, TABLE_RECT.bottom + 10, 50, 80)

P1_DISH_RECT = pygame.Rect(
    TABLE_RECT.left + 120,
    TABLE_RECT.centery - 20,
    40, 40
)

P2_DISH_RECT = pygame.Rect(
    TABLE_RECT.right - 120,
    TABLE_RECT.centery - 20,
    40, 40
)

FOOD_COLORS = {
    "good": (80, 220, 120),     # green
    "bad": (220, 80, 80),       # red
    "spicy": (200, 200, 200)      # gray
}

MISS_PENALTY = {
    "good": 4,
    "bad": 2,
    "spicy": 1
}

# PLAYER DATA

p1_size = 50
p2_size = 50

p1_rect = pygame.Rect(0, 0, 50, 50)
p2_rect = pygame.Rect(0, 0, 50, 50)

# GAME STATE

timer = GAME_LENGTH
state = "PLAYING"

cutscene_timer = 0
push_phase = "warmup"

# DISHES SPAWNING

p1_dish = None
p2_dish = None

def spawn_dish():
    return random.choice(["good", "bad", "spicy"])

# SCREEN SHAKE
shake_intensity = 0
shake_timer = 0

# ZOOM
zoom = 1.0
TARGET_ZOOM = 1.15

# SOUND CHANT

"""def generate_chant():
    sound = pygame.sndarray.make_sound(
        (pygame.surfarray.array2d(
            pygame.Surface((200, 1))
        ) % 255).astype('int16')
    )
    return sound

try:
    chant_sound = generate_chant()

except:
    chant_sound = None"""

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
        if p1_dish is None:
            p1_dish = spawn_dish()

        if p2_dish is None:
            p2_dish = spawn_dish()

        # PLAYER 1 (left)
        if p1_dish is not None:

            if p1_dish == "good" and keys[pygame.K_w]:
                p1_size += 5
                p1_dish = None

            elif p1_dish == "bad" and keys[pygame.K_a]:
                # TRASH (left)
                p1_dish = None

            elif p1_dish == "spicy" and keys[pygame.K_d]:
                # WOMAN (towards center)
                p1_dish = None
            
        # PLAYER 2 (right)

        if p2_dish is not None:

            if p2_dish == "good" and keys[pygame.K_UP]:
                p2_size += 5
                p2_dish = None

            elif p2_dish == "bad" and keys[pygame.K_RIGHT]:
                # TRASH (right)
                p2_dish = None

            elif p2_dish == "spicy" and keys[pygame.K_LEFT]:
                # WOMAN (towards center)
                p2_dish = None

        timer -= 1
        if timer <= 0:
            state = "CUTSCENE"
            foods.clear()

            p1_rect.center = (WIDTH // 2 - 90, HEIGHT // 2)
            p2_rect.center = (WIDTH // 2 + 90, HEIGHT // 2)

            cutscene_timer = 0
            push_phase = "warmup"

            if chant_sound:
                chant_sound.play(-1)

        if timer % (10 * FPS) == 0:
            food_speed += 0.5
            spawn_delay = max(25, spawn_delay - 5)

    # CUTSCENE

    elif state == "CUTSCENE":
        cutscene_timer += 1
        zoom = min(TARGET_ZOOM, zoom + 0.002)

        if push_phase == "warmup":
            offset = 4 if (cutscene_timer // 15) % 2 == 0 else -4
            p1_rect.x += offset
            p2_rect.x -= offset

            if cutscene_timer > 120:
                push_phase = "final"
                shake_timer = 30
                shake_intensity = 10

        else:
            force = max(2, abs(p1_size - p2_size) // 10)
            if p1_size > p2_size:
                # PLAYER 1 pushes PLAYER 2 to the RIGHT
                p2_rect.x += force
            else:
                # PLAYER 2 pushes PLAYER 1 to the LEFT
                p1_rect.x -= force

        if p1_rect.right < 0 or p2_rect.left > WIDTH:
            state = "RESULT"
            if chant_sound:
                chant_sound.stop()
    
    # CLAMP SIZE

    p1_size = max(30, p1_size)
    p2_size = max(30, p2_size)

    p1_rect.size = (p1_size, p1_size)
    p2_rect.size = (p2_size, p2_size)

    # DRAW WORLD

    if state == "PLAYING":
        
        # TABLE
        pygame.draw.rect(BASE_SURFACE, (180, 150, 90), TABLE_RECT)

        # TRASH CANS
        pygame.draw.rect(BASE_SURFACE, (120, 120, 120), TRASH_LEFT_RECT)
        pygame.draw.rect(BASE_SURFACE, (120, 120, 120), TRASH_RIGHT_RECT)

        # WOMAN (PLACEHOLDER)
        pygame.draw.rect(BASE_SURFACE, (200, 120, 200), WOMAN_RECT)

        # PLAYER 1 DISH
        if p1_dish:
            pygame.draw.rect(
                BASE_SURFACE,
                FOOD_COLORS[p1_dish],
                P1_DISH_RECT
            )

        # PLAYER 2 DISH
        if p2_dish:
            pygame.draw.rect(
                BASE_SURFACE,
                FOOD_COLORS[p2_dish],
                P2_DISH_RECT
            )

    pygame.draw.rect(BASE_SURFACE, (200, 80, 80), p1_rect)
    pygame.draw.rect(BASE_SURFACE, (80, 80, 220), p2_rect)

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
        "D : Pass junk food",
        "A : Reject spicy food"
    ]

    legend_p2 = [
        "PLAYER 2 (BLUE) - ARROWS",
        "UP    : Eat good food",
        "RIGHT : Pass junk food",
        "LEFT  : Reject spicy food"
    ]

    for i, line in enumerate(legend_p1):
        screen.blit(
            legend_font.render(line, True, (220, 100, 100)),
            (20, 20 + i * 22)
        )

    for i, line in enumerate(legend_p2):
        text = legend_font.render(line, True, (100, 100, 220))
        screen.blit(
            text,
            (WIDTH - text.get_width() - 20, 20 + i * 22)
        )

    food_legend_y = 120
    screen.blit(legend_font.render("FOOD TYPES:", True, (255, 255, 255)),
                (WIDTH // 2 - 60, food_legend_y))

    food_info = [
        ("Good food (Eat)", FOOD_COLORS["good"]),
        ("Junk food (Pass)", FOOD_COLORS["bad"]),
        ("Spicy food (Reject)", FOOD_COLORS["spicy"])
    ]

    for i, (label, color) in enumerate(food_info):
        pygame.draw.rect(
            screen, color,
            (WIDTH // 2 - 80, food_legend_y + 30 + i * 22, 14, 14)
        )
        screen.blit(
            legend_font.render(label, True, (230, 230, 230)),
            (WIDTH // 2 - 60, food_legend_y + 28 + i * 22)
        )

    # SIZE TEXT

    screen.blit(font.render(str(p1_size), True, (255, 255, 255)), (160, 520))
    screen.blit(font.render(str(p2_size), True, (255, 255, 255)), (510, 520))

    # RESULT
    
    if state == "RESULT":
        winner = "DRAW"
        if p1_size > p2_size:
            winner = "PLAYER 1 WINS!"
        elif p2_size > p1_size:
            winner = "PLAYER 2 WINS!"

        text = font.render(winner, True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 20))

    pygame.display.flip()